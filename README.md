# CAT Operator Companion

Fresh 24-hour hackathon workspace for a two-person team.

## Core idea
A proactive operator companion that:
1. understands live simulated machine/operator/task state,
2. predicts risk and likely next operator actions,
3. proactively alerts/coaches through dashboard + Vapi voice,
4. answers grounded questions,
5. teaches after mistakes or performance deviations,
6. verifies whether coaching improved subsequent behavior.

## Stack
- Frontend: React + Vite + Tailwind CSS
- Backend: Python + FastAPI
- Voice: Vapi
- Database: PostgreSQL
- Realtime/event flow: Redis Streams
- ML/data: Python, Pandas, NumPy, scikit-learn
- RAG: FAISS
- LLM: frontier LLM API
- Simulation: Python
- Testing: Pytest + frontend tests
- Git: GitHub feature branches

## Golden rule
LLM/Vapi never directly controls the machine and never owns numeric safety thresholds.
Deterministic rules own safety decisions; the LLM explains and coaches.

## Team workflow
Never work directly on `main`.

- Person 1: `feature/core-intelligence`
- Person 2: `feature/experience-voice`
- Shared contracts live in `backend/app/schemas/` and should be changed only after coordination.

Integration boundary:
`Event -> Shared State -> Analysis -> Decision -> Action -> Event`

See `docs/TEAM_WORKFLOW.md`.
