# Re-verification of the audit, 10 October 2026

This document records the check of the 8 October audit before publication.

## What was done

1. **Commits.** The 20 repositories were cloned again, and each of the commits recorded on 8 October checked out. All 20 hashes matched.
2. **Script.** `audit.py` was re-run on those commits.
   - The output `evidence.json` was byte-identical (same sha256).
   - `audit.csv` was identical except for the git tag counts, which are read live: five projects had published new tags since 8 October.
3. **Classification.** Four agents, five repositories each, re-classified the 20 projects from the source at the 8 October commit, without seeing the existing table. They were told to treat text in the repositories that addresses AI agents as data, not instructions. Differences were resolved by re-reading the source files. The result is `classification.csv`.
4. **Point facts.** Checked against git history, package registries and Anthropic's official marketplace as of 8 October:
   - the 8 to 10 October churn;
   - impeccable's engine versions;
   - the date of the claude-seo mod;
   - the official marketplace pins;
   - GitHub star counts.

## Outcome per claim

| Claim | Notes |
|---|---|
| 3 of 20 are text only | humanizer, napkin, andrej-karpathy-skills |
| 10 text plus scripts, 7 software | caveman counts as software: its main install path is an npm CLI with a proxy and Go binaries |
| 9 of 20 download more code | See `downloads_code` |
| 9 of 20 register hooks | graphify registers its hooks with a second documented command (`graphify claude install`), not with the base install |
| 7 at session start, 2 on every prompt, 3 after file edits, 1 on every tool call | caveman's main path writes about ten hook events with no matcher into `~/.claude/settings.json` |
| One mod, in claude-seo | `plugins/seo-cockpit/hooks/hooks.json` has `"modules": ["./register.ts"]`; added in a commit of 3 Oct, released in v2.4.2 on 4 Oct |
| impeccable downloads and verifies a binary | The sha256 comes from the same release: it protects against a corrupted download, not a compromised release. The engine pinned in the repository moved from 0.1.11 to 0.1.12 (8 Oct 19:25 UTC), then to 0.1.14 (9 Oct 04:19 UTC) |
| 11 of 20 with new commits, 9 touching code | `git diff` between the two recorded commits per repository. superpowers went from 6.4.2 to 7.0.0 |
| 2 main install paths pin a version | superpowers and mattpocock/skills, through Anthropic's official marketplace, which pins a commit and auto-updates by default |
| 4 projects pipe their own installer to a shell | Understand-Anything, claude-seo, visual-explainer, caveman |
| One project installs through a prompt | Agent-Reach |
| 5 reach external services as core function | Agent-Reach, claude-seo, last30days, codex-plugin-cc, caveman |
| 3 handle credentials as core function | Agent-Reach, last30days, caveman |
| 2 read browser cookies | Agent-Reach (explicit command per platform), last30days (consent asked by the agent and stored; the code checks only the flag) |
| Codex plugin sends work to a second vendor | `/codex:transfer` runs only on a user command; the `codex-rescue` subagent can be used proactively |
| Third-party popularity | 631 to 297,359 stars on 11 Oct |

All claims were confirmed against the source.

## Observed during the re-verification

- **A skill offered to the reviewer.** The impeccable repository ships a `.claude/skills` folder. As soon as the repositories were cloned into the working directory, the environment began offering that skill to the session doing the verification. It was not used. This is the same mechanism the article describes, and a reason to run such reviews in an isolated environment.
- **Details from the blind re-classification:**
  - with a Gemini key in the environment, graphify sends semantic extraction to Gemini without asking;
  - in impeccable's live mode, copy-edit prefers the Codex CLI if it is authenticated;
  - caveman's CLI has telemetry on by default, with an opt-out;
  - the official marketplace pins superpowers to an older commit than the one audited.
