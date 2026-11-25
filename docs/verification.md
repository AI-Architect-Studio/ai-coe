# Release evidence · 25 November 2026

Tested on Linux x86_64, Python 3.12.14, Git 2.56.1, Node 24.22.3 and Codex CLI 0.172.0-alpha.2. The Git commit containing this document identifies the tested source; use `git rev-parse HEAD` in the checkout. The canonical baseline is `064826f3c6c9f662c6f3f9b364ff428b48efcd91`. The upstream probes use their own immutable revisions in the registry and skill lock.

| Exercise | Observed result |
| --- | --- |
| Local test suite | 21 tests passed, including four profiles, exact checked example, replay from moved evidence, maturity gaps, contrary evidence, two competing activations, local edits, skill installation and registry constraints |
| Intake and registry schemas | Both schemas passed Draft 2020-12 metaschema validation; both published fixtures passed their matching schema |
| Synthetic founder activation | Two candidate actions, four source digests, one contrary interview, proposed handoff pilot, pending owner sign-off. Fourteen files written after approval |
| Independent changed-input review | Reclassifying one interview as contrary evidence changed the disposition to resolve conflicting evidence; the reviewer controlled sign-off |
| Repository selection with genuine source objects | Three fact records tied to six existing governance, operating-model and role files supported extension; absence of a baseline LICENSE supplied counterevidence. Selected experiment: contribute to the existing owner under explicit license scope |
| Codex host | Six project-local skills enabled and discovered via app-server; zero model turns. Five upstream goldens are included in the full upstream gate of 25 fixtures |
| Commerce and compute probes | A local fixture produced a EUR 120.00 quote draft with approval required, repeated idempotently and outbound disabled. The harness passed 22 deterministic checker fixtures |
| Academy bridge | Seven upstream practice-record checks passed. No learner credential or human pilot was issued |
| Legacy vendor drift check | Existing check skipped after HTTP 404 for its old plugin branch. No vendor match is claimed |

### Reproduce

```sh
python3 -B -m unittest discover -s tests -v
python3 scripts/coe.py assess --input examples/founder/input.json
mkdir synthetic-mission repository-mission
python3 scripts/coe.py activate --input examples/founder/input.json --workspace synthetic-mission
python3 scripts/coe.py activate --input examples/founder/input.json --workspace synthetic-mission --apply
python3 examples/repository_decision.py --workspace repository-mission --apply
cat repository-mission/.ai-coe/evaluations/receipt.json
node scripts/sync-check.mjs
```

The historical repository-selection example reads the baseline commit. A full clone contains it. For a shallow clone, fetch the specified baseline first. See [Codex reproducibility](../integrations/codex/README.md), [upstream fixture commands](portfolio-architecture.md), [Academy replay](../curriculum/academy-bridge.md) and [the complete synthetic workspace](../examples/founder/workspace).

All stated local mission and probe charges are zero metered provider calls. Machine time, human review and subscription allocation were not priced. Linux is the tested platform. Source matching verifies bytes and attributed excerpts. Claim truth, educational transfer, live provider routing, customer acquisition and commercial fulfillment require separate evidence.
