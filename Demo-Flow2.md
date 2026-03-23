# Demo Flow

Legend: 🔵 Plan | 🟣 HLD | 🟢 Architecture | 🟠 Design | 🔴 Dev | ✅ Validate | 💡 Tip

## 🎯 Goal

Demonstrate end-to-end Agentic SDLC in VS Code using one business prompt and a fixed 5-agent sequence.

## 🚀 Initial Prompt (in SDLC Plan Agent)

Plan an MVP appointment booking app where users can search doctors, book a slot, and manage bookings.

## 🧰 Pre-Demo Setup (2 minutes)

1. Open the repository in VS Code.
2. Confirm agents are visible in chat:
	- 1.SDLC Plan Agent
	- 2.SDLC HLD Agent
	- 3.SDLC Architecture Agent
	- 4.SDLC Design Agent
	- 5.SDLC Dev Agent
3. Keep Explorer open and pin these folders for visibility:
	- docs
	- wireframes
	- src
	- tests
4. Keep Markdown Preview ready for architecture and documentation files.

## 🎬 Step-by-Step Demo Sequence

### 🔵 Step 1 - Plan

Agent: 1.SDLC Plan Agent

Prompt to paste:

```text
Create BRD, Epics, and Features for this MVP:
Plan an MVP appointment booking app where users can search doctors, book a slot, and manage bookings.
Keep scope MVP-only and include measurable success criteria.
```

Expected outputs:
- docs/BRD.md
- docs/Epics.md
- docs/Features.md

Step validation:
- Business objectives are clear
- In-scope and out-of-scope are present
- Features trace back to epics

### 🟣 Step 2 - HLD and Data Model

Agent: 2.SDLC HLD Agent

Prompt to paste:

```text
Use the generated docs artifacts and produce App_HLD and App_DataModel for MVP only.
```

Expected outputs:
- docs/App_HLD.md
- docs/App_DataModel.md

Step validation:
- Modules and interfaces are defined
- Data entities and relationships are clear
- Design maps to MVP features

### 🟢 Step 3 - Architecture

Agent: 3.SDLC Architecture Agent

Prompt to paste:

```text
Create docs/App_Architecture.md from HLD and planning docs.
Include Mermaid diagrams and NFR mapping for MVP.
Required diagrams: System context, Component, Deployment, Data flow, and one key Sequence diagram.
```

Expected output:
- docs/App_Architecture.md

Step validation:
- All required diagrams exist
- NFRs are explicitly covered (security, performance, reliability, maintainability, scalability)
- Architecture decisions and trade-offs are documented

### 🟠 Step 4 - Design Wireframes

Agent: 4.SDLC Design Agent

Prompt to paste:

```text
Generate clickable MVP wireframes for booking flow and account management based on BRD and HLD.
Create an index page, core screen pages, and shared styles.
```

Expected outputs:
- wireframes/index.html
- wireframes/pages/*.html
- wireframes/styles/common.css
- wireframes/styles/theme.css
- wireframes/styles/components.css
- wireframes/README.md

Step validation:
- Wireframes are navigable
- Booking journey is complete end-to-end
- Core screens exist (search, slot selection, booking management)

### 🔴 Step 5 - Development (Python + Flask)

Agent: 5.SDLC Dev Agent

Prompt to paste:

```text
Implement MVP from approved docs and wireframes with basic tests using Python and Flask.
```

Expected outputs:
- src/*
- tests/*
- requirements.txt
- docs/ImplementationNotes.md

Step validation:
- Flask app starts
- Critical tests run
- Implementation notes map delivered scope to planned features

## ✅ Quick Validation Checklist (Final)

- [ ] Plan artifacts exist and are internally consistent
- [ ] HLD and Data Model are traceable to features
- [ ] Architecture has required Mermaid diagrams and NFR mapping
- [ ] Wireframes are clickable and cover core user journey
- [ ] Flask MVP runs locally and tests execute
- [ ] ImplementationNotes captures scope, limitations, and next steps

## 💡 Optional Finale (Change Request)

Use this change request to showcase controlled iteration:

```text
Add tele-consultation link support to bookings.
```

Rerun only impacted agents in this order:
1. 1.SDLC Plan Agent
2. 2.SDLC HLD Agent
3. 3.SDLC Architecture Agent
4. 4.SDLC Design Agent
5. 5.SDLC Dev Agent
