# Spec-Kit vs Agentic SDLC

| Dimension | Spec-Kit | Agentic SDLC |
|---|---|---|
| Core idea | Spec-first development framework | AI-agent-driven SDLC with staged handoffs |
| Primary focus | Requirements clarity and traceability | Execution speed and workflow orchestration |
| Workflow | Human-led with templates and gates | AI agents collaborate in sequence (Plan → HLD → Arch → Design → Dev) |
| Outputs | Specs, requirements, acceptance criteria | SDLC artifacts + runnable implementation |
| Governance | Process checkpoints and spec reviews | Agent instructions and workflow constraints |
| Automation | Moderate (manual execution after spec approval) | High (automated multi-step execution) |
| <span style="color:orange">Model flexibility</span> | <span style="color:orange">No per-stage model choice; process is human-driven, AI is optional and uniform if used at all</span> | <span style="color:orange">✓ Choose a different AI model for each agent/stage—e.g., GPT-4o for planning, Claude for architecture, Codex for dev—tuning cost, latency, and capability to the task</span> |
| Team consistency | Depends on human expertise | Embedded in agent behavior |
| Risk vs. Speed | Lower variance, slower cycle | Faster cycle, needs validation guardrails |
| Best for | Improving requirement discipline | Optimizing delivery velocity with AI |

## Why Model Flexibility Matters

In Agentic SDLC, each stage has different demands:

| Stage | Task type | Model strategy |
|---|---|---|
| Plan | Business analysis, BRD writing | Strong reasoning model (e.g., GPT-4o, Claude Opus) |
| HLD | Structured design, data modeling | Balanced model (e.g., Claude Sonnet, GPT-4o) |
| Architecture | Diagram generation, NFR mapping | Diagram-aware model with Mermaid support |
| Design | HTML/CSS wireframe generation | Fast creative model (e.g., GPT-4o-mini, Claude Haiku) |
| Dev | Code generation, test writing | Code-optimized model (e.g., Claude Sonnet, Codex) |

**Benefits:**
- **Cost control** — Use cheaper models where deep reasoning isn't needed
- **Latency optimization** — Faster models for high-volume generation stages
- **Quality targeting** — Match model strengths to task requirements (reasoning vs. coding vs. creative)
- **Vendor diversification** — Avoid lock-in by mixing providers across stages

Spec-Kit has no equivalent concept because execution is human-driven; the process doesn't select or configure AI models per phase.
