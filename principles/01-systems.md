# 1. Systems thinking comes first

“Make revenue” does not tell a worker what to do next. Define the customer's path and identify what is unproven.

For a simple one-off product, a planning model is:

`expected gross sales = qualified visits × purchase conversion × price`

If conversion is measured only on successfully delivered experiences, model delivery reliability separately. If observed conversion already includes failed visits, multiplying by reliability again double counts the loss. Fees, refunds, tax, support, acquisition, and operating costs belong in separate reconciliation; gross sales are not profit.

Track exposure → qualified visit → offer interaction → checkout → paid order → successful delivery → retained value. A count of zero needs a valid observation window and a working sensor. No tracking means unknown.

## What taught me this

In one loop, agents ran for 49.8 hours and recorded 54 experiments without a purchase. That was one historical loop, not the business's lifetime result. “Make revenue” left too many decisions implicit: whom to reach, which offer to test, what evidence to collect, and when to stop.

The change was to name the stages and give the next worker a bounded decision. If qualified visits are missing, another product revision may be wasted work. If visit tracking is broken, even that diagnosis is premature. [Published account](https://www.insightextractor.com/p/dont-spend-5000-on-an-ai-course-start).

**Rule:** fix a broken prerequisite first; otherwise choose the earliest stage with sufficient evidence of failure. If there is not enough evidence, collect it before diagnosing.

**Test:** give the agent no trustworthy visit data. It should choose measurement, not announce a conversion problem. The local demo tests this case.

**Limit:** subscriptions, enterprise sales, and marketplaces need different stages and time windows. Do not force them into a one-off purchase funnel.
