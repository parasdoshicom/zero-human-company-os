# 2. Fix the most brittle link

A capable model cannot finish work if it cannot reach the required computer, browser, account, or integration. Before improving reasoning, find out whether execution can reach the destination.

## What taught me this

I could have a reasonable plan and still lose the run to computer or browser access. In my setup, Codex computer use made that execution path more reliable. More reasoning capacity would not have repaired a session the worker could not use.

The change was to check the required route before handing it a long job, then isolate the failure when it breaks. That costs a small amount of setup time; it saves treating an access problem as a product or marketing problem. This is my operating experience, not a vendor benchmark.

**Rule:** preflight the exact access needed for the next bounded task. Record the observed failure, scope, retry condition, and approved routes still open. Repair once within budget, or stop that route. Keep unrelated work moving.

**Test:** set `access_ok` to false in the synthetic funnel. The router returns `execution_access` before diagnosing marketing. The regression test preserves this ordering. Production preflight must inspect the real route; the Boolean fixture is not an access probe.

**Limit:** access is necessary but does not establish demand, permission, or reliable unattended operation. An available account is not authorization to send.
