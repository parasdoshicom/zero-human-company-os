# Your first ten minutes

## 1. See the contract fail safely

Run `python3 scripts/company_os.py demo`, then `python3 scripts/company_os.py verify demo-output`. The first command completes a local offer-drafting task and prints a rejected fake sale plus a reconciled synthetic ledger. Open `demo-output/task.json` and the draft and proof files named in it; follow [the worked example](docs/worked-example.md). No network, accounts, or model is involved.

Use `--output /path/to/new-demo-folder` for another run. Existing output is refused so an earlier run stays inspectable.

## 2. Create a private workspace

```bash
python3 scripts/company_os.py init --workspace ../my-private-company --name "My Company"
```

This copies the starter templates and fictional example, writes a private-workspace warning and draft permissions, and creates folders for product, operations, evidence, and learning. It refuses existing paths and paths inside the public checkout.

## 3. Answer five questions with your agent

1. Who has a problem you understand well enough to help?
2. What small digital product could solve one part of it?
3. What would make a buyer believe the promise?
4. Where can you legitimately reach those people?
5. Who owns the accounts, budget, support, and final decisions?

Fill `brief.md` and the five required fields in `setup.json`, then review `permissions.json`. Unknown answers remain unknown. Do not fabricate research or testimonials.

From this source checkout run `python3 scripts/company_os.py check-workspace ../my-private-company`. It reports missing inputs and the next action. `ready_for_local_draft` means enough setup to draft locally; it does not authorize or validate live accounts.

## 4. Prepare one complete path

Use [the lifecycle](docs/business-lifecycle.md). Make a useful sample; draft the offer; plan checkout, fulfillment, refunds, and support. Test locally. Then ask the owner to approve a narrow live test using their business accounts. Record platform test-mode receipts separately from real transactions.

## 5. Run one decision loop

Pick a bottleneck from observations. Write a task using `templates/task.json`, take one bounded action, and verify its result against the declared source. Update `learning/` with what happened and the next measurement time. Do not schedule a repeat until the manual flow works and the owner authorizes the schedule.

You are ready for a real pilot when the owner approves the offer and accounts, checkout and delivery pass an end-to-end test, support and refunds have an owner, tracking distinguishes tests from customers, and one legitimate distribution path is available. Those are acceptance criteria, not claims made by this starter.

## What to do after setup

Use [the pilot plan](docs/pilot-plan.md) to connect the local patterns to your own business. The initializer creates a workspace; it does not validate your product, accounts or permissions.
