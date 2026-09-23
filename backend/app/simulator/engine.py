from app.core.store import StateStore
from app.simulator.scenarios import SCENARIOS, simulate


class Simulator:
    """Deterministic synthetic event source used by the demo and tests."""

    def __init__(self, state_store: StateStore):
        self.state_store = state_store

    def run(self, scenario: str) -> dict:
        return simulate(self.state_store, scenario)


__all__ = ["SCENARIOS", "Simulator"]