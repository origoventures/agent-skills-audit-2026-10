# The 20 repositories in the sample

## How the sample was built

This is a convenience sample, not a random or exhaustive one.

- **Source.** Every day I read and review the articles in my Medium Daily Digest. The 19 third-party repositories are the agent skills and Claude Code plugins named in my reviews of three Medium articles. All three were published between 16 and 25 September 2026 (by byline date) and read between 23 September and 5 October.
- **Inclusion.** I took every item that installs into Claude Code as a skill or plugin and that my review of the article named. MCP servers, hosted services and tools that do not exist under the given name were excluded.
- **Partial list.** From the "20 AI Agent Skills" list I took the 11 entries named in my review (graphify among them, also recommended by The Explainer). The other 9 entries of that list were not included.
- **Baseline.** `anthropics/skills`, Anthropic's official skills repository, is added as a baseline. Medium did not recommend it.
- **Concentration.** Half of the third-party sample (10 of 19) comes from one article.

Each repository was cloned on **8 October 2026**, between about 05:40 and 08:45 UTC, and read at the commit below. The full 40-character SHA is given so that a fresh clone can check it out:

```
git clone --filter=blob:none https://github.com/<owner>/<repo> repos/<owner>__<repo>
git -C repos/<owner>__<repo> checkout <sha>
```

A shallow clone cannot reach these commits once the repository has moved on.

Stars were read from the GitHub API on 11 October 2026 at 08:57 UTC.

| # | Repository | Commit read on 8 Oct 2026 | Type | Stars (11 Oct) | Recommended in |
|---|---|---|---|---|---|
| 1 | [anthropics/skills](https://github.com/anthropics/skills) | 683bc88e56f3e09ba94f7055977f3d3aa499f202 | text+scripts | 180,399 | Baseline (also named in C) |
| 2 | [obra/superpowers](https://github.com/obra/superpowers) | 8ca22dba9a94f28898bbce59f2537ff4d87c747d | text+scripts | 297,359 | C |
| 3 | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 6478eb71237c86ee5fb6a35c702835e987ca445d | software | 125,376 | A, B |
| 4 | [dietrichgebert/ponytail](https://github.com/dietrichgebert/ponytail) | b088b2df6e08d4306c6a3c3d575fe38c2d2d2989 | text+scripts | 160,694 | B |
| 5 | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 1a2c459b35f26116fd165b0a0f30597f252749ff | text+scripts | 134,632 | B, C |
| 6 | [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) | 94f06c1969dfc1834001269d79d3ad0972d9dee6 | software | 95,605 | B |
| 7 | [egonex-ai/Understand-Anything](https://github.com/egonex-ai/Understand-Anything) | 790b157028637b626c8666fa7fa28248944b900c | software | 85,877 | B |
| 8 | [blader/humanizer](https://github.com/blader/humanizer) | 225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8 | text-only | 55,526 | B |
| 9 | [blader/napkin](https://github.com/blader/napkin) | 27fa60a895de4383b26a539136bc983155cb979c | text-only | 631 | B |
| 10 | [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | 4b99de2f7de7e7d5247042e5fb5b4ea9368ef734 | software | 18,677 | B |
| 11 | [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | b96afd53998458e6ef068633719e84f6659014e8 | software | 63,934 | B |
| 12 | [nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer) | 0cc6f15452c455a05fb7fceb036d0da31387c69c | text+scripts | 10,344 | B |
| 13 | [yizhiyanhua-ai/fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph) | 31fea364eda5f1852b1175f3d9e29ea31d22dcb4 | text+scripts | 11,656 | B |
| 14 | [mattpocock/skills](https://github.com/mattpocock/skills) | f3fc5632f401156837ee3872f14fe33ccf1024ea | text+scripts | 285,069 | A |
| 15 | [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) (now multica-ai/andrej-karpathy-skills) | 2c606141936f1eeef17fa3043a72095b4765b9c2 | text-only | 218,540 | A |
| 16 | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | 2e08b9177c07bb7249a8a2d1a6758e5db281d002 | software | 110,964 | C |
| 17 | [latent-spaces/brag](https://github.com/latent-spaces/brag) | 7079945d391573edebe48fdc0a23b39c4b4e8726 | text+scripts | 15,044 | C |
| 18 | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | 778c8a7b71ccd5bfe3ca6ac68c15d9d872d0f87d | software | 79,575 | A |
| 19 | [AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) | 32ac5a02c4e082e4a5628ca810776375e134708e | text+scripts | 15,454 | A |
| 20 | [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) | db52e28f4d9ded852ab3942cea316258ae4ef346 | text+scripts | 34,072 | A |

## Sources

Dates are the byline dates shown on Medium. Medium's `article:published_time` metadata can be later.

- **A.** The Explainer, [10 Claude Code Plugins That Deserve More Attention](https://medium.com/@theexplainer/10-claude-code-plugins-that-deserve-more-attention-3ef2bb050dae), 16 Sep 2026.
- **B.** Agent Native, [20 AI Agent Skills With ~800K GitHub Stars That Form a Real Agent Stack](https://medium.com/@agentnativedev/20-ai-agent-skills-with-800k-github-stars-that-form-a-real-agent-stack-e0988bbaa365), 25 Sep 2026.
- **C.** Divy Yadav, [I Tested 100+ Claude Skills. Only 7 Survived.](https://medium.com/@yadavdivy296/i-tested-100-claude-skills-only-7-survived-304012a2cb2d), 24 Sep 2026.

Totals: 3 text-only, 10 text+scripts, 7 software. The full classification is in `classification.csv`.
