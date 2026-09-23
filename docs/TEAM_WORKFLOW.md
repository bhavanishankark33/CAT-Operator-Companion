# Two-person simultaneous workflow

## Branches
Person 1:
`feature/core-intelligence`

Own:
- core
- state
- simulator
- situation
- risk
- intentguard
- performance
- counterfactual

Person 2:
`feature/experience-voice`

Own:
- companion
- knowledge
- API integration
- frontend
- Vapi integration

Shared:
- schemas/contracts
- database migrations
- README/docs

## Rules
1. Pull/rebase before starting.
2. Do not edit the same file at the same time.
3. Do not commit secrets or API keys.
4. Every module exposes a small function/class interface.
5. Contract changes are announced before implementation.
6. Merge frequently; keep commits small.
7. `main` must stay runnable.

## Git setup
```bash
git clone <YOUR_GITHUB_REPO>
cd <REPO>
git checkout -b feature/core-intelligence
```

Friend:
```bash
git clone <YOUR_GITHUB_REPO>
cd <REPO>
git checkout -b feature/experience-voice
```

Before coding:
```bash
git fetch origin
git rebase origin/main
```

After coding:
```bash
git add .
git commit -m "feat: short description"
git push -u origin <branch-name>
```

Use pull requests to merge into `main`.
