# Five-minute live demo

No login, live payment, or network dependency. All data is synthetic.

1. **Show the business (45 seconds).** Open `examples/fieldnotes-kit/README.md`. A fictional $29 workbook helps independent consultants prepare customer interviews. The product and sample landing page are local files.
2. **Run the operating loop (60 seconds).** `python3 scripts/company_os.py demo --output /tmp/company-os-demo-unique` (choose a path that does not exist). Show the selected bottleneck and task. Reliable visits but zero offer interactions point to the offer handoff in this synthetic scenario.
3. **Catch false success (60 seconds).** The worker says it sold something; the verifier rejects the claim because the ledger has no matching purchase. Show `claim-rejected.json`.
4. **Show financial distinctions (60 seconds).** Two synthetic $29 purchases, one $29 refund, and $2 in fees yield $58 gross, $29 refunds, $27 after fees. Settlement and profit remain unknown. Run `python3 scripts/company_os.py verify /tmp/company-os-demo-unique`.
5. **Make it theirs (75 seconds).** Show START_HERE.md, the boot prompt, and principles. Ask: which business step would you trust an agent with today, and what evidence would make you trust the next one?

Backup: keep a completed demo directory open. Say it is a recorded synthetic run if using it. A successful local demo does not prove access to a live commerce provider or demand for the product.
