from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


RiskLevel = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]


class MachineState(BaseModel):
    machine_id: str = "EXC001"
    machine_type: str = "Excavator"
    engine_hours: float = 1526.5
    fuel: float = Field(default=62.0, ge=0, le=100)
    temperature: float = 82.0
    load: float = Field(default=71.0, ge=0, le=100)
    operating_state: str = "DIGGING"
    fault_code: str | None = None


class OperatorState(BaseModel):
    operator_id: str = "OP001"
    name: str = "Jordan Lee"
    experience_level: str = "Beginner"
    current_action: str = "DIG"
    skill_profile: dict[str, float] = Field(default_factory=lambda: {
        "safety_awareness": 0.82,
        "task_efficiency": 0.64,
        "machine_care": 0.75,
        "task_knowledge": 0.71,
        "troubleshooting": 0.58,
    })


class TaskState(BaseModel):
    task_id: str = "TASK001"
    task_type: str = "Trenching"
    target: str = "Complete trench section"
    progress: float = Field(default=64.0, ge=0, le=100)
    eta_minutes: float = 48.0
    baseline_cycle_time: float = 31.0
    current_cycle_time: float = 34.2
    cycles_completed: int = 18


class SafetyState(BaseModel):
    seatbelt: bool = True
    nearby_worker: bool = False
    worker_distance_m: float | None = None
    worker_direction: str | None = None
    risk: RiskLevel = "LOW"
    active_alert: str | None = None


class EnvironmentState(BaseModel):
    weather: str = "Cloudy"
    visibility: str = "Good"
    ground_condition: str = "Firm"


class PerformanceState(BaseModel):
    recent_cycle_times: list[float] = Field(default_factory=lambda: [32.0, 33.5, 34.2])
    phase_durations: dict[str, float] = Field(default_factory=lambda: {
        "DIG": 8.0, "LIFT": 4.0, "SWING": 10.0, "DUMP": 5.0, "RETURN": 7.0,
    })
    baseline_phase_durations: dict[str, float] = Field(default_factory=lambda: {
        "DIG": 8.0, "LIFT": 4.0, "SWING": 7.0, "DUMP": 5.0, "RETURN": 7.0,
    })
    deviation: bool = False
    dominant_contributor: str | None = None


class Event(BaseModel):
    event_id: str
    timestamp: datetime
    type: str
    severity: RiskLevel = "LOW"
    confidence: float = Field(default=1.0, ge=0, le=1)
    machine_id: str | None = None
    operator_id: str | None = None
    task_id: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class Intervention(BaseModel):
    level: int = Field(ge=0, le=3)
    channel: Literal["log", "dashboard", "voice", "teach"]
    message: str
    reason: str
    expires_in_sec: int | None = None


class SharedState(BaseModel):
    operator: OperatorState = Field(default_factory=OperatorState)
    machine: MachineState = Field(default_factory=MachineState)
    task: TaskState = Field(default_factory=TaskState)
    safety: SafetyState = Field(default_factory=SafetyState)
    environment: EnvironmentState = Field(default_factory=EnvironmentState)
    performance: PerformanceState = Field(default_factory=PerformanceState)
    recent_events: list[Event] = Field(default_factory=list)
    intentguard: dict[str, Any] = Field(default_factory=dict)
    intervention: Intervention | None = None


class Analysis(BaseModel):
    module: str
    status: Literal["ok", "warning", "critical"]
    confidence: float = Field(ge=0, le=1)
    findings: list[str] = Field(default_factory=list)
    recommended_action: str = "SILENT"


class IntentPrediction(BaseModel):
    predicted_action: str
    intent_confidence: float = Field(ge=0, le=1)
    consequence: str
    risk: RiskLevel
    recommended_intervention: str


class Counterfactual(BaseModel):
    problem: str
    dominant_contributor: str
    observed_metric: float
    counterfactual_metric: float
    intervention: str
    trial_window: int
    verification_status: Literal["pending", "positive", "neutral", "negative"] = "pending"


class SimulationRequest(BaseModel):
    scenario: str


class QuestionRequest(BaseModel):
    operator_id: str = "OP001"
    question: str


class TeachRequest(BaseModel):
    operator_id: str = "OP001"
    skill: str = "swing_efficiency"


class DiagnoseRequest(BaseModel):
    machine_id: str = "EXC001"
    symptom: str


class InterventionStartRequest(BaseModel):
    operator_id: str = "OP001"
    skill: str = "swing_efficiency"


class InterventionCompleteRequest(BaseModel):
    intervention_id: str
    cycle_times: list[float] = Field(min_length=1)
