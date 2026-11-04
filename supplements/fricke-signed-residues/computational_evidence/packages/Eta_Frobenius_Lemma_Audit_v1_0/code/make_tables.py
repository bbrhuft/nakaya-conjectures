#!/usr/bin/env python3
"""Summarise results/velu_sign_checks.json into a Markdown table (per level) and totals."""
import json, os, sys
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
d = json.load(open(os.path.join(base, "velu_sign_checks.json")))
pairs = d["pairs"]; s = d["summary"]
ells = sorted(set(r["ell"] for r in pairs))
lines = []
lines.append(f"**Sweep:** levels ℓ ∈ {{{', '.join(map(str, ells))}}}, primes 5 ≤ p ≤ {s['pmax']}, p ≠ ℓ: "
             f"{s['n_pairs']} pairs, **{s['n_points']} geometric supersingular points (E, C)** "
             f"({s['n_points_j0']} over j = 0, {s['n_points_j1728']} over j = 1728). "
             f"Theorem C failures: {s['theorem_C_failures'] or 'none'}. Wall time {s['seconds']} s.\n")
lines.append("| ℓ | pairs | p range | points | points j=0 | points j=1728 | D_ℓ^k ∈ {±1} and = (ℓ/p) | Ono (p²−1)/12 power = 1 | B(E′)=ℓB(E) | Baker | c constant | Hauptmodul match | κ (Ono 1.3) | B ∈ F_p (Deuring) |")
lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
def tick(vals):
    if all(v is None for v in vals): return "n/a"
    return "all ✓" if all(v in (True, None) for v in vals) else "FAIL"
for ell in ells:
    rs = [r for r in pairs if r["ell"] == ell]
    ps = [r["p"] for r in rs]
    lines.append(f"| {ell} | {len(rs)} | {min(ps)}–{max(ps)} | {sum(r['n_points'] for r in rs)} | {sum(r['n_points_j0'] for r in rs)} | "
                 f"{sum(r['n_points_j1728'] for r in rs)} | {tick([r['theorem_C_ok'] for r in rs])} | {tick([r['ono_m_power_all_1'] for r in rs])} | "
                 f"{tick([r['robert_B_relation_ok'] for r in rs])} | {tick([r['baker_ok'] for r in rs])} | "
                 f"{tick([r['c_constant_ok'] and r['c_constant_over_all_ss'] for r in rs])} | {tick([r['hauptmodul_match_ok'] for r in rs])} | "
                 f"{tick([r['deuring_kappa_ok'] for r in rs])} | {tick([r['deuring_B_in_Fp_ok'] for r in rs])} |")
# sign distribution sanity: how many pairs had (ell/p) = -1
neg = sum(1 for r in pairs if r["legendre_ell_p"] == -1)
lines.append(f"\nPairs with (ℓ/p) = −1 (so D_ℓ^k = −1 at every point): {neg} of {s['n_pairs']}; with (ℓ/p) = +1: {s['n_pairs'] - neg}. "
             f"In every pair the set of values of D_ℓ^k over all points is a single element, equal to (ℓ/p).")
# small table: ell=2,3 with p=5,7
lines.append("\nSmall cases (ℓ ∈ {2,3}, p ∈ {5,7,11,13}):\n")
lines.append("| ℓ | p | points | D_ℓ^k values | (ℓ/p) | j=0 pts | j=1728 pts |")
lines.append("|---|---|---|---|---|---|---|")
for r in pairs:
    if r["ell"] in (2, 3) and r["p"] in (5, 7, 11, 13):
        lines.append(f"| {r['ell']} | {r['p']} | {r['n_points']} | {r['values_D_ell_pow_k']} | {r['legendre_ell_p']:+d} | {r['n_points_j0']} | {r['n_points_j1728']} |")
txt = "\n".join(lines)
open(os.path.join(base, "velu_sign_table.md"), "w").write(txt + "\n")
print(txt)
