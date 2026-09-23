from app.core.pipeline import run_pipeline
from app.core.store import StateStore


SCENARIOS = {
    "NORMAL_OPERATION", "WORKER_APPROACHING", "SEATBELT_UNFASTENED", "TEMPERATURE_RISING",
    "EXCESSIVE_IDLE", "SLOW_CYCLES", "REPEATED_OPERATOR_ERROR", "MACHINE_START_FAILURE",
    "TASK_DELAY", "WEATHER_CHANGE",
}


def simulate(store: StateStore, scenario: str) -> dict:
    scenario = scenario.upper()
    if scenario not in SCENARIOS:
        raise ValueError(f"Unsupported scenario. Choose one of: {', '.join(sorted(SCENARIOS))}")
    state = store.state
    if scenario == "WORKER_APPROACHING":
        state.safety.nearby_worker = True
        state.safety.worker_distance_m = 8.7
        state.safety.worker_direction = "toward_machine"
        state.safety.risk = "HIGH"
        state.safety.active_alert = "Worker approaching right swing area"
        state.operator.current_action = "LIFT_RIGHT"
        return run_pipeline(store, scenario, distance_m=8.7, direction="toward_machine")
    if scenario == "SEATBELT_UNFASTENED":
        state.safety.seatbelt = False
        state.safety.risk = "MEDIUM"
        state.safety.active_alert = "Seatbelt unfastened during operation"
    elif scenario == "TEMPERATURE_RISING":
        state.machine.temperature = 94.0
        state.machine.load = 86.0
        state.safety.risk = "MEDIUM"
        state.safety.active_alert = "Engine temperature trend rising"
    elif scenario in {"SLOW_CYCLES", "REPEATED_OPERATOR_ERROR", "TASK_DELAY"}:
        state.performance.recent_cycle_times = [38.0, 37.0, 36.0]
        state.performance.phase_durations["SWING"] = 13.0
        state.performance.deviation = True
        state.performance.dominant_contributor = "SWING"
        state.task.current_cycle_time = 38.0
        state.task.eta_minutes = 56.0
    elif scenario == "MACHINE_START_FAILURE":
        state.machine.fault_code = "START_CONDITION"
        state.machine.operating_state = "FAULT"
        state.safety.risk = "MEDIUM"
    elif scenario == "EXCESSIVE_IDLE":
        state.machine.operating_state = "IDLE"
        state.safety.active_alert = "Extended idle detected"
    elif scenario == "WEATHER_CHANGE":
        state.environment.weather = "Rainy"
        state.environment.visibility = "Moderate"
        state.environment.ground_condition = "Wet"
        state.task.eta_minutes = 54.0
    else:
        state.machine.operating_state = "DIGGING"
        state.safety.risk = "LOW"
    return run_pipeline(store, scenario)