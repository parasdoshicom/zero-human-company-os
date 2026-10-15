# What works and what still needs integration

**Implemented:** dependency-free workspace initializer; private-workspace input check; deterministic synthetic funnel routing; checked local offer artifact and terminal task record; file-based local ownership; rejection of unsupported payment claims; integer-cent reconciliation of purchase/refund/fee fixtures; business identity, event-window and synthetic-mode checks; unit tests; local link and secret-pattern scan.

**Not implemented:** model invocation, autonomous planning, live analytics, payment collection, payment-provider authentication, hosting, customer delivery, email/social publishing, customer support inboxes, production scheduling, distributed ownership, idempotent external side effects, durable secret storage, legal/tax compliance, or fraud detection.

The demo verifier replays declared fixtures, checks the complete recorded task contract and compares the artifact and proof with the supplied deterministic example. It is a separate function reading local files. It is independent of the worker's claimed result, but the files share a writable machine. It is not a tamper-proof trust boundary. Production verification must read authoritative systems with appropriate access separation.

The funnel router is a teaching heuristic. It uses minimum exposure thresholds supplied in the fixture; these are not statistically justified commercial benchmarks. Real operators should set thresholds and windows for their business and inspect measurement validity.

The demo's local lock never deletes another owner's lock. A crash can leave it behind. Inspect the prior run, ensure no worker remains, and remove the stale local lock manually. Never apply this recovery blindly to live external work.

The repository checker catches some common secret and private-path patterns. Passing it is not a complete security audit. Review the diff and all artifacts before publishing.

`check-workspace` checks required setup fields and reports account scope; it does not establish product quality, valid customer evidence, identity ownership or permission to use external tools. Its highest readiness state is `ready_for_local_draft`, and `live_ready` remains false.
