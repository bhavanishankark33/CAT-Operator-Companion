# Demo scenarios

## A — Predictive safety
1. Worker moves toward excavator.
2. Operator begins a swing sequence.
3. IntentGuard predicts SWING_RIGHT.
4. Risk engine identifies possible worker intersection.
5. Companion emits urgent Vapi voice warning.
6. Dashboard shows why the warning happened.

## B — Closed-loop skill improvement
1. Cycle time degrades.
2. Performance identifies the dominant slow phase.
3. Counterfactual estimates a better cycle.
4. Companion gives one short coaching intervention.
5. Simulator produces the next 3 cycles.
6. System verifies whether performance improved.

## C — Voice troubleshooting
1. Operator asks a machine/training question through Vapi.
2. Companion identifies intent.
3. Knowledge module retrieves grounded synthetic guidance.
4. LLM turns retrieved material into a concise spoken answer.
5. Unsafe/uncertain requests are escalated rather than invented.
