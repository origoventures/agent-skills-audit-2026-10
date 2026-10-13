# Human check of the article's claims (13 October 2026)

Fulvio Vanacore checked, by hand, every claim the article makes about a named project, plus the main counts and the two cited studies, against the source lines linked below. All links point to the commits audited on 8 October 2026. The check was guided by an AI agent, which prepared the links and said what to look for; the reading and the confirmation are his.

Result: 16 of 16 claims confirmed; no corrections needed.

## 1. [ ] Only 3 of the 20 are pure text: humanizer, napkin, andrej-karpathy-skills.

- https://github.com/blader/humanizer/tree/225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8
- https://github.com/blader/napkin/tree/27fa60a895de4383b26a539136bc983155cb979c
- https://github.com/forrestchang/andrej-karpathy-skills/tree/2c606141936f1eeef17fa3043a72095b4765b9c2

Checked: humanizer: only `scripts/validate-package.py`, a package validator. napkin: only LICENSE, README.md, SKILL.md. andrej-karpathy-skills: text and manifests only.

## 2. [ ] Eight register hooks on their main install path; seven at session start, two on every prompt, three after file edits.

- https://github.com/dietrichgebert/ponytail/blob/b088b2df6e08d4306c6a3c3d575fe38c2d2d2989/hooks/claude-codex-hooks.json
- https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/hooks/hooks.json
- https://github.com/pbakaus/impeccable/blob/778c8a7b71ccd5bfe3ca6ac68c15d9d872d0f87d/plugin/hooks/hooks.json
- https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/hooks/hooks.json
- https://github.com/egonex-ai/Understand-Anything/blob/790b157028637b626c8666fa7fa28248944b900c/understand-anything-plugin/hooks/hooks.json
- https://github.com/AgriciDaniel/claude-obsidian/blob/32ac5a02c4e082e4a5628ca810776375e134708e/hooks/hooks.json
- https://github.com/openai/codex-plugin-cc/blob/db52e28f4d9ded852ab3942cea316258ae4ef346/plugins/codex/hooks/hooks.json
- https://github.com/JuliusBrussee/caveman/blob/2e08b9177c07bb7249a8a2d1a6758e5db281d002/packages/cli/src/index.ts#L6903-L6918

Checked: Each file opened: ponytail, claude-seo, impeccable, superpowers, Understand-Anything, claude-obsidian, codex-plugin-cc (hooks.json) and caveman (`index.ts:6912`). SessionStart in 7, UserPromptSubmit in 2, after file edits in 3.

## 3. [ ] Caveman, on its main path, runs before and after every tool call and can rewrite shell commands to compress their output.

- https://github.com/JuliusBrussee/caveman/blob/2e08b9177c07bb7249a8a2d1a6758e5db281d002/packages/cli/src/index.ts#L6903-L6945

Checked: `index.ts:6912`: PreToolUse and PostToolUse with no matcher. Lines 6926-6941: the `shrink-hook` on PreToolUse, which rewrites commands.

## 4. [ ] Graphify adds hooks only through an optional second command, on Bash, Grep, Read and Glob.

- https://github.com/Graphify-Labs/graphify/blob/6478eb71237c86ee5fb6a35c702835e987ca445d/README.md#L186-L190
- https://github.com/Graphify-Labs/graphify/blob/6478eb71237c86ee5fb6a35c702835e987ca445d/README.md#L297-L297
- https://github.com/Graphify-Labs/graphify/blob/6478eb71237c86ee5fb6a35c702835e987ca445d/graphify/install.py#L444-L479

Checked: README lines 186-190 (main install ends with "That's it"), README line 297 (`graphify claude install` is a separate step), `install.py` lines 444-479 (matchers `Bash|Grep` and `Read|Glob`).

## 5. [ ] Understand-Anything: when auto-update is on, the hook tells the model "Do not ask the user for confirmation"; the switch is a project config file the README suggests committing.

- https://github.com/egonex-ai/Understand-Anything/blob/790b157028637b626c8666fa7fa28248944b900c/understand-anything-plugin/hooks/post-tool-use-auto-update.mjs#L9-L45
- https://github.com/egonex-ai/Understand-Anything/blob/790b157028637b626c8666fa7fa28248944b900c/README.md#L283-L283

Checked: `post-tool-use-auto-update.mjs` lines 9-45 (`autoUpdate` read from the project config; text "Do not ask the user for confirmation"); README line 283 ("What to commit: everything in .ua/").

## 6. [ ] Impeccable: binary downloaded on first run, checked against a fingerprint from the same release.

- https://github.com/pbakaus/impeccable/blob/778c8a7b71ccd5bfe3ca6ac68c15d9d872d0f87d/plugin/skills/impeccable/scripts/impeccable#L118-L160

Checked: Line 122 (download from GitHub Releases), 125 (`engine-v$version` URL), 149-153 (fail closed on the `.sha256` check); line 156 fetches the fingerprint from `"$url.sha256"`, the same release.

## 7. [ ] Impeccable live mode: with no agent session listening, Apply on text edits goes to the logged-in Codex or Claude CLI with approvals and sandbox off; documented only in a developer contract file.

- https://github.com/pbakaus/impeccable/blob/778c8a7b71ccd5bfe3ca6ac68c15d9d872d0f87d/crates/live/src/copy_edit_agent.rs#L1269-L1320
- https://github.com/pbakaus/impeccable/blob/778c8a7b71ccd5bfe3ca6ac68c15d9d872d0f87d/crates/live/src/copy_edit_agent.rs#L1504-L1550
- https://github.com/pbakaus/impeccable/blob/778c8a7b71ccd5bfe3ca6ac68c15d9d872d0f87d/docs/CLI-CONTRACT.md#L1789-L1789

Checked: `copy_edit_agent.rs` 1269-1320 (`auto`: Codex first, then Claude), 1520 (`--dangerously-bypass-approvals-and-sandbox`), 1548 (`bypassPermissions`); `CLI-CONTRACT.md` line 1789.

## 8. [ ] Codex plugin: a subagent Claude can use on its own initiative; Codex then runs without asking for approval.

- https://github.com/openai/codex-plugin-cc/blob/db52e28f4d9ded852ab3942cea316258ae4ef346/plugins/codex/agents/codex-rescue.md#L1-L6
- https://github.com/openai/codex-plugin-cc/blob/db52e28f4d9ded852ab3942cea316258ae4ef346/plugins/codex/scripts/lib/codex.mjs#L60-L82

Checked: `codex-rescue.md` line 3 ("Proactively use when Claude Code is stuck"); `codex.mjs` lines 67 and 80 (`approvalPolicy ... "never"`).

## 9. [ ] Graphify skill: with a Gemini key set, sends documents, PDFs and images to Gemini without asking; code is parsed locally; the README says the skill uses the IDE session's model.

- https://github.com/Graphify-Labs/graphify/blob/6478eb71237c86ee5fb6a35c702835e987ca445d/graphify/skill.md#L163-L170
- https://github.com/Graphify-Labs/graphify/blob/6478eb71237c86ee5fb6a35c702835e987ca445d/README.md#L612-L612

Checked: `skill.md` lines 163-170 (Gemini only when a key is set, no question to the user, code parsed locally, optional `graphifyy[gemini]` extra); README line 612 ("whatever model your IDE session runs").

## 10. [ ] claude-seo: since 4 October (2.4.2) an optional second plugin is a mod that intercepts shell, WebFetch/MCP calls and prompts, and holds or asks rather than approving.

- https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/plugins/seo-cockpit/hooks/hooks.json
- https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/plugins/seo-cockpit/hooks/register.ts#L754-L800
- https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/plugins/seo-cockpit/README.md#L7-L20
- https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/CHANGELOG.md#L10-L10

Checked: `hooks.json` with only `"modules"`; `register.ts` lines 754 (`tool.call`) and 771 (`prompt.submit`); plugin README lines 7-20; CHANGELOG 2.4.2 dated 2026-10-04. Also checked in an earlier session.

## 11. [ ] Caveman's main install writes Claude Code's global settings: proxy via ANTHROPIC_BASE_URL, about ten hooks, an MCP server; telemetry on by default, stored with IP, opt-out; reversible.

- https://github.com/JuliusBrussee/caveman/blob/2e08b9177c07bb7249a8a2d1a6758e5db281d002/packages/cli/src/index.ts#L7500-L7530
- https://github.com/JuliusBrussee/caveman/blob/2e08b9177c07bb7249a8a2d1a6758e5db281d002/INSTALL.md#L430-L440
- https://github.com/JuliusBrussee/caveman/blob/2e08b9177c07bb7249a8a2d1a6758e5db281d002/SECURITY.md#L45-L45

Checked: `index.ts` 7500-7530 (`settings.env`, hooks, `mcpServers`); `INSTALL.md` 432-438 (`ANTHROPIC_BASE_URL` in `~/.claude/settings.json`, `caveman disable`); `SECURITY.md` line 45 (telemetry on by default, stored with IP, opt-out).

## 12. [ ] Two tools can read browser cookies, both behind an opt-in: Agent-Reach for one explicitly chosen platform, last30days after consent.

- https://github.com/Panniantong/Agent-Reach/blob/94f06c1969dfc1834001269d79d3ad0972d9dee6/agent_reach/cookie_extract.py#L1-L10
- https://github.com/mvanhorn/last30days-skill/blob/b96afd53998458e6ef068633719e84f6659014e8/skills/last30days/scripts/lib/setup_wizard.py#L70-L115

Checked: Agent-Reach `cookie_extract.py` lines 3-8 (one explicitly chosen platform); last30days `setup_wizard.py` line 113 (`BROWSER_CONSENT` recorded only with consent).

## 13. [ ] One project asks to be installed by telling your agent to read an instructions file from its repository.

- https://github.com/Panniantong/Agent-Reach/blob/94f06c1969dfc1834001269d79d3ad0972d9dee6/README.md#L79-L79

Checked: Agent-Reach README line 79 (a sentence to give one's agent, linking to `docs/install.md` on the main branch).

## 14. [ ] On alternative paths, four projects suggest piping their installer into a shell.

- https://github.com/egonex-ai/Understand-Anything/blob/790b157028637b626c8666fa7fa28248944b900c/README.md#L200-L200
- https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/docs/INSTALLATION.md#L135-L135
- https://github.com/nicobailon/visual-explainer/blob/0cc6f15452c455a05fb7fceb036d0da31387c69c/README.md#L89-L89
- https://github.com/JuliusBrussee/caveman/blob/2e08b9177c07bb7249a8a2d1a6758e5db281d002/README.md#L197-L197

Checked: Understand-Anything README 200, claude-seo `docs/INSTALLATION.md` 135, visual-explainer README 89 (installer for Pi), caveman README 197 (pinned to tag v3.2.0).

## 15. [ ] Only Anthropic's official marketplace pins a commit (superpowers, mattpocock/skills); 11 of 20 repositories had new commits two days later, 9 in code, scripts or manifests.

- https://github.com/origoventures/agent-skills-audit-2026-10/blob/main/official-marketplace-pins.csv
- https://github.com/origoventures/agent-skills-audit-2026-10/blob/main/recheck-2026-10-10.csv

Checked: `official-marketplace-pins.csv` (superpowers and mattpocock-skills, pins of 18 September); `recheck-2026-10-10.csv` (11 rows with `changed = yes`, 9 of them code, scripts or manifests; Understand-Anything docs only, brag metadata only).

## 16. [ ] Liu et al.: 88.5% of 31,132 skills instruction-only, odds ratio 2.12. Snyk: 13.4% of 3,984 skills with a critical issue, 76 malicious payloads.

- https://arxiv.org/html/2601.10338
- https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub

Checked: Liu et al. (abstract: 31,132 skills, odds ratio 2.12; Table 6: 88.5% instruction-only) and Snyk ToxicSkills (3,984 skills, 13.4%, 76 malicious payloads, 5 February 2026).
