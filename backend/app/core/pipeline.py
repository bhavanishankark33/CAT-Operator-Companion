from datetime import datetime, timezone
from uuid import uuid4

from app.core.store import StateStore
from app.companion import companion
from app.schemas.contracts import Event, IntentPrediction, RiskLevel


TRANSITIONS = {
    "DIG": {"LIFT": 0.90, "IDLE": 0.10},
    "LIFT": {"SWING_LEFT": 0.35, "SWING_RIGHT": 0.35, "DUMP": 0.20, "IDLE": 0.10},
    "LIFT_RIGHT": {"SWING_RIGHT": 0.90, "SWING_LEFT": 0.05, "DUMP": 0.05},
    "SWING_RIGHT": {"DUMP": 0.80, "RETURN": 0.20},
    "SWING_LEFT": {"DUMP": 0.80, "RETURN": 0.20},
    "DUMP": {"RETURN": 0.90, "IDLE": 0.10},
    "RETURN": {"DIG": 0.85, "IDLE": 0.15},
}


def _event(store: StateStore, event_type: str, severity: RiskLevel = "LOW", confidence: float = 1.0, **payload) -> Event:
    state = store.state
    event = Event(
        event_id=f"EVT-{uuid4().hex[:8].upper()}",
        timestamp=datetime.now(timezone.utc),
        type=event_type,
        severity=severity,
        confidence=confidence,
        machine_id=state.machine.machine_id,
        operator_id=state.operator.operator_id,
        task_id=state.task.task_id,
        payload=payload,
    )
    store.add_event(event)
    return event


def predict_intent(store: StateStore) -> IntentPrediction:
    state = store.state
    current = state.operator.current_action
    next_actions = TRANSITIONS.get(current, {"IDLE": 1.0})
    action, confidence = max(next_actions.items(), key=lambda item: item[1])
    consequence = "none"
    risk: RiskLevel = "LOW"
    intervention = "SILENT"
    if action == "SWING_RIGHT" and state.safety.nearby_worker and (state.safety.worker_distance_m or 999) < 12:
        consequence, risk, intervention = "potential_worker_intersection", "HIGH", "VOICE_WARNING"
    elif action.startswith("SWING") and state.performance.deviation:
        consequence, risk, intervention = "likely_efficiency_loss", "MEDIUM", "UI_WARNING"
    prediction = IntentPrediction(
        predicted_action=action,
        intent_confidence=confidence,
        consequence=consequence,
        risk=risk,
        recommended_intervention=intervention,
    )
    state.intentguard = prediction.model_dump()
    return prediction


def understand_situation(store: StateStore) -> dict:
    state = store.state
    if state.safety.nearby_worker and state.safety.worker_direction == "toward_machine":
        label, confidence = "worker_approaching_operating_machine", 0.96
    elif state.machine.operating_state == "IDLE":
        label, confidence = "operator_waiting_or_idle", 0.82
    elif state.machine.operating_state == "FAULT":
        label, confidence = "machine_fault_requires_attention", 0.98
    elif state.performance.deviation:
        label, confidence = "operator_cycle_efficiency_deviation", 0.91
    else:
        label, confidence = "normal_operation", 0.88
    result = {
        "situation": label,
        "confidence": confidence,
        "risk": state.safety.risk.lower(),
        "productivity_impact": "moderate" if state.performance.deviation else "low",
    }
    state.situation = result
    return result


def analyze_performance(store: StateStore) -> None:
    state = store.state
    performance = state.performance
    if not performance.recent_cycle_times:
        return
    average = sum(performance.recent_cycle_times) / len(performance.recent_cycle_times)
    performance.average_cycle_time = round(average, 1)
    excess_by_phase = {
        phase: max(0.0, performance.phase_durations.get(phase, 0) - performance.baseline_phase_durations.get(phase, 0))
        for phase in performance.phase_durations
    }
    dominant, excess = max(excess_by_phase.items(), key=lambda item: item[1], default=(None, 0.0))
    performance.dominant_contributor = dominant if excess > 0 else None
    performance.estimated_excess_seconds = round(excess, 1)
    performance.deviation = average > state.task.baseline_cycle_time * 1.10
    performance.counterfactual_cycle_time = round(max(state.task.baseline_cycle_time, average - excess), 1) if performance.deviation else None
    weather_factor = 1.12 if state.environment.ground_condition.lower() == "wet" else 1.0
    skill_factor = 1.0 + max(0.0, 0.75 - state.operator.skill_profile.get("task_efficiency", 0.64)) * 0.2
    state.task.eta_minutes = round(max(1.0, 48.0 * (average / state.task.baseline_cycle_time) * weather_factor * skill_factor), 1)


def analyze_risk(store: StateStore, intent: IntentPrediction) -> list[dict]:
    state = store.state
    predictions: list[dict] = []
    if state.safety.nearby_worker and (state.safety.worker_distance_m or 999) < 12:
        predictions.append({
            "type": "PREDICTED_WORKER_INTERSECTION",
            "severity": "HIGH",
            "confidence": 0.94,
            "reason": "worker_distance_decreasing_near_predicted_swing",
        })
    if not state.safety.seatbelt:
        predictions.append({
            "type": "SEATBELT_VIOLATION",
            "severity": "MEDIUM",
            "confidence": 0.99,
            "reason": "seatbelt_unfastened_during_operation",
        })
    if state.machine.temperature >= 90:
        predictions.append({
            "type": "TEMPERATURE_RISING",
            "severity": "MEDIUM",
            "confidence": 0.9,
            "reason": "temperature_above_demo_threshold_with_load",
        })
    if state.performance.deviation:
        predictions.append({
            "type": "ETA_SLIP",
            "severity": "MEDIUM",
            "confidence": 0.86,
            "reason": "cycle_time_above_baseline",
        })
    state.risk_predictions = predictions
    return predictions


def build_counterfactual(store: StateStore) -> None:
    state = store.state
    performance = state.performance
    if not performance.deviation or not performance.dominant_contributor:
        return
    previous = state.counterfactual or {}
    state.counterfactual = {
        "problem": "slow_cycle",
        "dominant_contributor": performance.dominant_contributor,
        "observed_metric": performance.average_cycle_time,
        "counterfactual_metric": performance.counterfactual_cycle_time,
        "estimated_excess_seconds": performance.estimated_excess_seconds,
        "intervention": "smooth_swing_coaching",
        "trial_window": 3,
        "verification_status": "pending",
        "explanation": (
            f"The {performance.dominant_contributor.lower()} phase contributed approximately "
            f"{performance.estimated_excess_seconds:.1f} extra seconds. "
            f"Estimated cycle with that phase at baseline: {performance.counterfactual_cycle_time:.1f} seconds."
        ),
    }
    for key in ("verification_status", "after_metric", "improvement_seconds"):
        if key in previous:
            state.counterfactual[key] = previous[key]


def run_pipeline(store: StateStore, event_type: str, **payload) -> dict:
    state = store.state
    event = _event(store, event_type, **payload)
    understand_situation(store)
    analyze_performance(store)
    prediction = predict_intent(store)
    analyze_risk(store, prediction)
    build_counterfactual(store)
    if state.risk_predictions:
        highest = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
        event.severity = max((item["severity"] for item in state.risk_predictions), key=lambda item: highest[item])
    state.intervention = companion.decide(state, prediction, state.risk_predictions)
    if state.intervention:
        store.add_alert({"event": event.model_dump(mode="json"), "intervention": state.intervention.model_dump()})

    state.recent_events = store.events[:20]
    store.save()
    return {
        "event": event,
        "state": state,
        "situation": state.situation,
        "risk_predictions": state.risk_predictions,
        "intentguard": prediction,
        "counterfactual": state.counterfactual,
        "intervention": state.intervention,
    }