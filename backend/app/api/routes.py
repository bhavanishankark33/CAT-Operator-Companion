from fastapi import APIRouter, HTTPException

from app.core.pipeline import run_pipeline
from app.core.gemini import gemini
from app.core.store import store
from app.schemas.contracts import (
    DiagnoseRequest, InterventionCompleteRequest, InterventionStartRequest,
    QuestionRequest, SimulationRequest, TeachRequest,
)
from app.simulator.scenarios import simulate

router = APIRouter(prefix="/api")


@router.get("/state")
def get_state():
    return store.state.model_dump(mode="json")


@router.get("/events")
def get_events():
    return [event.model_dump(mode="json") for event in store.events]


@router.get("/alerts")
def get_alerts():
    return store.alerts[:30]


@router.get("/risk")
def get_risk():
    state = store.state
    return {
        "risk": state.safety.risk,
        "confidence": 0.94 if state.safety.risk in ("HIGH", "CRITICAL") else 0.88,
        "active_alert": state.safety.active_alert,
        "intentguard": state.intentguard,
    }


@router.get("/tasks")
def get_tasks():
    return [store.state.task.model_dump(mode="json")]


@router.get("/operator/{operator_id}")
def get_operator(operator_id: str):
    if operator_id != store.state.operator.operator_id:
        raise HTTPException(status_code=404, detail="Operator not found")
    return store.state.operator.model_dump(mode="json")


@router.get("/performance")
def get_performance():
    return store.state.performance.model_dump(mode="json")


@router.get("/training")
def get_training():
    return store.training


@router.post("/simulate")
def post_simulation(request: SimulationRequest):
    try:
        result = simulate(store, request.scenario)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {key: value.model_dump(mode="json") if hasattr(value, "model_dump") else value for key, value in result.items()}


@router.post("/ask")
def ask(request: QuestionRequest):
    question = request.question.lower()
    state = store.state
    if "eta" in question or "time" in question:
        answer = f"Your ETA is {state.task.eta_minutes:.0f} minutes because recent cycles average {sum(state.performance.recent_cycle_times) / len(state.performance.recent_cycle_times):.1f} seconds, above the {state.task.baseline_cycle_time:.1f}-second baseline."
    elif "warning" in question or "worker" in question:
        answer = "The warning indicates a worker is approaching the predicted swing area. Hold movement until the area is clear."
    elif "improve" in question or "efficien" in question:
        answer = "Focus on a smooth, shorter swing for the next three cycles. I will compare cycle time and swing duration with your baseline."
    else:
        answer = "I can explain the current ETA, safety warning, machine condition, or performance coaching from the live simulated state."
    answer, source = gemini.answer(request.question, state.model_dump(mode="json"), answer)
    return {"answer": answer, "speech_text": answer, "source": source, "confidence": 0.92}


@router.post("/voice/tool")
def voice_tool(request: QuestionRequest):
    """Voice transport boundary; the frontend can speak speech_text with browser speech synthesis."""
    return ask(request)


@router.get("/voice/config")
def voice_config():
    return {"provider": "browser_speech_synthesis", "available": True, "external_api_required": False}


@router.post("/teach")
def teach(request: TeachRequest):
    lesson = "For your next three cycles, keep the swing smooth and within your efficient range. Avoid unnecessary travel before dumping."
    lesson, source = gemini.answer(
        f"Create a 30-second micro-lesson for the skill {request.skill}.",
        store.state.model_dump(mode="json"),
        lesson,
    )
    return {
        "skill": request.skill,
        "problem": "slow_cycle",
        "lesson": lesson,
        "speech_text": lesson,
        "source": source,
        "trial_cycles": 3,
        "metric": "cycle_time",
        "secondary_metric": "swing_duration",
    }


@router.post("/diagnose")
def diagnose(request: DiagnoseRequest):
    if "start" not in request.symptom.lower():
        return {"answer": "I do not have a verified guide for that symptom. Stop and request qualified service support.", "grounded": False}
    return {
        "answer": "Verify operator presence and displayed warnings, then check the basic start conditions in the provided machine guide. If unresolved, stop troubleshooting and request qualified service support.",
        "grounded": True,
        "source": "synthetic_curated_startup_guide",
    }


@router.post("/intervention/start")
def start_intervention(request: InterventionStartRequest):
    intervention = {
        "intervention_id": f"INT-{len(store.training) + 1:04d}",
        "operator_id": request.operator_id,
        "skill": request.skill,
        "status": "active",
        "trial_cycles": 3,
        "before_metric": sum(store.state.performance.recent_cycle_times) / len(store.state.performance.recent_cycle_times),
    }
    store.training.insert(0, intervention)
    store.save()
    return intervention


@router.post("/intervention/complete")
def complete_intervention(request: InterventionCompleteRequest):
    item = next((entry for entry in store.training if entry["intervention_id"] == request.intervention_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Intervention not found")
    after = sum(request.cycle_times) / len(request.cycle_times)
    improvement = item["before_metric"] - after
    item.update({"status": "completed", "after_metric": after, "improvement": improvement, "result": "positive" if improvement > 0 else "neutral"})
    store.state.operator.skill_profile["task_efficiency"] = min(1.0, store.state.operator.skill_profile["task_efficiency"] + (0.04 if improvement > 0 else 0))
    run_pipeline(store, "INTERVENTION_VERIFIED", improvement=round(improvement, 2))
    return item