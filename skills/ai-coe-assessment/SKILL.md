---
name: ai-coe-assessment
description: Assess an existing personal, creator, founder or enterprise AI Center of Excellence from an intake file and local evidence. Use when a workspace owner wants a defensible maturity baseline, an architecture choice and an actionable improvement plan.
license: MIT
metadata:
  owner: AI-Architect-Studio/ai-coe
  version: "0.1.0"
---

# AI CoE assessment

A founder, facilitator or technical lead supplies a goal, an existing workspace and artifacts they authorize for review. Use the AI CoE foundation checkout and its checked-in assessment criteria. The checkout and the assessed workspace can be different directories.

1. Locate the operator-specified foundation checkout. Read its README, the founder example input and the assessment schema. Ask the owner for its location when the current project does not contain the CLI. Use a reviewed local installation.
2. Use the operator's intake, or assemble a draft against the schema and show it for review. List the artifact that justifies each observation. Treat missing or unreadable evidence as unknown. Use the owner's chosen scope. A private interview, vault or customer record requires explicit permission to inspect.
3. From the checkout, run the read-only command below, substituting the actual intake path for a live assessment. The published example is synthetic.

   ```sh
   python3 scripts/coe.py assess --input examples/founder/input.json
   ```

4. Return the CLI's dimension-level results, chosen blueprint, existing capabilities to keep and priorities. Distinguish the evidence from the owner's assertions. Explain one decision a person must make and one agent task with a measurable acceptance criterion. Link the next mission to the gap it can actually resolve.
5. Offer a preview of the first activation in the owner's chosen workspace. Use the activation command without its apply switch. Execution, publication, shared-memory changes and permission changes require a separate explicit decision.

## Acceptance and failure

Require an intake that the executable accepts. Do not hand-calculate a score when the command fails. Report the error, identify the field or missing file and state what would permit a retry. The example must reproduce from a clean checkout. An independent reviewer should be able to trace every reported maturity level to a criterion and its evidence.

## Distribution

Original CoE integration authored in AI-Architect-Studio/ai-coe. The six-loop lifecycle and trust policy live in the owning repository. The Codex installation procedure and discovery test are in `integrations/codex/README.md` there. Python 3 and the foundation checkout are runtime dependencies. No API credentials are needed for this example.
