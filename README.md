# CAT Operator Companion

Fresh 24-hour hackathon workspace for a two-person team.

## Core idea
A proactive operator companion that:
1. understands live simulated machine/operator/task state,
2. predicts risk and likely next operator actions,
3. proactively alerts/coaches through dashboard + browser voice,
4. answers grounded questions,
5. teaches after mistakes or performance deviations,
6. verifies whether coaching improved subsequent behavior.

## Stack
- Frontend: React + Vite + Tailwind CSS
- Backend: Python + FastAPI
- Voice: optional Deepgram MP3 TTS with free browser speech fallback
- Storage: local JSON file (`data/companion_state.json`)
- LLM: Gemini API with optional comma-separated key rotation
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

## Backend quick start

```powershell
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

The demo works without an LLM key. To enable Gemini explanations and lessons, set `GEMINI_API_KEY`, or provide multiple keys with `GEMINI_API_KEYS=key1,key2,key3`. The backend rotates keys when a request fails or reaches quota, then falls back to deterministic answers.

To enable generated audio, set `DEEPGRAM_API_KEYS=key1,key2,key3`. The backend rotates keys on failed requests through `POST /api/voice/speak`. If Deepgram is unavailable, the frontend should speak the returned `speech_text` with browser speech synthesis.
