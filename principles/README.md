# Company Stack principles

These are operating hypotheses with consequences. Try them, record counterexamples, and improve them. The ranking reflects the current teaching order, not a universal law.

| Rank | Judgment | Put it to work |
|---|---|---|
| 1 | [Systems thinking comes first](01-systems.md) | Define stages before delegating |
| 2 | [Fix the brittle link](02-brittle-link.md) | Check required access before committing a run |
| 3 | [Independent proof](03-proof.md) | Make false success fail |
| 4 | [Earn the switch](04-switching.md) | Compare on the same real workflow |
| 5 | [Encode the lesson](05-encode-lessons.md) | Replace repeated reminders with checks |

Additional mechanisms: [one execution owner](execution-ownership.md) and [distribution dependencies](distribution.md). Humans remain accountable; execution ownership is a coordination rule.

## Supporting rules

- **Freshness is part of truth.** An old account error is not today's status. Recheck the precise dependency when its retry condition arrives.
- **Local failure stays local.** Record which route failed and which approved routes remain available.
- **Memory needs evidence.** Store a result, uncertainty, and next test; don't promote a plausible story into strategy.
- **One variable per commercial test.** Changing audience, price, promise, and channel at once makes learning harder.
- **Costs include human recovery.** Track money and minutes spent repairing the system.
- **Support is part of the product.** Someone owns delivery failures, refunds, and customer expectations.
- **Use small permissions.** A scoped pilot is easier to inspect and revoke than a broad autonomous mandate.

To add a principle, include the failure it addresses, the rule, a runnable or observable test, and when it does not apply. Use [CONTRIBUTING.md](../CONTRIBUTING.md).
