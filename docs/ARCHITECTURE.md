# Fresh Architecture

```text
Synthetic Simulator
       |
       v
Event Bus / Event Store
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
             Dashboard          Vapi Voice
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

### 10. Frontend + Vapi
Provides the operator-facing experience. These are interaction surfaces, not the source of truth.
