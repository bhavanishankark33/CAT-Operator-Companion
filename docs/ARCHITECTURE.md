# Fresh Architecture

```text
Synthetic Simulator
       |
       v
Local JSON Event Store
       |
       v
Shared Operational State
       |
       +------------------+------------------+
       |                  |                  |
       v                  v                  v
Situation           Risk Engine        IntentGuard
       |                  |                  |
       +------------------+------------------+
                          |
                          v
                Performance / Learning
                          |
                          v
                Companion Orchestrator
                    /           \
                   /             \
             Dashboard          Deepgram / Browser Voice
                   \             /
                    \           /
                     Operator
                          |
                          v
                Counterfactual Learning
                          |
                          v
                  Shared Operational State
                          |
                          +----> next event
```

The prototype intentionally uses local JSON instead of PostgreSQL, Redis, or a vector database. This keeps the demo reproducible while preserving replaceable interfaces for real telemetry and production storage.

## Responsibilities

### 1. Simulator
Produces realistic synthetic telemetry, operator actions, safety events, tasks and environment changes.

### 2. Shared State
Maintains the latest operator, machine, task, safety, environment and performance context.

### 3. Situation
Converts raw events/state into a compact situation summary.

### 4. Risk
Uses deterministic rules + simple statistical models for safety and operational risk.

### 5. IntentGuard
Predicts the operator's likely next action and short-horizon consequence.

### 6. Performance
Tracks cycle time, phase contribution, ETA and deviations.

### 7. Knowledge
Retrieves grounded synthetic training/troubleshooting material.

### 8. Companion
Combines analysis into one intervention decision: silent, UI, voice, or urgent voice.

### 9. Counterfactual
After an event, estimates a better alternative, creates one intervention, observes the next few cycles, and verifies improvement.

### 10. Frontend + Voice
Provides the operator-facing experience. Deepgram returns audio when configured; browser speech synthesis is the no-key fallback. These are interaction surfaces, not the source of truth.
