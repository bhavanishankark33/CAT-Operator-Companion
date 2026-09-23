import json
import os
from threading import Lock
from pathlib import Path

from app.schemas.contracts import Event, SharedState


class StateStore:
    """Durable local JSON store for the prototype; no database required."""

    def __init__(self) -> None:
        self._lock = Lock()
        default_path = Path(__file__).resolve().parents[3] / "data" / "companion_state.json"
        self.path = Path(os.getenv("COMPANION_DATA_FILE", str(default_path)))
        self.state = SharedState()
        self.events: list[Event] = []
        self.alerts: list[dict] = []
        self.training: list[dict] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self.state = SharedState.model_validate(data.get("state", {}))
            self.events = [Event.model_validate(item) for item in data.get("events", [])]
            self.alerts = data.get("alerts", [])
            self.training = data.get("training", [])
            self.state.recent_events = self.events[:20]
        except (OSError, ValueError):
            # A broken demo file should not prevent the app from starting.
            self.state = SharedState()
            self.events, self.alerts, self.training = [], [], []

    def _save_unlocked(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(".tmp")
        payload = {
            "state": self.state.model_dump(mode="json"),
            "events": [event.model_dump(mode="json") for event in self.events[:100]],
            "alerts": self.alerts[:30],
            "training": self.training[:30],
        }
        temporary_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        temporary_path.replace(self.path)

    def save(self) -> None:
        with self._lock:
            self._save_unlocked()

    def reset(self) -> None:
        with self._lock:
            self.state = SharedState()
            self.events = []
            self.alerts = []
            self.training = []
            self._save_unlocked()

    def add_event(self, event: Event) -> None:
        with self._lock:
            self.events.insert(0, event)
            self.events = self.events[:100]
            self.state.recent_events = self.events[:20]
            self._save_unlocked()


store = StateStore()