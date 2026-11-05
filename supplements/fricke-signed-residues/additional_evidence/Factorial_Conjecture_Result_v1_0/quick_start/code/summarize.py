"""
Aggregate per-pair JSON into results/summary.json, results/pairs.csv and LaTeX tables
(results/table_p_le_29.tex, results/table_levels.tex, results/table_nonthin_small.tex).
"""
import csv, glob, json, os
from collections import defaultdict

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
rows = []
for mode in ("certified", "kz"):
    for fn in sorted(glob.glob(os.path.join(base, mode, "N*_p*.json"))):
        r = json.load(open(fn))
        rows.append(r)
rows.sort(key=lambda r: (r["p"], r["N"]))

BOOL_KEYS = ["ss_j_sources_agree", "mass_ok", "exponents_integral", "certificate_ok", "gcd_P_D_is_1",
             "deg_P_lt_deg_D", "pade_den_equals_D_thin", "all_r_in_Fp", "all_W_in_Fp", "ratio_constant",
             "matches_conjecture", "frobenius_conjugation_ok", "hasse_power_identity_ok",
             "kz_polynomial_identity_ok_to_extra_200_terms", "kz_polynomial_identity_ok_to_extra_100_terms",
             "kz_double_pole_equals_residue", "kz_orders_at_nonthin_ok", "level1_basis_ok",
             "eta_frobenius_U_ok_all_ss", "E_{p-1}_vanishes_at_ss", "baker_beta_ok",
             "c_constant_on_ss_locus", "rW_equals_legN_c_c", "all_r_nonzero"]

failures = []
for r in rows:
    for k in BOOL_KEYS:
        if k in r and r[k] is False:
            failures.append({"N": r["N"], "p": r["p"], "mode": r["mode"], "check": k})


def agg(sel):
    d = {"pairs": len(sel), "thin_points": sum(r["n_thin"] for r in sel),
         "nonrational_thin_points": sum(r["n_thin_nonrational"] for r in sel),
         "pairs_with_ge2_thin": sum(1 for r in sel if r["n_thin"] >= 2),
         "pairs_with_1_thin": sum(1 for r in sel if r["n_thin"] == 1),
         "pairs_with_0_thin": sum(1 for r in sel if r["n_thin"] == 0),
         "all_match_conjecture": all(r["matches_conjecture"] for r in sel),
         "pmin": min(r["p"] for r in sel) if sel else None, "pmax": max(r["p"] for r in sel) if sel else None}
    return d

summary = {
    "reproduction_p_le_29": agg([r for r in rows if r["p"] <= 29 and r["mode"] == "certified"]),
    "certified_all": agg([r for r in rows if r["mode"] == "certified"]),
    "kz_all": agg([r for r in rows if r["mode"] == "kz"]),
    "by_level_certified": {N: agg([r for r in rows if r["mode"] == "certified" and r["N"] == N]) for N in (2, 3, 5, 7, 13)},
    "by_level_kz": {N: agg([r for r in rows if r["mode"] == "kz" and r["N"] == N]) for N in (2, 3, 5, 7, 13)},
    "diagnostic_p29": {r["N"]: r["ratio_set_signed"] for r in rows if r["p"] == 29 and r["mode"] == "certified"},
    "failed_checks": failures,
    "ratio_sets_seen": sorted(set(tuple(r["ratio_set_signed"]) for r in rows)),
    "counterexamples": [{"N": r["N"], "p": r["p"]} for r in rows if not r["matches_conjecture"]],
}
with open(os.path.join(base, "summary.json"), "w") as f:
    json.dump(summary, f, indent=1)

with open(os.path.join(base, "pairs.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["N", "p", "mode", "n_ss_j", "n_ss_points_X0N", "n_ss_T_values", "weight_counts", "mass",
                "n_thin", "n_thin_nonrational", "ratio_set", "expected", "matches", "certificate_ok",
                "pade_den_equals_D_thin", "hasse_power_identity_ok", "kz_double_pole_equals_residue",
                "eta_frobenius_U_ok_all_ss", "baker_beta_ok", "c_constant_on_ss_locus"])
    for r in rows:
        w.writerow([r["N"], r["p"], r["mode"], r["n_ss_j"], r["n_ss_points_X0N"], r["n_ss_T_values"],
                    ";".join(f"e{k}:{v}" for k, v in r["weight_counts"].items()), r["mass"], r["n_thin"],
                    r["n_thin_nonrational"], " ".join(str(x) for x in r["ratio_set_signed"]),
                    r["expected_constant"], r["matches_conjecture"], r.get("certificate_ok", ""),
                    r.get("pade_den_equals_D_thin", ""), r.get("hasse_power_identity_ok", ""),
                    r.get("kz_double_pole_equals_residue", ""), r["eta_frobenius_U_ok_all_ss"],
                    r["baker_beta_ok"], r["c_constant_on_ss_locus"]])


def sgn(x):
    return "+1" if x == 1 else ("-1" if x == -1 else str(x))


def wc(r):
    return ", ".join(f"{v}\\times{k}" if v > 1 else f"{k}" for k, v in sorted(r["weight_counts"].items(), key=lambda kv: int(kv[0])))

# Table 1: reproduction range p <= 29
lines = [r"\begin{longtable}{rrrrrlrrcc}", r"\toprule",
         r"$N$ & $p$ & $\#j_{ss}$ & $\#x$ & $s$ & weights $e$ & thin & non-rat. & $\{r_iW_i\}$ & $-\left(\frac{-N}{p}\right)$\\",
         r"\midrule", r"\endhead"]
for r in rows:
    if r["mode"] != "certified" or r["p"] > 29:
        continue
    rs = "\\{" + ",".join(sgn(x) for x in r["ratio_set_signed"]) + "\\}" if r["ratio_set_signed"] else "--"
    weights = ", ".join(f"{k}^{{{v}}}" for k, v in sorted(r["weight_counts"].items(), key=lambda kv: int(kv[0])))
    lines.append(f"{r['N']} & {r['p']} & {r['n_ss_j']} & {r['n_ss_points_X0N']} & {r['n_ss_T_values']} & ${weights}$ & "
                 f"{r['n_thin']} & {r['n_thin_nonrational']} & ${rs}$ & ${sgn(r['expected_constant'])}$\\\\")
lines += [r"\bottomrule", r"\end{longtable}"]
open(os.path.join(base, "table_p_le_29.tex"), "w").write("\n".join(lines) + "\n")

# Table 2: per level aggregates
lines = [r"\begin{tabular}{rrrrrrrc}", r"\toprule",
         r"$N$ & range & tier & pairs & thin pts & non-rat. thin & $\#\{r_iW_i\}>1$ & all $=-\left(\frac{-N}{p}\right)$\\", r"\midrule"]
for mode in ("certified", "kz"):
    for N in (2, 3, 5, 7, 13):
        sel = [r for r in rows if r["mode"] == mode and r["N"] == N]
        if not sel:
            continue
        a = agg(sel)
        nonconst = sum(1 for r in sel if not r["ratio_constant"])
        lines.append(f"{N} & ${a['pmin']}\\le p\\le {a['pmax']}$ & {'Tier 1' if mode == 'certified' else 'Tier 2'} & {a['pairs']} & {a['thin_points']} & "
                     f"{a['nonrational_thin_points']} & {nonconst} & {'yes' if a['all_match_conjecture'] else 'NO'}\\\\")
lines += [r"\bottomrule", r"\end{tabular}"]
open(os.path.join(base, "table_levels.tex"), "w").write("\n".join(lines) + "\n")

# Table 3: non-thin points for p <= 13 (collisions / exceptional automorphisms)
lines = [r"\begin{longtable}{rrllllr}", r"\toprule", r"$N$ & $p$ & $t$ & $u$ over $t$ & $j$ & $(m_x,|\mathrm{Stab}|)$ & $e$\\",
         r"\midrule", r"\endhead"]
for r in rows:
    if r["mode"] != "certified" or r["p"] > 13:
        continue
    for x in r["nonthin"]:
        lines.append(f"{r['N']} & {r['p']} & ${x['t'].replace('*','')}$ & ${', '.join(x['u']).replace('*','')}$ & ${', '.join(sorted(set(x['j']))).replace('*','')}$ & "
                     f"$({x['m']},{x['stab']})$ & {x['e']}\\\\")
lines += [r"\bottomrule", r"\end{longtable}"]
open(os.path.join(base, "table_nonthin_small.tex"), "w").write("\n".join(lines) + "\n")
print(json.dumps({k: v for k, v in summary.items() if k not in ("by_level_certified", "by_level_kz")}, indent=1))
