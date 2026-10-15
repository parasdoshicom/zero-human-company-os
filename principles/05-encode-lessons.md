# 5. Put repeated lessons into the structure

A repeated correction should change the next run. A longer prompt is useful only if the system follows it when the failure returns.

## What taught me this

Six seller agents kept coordinating while nobody sold. Telling them to choose one owner was not enough. The system needed a check before work started: one worker enters; the others exit.

The change was to move a recurring correction into the mechanism. This starter demonstrates a local exclusive lock and a regression test that rejects a second worker. Humans remain accountable for the business; the lock only coordinates execution. [Published account](https://www.insightextractor.com/p/dont-spend-5000-on-an-ai-course-start).

**Rule:** turn a recurring mistake into the smallest enforceable change: a validation check, restricted state transition, ownership boundary, idempotency key, or regression test. Record the observation and the new rule separately. Keep uncertain explanations as hypotheses.

**Test:** this starter rejects a sale with no matching source event, refuses existing workspace paths, blocks duplicate owners, and rejects duplicated payment events. Each has a regression test. Removing the guard should make its test fail.

**Limit:** passing synthetic tests is not proof that production is safe. Add a test from the actual failure, replay it without side effects, and verify the real integration separately. Do not encode a one-off anecdote as a universal business policy.
