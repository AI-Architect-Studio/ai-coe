# Use the existing Academy practice record

The CoE workspace records what happened during a mission. A separate Academy practice record preserves how a particular learner approached it. An assessor can inspect both with the learner's permission. Keep the learner's original attempt, actual assistance, artifact references, critique, revision and response to a transfer task.

The optional bridge delegates practice-record validation to the existing Apache-2.0 Academy plugin. For source inspection, use [the upstream quest skill at the reviewed revision](https://github.com/Starlight-Intelligence/starlight-academy-plugin/blob/01eab519152c5d82368fbe0de46d28ef5718032f/plugins/starlight-academy/skills/run-learning-quest/SKILL.md). For deeper curriculum use the [upstream installation guide](https://github.com/Starlight-Intelligence/starlight-academy-plugin/blob/01eab519152c5d82368fbe0de46d28ef5718032f/docs/academy/README.md).

## Reproduce the optional local inspection

Use Git and Node.js 20 or later. Run in a fresh directory. Network access is needed to fetch the upstream source. The tests and inspector subsequently run offline.

```sh
git clone https://github.com/Starlight-Intelligence/starlight-academy-plugin.git
git -C starlight-academy-plugin checkout --detach 01eab519152c5d82368fbe0de46d28ef5718032f
cd starlight-academy-plugin/plugins/starlight-academy
node --test tests/quest_record.test.mjs
node scripts/quest_record.mjs create frontier-operator | node scripts/quest_record.mjs inspect
```

The blank practice record should inspect as valid with a draft phase. It should report missing learner work and false values for authentication, assessment, certification and authority. Open the [practice-record reference](https://github.com/Starlight-Intelligence/starlight-academy-plugin/blob/01eab519152c5d82368fbe0de46d28ef5718032f/plugins/starlight-academy/skills/run-learning-quest/references/practice-record.md) before editing or importing a learner record.

## Verification, 25 November 2026

Linux, Node.js 24.22.3. The helper, quest catalog and seven upstream tests were fetched from that exact revision. Each local Git blob ID matched its upstream response. The two Node commands above returned zero. The test runner reported seven passed, zero failed. The inspector returned schema `starlight.academy_quest_inspection.v1`, quest `frontier-operator`, catalog `1.0.0`, phase `draft`, and all four truth flags false. There were zero model calls. This replay used GitHub-supplied source bytes and did not exercise the git clone transport, an agent marketplace, a hosted account, or participant assessment.

The upstream technical academy is separately licensed under [FSL-1.1-ALv2](https://github.com/frankxai/ai-architect-academy/blob/main/LICENSE). Point advanced learners directly to its independent repository for RAG, orchestration and MCP labs. This teaching pack contains original exercises and references upstream classroom material by link.
