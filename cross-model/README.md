# Cross-model check (13 October 2026)

The published classification was produced and verified by Claude agents. To test it against a model from another vendor, the 20 repositories were classified again, blind, by OpenAI's Codex.

## How it was run

- **Model.** Codex CLI 0.154.0, model `gpt-6-astra`, reasoning effort medium, sandbox `read-only`, run by the author on his own machine.
- **Input.** Only `BRIEF.md`: the column rules from this repository's README and the list of commits. Codex did not see `classification.csv`, the counts or the article.
- **Repositories.** Cloned at the audited commits with `setup.sh`. Nothing from them was executed.
- **Output.** The read-only sandbox prevented Codex from writing the file, so it printed the CSV in its final message (`codex-run-2026-10-13.log`); `classification-blind-codex.csv` is that block, unchanged.
- **Comparison.** `compare.py` compares the leading category word of each cell. For the yes/no columns, anything other than `yes` counts as `no`, because the article counts only `yes`.

## Result

Agreement on the 12 categorical columns: **231 of 240 cells (96%)**. Codex agreed on every hook column, the mod, pinned main paths, piped installers and network as a core function. There were 9 disagreements, each re-read against the source:

| Repository | Column | Published | Codex | Resolution |
|---|---|---|---|---|
| AgriciDaniel/claude-seo | type | software | text+scripts | Published kept: about 28,000 lines of Python outside tests; setup installs dependencies and Chromium. |
| AgriciDaniel/claude-obsidian | type | text+scripts | software | **Corrected to software**: the claude_obsidian package is about 19,500 lines of Python. |
| openai/codex-plugin-cc | type | text+scripts | software | **Corrected to software**: the plugin depends on the Codex CLI, a separate software product installed at setup. |
| latent-spaces/brag | type | text+scripts | software | Published kept, judgement call: classic `/brag` depends on Hyperframes, but the first-presented install is `/brag-slim`, which does not. |
| openai/codex-plugin-cc | credentials_core | no | yes | Published kept, judgement call: the login is held and used by the Codex CLI, not by the plugin. |
| JuliusBrussee/caveman | reads_browser_cookies | no | yes | Published kept, **rule clarified**: caveman does not read the browser; an optional usage import sends a claude.ai session cookie the user supplies (`proxy/internal/store/usage_import.go:124-138`). The rule previously also mentioned session tokens; it now covers reading cookies from the user's browser, and this case is in the notes. |
| pbakaus/impeccable | reads_browser_cookies | no | yes | Published kept: `Storage.getCookies` runs on a fresh temporary browser profile and the response is discarded (`crates/browser/src/cdp.rs:159-160, 263`). |
| nextlevelbuilder/ui-ux-pro-max-skill | downloads_code | no | yes | **Corrected to yes**: the README labels the npm CLI path "Recommended" (README.md:262). The main path is the recommended one, as already applied to impeccable; the rule now says so explicitly. |
| yizhiyanhua-ai/fireworks-tech-graph | downloads_code | no | yes | **Corrected to yes**: the main path `npx -y skills@1.5.17 add ...` fetches the skills CLI package. |

## Effect on the counts

- type: 3 / 10 / 7 became **3 / 8 / 9** (text-only / text+scripts / software).
- downloads_code: 9 became **11**.
- Every other count used in the article is unchanged.
- After the corrections, Codex and the published classification agree on 235 of 240 cells; the remaining 5 are the rows marked "Published kept".

## Limits

One run of one model from one other vendor. Agreement on a cell does not prove the cell is right: both classifiers could share a misreading. The two "judgement call" rows remain debatable and are kept as published, with the reasoning in `classification.csv`.

## Reproduce

```bash
bash setup.sh
codex exec --skip-git-repo-check --sandbox read-only --cd . "$(cat BRIEF.md)" > codex-run.log
# agreement before the corrections (classification as of commit badc399): 231/240
git -C .. show badc399:classification.csv > /tmp/before.csv && python3 compare.py /tmp/before.csv classification-blind-codex.csv
# after: 235/240
python3 compare.py ../classification.csv classification-blind-codex.csv
```
