# Give execution one owner

Parallel analysis can help. Competing workers mutating the same business state can duplicate messages, collide on files, or wait for one another forever.

**Rule:** one active owner per mutation scope. Acquire ownership before work, retain an idempotency key for each side effect, and close the task with evidence or a reason.

A task needs an owner, verifier, budget, deadline, permitted actions, proof, and stop condition. Handoffs name the next owner. A denied lock means no mutation.

**Test:** the demo's local lock rejects a second owner. The unit tests exercise denial and release after an exception.

**Limit:** the sample lock has no distributed lease or automatic stale-lock recovery. A crash requires inspection before manual removal. Production workers need expiration plus fencing so an expired worker cannot resume writing. Do not treat a file lock as a distributed scheduler.
