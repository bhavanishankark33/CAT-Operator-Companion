from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.core.deepgram import deepgram
from app.core.pipeline import run_pipeline
from app.core.gemini import gemini
from app.core.store import store
from app.knowledge import KnowledgeService
from app.schemas.contracts import (
    DiagnoseRequest, InterventionCompleteRequest, InterventionStartRequest,
    QuestionRequest, ResetRequest, SimulationRequest, TeachRequest, VoiceRequest,
)
from app.simulator.scenarios import SCENARIOS, simulate

router = APIRouter(prefix="/api")
knowledge = KnowledgeService()


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


@router.get("/operator-profile/{operator_id}")
def get_operator_profile(operator_id: str):
    return get_operator(operator_id)


@router.get("/performance")
def get_performance():
    return store.state.performance.model_dump(mode="json")


@router.get("/training")
def get_training():
    return store.training


@router.get("/analysis")
def get_analysis():
    state = store.state
    return {
        "situation": state.situation,
        "risk_predictions": state.risk_predictions,
        "intentguard": state.intentguard,
        "counterfactual": state.counterfactual,
    }


@router.get("/counterfactual")
def get_counterfactual():
    return store.state.counterfactual or {
        "verification_status": "not_started",
        "message": "Simulate SLOW_CYCLES to create a counterfactual coaching opportunity.",
    }


@router.get("/scenarios")
def get_scenarios():
    return {"scenarios": sorted(SCENARIOS)}


@router.post("/reset")
def reset(request: ResetRequest | None = None):
    keep_training = request.keep_training if request else False
    training = store.training if keep_training else []
    store.reset()
    if keep_training:
        store.training = training
        store.save()
    return {"status": "reset", "training_preserved": keep_training}


@router.post("/simulate")
def post_simulation(request: SimulationRequest):
    try:
        result = simulate(store, request.scenario)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {key: value.model_dump(mode="json") if hasattr(value, "model_dump") else value for key, value in result.items()}


@router.post("/ask")
def ask(request: QuestionRequest):
    state = store.state
    answer = knowledge.answer(request.question, state)
    answer, source = gemini.answer(request.question, state.model_dump(mode="json"), answer)
    return {"answer": answer, "speech_text": answer, "source": source, "confidence": 0.92}


@router.post("/voice/tool")
def voice_tool(request: QuestionRequest):
    """Voice transport boundary; the frontend can speak speech_text with browser speech synthesis."""
    return ask(request)


@router.get("/voice/config")
def voice_config():
    return {
        "provider": "deepgram_with_browser_fallback",
        "available": True,
        "deepgram_available": deepgram.enabled,
        "browser_fallback_available": True,
        "format": "audio/mpeg",
    }


@router.post("/voice/speak")
def voice_speak(request: VoiceRequest):
    try:
        audio = deepgram.synthesize(request.text)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return Response(content=audio, media_type="audio/mpeg", headers={"Content-Disposition": "inline; filename=companion.mp3"})


@router.post("/teach")
def teach(request: TeachRequest):
    counterfactual = store.state.counterfactual
    lesson = knowledge.lesson(request.skill, counterfactual)
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
    return knowledge.diagnose(request.symptom)


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
    run_pipeline(store, "TRAINING_STARTED", skill=request.skill, intervention_id=intervention["intervention_id"])
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
    store.state.performance.recent_cycle_times = [float(value) for value in request.cycle_times]
    store.state.performance.average_cycle_time = round(after, 1)
    store.state.task.current_cycle_time = round(after, 1)
    store.state.operator.skill_profile["task_efficiency"] = min(1.0, store.state.operator.skill_profile["task_efficiency"] + (0.04 if improvement > 0 else 0))
    if store.state.counterfactual:
        store.state.counterfactual["verification_status"] = "positive" if improvement > 0 else "neutral"
        store.state.counterfactual["after_metric"] = round(after, 1)
        store.state.counterfactual["improvement_seconds"] = round(improvement, 1)
    run_pipeline(store, "INTERVENTION_VERIFIED", improvement=round(improvement, 2))
    return item