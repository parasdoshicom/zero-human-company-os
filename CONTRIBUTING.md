# Contribute a useful operating lesson

A good contribution makes a failure easier to catch or a decision easier to make.

For a principle, include: observed failure (anonymized), proposed rule, evidence and date, test or counterexample, limitation, and what would change your mind. Personal experience is welcome when labeled. Please do not turn vendor preferences into universal rankings.

For code, add a regression test and run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_repo.py
```

Use synthetic data. Never submit customer records, private prompts, credentials, raw receipts, account IDs, or employer information. Do not add automatic outbound actions or broaden the default permissions. Discuss live integration designs before implementing them.

Keep each change small enough to review. Explain the problem, the behavior after the change, and how you verified it. Contributions use the repository's MIT license.
