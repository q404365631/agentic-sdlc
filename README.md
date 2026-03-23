# Agentic-SDLC

A lightweight VS Code custom-agent workspace for demonstrating an Agentic SDLC flow.

## Default Implementation Stack

- Python 3.11+
- Flask
- SQLite (local MVP)
- pytest

## Repository Structure

- `.github/agents/plan.agent.md` - Planning agent (BRD, Epics, Features)
- `.github/agents/hld.agent.md` - HLD and data model agent
- `.github/agents/arch.agent.md` - Architecture and Mermaid diagrams agent
- `.github/agents/design.agent.md` - UI/UX wireframe agent
- `.github/agents/dev.agent.md` - Development/implementation agent

## Quick Start

1. Open this folder in VS Code.
2. Ensure GitHub Copilot custom agents are enabled.
3. Start with the Plan agent and provide a simple business requirement.
4. Run agents in order:
   - Plan -> HLD -> Architecture -> Design -> Dev
5. Store generated documentation under `docs/` and wireframes under `wireframes/`.

## Dev Bootstrap (Python + Flask)

1. Create and activate a virtual environment.
2. Install dependencies from `requirements.txt`.
3. Start Flask app.
4. Run tests.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app src.app run --debug
pytest -q
```

## Suggested Demo Prompt

"Plan an MVP appointment booking app where users can search doctors, book a slot, and manage bookings."

Then pass outputs stage by stage to the next agent.

## Notes

If files do not appear in Explorer, run **Developer: Reload Window** in VS Code.
