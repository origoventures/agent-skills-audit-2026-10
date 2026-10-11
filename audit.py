#!/usr/bin/env python3
"""Static capability audit of agent-skill repositories.
Usage: python3 audit.py <repos_dir> <out_dir>
Each subdir of repos_dir is a shallow git clone named owner__repo.
Counts what the shipped files CAN do (capabilities), not whether they are malicious.
"""
import os, re, sys, json, csv, subprocess, collections

CODE_EXT = {'.py','.sh','.bash','.zsh','.js','.mjs','.cjs','.ts','.tsx','.rb','.go','.rs','.ps1','.bat','.cmd','.php','.pl','.lua'}
SKIP_DIRS = {'.git','node_modules','dist','build','vendor','__pycache__','.venv','venv'}
TEST_RE = re.compile(r'(^|/)(tests?|__tests__|spec|e2e|fixtures?|examples?|evals?|benchmarks?)(/|$)|(_test|\.test|\.spec)\.[a-z]+$', re.I)

PAT = {
 'network': re.compile(r"\b(requests\.(get|post|put|delete|Session)|urllib\.request|urlopen\(|http\.client|httpx\.|aiohttp|fetch\(|axios|XMLHttpRequest|WebSocket\(|socket\.socket|curl\s|wget\s|Invoke-WebRequest|net/http|reqwest)", re.I),
 'subprocess': re.compile(r"\b(subprocess\.|os\.system\(|os\.popen\(|child_process|execSync\(|spawnSync\(|spawn\(|exec\(|Popen\(|shell=True|Bun\.spawn|Deno\.Command)"),
 'secrets_env': re.compile(r"(os\.environ|process\.env|getenv\(|\$\{?)[\[\.\(\"' ]*[A-Z0-9_]*(API_KEY|TOKEN|SECRET|PASSWORD|COOKIE|CREDENTIAL|AUTH)[A-Z0-9_]*"),
 'sensitive_paths': re.compile(r"(~|\$HOME|expanduser\(['\"]~|homedir\(\))[/\\\"', ]*\.?(ssh|aws|gnupg|kube|netrc|npmrc|docker/config|config/gh|git-credentials)|Cookies\b|cookies\.sqlite|browser_cookie3|keychain|Login Data|keyring\.get", re.I),
 'home_config_write': re.compile(r"(~|\$HOME|expanduser\(['\"]~|homedir\(\)|Path\.home\(\))[^\n]{0,40}\.(claude|codex|cursor|config|bashrc|zshrc|profile|gemini|agents)\b"),
 'pipe_to_shell': re.compile(r"(curl|wget|irm|iwr)[^\n|]{0,200}\|\s*(sudo\s+)?(ba|z)?sh\b|\|\s*iex\b", re.I),
 'pkg_install': re.compile(r"\b(pip3? install|pipx install|uv tool install|uvx |npm (i|install)\b|npx |pnpm (add|dlx)|bunx |brew install|apt(-get)? install|cargo install|go install)", re.I),
 'git_hooks': re.compile(r"\.git/hooks|core\.hooksPath|post-commit|pre-commit", re.I),
}
SKILL_FILES = re.compile(r'(^|/)(SKILL(_[a-z]+)?\.md|skill(-[a-z]+)?\.md)$')
FRONT_ALLOWED = re.compile(r'^allowed-tools:\s*(.+)$', re.M|re.I)
BASH_BLOCK = re.compile(r'```(bash|sh|shell|zsh|console)\n', re.I)
HOOK_EVENTS = re.compile(r'"(PreToolUse|PostToolUse|UserPromptSubmit|SessionStart|SessionEnd|Stop|SubagentStop|PreCompact|Notification)"')

def walk(root):
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for f in fns:
            p = os.path.join(dp, f)
            yield os.path.relpath(p, root)

def read(p):
    try:
        if os.path.getsize(p) > 2_000_000: return ''
        with open(p, 'r', errors='ignore') as fh: return fh.read()
    except Exception: return ''

def main(repos_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    rows, evidence = [], collections.defaultdict(list)
    for name in sorted(os.listdir(repos_dir)):
        root = os.path.join(repos_dir, name)
        if not os.path.isdir(root): continue
        repo = name.replace('__','/',1)
        r = collections.Counter(); files_hit = collections.defaultdict(set)
        skill_files, allowed, hook_cfg = [], [], []
        for rel in walk(root):
            p = os.path.join(root, rel); ext = os.path.splitext(rel)[1].lower()
            txt = None
            if SKILL_FILES.search(rel):
                skill_files.append(rel); txt = read(p)
                r['skill_bash_blocks'] += len(BASH_BLOCK.findall(txt))
                for m in FRONT_ALLOWED.finditer(txt[:3000]): allowed.append((rel, m.group(1).strip()))
            if rel.endswith('.json') and ('hook' in rel.lower() or rel.endswith('settings.json') or rel.endswith('plugin.json')):
                t = read(p)
                if HOOK_EVENTS.search(t): hook_cfg.append(rel)
            is_code = ext in CODE_EXT or (ext == '' and read(p)[:2] == '#!')
            if is_code and not TEST_RE.search(rel):
                r['code_files'] += 1
                txt = txt if txt is not None else read(p)
                for k, rx in PAT.items():
                    for i, line in enumerate(txt.splitlines(), 1):
                        if rx.search(line):
                            r[k] += 1; files_hit[k].add(rel)
                            if len(evidence[(repo,k)]) < 12: evidence[(repo,k)].append(f"{rel}:{i}: {line.strip()[:200]}")
            elif ext in {'.md','.txt','.toml','.json','.yaml','.yml'}:
                txt = txt if txt is not None else read(p)
                for k in ('pipe_to_shell','pkg_install','home_config_write'):
                    for i, line in enumerate(txt.splitlines(), 1):
                        if PAT[k].search(line):
                            r[k+'_docs'] += 1; files_hit[k+'_docs'].add(rel)
                            if len(evidence[(repo,k+'_docs')]) < 12: evidence[(repo,k+'_docs')].append(f"{rel}:{i}: {line.strip()[:200]}")
        tags = subprocess.run(['git','ls-remote','--tags',f'https://github.com/{repo}'],capture_output=True,text=True,timeout=60).stdout.strip().splitlines()
        head = subprocess.run(['git','-C',root,'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
        row = {'repo':repo,'commit':head[:12],'skill_files':len(skill_files),'code_files':r['code_files'],
               'skill_bash_blocks':r['skill_bash_blocks'],'allowed_tools_decls':len(allowed),
               'allowed_tools_with_bash':sum(1 for _,a in allowed if 'bash' in a.lower()),
               'hook_configs':len(hook_cfg),'git_tags':len([t for t in tags if not t.endswith('^{}')])}
        for k in PAT: row[k+'_files'] = len(files_hit[k])
        for k in ('pipe_to_shell','pkg_install','home_config_write'): row[k+'_docs_files'] = len(files_hit[k+'_docs'])
        rows.append(row)
        for rel in hook_cfg: evidence[(repo,'hook_configs')].append(rel)
        for rel,a in allowed[:12]: evidence[(repo,'allowed_tools')].append(f"{rel}: {a[:200]}")
    with open(os.path.join(out_dir,'audit.csv'),'w',newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    with open(os.path.join(out_dir,'evidence.json'),'w') as fh:
        json.dump({f"{a}|{b}":v for (a,b),v in evidence.items()}, fh, indent=1)
    for row in rows: print(row)

if __name__ == '__main__': main(sys.argv[1], sys.argv[2])
