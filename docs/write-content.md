# Write in the owner's voice, then verify the result

Use [Your Voice](https://github.com/parasdoshicom/your-voice) for blog posts, product guides, landing pages, LinkedIn drafts, Reddit contributions, and customer-facing explanations. It is an optional agent skill. Once installed, use it by default for human-facing prose; its instructions remain the writing-policy source. Company OS supplies the business brief, evidence, permissions, and completion checks.

This is a workflow for your agent, not an automatic publishing integration. The deterministic Company OS demo does not call a model or invoke Your Voice.

## Optional setup

The upstream [installation instructions](https://github.com/parasdoshicom/your-voice#install-or-update), checked October 15, 2026, use:

```bash
git clone https://github.com/parasdoshicom/your-voice.git
cd your-voice
./scripts/install.sh
python3 scripts/check_install.py
```

Run the installer only when you choose to install the skill. It links the checkout into supported user skill directories for Codex and Hermes, and existing OpenClaw installations where present; it does not install OpenClaw. For other agents, follow the upstream instructions to link or copy `your-voice` into the supported skill directory. Company OS does not run this installer or change your runtime.

Set the default in your agent's shared instructions, following upstream:

> For human-facing prose, apply Your Voice by default. Use its instructions as one writing policy; do not stack or restate generic prose-cleanup rules.

Create your own private voice profile using the upstream profile template and approved writing samples. Do not adopt the repository author's personal profile as your own voice. If the skill is unavailable, say so and follow the owner's supplied writing brief; do not claim a Your Voice review occurred.

## One content task, end to end

| Step | Save in the private workspace | Completion check |
|---|---|---|
| Brief | Reader, problem, purpose, channel, useful next action, scope, source dates, claims that must survive | The content addresses the selected business bottleneck |
| Draft | One version with its sources and unresolved questions | It contains useful substance rather than unsupported promises |
| Voice review | Your Voice review against the brief and the owner's approved samples | Meaning, uncertainty, and the owner's voice survive the edit |
| Fact check | Claim-to-source notes; calculations reproduced separately where needed | No invented evidence, customer outcomes, testimonials, or misleading certainty |
| Approval | Exact final artifact, business account, destination, time window, and approval reference | Approval covers this version and action; later changes require renewed approval |
| Publication | Only through a separately authorized connector or owner action | Correct destination confirms persistent content; a draft or click is not publication |
| Review | Observed reach, qualified engagement, and next funnel event with source/time | Separate publication, engagement, and commercial outcomes |

For an analytical claim, use [GetChatData](https://github.com/parasdoshicom/getchatdata) as a companion workflow for definitions, data checks, and reproducible analysis. Preserve the underlying evidence and its limitations. A polished explanation does not validate the analysis, and analysis output does not authorize publication.

## A reusable agent request

> Read the company brief and current task. Draft one useful [blog post / guide / LinkedIn post / Reddit contribution] for [reader] about [problem], using only the attached public-safe sources. Apply the installed Your Voice skill and my private approved samples. Preserve uncertainty and flag unsupported claims. Save the draft and claim-to-source notes locally. Stop for review before publication. Do not publish, send, or change accounts.

Replace the bracketed fields before use. For a Reddit community or another moderated channel, first read its current participation rules. A contribution should answer an actual need; do not disguise promotion or work around access restrictions.

## Optional draft audit

From the Your Voice checkout:

```bash
python3 scripts/audit_text.py /path/to/private/draft.md
```

The upstream auditor produces review candidates. Exit status 1 is not a writing failure, and a clean audit does not prove truth, quality, or voice fidelity. Review the actual draft; never edit just to make the count reach zero.
