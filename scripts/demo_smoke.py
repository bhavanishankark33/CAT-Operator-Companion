import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.core.store import store  # noqa: E402
from app.simulator.engine import Simulator  # noqa: E402


def run_demo() -> None:
    simulator = Simulator(store)
    summaries = []
    for scenario in ("WORKER_APPROACHING", "SLOW_CYCLES", "MACHINE_START_FAILURE"):
        store.reset()
        result = simulator.run(scenario)
        summaries.append({
            "scenario": scenario,
            "situation": result["situation"],
            "risk_predictions": result["risk_predictions"],
            "intentguard": result["intentguard"].model_dump(mode="json"),
            "counterfactual": result["counterfactual"],
            "intervention": result["intervention"].model_dump(mode="json") if result["intervention"] else None,
        })
    print(json.dumps(summaries, indent=2))


if __name__ == "__main__":
    run_demo()