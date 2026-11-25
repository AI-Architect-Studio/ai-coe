# Where this CoE belongs

An architect should be able to hand a founder a working environment, walk away, and watch the founder run and improve the next mission. That is the product test.

An AI Center of Excellence already has an established institutional meaning. Microsoft describes a team with executive sponsorship, governance duties and responsibility for adoption. This project translates those responsibilities into artifacts one person can maintain: a mission brief, named decision owner, permitted tools, evidence of the outcome and a reviewed change for the next run. In a larger organization, different people can hold those responsibilities. The portfolio's own AI Architect Studio already publishes a company-of-one reference. [Microsoft Cloud Adoption Framework](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai/center-of-excellence) · [AI Architect Studio](https://github.com/AI-Architect-Studio/ai-coe)

## Decisions against existing alternatives

Reviewed 25 November 2026. Public documentation supports the descriptions below. The last column proposes how to use the comparison. It does not certify an integration.

| Existing category | What a builder already gets | Decision for this reference |
| --- | --- | --- |
| Enterprise AI CoE | Microsoft's adoption framework defines sponsorship, responsibilities and organizational evolution. [Framework](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai/center-of-excellence) | Adopt named owners and a review cadence. Let one operator fill multiple roles while logging consequential decisions. |
| Agent engineering | The OpenAI Agents SDK traces generations, tool calls, handoffs and guardrails. [Tracing guide](https://openai.github.io/openai-agents-js/guides/tracing/) | Keep the runtime replaceable. A future adapter can reference a trace ID, subject to the workspace's data policy. |
| Coding-agent skills | Agent Skills defines discovery metadata. OpenAI and Anthropic each maintain host-oriented catalogs. [Specification](https://agentskills.io/specification) · [OpenAI](https://github.com/openai/skills) · [Anthropic](https://github.com/anthropics/skills) | Follow the format. Pin upstream skills and inspect their individual licenses. Contribute fixture failures upstream when a host's behavior differs. |
| Software factories | GitHub's coding agent can take issue-shaped work through tests into a pull request. [GitHub guide](https://awesome-copilot.github.com/learning-hub/using-copilot-coding-agent/) | Delegate implementation in that environment. Keep acceptance criteria and release authority with the mission owner. |
| Personal intelligence | Obsidian stores notes in a local folder as Markdown. [Storage](https://obsidian.md/help/data-storage) | Use ordinary workspace files for private decisions. The owner chooses which records can enter a shared project. |
| AI developer education | Hugging Face teaches agent theory, practical work and multiple libraries. [Course](https://huggingface.co/learn/agents-course/en/unit0/introduction) | Refer learners there for runtime fundamentals. Grade the CoE exercise by what a second operator can reproduce. |
| Founder acceleration | YC's accelerator targets better products and more users. Startup School offers free startup instruction and weekly accountability. [Accelerator](https://www.ycombinator.com/about) · [Startup School](https://www.startupschool.org/) | Equip an existing cohort with a founder-owned workbench. Keep one externally observed customer signal distinct from an agent's hypothesis. |
| Organizational knowledge | Notion offers permission-aware search across connected applications. [Enterprise Search](https://www.notion.com/product/enterprise-search) | Keep source permissions in the source system. Reference an approved record and revision instead of indexing a company's entire workspace by default. |
| Evaluation | Langfuse supports repeatable checks and experiment comparisons for LLM applications. [Evals](https://langfuse.com/docs/evaluation/overview) | Start with a replayable local case. Export to an existing evaluation platform once the team needs comparisons across many runs. |
| Creative production | ComfyUI provides a local, node-based engine for image, video, audio and 3D workflows. [Comfy](https://support.comfy.org/articles/9806306061-about-comfy) | Keep rendering in a specialist tool. Capture the source-rights decision, workflow revision and approved output in the creator's workspace. |

## What would establish the difference

Run one real workflow twice with the same acceptance test. Record human minutes, correction count, paid compute where available, and whether the owner accepted the output. Have a second operator rerun it after one reviewed change. Publish only the redacted example and its scope. Faster first drafts alone cannot establish improvement when review time or failure rates grow.

The first commercial experiment should be a scoped Founder Activation Lab: a founder brings one recurring decision, receives an executable configuration, and runs it independently a week later. Ask permission to retain the pass/fail result. A paid cohort, revenue lift and repeat adoption each require separate evidence.
