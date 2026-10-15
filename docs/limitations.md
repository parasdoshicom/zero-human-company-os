# What works and what still needs integration

**Implemented:** dependency-free workspace initializer; deterministic synthetic funnel routing; file-based local ownership; rejection of unsupported payment claims; integer-cent reconciliation of purchase/refund/fee fixtures; provenance and synthetic-mode checks; unit tests; local link and secret-pattern scan.

**Not implemented:** model invocation, autonomous planning, live analytics, payment collection, payment-provider authentication, hosting, customer delivery, email/social publishing, customer support inboxes, production scheduling, distributed ownership, idempotent external side effects, durable secret storage, legal/tax compliance, or fraud detection.

The verifier is a separate function reading a ledger file. It is independent of the worker's claimed result, but the files share a writable machine. It is not a tamper-proof trust boundary. Production verification must read authoritative systems with appropriate access separation.

The funnel router is a teaching heuristic. It uses minimum exposure thresholds supplied in the fixture; these are not statistically justified commercial benchmarks. Real operators should set thresholds and windows for their business and inspect measurement validity.

The demo's local lock never deletes another owner's lock. A crash can leave it behind. Inspect the prior run, ensure no worker remains, and remove the stale local lock manually. Never apply this recovery blindly to live external work.

The repository checker catches some common secret and private-path patterns. Passing it is not a complete security audit. Review the diff and all artifacts before publishing.
