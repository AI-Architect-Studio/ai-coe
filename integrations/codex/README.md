# Install AI CoE skills in Codex

The assessment runs against the local foundation checkout. Five additional skills come from Starlight Agent Skills at the commit in [skills.lock.json](skills.lock.json). The installer reads Git objects from that revision, ignores working-tree changes and keeps each package's original instructions, manifest, example, evaluation checklist and MIT notice.

## One skill, offline

From the foundation checkout, choose an existing local Git workspace. These commands create a fresh example workspace. The first installation command prints the changes. The second applies them locally.

```sh
COE_WORKSPACE="$(mktemp -d)"
git init -q "$COE_WORKSPACE"
python3 integrations/codex/install.py --workspace "$COE_WORKSPACE" --skill ai-coe-assessment
python3 integrations/codex/install.py --workspace "$COE_WORKSPACE" --skill ai-coe-assessment --apply
python3 integrations/codex/verify.py --workspace "$COE_WORKSPACE" --skill ai-coe-assessment
```

Start Codex in the workspace. Use `$ai-coe-assessment` with the absolute paths to the foundation checkout and the intake JSON. For a synthetic intake, use `examples/founder/input.json` from the checkout. The assessment command runs without a model or credentials. An interactive coding-agent turn uses your own authorized environment.

## Five existing Starlight skills

Get the public dependency once. Use an existing checkout containing the pinned commit when offline. The installer never contacts a remote, executes upstream scripts, enables tools or changes user-wide Codex settings. Adding the same bytes again returns `present`. A conflict stops preflight and identifies the path for human review.

```sh
COE_DEPENDENCY="$(mktemp -d)"
git clone -q https://github.com/Starlight-Intelligence/starlight-agent-skills "$COE_DEPENDENCY"
python3 integrations/codex/install.py --workspace "$COE_WORKSPACE" --upstream "$COE_DEPENDENCY"
python3 integrations/codex/install.py --workspace "$COE_WORKSPACE" --upstream "$COE_DEPENDENCY" --apply
python3 integrations/codex/verify.py --workspace "$COE_WORKSPACE"
```

Pass repeated `--skill NAME` flags to select a subset. Installation requires Python 3.10+ and Git. The discovery check requires `codex` on PATH. Each package is installed under `.agents/skills/<name>/`; delete that package directory after reviewing local changes to uninstall it.

## Choose a skill by outcome

Each upstream package describes its inputs, outputs and tool requirements in `manifest.json`, demonstrates a complete exchange in `examples/example-01.md` and provides a review rubric in `tests/contract.md`. Use the following additional CoE acceptance gates. Keep customer sources, drafts and interview notes within the owner's named boundary.

| Skill | Operator and input | Expected outcome and rejection condition |
| --- | --- | --- |
| ai-coe-assessment | Workspace owner with evidence-backed intake | Return the blueprint, dimension levels and next evidence to collect. Reject inferred scores and cross-boundary evidence collection. |
| claim-verification | Researcher or founder with an exact claim and sources | Return a verdict with traceable evidence and confidence. Use an unverifiable verdict when evidence is unavailable. |
| arxiv-paper-to-brief | Architect with a research paper and decision to inform | Preserve the paper's result, setting and limitations. Omit unsupported metrics and distinguish extrapolation from observation. |
| capability-foundry | Maintainer with a successful mission and named target environments | Return a portable draft and verification handoff. A maintainer reviews every proposed shared-skill change. |
| social-repurposer | Creator with a rights-cleared asset and intended channels | Generate drafts grounded in the original asset. Missing source permissions block reuse. Publishing requires separate approval. |
| simulation-lab-builder | Educator with a learning goal and adjustable variables | Produce a simulation and guided experiment. Review generated code before opening it and test the predicted behavior at each parameter boundary. |

For the founder handoff exercise, use the assessment to identify the evidence gap, `claim-verification` to examine the decision, then `capability-foundry` to propose the next reusable workflow. A reviewer decides whether to promote the proposal.

## Reproduce the evidence

Tested on 2026-11-25 using Linux x86_64, Python 3.12.14, Git 2.56.1, Node v24.22.3 and codex-cli 0.172.0-alpha.2. The probe initializes a real Codex app server in a temporary local profile, calls `skills/list`, then checks the enabled flag, repository scope and absolute path of every requested skill. The probe starts zero model turns. Its output for the six-package installation was:

```json
{
  "client": "codex-cli 0.172.0-alpha.2",
  "method": "skills/list",
  "enabled_repo_skills": ["ai-coe-assessment", "arxiv-paper-to-brief", "capability-foundry", "claim-verification", "simulation-lab-builder", "social-repurposer"],
  "model_turns": 0
}
```

The assessment example selected the founder blueprint and reported level 1 for human expertise and commercial execution. Its research-quality recommendation requests a claim, an attributed excerpt and disconfirming evidence. This exercises the deterministic assessment entry point independently of Codex. The skill installer has regression coverage for preview, repeated installation, local edits, symlinks, missing dependencies, immutable blobs and attribution.

```sh
python3 -m unittest discover -s tests -p 'test_skill_install.py' -v
python3 scripts/coe.py assess --input examples/founder/input.json
git -C "$COE_DEPENDENCY" worktree add --detach "$COE_DEPENDENCY-pinned" 1e5577124c7c8ff48fceaf66037e0d5723cb41cf
make -C "$COE_DEPENDENCY-pinned" check
```

The upstream gate passed on a full-history checkout. It validated 44 skill metadata records and 25 worked output fixtures including all five selected dependencies. Nineteen other skills lacked a fixture or manifest. Plugin and release checks also passed. Runtime discovery and deterministic fixture checks provide different evidence. Model-generated quality, live research, publishing and interactive invocation in other runtimes remain unmeasured.

## Packaging decisions and prior art

| Source | Decision applied |
| --- | --- |
| [Agent Skills specification](https://agentskills.io/specification) | Use a directory with a matching lowercase skill name, required frontmatter and loadable instruction body. |
| [OpenAI Codex installation reference](https://developers.openai.com/api/reference/cli) and [app-server protocol](https://developers.openai.com/codex/app-server/) | Install project-scoped packages and verify discovery through the runtime. |
| [OpenAI Skills Catalog](https://github.com/openai/skills) and [Anthropic skills](https://github.com/anthropics/skills) | Benchmark discoverable task descriptions, concrete examples and per-package licensing. The implementation contains no material copied from these catalogs. |
| [Starlight Agent Skills at the lock](https://github.com/Starlight-Intelligence/starlight-agent-skills/tree/1e5577124c7c8ff48fceaf66037e0d5723cb41cf/skills) | Reuse the five selected maintained packages. The lock excludes the separately licensed Arcanea material. |
| [Starlight Design Intelligence](https://github.com/frankxai/starlight-design-intelligence/tree/ac43168bb58587c4b92b84f05a8b2bab8e360df5) | Use the canonical design release method for future web design expansion. Its package and runtime have a separate verification boundary. |

### A founder decision reviewed against the sources

A reviewer applied the installed `claim-verification` workflow to the founder example in this authoring session. The synthetic interviews establish a retrieval problem but contain no price discussion, purchasing commitment or integration requirement. The [result](examples/founder-claim-review.json) records the verdict, three exact source quotations and the scope of its confidence. The source-grounding test below makes the artifact independently checkable. Codex's app server was used separately for discovery.

```sh
python3 -m unittest discover -s tests -p 'test_skill_install.py'
```
