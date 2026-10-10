# AI Center of Excellence (AI CoE)

A practical reference implementation for a **company of one** (or a small team) to run an AI-native operating model using:
- Multi-agent collaboration (Codex, Claude Code, Grok Build, and more)
- Governance-first design
- Private execution dashboard + public Vercel layer
- Reusable templates, skills, and configuration compilers

## Repository Foundations

```text
ai-coe/
  README.md
  templates/
    company-of-one/
    creator-business/
    ai-agency/
    engineering-team/
    university-lab/
  governance/
    ai-policy.md
    mcp-trust-levels.md
    data-boundaries.md
  agents/
    chief-of-staff.md
    research-agent.md
    builder-agent.md
    growth-agent.md
    governance-agent.md
  skills/
    demand-generation/
    product-architecture/
    content-engine/
    repo-maintenance/
    weekly-review/
  config-compilers/
    agents-md/
    claude-md/
    cursor-rules/
    codex-instructions/
  apps/
    dashboard/
  content/
    README.md
    ai-skills-and-ai-coe-ultimate-guide.md
    claude-skills-operating-layer-blog.md
  examples/
    frankx-ai-coe/
    arcanea-ai-coe/
    starlight-intelligence-system/
```

## Getting Started

1. Choose a template under `/templates` that matches your operating model.
2. Tailor governance rules under `/governance` before enabling autonomous execution.
3. Define your core agents under `/agents` and map them to `/skills`.
4. Compile agent/tool configs through `/config-compilers`.
5. Use `/apps/dashboard` as the private control plane and expose approved outputs via public channels.

## Publication-Ready Content

- [The Ultimate Guide to Building AI Skills and an AI Center of Excellence](content/ai-skills-and-ai-coe-ultimate-guide.md)
- [Claude Skills Are Not Just Prompts. They Are an Operating Layer for AI Teams.](content/claude-skills-operating-layer-blog.md)

## Design Principles

- **Governance before automation**
- **Clear trust boundaries for tools and data**
- **Skill-driven execution**
- **Observable weekly review loops**
- **Portable templates and examples**

<!-- STARLIGHT:OPERATING:BEGIN v2 sha=9f8fecc91edc source=794db1e51a55a128816f7aa266eb0ac1dbd452c3 -->

## Agent operating guidance

Repository agents use the shared Starlight operating contract in `AGENTS.md` alongside local instructions.
The contract asks agents to establish a useful outcome, select relevant skills, complete authorized work,
verify current sources, refine the actual artifact, and report evidence and remaining gates.
It covers human agency, privacy, rights, resource stewardship and bounded proactivity.
Repository identity, brand, canon, build commands and release gates remain local.

[Pinned contract](https://github.com/frankxai/Starlight-Intelligence-System/blob/794db1e51a55a128816f7aa266eb0ac1dbd452c3/docs/architecture/agents-md/band-a.md)
· [Projection and verification](https://github.com/frankxai/Starlight-Intelligence-System/blob/794db1e51a55a128816f7aa266eb0ac1dbd452c3/docs/architecture/AGENTS-MD-CONTRACT.md)

These files supply operating guidance. They do not activate an agent, grant tool permissions,
schedule recurring work, certify compliance or prove a live capability.

<!-- STARLIGHT:OPERATING:END -->
