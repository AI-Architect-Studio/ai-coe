# Evidence-based capability assessment

The owner attests that a specific source demonstrates a gate in a specific domain. The runner verifies the excerpt, hashes the file and evaluates the gates in order. Every earned level requires at least one source with a digest new to that domain's preceding gates. A missing earlier gate blocks advancement. An empty record is unknown. There is no aggregate score. A machine can verify bytes; a second operator judges whether the example deserves its claimed level.

| Level | Name | Evidence to inspect |
| --- | --- | --- |
| 1 | Fragmented experimentation | An attributable observed attempt |
| 2 | Repeatable individual workflows | A separate repeat using a reusable method |
| 3 | Connected intelligence environment | Persistent context crosses a capability boundary |
| 4 | Governed human–agent organization | Owner, boundary and evaluation are visible in a reviewed decision |
| 5 | Continuously improving intelligence system | Comparable before/after results tied to an approved change |

The [rubric](rubric.json) supplies domain-specific actions for all eleven capabilities. A blueprint nominates two priorities for the next sprint. The baseline also returns the next missing evidence for every domain. Review a sample of attestations for relevance, disputed provenance and duplicated events across differently formatted files. A human-attested level is provisional until that review.

In the [founder intake](../examples/founder/input.json), a customer interview and a founder decision note earn level 1 for commercial execution and human expertise. Nine domains stay unknown. The synthetic operators have demonstrated neither a second use nor an accepted business outcome. Select evidence dated after the first attempt to support a repeat. An improvement claim should name task, denominator, measurement window, comparable conditions and the approving reviewer.

The [intake JSON Schema](../schemas/intake.schema.json) defines the wire format. Runtime checks additionally enforce source containment, matching excerpts, candidate/source references, duplicate-key rejection and digest-based evidence counts.

Consumers can validate the emitted report against the [assessment result schema](../schemas/assessment-result.schema.json). The [example baseline](../examples/founder/workspace/assessments/baseline.json) is byte-checked by the activation tests.
