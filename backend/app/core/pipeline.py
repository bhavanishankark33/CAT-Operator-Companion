from datetime import datetime, timezone
from uuid import uuid4

from app.core.store import StateStore
from app.schemas.contracts import Event, Intervention, IntentPrediction, RiskLevel


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


def run_pipeline(store: StateStore, event_type: str, **payload) -> dict:
    state = store.state
    event = _event(store, event_type, **payload)
    prediction = predict_intent(store)
    state.intervention = None

    if state.safety.risk in ("HIGH", "CRITICAL") or prediction.risk in ("HIGH", "CRITICAL"):
        state.intervention = Intervention(
            level=3,
            channel="voice",
            message="Warning. Worker approaching your right swing area. Hold movement until the area is clear.",
            reason="predicted_worker_intersection",
            expires_in_sec=8,
        )
        store.alerts.insert(0, {"event": event.model_dump(mode="json"), "intervention": state.intervention.model_dump()})
    elif state.safety.risk == "MEDIUM":
        state.intervention = Intervention(
            level=1,
            channel="dashboard",
            message=state.safety.active_alert or "A medium-risk condition needs attention.",
            reason="risk_condition",
        )
        store.alerts.insert(0, {"event": event.model_dump(mode="json"), "intervention": state.intervention.model_dump()})
    elif state.performance.deviation:
        state.intervention = Intervention(
            level=1,
            channel="dashboard",
            message="Cycle time is above your recent efficient baseline; the swing phase is the main contributor.",
            reason="performance_deviation",
        )
        store.alerts.insert(0, {"event": event.model_dump(mode="json"), "intervention": state.intervention.model_dump()})

    state.recent_events = store.events[:20]
    return {"event": event, "state": state, "intentguard": prediction, "intervention": state.intervention}