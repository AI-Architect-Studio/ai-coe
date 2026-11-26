# Review an outcome and measure a repeat

An operator who has inspected the actual work can record an acceptance, revision request or stop decision. Measure elapsed task minutes and count substantive operator interventions with one agreed definition for both runs. A run can finish with a useful decision to stop.

From the repository, set the variables below to your actual review. Use `accept`, `revise` or `stop`. Review the preview and add `--apply` to that command to save the local record. The script never sends a decision to an upstream system.

```bash
python3 scripts/mission_review.py record --workspace my-coe \
  --reviewer "$REVIEWER" --decision "$DECISION" --reason "$REVIEW_REASON" \
  --minutes "$ELAPSED_MINUTES" --interventions "$INTERVENTIONS"
```

Finish a second mission with the same owner, goal and blueprint in another workspace. Keep the baseline task comparable and document what changed. After recording both reviews, compare them:

```bash
python3 scripts/mission_review.py compare --before my-coe --after my-coe-repeat
```

The comparison reports deltas as **after minus before** and both decisions. An illustrative regression fixture supplies 12 and 8 minutes, producing `minutes_delta: -4`. Those are invented test inputs. A real improvement claim requires actual observations, comparable work and review of outcome quality. A faster rejected result may be less valuable.

The local record binds the reviewer’s assertion to the byte hashes of the decision, machine receipt assessment, source manifest and replay intake. It checks the stored source digests against the replayed evidence. It refuses to overwrite an existing review or compare an artifact subsequently edited in place. These records are owner-controlled and unsigned. They support local review; an enterprise requiring authenticated attestations must bind its identity and immutable storage separately. Promote a proposed skill or policy change through the existing six-loop review.
