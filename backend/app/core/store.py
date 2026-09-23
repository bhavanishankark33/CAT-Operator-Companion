from threading import Lock

from app.schemas.contracts import Event, SharedState


class StateStore:
    """Small process-local store for the prototype; replaceable by Redis/Postgres later."""

    def __init__(self) -> None:
        self._lock = Lock()
        self.state = SharedState()
        self.events: list[Event] = []
        self.alerts: list[dict] = []
        self.training: list[dict] = []

    def reset(self) -> None:
        with self._lock:
            self.state = SharedState()
            self.events = []
            self.alerts = []
            self.training = []

    def add_event(self, event: Event) -> None:
        with self._lock:
            self.events.insert(0, event)
            self.events = self.events[:100]
            self.state.recent_events = self.events[:20]


store = StateStore()