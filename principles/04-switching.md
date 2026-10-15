# 4. New tools have to earn the switch

A working workflow is an asset. Replacing it costs setup time, access debugging, regression recovery, and attention even when token capacity looks attractive.

## What taught me this

OpenClaw was working. The move to Hermes cost a full week of regression before returning to that baseline; after 30 days, it still had not surpassed it. Dot's advertised capacity was appealing, but repeated access failures stopped the work and I moved it back to Hermes.

The change is a smaller trial before a full migration. Preserve the working path, run the same task on both, and count the time you spend repairing the candidate. My timeline is a firsthand assessment, not a controlled benchmark. It says nothing about a model's reasoning quality in isolation.

**Rule:** run a candidate alongside the baseline on one bounded workflow. Measure destination-verified completion, time, total cost, recovery effort, and access reliability. Set the acceptance rule and rollback path before migrating.

**Test:** fill [the switch trial](../templates/switch-trial.md). A candidate that is cheaper per token but cannot reach the required business system does not pass.

**Limit:** a security issue, unsupported baseline, or essential new capability can justify migration before performance improves. Record that tradeoff explicitly.
