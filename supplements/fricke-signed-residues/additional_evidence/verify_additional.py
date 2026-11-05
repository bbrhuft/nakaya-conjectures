#!/usr/bin/env python3
"""Check the two additional evidence packages against their manifests and the paper.

Standard library only. This verifies file hashes and recounts the recorded totals
reported in journal draft v1.9 (Section 8 and Table 4). It does not rerun the
mathematical computations; see README.md for the reproduction commands.

Usage (from this directory):  python verify_additional.py
"""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIFTEEN = HERE / "Fricke_Fifteen_Levels_Extension_v1_0"
FACTORIAL = HERE / "Factorial_Conjecture_Result_v1_0"

# Files listed in the factorial package's top-level manifest but deliberately not
# committed here (see README.md, "Files not committed").
EXCLUDED = {
    "sources/Robert 1980.pdf",
    "sources/Landweber 1988.pdf",
    "sources/Kaneko & Zagier 1998.pdf",
    "evidence/Signed_Weighted_Residue_v1_0.zip",
    "evidence/Eta_Frobenius_Lemma_Audit_v1_0.zip",
}

# Totals stated in journal draft v1.9, Section 8 and Table 4.
PAPER_TABLE4 = {
    11: (12, 136, 86), 17: (12, 203, 140), 19: (12, 231, 170),
    23: (12, 267, 202), 29: (12, 334, 260), 31: (12, 350, 272),
    41: (12, 445, 352), 47: (12, 483, 382), 59: (13, 733, 614),
    71: (13, 874, 744),
}
PAPER_REGRESSION = (62, 402, 226)
PAPER_ALL_FIFTEEN = (184, 4458, 3448)
PAPER_FACTORIAL = {"primes": 166, "pmin": 5, "pmax": 997,
                   "ss_j": 6430, "ss_j_not_in_Fp": 4734}
PAPER_MECHANISM_PRIMES = [23, 47, 71, 167]

failures = []


def check(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        failures.append(msg)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def verify_manifest(base, manifest, skip=()):
    n_ok = n_skip = 0
    for line in (base / manifest).read_text(encoding="utf8").splitlines():
        if not line.strip():
            continue
        digest, name = line.split(None, 1)
        name = name.lstrip("*")
        if name in skip:
            n_skip += 1
            continue
        p = base / name
        if not p.is_file():
            check(False, f"{base.name}/{name} missing")
        elif sha256(p) != digest:
            check(False, f"{base.name}/{name} hash mismatch")
        else:
            n_ok += 1
    return n_ok, n_skip


def main():
    print("Manifests")
    ok, _ = verify_manifest(FIFTEEN, "SHA256SUMS.txt")
    check(ok == 18, f"fifteen-level package: {ok} of 18 files verify")
    ok, skipped = verify_manifest(FACTORIAL, "SHA256SUMS.txt", EXCLUDED)
    check(ok == 25 and skipped == 5,
          f"factorial package top manifest: {ok} of 25 committed files verify "
          f"({skipped} listed files intentionally not committed)")
    ok, _ = verify_manifest(FACTORIAL / "new_work", "SHA256SUMS_new_work.txt")
    check(ok == 46, f"factorial package new_work manifest: {ok} of 46 files verify")

    print("Ten additional levels (Table 4)")
    recs = json.loads((FIFTEEN / "results/new_levels_p47.json").read_text(encoding="utf8"))
    tally = defaultdict(lambda: [0, 0, 0])
    for r in recs:
        t = tally[r["N"]]
        t[0] += 1
        t[1] += r["n_thin"]
        t[2] += r["n_nonrational_thin"]
    for N, expected in PAPER_TABLE4.items():
        check(tuple(tally[N]) == expected,
              f"N={N}: pairs/thin/non-rational {tuple(tally[N])} vs paper {expected}")
    check(all(r["certificate"] is True for r in recs), "all 122 certificates pass")
    check(all(r["ratio_set"] == [r["expected"]] for r in recs if r["n_thin"]),
          "every weighted residue product equals -(-N/p)")
    check(max(r["p"] for r in recs) == 47, "range ends at p = 47")

    print("Fresh five-level regression")
    reg = json.loads((FIFTEEN / "results/five_level_regression_p47.json").read_text(encoding="utf8"))
    got = (len(reg), sum(r["n_thin"] for r in reg), sum(r["n_thin_nonrational"] for r in reg))
    check(got == PAPER_REGRESSION, f"pairs/thin/non-rational {got} vs {PAPER_REGRESSION}")
    check(all(r["certificate_ok"] for r in reg), "all 62 regression certificates pass")
    combined = tuple(a + b for a, b in zip(got, (len(recs), sum(t[1] for t in tally.values()),
                                                  sum(t[2] for t in tally.values()))))
    check(combined == PAPER_ALL_FIFTEEN,
          f"all fifteen levels through p = 47: {combined} vs {PAPER_ALL_FIFTEEN}")

    print("Factorial evaluation (Theorem 1.3)")
    fac = json.loads((FACTORIAL / "new_work/results/verify_factorial_p5_997.json").read_text(encoding="utf8"))
    meta, frecs = fac["meta"], fac["records"]
    check(meta["n_primes"] == PAPER_FACTORIAL["primes"] == len(frecs)
          and meta["pmin"] == PAPER_FACTORIAL["pmin"] and meta["pmax"] == PAPER_FACTORIAL["pmax"],
          f"{len(frecs)} primes, {meta['pmin']} <= p <= {meta['pmax']}")
    nss = sum(r["n_ss_j"] for r in frecs)
    nout = sum(r["n_ss_j_not_in_Fp"] for r in frecs)
    check((nss, nout) == (PAPER_FACTORIAL["ss_j"], PAPER_FACTORIAL["ss_j_not_in_Fp"]),
          f"{nss} supersingular j-values, {nout} outside F_p")
    check(meta["all_ok"] and all(r["all_ok"] for r in frecs), "all four routes pass at every prime")
    check(meta["models_per_j"] == 3, "three rescaled models per j-value")
    neg = json.loads((FACTORIAL / "new_work/results/negative_control_p5_997.json").read_text(encoding="utf8"))
    check(not neg["meta"]["all_ok"] and len(neg["meta"]["failures"]) == PAPER_FACTORIAL["primes"],
          "negated constant fails at all 166 primes")
    mech = (FACTORIAL / "new_work/results/mechanism_check_p23mod24_le167.log").read_text(encoding="utf8")
    for p in PAPER_MECHANISM_PRIMES:
        line = next((l for l in mech.splitlines() if l.startswith(f"p={p}:")), "")
        check(line.count("True") >= 4 and "control A|B^h+(6/p)h!D^k: False" in line,
              f"theta identities checked at p = {p}")

    print()
    print("status:", "FAIL" if failures else "PASS")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
