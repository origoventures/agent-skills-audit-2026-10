#!/usr/bin/env python3
"""Compare a blind classification with the published one.
Usage: python3 compare.py published.csv blind.csv [more_blind.csv ...]
Compares the leading category word of each categorical cell (yes/no columns binarised); prints per-column agreement and Cohen's kappa, and lists disagreements."""
import csv, sys, collections
COLS = ["type","session_start","user_prompt_submit","after_file_edit","every_tool_call","mod",
        "network_core","credentials_core","reads_browser_cookies","downloads_code","pinned_main_path",
        "pipes_own_installer_to_shell"]
def lead(v):
    v = (v or "").strip().lower()
    for w in ("text+scripts","text-only","software","none","yes","no","optional","partial"):
        if v.startswith(w): return w
    return v.split(";")[0].split(" ")[0]
def load(p):
    rows = {r["repo"].lower(): r for r in csv.DictReader(open(p, newline=""))}
    for r in rows.values(): r["hooks_any"] = "no" if lead(r.get("hooks","")) == "none" else "yes"
    return rows
def kappa(a, b):
    n = len(a); po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n / n
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)
pub = load(sys.argv[1])
for path in sys.argv[2:]:
    blind = load(path); print(f"\n== {path}")
    tot = agree = 0
    for c in COLS:
        keys = [k for k in pub if k in blind]
        a = [lead(pub[k][c]) for k in keys]; b = [lead(blind[k][c]) for k in keys]
        if c != "type":  # yes/no columns: anything other than "yes" counts as "no"
            a = ["yes" if x == "yes" else "no" for x in a]; b = ["yes" if x == "yes" else "no" for x in b]
        ag = sum(x == y for x, y in zip(a, b)); tot += len(keys); agree += ag
        print(f"{c:30s} {ag:2d}/{len(keys)}  kappa={kappa(a, b):.2f}")
        for k, x, y in zip(keys, a, b):
            if x != y: print(f"    {k}: published={x} blind={y}")
    print(f"TOTAL {agree}/{tot} cells agree ({agree/tot:.0%})")
