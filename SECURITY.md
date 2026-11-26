# Security and ownership

The operator owns the destination workspace and decides which source material may enter it. Use a directory under your control, with private filesystem permissions for personal or customer material. A shared filesystem, cloud-synced folder or Git working tree also inherits that system's access and backup settings.

## Activation boundary

| Decision | Authority | Evidence to keep |
| --- | --- | --- |
| Read a mission brief and evidence | The operator selects the inputs and their intended audience | References to approved files or redacted excerpts |
| Write a local workspace | The operator reviews the plan and authorizes the local apply step | Destination, generated artifacts and evaluation |
| Change a shared skill or production workflow | The accountable maintainer reviews a candidate diff and runs its evaluation | Old and proposed revisions, result, reviewer and rollback target |
| Change a memory policy, permission, budget or destination | The data or system owner approves the exact scope before configuration changes | Scope, reviewer, destination and revocation procedure |
| Publish, send, spend or deploy | A separate authorization identifies the external target, payload and cost ceiling where applicable | Receipt from the executing system |

An activation approval covers the local write. The mission brief, imported document, model output and evidence record each supply **data**. None can approve an action, enlarge a tool's permissions or authorize transmission. The agent host can have broader access than this CLI. Configure its filesystem and network permissions for the particular mission.

Use the repository's [data boundaries](governance/data-boundaries.md) to classify sources and the [trust model](governance/trust-tiers.md) to evaluate each integration. Provenance helps set the maximum scope. Grant only the access needed for this mission, including for local tools. Keep customer, personal and shared business evidence in separately controlled workspaces.

## Interrupted activation

The runner snapshots each complete supplied file into a replay bundle. Use a trusted workspace where other users cannot replace paths while it runs. Staging uses a mode-0700 directory with a Git ignore rule. The runner stages output inside the chosen workspace and publishes the finished directory as `.ai-coe`. After a hard process termination, an activation lock or a temporary `.coe-stage-*` directory can remain. Check that the original process has ended. Inspect `.ai-coe` first: a complete published workspace may already exist. With exclusive control of the workspace, the operator can remove that run’s stale lock and staging files and rerun preview. Leave a published workspace and other operators’ files intact. Ordinary retries preserve existing state.

## Improvement and rollback

A mission concludes with an artifact, a judgment about its quality, and a candidate improvement. Promote the candidate using the existing [capability and risk reviews](operating-model/04-review.md). For a proposed workflow change, rerun the old and new revisions on the same fixture, inspect the actual outcome and record any regression. Keep the last accepted revision available. Change requests for shared memory policies and permissions go to their owner even when the mission was successful.

## Handling private evidence

- Keep credentials in the provider's credential store or the runtime's secret manager. Use purpose-created fixtures in examples and test receipts. Review free-text briefs, filenames, source references and generated artifacts before sharing them.
- The operator selects retention, backup and deletion for local data. Check copied artifacts, Git history, provider logs and backups when handling a deletion request.
- A hash establishes that bytes match a recorded digest. Human review determines source ownership, truth of a claim and fitness of a generated result.
- Installing the foundation does not assign rights in operator inputs or outputs. Existing rights, contracts, provider terms and third-party licenses still apply. A link to a dependency does not grant redistribution rights.
- When a source or destination is outside the approved boundary, retain a local reference or synthetic example and have its owner decide whether any excerpt may leave.

## Reporting an issue

Use the repository's **Security → Report a vulnerability** action when available. If disabled, ask a maintainer for a private reporting channel without including sensitive details. Provide the affected revision, expected boundary, observed result and a minimal sanitized example. Rotate an exposed credential through its issuer and check its access history.

[GitHub reporting guidance](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately) · [OWASP excessive agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
