# 3. Completion needs independent proof

A worker can create a file called `sale-confirmed.md` without selling anything. A verifier must use a source that establishes the claimed event.

## What taught me this

An agent could see its own Reddit post and treated it as published. Other people could not see it. Checking from outside the posting account changed the answer. In another failure, yesterday's sale satisfied today's goal because the decision window was missing.

The change was to specify what claim a source can establish, including business identity and event time. A visible draft, a published post, a purchase and a settled payout need different proof. [Published account](https://www.insightextractor.com/p/dont-spend-5000-on-an-ai-course-start).

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
