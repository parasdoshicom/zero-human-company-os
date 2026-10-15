# Five-minute live demo

No login, live payment or network dependency. All business data is synthetic. The offer revision is deterministic supplied copy; no model writes it during the run.

1. **Show the business (45 seconds).** Open [Fieldnotes Kit](../examples/fieldnotes-kit/README.md). A fictional $29 workbook helps independent consultants prepare customer interviews. Show the sample product.
2. **Run one local task (75 seconds).** Run the commands below. Open `funnel.json`, `task.json` and `draft.md`. Access and measurement are valid in this fixture; 120 visits with zero offer interactions select the offer handoff. The task saves a draft locally, within its stated contract.
3. **Check completion (60 seconds).** Open `artifact-proof.json` and the task's terminal state. A file hash and deterministic checks establish which local example was saved. They do not establish demand or better conversion. The verifier rejects changed task permissions, budgets, terminal state, artifacts or proof.
4. **Catch false success (60 seconds).** Show `claim-rejected.json`. Then show `report.json`: two synthetic $29 purchases, one $29 refund and $2 in fees yield $27 after fees. This is a separate accounting window from the zero-purchase acquisition cohort. Settlement and profit remain unknown.
5. **Make it theirs (60 seconds).** Open `learning.json`, then [setup](../START_HERE.md) and [the pilot plan](pilot-plan.md). Ask what single business task the audience would start with and what evidence would close it.

```bash
python3 scripts/company_os.py demo --output /tmp/company-os-stage-run
python3 scripts/company_os.py verify /tmp/company-os-stage-run
```

Choose a new output path for each rehearsal. Existing directories are refused to preserve prior evidence. After updating this repo, create a fresh demo; old outputs may not match the current verifier's fixtures.

Backup: keep a completed directory open. Say it is a recorded synthetic run if using it. A successful local demo does not prove access to live commerce or demand for the product. For the full narrative, read [the worked example](worked-example.md).
