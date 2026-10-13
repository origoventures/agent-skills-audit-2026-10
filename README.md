# Agent skills audit (October 2026)

This is a static analysis of 20 agent skills and Claude Code plugins recommended on Medium: an automated scan of the shipped files, followed by a review of the manifests, hooks, installers and scripts they reference. It was made for the article "Skills Are Dependencies Now. Who Approved Yours?" [link to the article].

The audit measures **capabilities, not intent**. Nothing in the parts reviewed suggested malicious behaviour. Nothing from the audited repositories was executed.

## Admin checklist

The article's six screening questions, with the commands and settings that help answer them. Commands refer to Claude Code v2.1.287 or later. Read everything in a cloned copy, in a session with no credentials; text inside a plugin is data, not instructions.

1. **Text or software?** Look for scripts, `hooks/hooks.json`, `.mcp.json`, a `bin/` folder and skill headers (`allowed-tools`, `hooks`). `claude --plugin-dir <plugin folder> plugin details <name>` lists skills, agents, hooks and MCP servers before you install, and `claude plugin details <name>` after. It does not show mods, `bin/` or skill headers.
2. **What runs without being called?** Read every hook command and the event it is attached to. A mod is a `hooks.json` with a `modules` key: `claude plugin validate <plugin folder>` lists the events it handles (`hooks:`) and the APIs it calls (`calls:`) without running it. The `calls:` line bounds the APIs used, not the behaviour.
3. **What did the installer write?** After any command-line installer, check `~/.claude/settings.json`, `.claude/settings.json`, `.claude/settings.local.json`, `~/.claude.json`, `.mcp.json`, `~/.claude/CLAUDE.md` and `~/.claude/skills/`. `allowManagedHooksOnly` and `strictPluginOnlyCustomization` can block hooks and MCP servers written there, but no plugin control covers the `env` block (for example `ANTHROPIC_BASE_URL`) or instruction files.
4. **What leaves the machine, and to whom?** List network endpoints, model providers chosen from environment keys, subagents or subprocesses that call other vendors, and telemetry defaults.
5. **Which credentials can it see?** Environment variables, keychains, browser cookies, settings files.
6. **Which version, and who decides when it changes?** Pin a tag when you add a marketplace (`/plugin marketplace add owner/repo#<tag>`); `#ref` accepts a branch or tag, not a commit. To pin a commit, host your own marketplace whose entries set `sha`. Pin npm and PyPI installs to an exact version. Decide auto-update per marketplace (`autoUpdate` in managed settings, or `DISABLE_AUTOUPDATER` for the whole fleet), including the official marketplace, where it is on by default. Give updates an owner.

### Managed settings for teams

- `strictKnownMarketplaces`: allowlist of marketplace sources. An entry for a pinned marketplace must carry the same `ref`.
- `blockedMarketplaces`: blocklist, checked first.
- `disableSideloadFlags`: without it, anyone can load plugins and mods from a folder with `--plugin-dir`, even with the allowlist on.
- `syncClaudeAiPlugins`: plugins synced from members' claude.ai accounts do not come from a marketplace, so the allowlist does not cover them; set this to `false` to stop them loading in Claude Code.
- `disableCommandPluginSources`: blocks plugins whose directory is produced by running a command.
- `allowManagedHooksOnly`: limit hooks to managed ones where that is realistic.
- `strictPluginOnlyCustomization`: block skills, agents, hooks and MCP servers added outside plugins. Without it, a plain `SKILL.md` copied into a skills folder keeps loading under a marketplace allowlist.
- Mods: `allowManagedModsOnly` is not a top-level key. It is an option of the built-in guard, under `pluginConfigs` → `cc-plugin-sec-default@builtin` → `options`. It stops user-installed mods from loading; see [Manage mods for your organization](https://code.claude.com/docs/en/plugins/mods/admin) for which mods count as the organisation's.

Sources: Claude Code documentation, [plugin security](https://code.claude.com/docs/en/plugins/security), [install and manage plugins](https://code.claude.com/docs/en/discover-plugins), [plugins for your organization](https://code.claude.com/docs/en/plugins/org), [mods overview](https://code.claude.com/docs/en/plugins/mods/overview).

## Sample

The sample is 19 third-party skills and plugins plus `anthropics/skills` as a baseline. The third-party projects are those named in my reviews of three Medium articles published between 16 and 25 September 2026.

It is a convenience sample: half of the third-party projects come from one article. `SAMPLE.md` gives the inclusion rule, the sources with their dates, the full commit SHAs and star counts.

Each repository was cloned on **8 October 2026** and read at the commit listed in `SAMPLE.md`.

## Files

| File | What it is |
|---|---|
| `SAMPLE.md` | The 20 repositories: inclusion rule, Medium sources, full commit SHAs, stars |
| `classification.csv` | The classification used in the article (one row per repository) |
| `audit.py` | Signal counter used for the first pass (Python 3, standard library only) |
| `audit.csv`, `evidence.json` | Raw output of `audit.py` on 8 October |
| `recheck-2026-10-10.csv` | Commit comparison two days later, with full SHAs and UTC dates |
| `official-marketplace-pins.csv` | Commits pinned by Anthropic's official marketplace for the two projects installed from it |
| `reverification-2026-10-10.md` | Blind re-classification and fact check |
| `review-2026-10-11.md` | Adversarial review of 11 October |
| `review-2026-10-13.md` | Second adversarial review, on the shortened article (13 October) |
| `human-check-2026-10-13.md` | The author's line-by-line check of every claim the article makes about a named project (13 October) |
| `cross-model/` | Blind re-classification by OpenAI's Codex, agreement and resolution of every disagreement (13 October) |
| `repos.txt` | Repository list |

## Method

1. **Automated pass.** `audit.py` counts signals in the shipped files: shell execution, network calls, secret-looking environment variables, references to sensitive paths, install commands, hook configurations and git tags. It skips tests, examples, `dist`, `build`, `vendor` and files over 2 MB. Regex counts are noisy (a comment that mentions `~/.ssh` is not code that reads it), so they were used only to find what to read.
2. **Classification.** AI agents checked each repository against its source:
   - plugin and marketplace manifests;
   - `hooks.json` files, including those of every plugin in multi-plugin repositories;
   - installers and the settings files they write;
   - READMEs and the scripts they reference.
3. **Recheck (10 October).** The 20 repositories were cloned again and each pair of commits was diffed (`recheck-2026-10-10.csv`). 11 of 20 had new commits: 9 touched code, scripts or manifests, and 2 touched docs or metadata only. The mod shipped in `AgriciDaniel/claude-seo` (`plugins/seo-cockpit`) was already present at the audited commit.
4. **Re-verification (10 October).** `audit.py` was re-run on the same commits and reproduced `audit.csv` and `evidence.json`; only the live git-tag counts differed. Four separate agent runs then re-classified the 20 repositories blind, without seeing the table, and the differences were resolved against the source. (`reverification-2026-10-10.md`).
5. **Adversarial review (11 October).** Six independent reviewers attacked the repository and the article, each from a different angle:
   - reproducibility;
   - security;
   - methodology;
   - Claude Code platform;
   - editorial;
   - maintainers of the named projects.

   Each cloned everything fresh. What they checked and the outcome are in `review-2026-10-11.md`.
6. **Second adversarial review (13 October).** Six new reviewers attacked the shortened article and this repository; corrections are in `review-2026-10-13.md`.
7. **Cross-model check (13 October).** OpenAI's Codex (`gpt-6-astra`) classified the 20 repositories blind from the column rules alone. It agreed on 231 of 240 categorical cells; every disagreement was re-read against the source and four cells were corrected (`cross-model/`).

## Classification rules

Each column of `classification.csv`:

- **type**: one of three categories.
  - `text-only`: instructions only; at most a packaging validator.
  - `text+scripts`: instructions plus helper scripts, templates or a small CLI.
  - `software`: a real software product the skill depends on (a package, a compiled binary or a substantial application).
- **hooks**: hook events registered automatically, either by a plugin manifest or by the documented main install path when that path writes them into a settings file. The flag columns break this down:
  - `session_start`: runs when a session starts;
  - `user_prompt_submit`: runs on every prompt;
  - `after_file_edit`: runs after file edits;
  - `every_tool_call`: runs before and after every tool call.
- **mod**: a `hooks.json` with a `modules` key (Claude Code mods, v2.1.287 and later).
- **network_core / credentials_core**: `yes` only when the capability is part of the core function, not optional extras.
- **reads_browser_cookies**: reads cookies from the user's browser, whether opt-in or not. Session cookies the user supplies by hand are noted, not counted (clarified on 13 October after the cross-model check).
- **downloads_code**: the main install path, or the core function on first use, fetches packages, CLIs or binaries. Optional extras that one sub-skill or the user installs by hand do not count. Borderline cases are explained in the notes.
- **main_install**: the path the project's README explicitly recommends; if none is marked as recommended, the path it presents first.
- **pinned_main_path**: whether the main path fixes a release, tag or commit. For the two projects whose main path is Anthropic's official marketplace, the pin set there counts. That marketplace updates its pins itself and has auto-update on by default, so a pin decides who moves the version, not whether it moves.
- **pipes_own_installer_to_shell**: the project's own docs tell users to pipe its installer into a shell. Third-party installers (for example uv) do not count.

## How the article's numbers are derived

All counts come from `classification.csv`; `n = 20` includes the baseline. A cell counts as `yes` or `none` when it starts with that word; the rest of the cell is a note.

| Article claim | Rule | Count |
|---|---|---|
| text-only / text+scripts / software | `type` | 3 / 8 / 9 |
| register hooks on the main install path | `hooks` not `none` | 8 (graphify adds hooks only through an optional second command; see its notes) |
| at session start | `session_start = yes` | 7 |
| on every prompt | `user_prompt_submit = yes` | 2 |
| after file edits | `after_file_edit = yes` | 3 |
| on every tool call | `every_tool_call = yes` | 1 |
| download more code | `downloads_code = yes` | 11 |
| network as core function | `network_core = yes` | 5 |
| credentials as core function | `credentials_core = yes` | 3 |
| read browser cookies | `reads_browser_cookies = yes` | 2 |
| pinned main install path | `pinned_main_path = yes` | 2 |
| pipe their own installer to a shell | `pipes_own_installer_to_shell = yes` | 4 |
| had new commits two days later / touching code | `recheck-2026-10-10.csv` | 11 / 9 |

## Reproduce

**Requirements:**

- git and Python 3.7 or later (tested on 3.13);
- network access, because `git_tags` is read live with `git ls-remote` and will differ from the 8 October values.

`audit.py` does not check that call. Offline it silently writes 0 for every tag count.

```bash
mkdir repos
while read sha repo; do
  d="repos/${repo/\//__}"
  git clone -q --filter=blob:none "https://github.com/$repo" "$d"
  git -C "$d" checkout -q "$sha"
done < <(python3 -c "import csv;[print(r['commit'],r['repo']) for r in csv.DictReader(open('classification.csv'))]")
python3 -I audit.py repos out
```

**What should match.** The counts in `out/audit.csv` should match `audit.csv` except `git_tags`. `audit.py` walks directories in filesystem order and keeps at most 12 evidence lines per signal, so `out/evidence.json` can list different sample lines on another filesystem; the counts do not depend on order. On Linux ext4 it reproduced byte for byte.

**`repos/` contents.** `repos/` must contain only these 20 directories.

**Recheck.** To reproduce `recheck-2026-10-10.csv`, run `git diff --name-only <commit_2026-10-08> <commit_2026-10-10>` in each repository.

## Authorship and supervision

The audit was run by AI agents (Claude) in disposable cloud sandboxes with no credentials, as part of the article's own point. Fulvio Vanacore defined the questions and the classification criteria, discussed the findings with the agents and decided what to publish.

For verification, the work was redone from scratch. On 10 October, separate agent runs re-classified the 20 repositories blind, and the differences were resolved against the source code. On 11 October, six independent agent reviewers attacked the result. On 13 October, because all of these agents were Claude models, a model from another vendor (OpenAI's Codex, `gpt-6-astra`) classified the 20 repositories blind as a cross-check (`cross-model/`).

On 13 October, Fulvio personally checked every claim the article makes about a named project, plus the main counts and the two cited studies, against the linked source lines (`human-check-2026-10-13.md`: 16 of 16 confirmed). The classification cells not cited in the article were verified by agents and by the cross-model check, not by him line by line.

## Limits

- **Time.** One commit per repository on one day.
- **Sample.** A convenience sample of popular projects, half from one article.
- **Classification.** Judgement calls are documented in the notes column.
- **Method.** Static reading only: the audit says what the code can do, not what it did on a real machine.
- **Official marketplace.** For the two projects installed from Anthropic's official marketplace, the commit installed on 8 October was older than the one audited (see `official-marketplace-pins.csv`).

## License

Code (`audit.py`): MIT, see `LICENSE`. Data and documents (CSV, JSON, Markdown): CC BY 4.0.
