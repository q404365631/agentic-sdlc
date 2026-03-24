---
name: sdlc-kickoff
description: "Generate a complete SDLC kickoff plan from a business idea. Use when: starting a new project, onboarding a new idea into the agentic pipeline, or preparing a demo. Produces agent prompts for all 5 stages."
---

# SDLC Kickoff from Business Idea

## When to Use
- Starting a brand-new project from a business idea or one-liner
- Preparing a structured demo of the Agentic SDLC pipeline
- Onboarding a team member who needs to understand the full flow

## Procedure

1. **Capture the idea** — Accept a business idea in natural language
2. **Clarify MVP scope** — Identify 3-5 core capabilities and explicit exclusions
3. **Define success criteria** — 2-3 measurable outcomes
4. **Generate agent prompts** — Produce a ready-to-paste prompt for each of the 5 SDLC agents:
   - Plan Agent prompt (BRD, Epics, Features)
   - HLD Agent prompt (modules, data model)
   - Architecture Agent prompt (diagrams, NFRs)
   - Design Agent prompt (wireframes, screens)
   - Dev Agent prompt (implementation, tests)
5. **Output the kickoff brief** as a single Markdown document

## Output Format

The kickoff brief must follow this structure:

### Kickoff Brief Sections
- **Business Idea** — The user's original idea, restated
- **MVP Scope** — 3-5 core capabilities as bullet points
- **Explicitly Out of Scope** — Features deferred to future versions
- **Success Criteria** — 2-3 measurable outcomes as checkboxes
- **Agent Prompts** — One ready-to-paste prompt per agent (Plan, HLD, Architecture, Design, Dev)

### Agent Prompt Format
Each prompt block should be labeled with the agent name and include a copyable text block:
- `@1.SDLC Plan Agent` — Plan prompt
- `@2.SDLC HLD Agent` — HLD prompt
- `@3.SDLC Architecture Agent` — Architecture prompt
- `@4.SDLC Design Agent` — Design prompt
- `@5.SDLC Dev Agent` — Dev prompt

## Prompt Generation Rules
- Each prompt must reference the artifacts produced by the prior stage
- Plan prompt must include MVP scope boundaries and success criteria
- HLD prompt must reference `/docs/BRD.md`, `/docs/Epics.md`, `/docs/Features.md`
- Architecture prompt must specify the 5 required diagram types (System context, Component, Deployment, Data flow, Sequence)
- Design prompt must reference BRD and HLD for screen derivation
- Dev prompt must specify the tech stack: Python 3.11+, Flask, SQLite, pytest