# 3. Completion needs independent proof

A worker can create a file called `sale-confirmed.md` without selling anything. A verifier must use a source that establishes the claimed event.

**Rule:** declare the evidence source before execution. Read it after the action. Preserve uncertainty if the source is missing, stale, contradictory, or in test mode.

| Claim | Appropriate evidence |
|---|---|
| Draft ready | Saved artifact, reviewed against brief |
| Published | Correct destination and account; persistent content readback |
| Paid | Authoritative payment record, correct currency and business, live mode |
| Settled | Payout or bank reconciliation with timing and fees |
| Profitable | Revenue less all relevant costs over a defined window |

**Test:** the demo rejects a sale claim with no payment record. Its valid synthetic ledger proves only that the reconciliation code handles those fixtures. The fixture is not an independent external payment source.

**Limit:** a second agent reading the first agent's summary is not independent verification. Production needs provider readback, immutable records where appropriate, and access controls beyond this starter.
