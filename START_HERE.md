# Your first ten minutes

## 1. See the contract fail safely

Run `python3 scripts/company_os.py demo`, then `python3 scripts/company_os.py verify demo-output`. The first command prints a rejected fake sale and a verified synthetic ledger. Open `demo-output/report.json` and `demo-output/task.json`. No network, accounts, or model is involved.

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

Fill `brief.md`, then `permissions.json`. Unknown answers remain unknown. Do not fabricate research or testimonials.

## 4. Prepare one complete path

Use [the lifecycle](docs/business-lifecycle.md). Make a useful sample; draft the offer; plan checkout, fulfillment, refunds, and support. Test locally. Then ask the owner to approve a narrow live test using their business accounts. Record platform test-mode receipts separately from real transactions.

## 5. Run one decision loop

Pick a bottleneck from observations. Write a task using `templates/task.json`, take one bounded action, and verify its result against the declared source. Update `learning/` with what happened and the next measurement time. Do not schedule a repeat until the manual flow works and the owner authorizes the schedule.

You are ready for a real pilot when the owner approves the offer and accounts, checkout and delivery pass an end-to-end test, support and refunds have an owner, tracking distinguishes tests from customers, and one legitimate distribution path is available. Those are acceptance criteria, not claims made by this starter.
