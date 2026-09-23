from typing import Any
from pydantic import BaseModel, Field

class Event(BaseModel):
    event_id: str
    timestamp: str
    type: str
    machine_id: str | None = None
    operator_id: str | None = None
    task_id: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)

class Intervention(BaseModel):
    level: int
    channel: str
    message: str
    reason: str
    expires_in_sec: int | None = None
