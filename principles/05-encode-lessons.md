# 5. Put repeated lessons into the structure

A repeated correction should change the next run. A longer prompt is useful only if the system follows it when the failure returns.

**Rule:** turn a recurring mistake into the smallest enforceable change: a validation check, restricted state transition, ownership boundary, idempotency key, or regression test. Record the observation and the new rule separately. Keep uncertain explanations as hypotheses.

**Test:** this starter rejects a sale with no matching source event, refuses existing workspace paths, blocks duplicate owners, and rejects duplicated payment events. Each has a regression test. Removing the guard should make its test fail.

**Limit:** passing synthetic tests is not proof that production is safe. Add a test from the actual failure, replay it without side effects, and verify the real integration separately. Do not encode a one-off anecdote as a universal business policy.
