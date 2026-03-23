# Agentic SDLC Demo

This repository demonstrates an Agentic SDLC workflow in VS Code, where specialized agents collaborate to move from business idea to implementation-ready outputs.

## Sample Use Case
Build an MVP appointment booking app where patients/users can book, reschedule, and cancel visits with doctors.

## Why Agentic SDLC
- Breaks work into clear SDLC stages
- Uses specialized agents for planning, architecture, design, and delivery
- Improves traceability from requirement to implementation artifacts

## Suggested Agent Flow
1. Plan Agent: BRD, epics, and features
2. HLD Agent: high-level design and data model
3. Architecture Agent: diagrams and NFR-focused architecture
4. UI/UX Agent: wireframes and user flow screens

## Python Tech Stack (Candidate)
- Backend: Python (FastAPI or Flask)
- Data layer: PostgreSQL
- API docs: OpenAPI/Swagger
- Optional worker: Celery + Redis

## Quick Start
1. Create or update agent definitions.
2. Run Plan -> HLD -> Architecture -> Design.
3. Review outputs in docs and wireframes.
4. Scaffold implementation in Python.
