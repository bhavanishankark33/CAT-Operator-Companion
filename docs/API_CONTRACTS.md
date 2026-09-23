# API contracts

Keep these stable so both people can work independently.

## Event
```json
{
  "event_id": "E001",
  "timestamp": "2026-09-23T10:00:00Z",
  "type": "WORKER_APPROACHING",
  "machine_id": "EXC001",
  "operator_id": "OP001",
  "task_id": "TASK001",
  "payload": {}
}
```

## Shared state
```json
{
  "operator": {},
  "machine": {},
  "task": {},
  "safety": {},
  "environment": {},
  "performance": {},
  "recent_events": []
}
```

## Analysis
```json
{
  "module": "intentguard",
  "status": "warning",
  "confidence": 0.87,
  "findings": [],
  "events": [],
  "recommended_action": "VOICE_WARNING"
}
```

## Intervention
```json
{
  "level": 3,
  "channel": "voice",
  "message": "Stop your swing. A worker is entering your swing path.",
  "reason": "predicted_worker_intersection",
  "expires_in_sec": 8
}
```

## IntentGuard
```json
{
  "predicted_action": "SWING_RIGHT",
  "intent_confidence": 0.87,
  "consequence": "potential_worker_intersection",
  "risk": "HIGH",
  "recommended_intervention": "VOICE_WARNING"
}
```

## Counterfactual
```json
{
  "problem": "slow_cycle",
  "dominant_contributor": "SWING",
  "observed_metric": 38.0,
  "counterfactual_metric": 32.0,
  "intervention": "smooth_swing_coaching",
  "trial_window": 3,
  "verification_status": "pending"
}
```

## Frontend endpoints

The backend is intentionally local-first. It stores state, events, alerts, and training history in `data/companion_state.json`.

```text
GET  /api/state
GET  /api/analysis
GET  /api/risk
GET  /api/events
GET  /api/alerts
GET  /api/performance
GET  /api/training
GET  /api/counterfactual
GET  /api/scenarios
GET  /api/operator-profile/{id}
POST /api/simulate
POST /api/ask
POST /api/voice/tool
GET  /api/voice/config
POST /api/voice/speak
POST /api/teach
POST /api/diagnose
POST /api/intervention/start
POST /api/intervention/complete
POST /api/reset
```

Voice returns `speech_text`. `POST /api/voice/speak` returns `audio/mpeg` from Deepgram when configured; the browser can use Web Speech API as a free fallback.
