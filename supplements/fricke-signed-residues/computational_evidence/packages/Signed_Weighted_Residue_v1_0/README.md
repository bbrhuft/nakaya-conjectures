# Signed weighted residues for the Fricke Hauptmoduln of levels 2, 3, 5, 7, 13

Research package, version 1.0 (3 November 2026). AI-assisted; not refereed.
The level-two paper and its handoff bundle were **not modified**.

## Result in one paragraph

For N ∈ {2,3,5,7,13}, every prime p ≥ 5 with p ≠ N, and every thin supersingular value t_i
of T_N (effective inertia e_i = 1):

    Res_{T=t_i} R_{N,p}(T) · ∏_{k≠i} (t_i − t_k)^{(p+1)/e_k}  =  −(−N/p).

The reduced denominator of R_{N,p} is ∏_{thin}(T − t_i). All poles are simple, every residue is
nonzero, and all residues and weighted products lie in F_p^×, including at non-rational points.
`note/Signed_Weighted_Residue_Note.pdf` gives the proof. It is uniform in N and rests on the
imported facts listed in its Section 2. The main ingredients are:

1. **Kaneko–Zagier step (elementary).** The residue equals the coefficient of (T − t_i)^{-2} in
   (θT)^{p−1}/A², where A is the Hasse invariant. This proves the pole theorem and gives
   r_i W_i = E_{p+1}^{p−1} / (Δ(τ)Δ(Nτ))^{(p²−1)/24} at the supersingular point.
2. **Baker (Acta Arith. 1998).** E_{p+1}^{p−1} ≡ −(−1/p) Δ^{(p²−1)/12} mod (p, E_{p−1}).
3. **New: eta quotient at supersingular points.** (Δ(τ)/Δ(Nτ))^{(p²−1)/24} = (N/p) at every
   supersingular point of X_0(N), for every prime N ≠ p. The proof uses the eta multiplier
   (Gordon–Hughes–Newman) and diamond operators. This refines Ono (arXiv:2509.16175), Thm 1.2.

Corollary: c(E) = E_{p+1}^{(p−1)/2}/Δ^{(p²−1)/24} is constant on the supersingular locus, which is a
square root of Baker's congruence. Observed for 5 ≤ p ≤ 997 but **not proved**: the constant is
(6/p)·((p−1)/2)! mod p.

## Layout

    README.md
    note/   Signed_Weighted_Residue_Note.tex   self-contained LaTeX (numbers and tables filled in)
            Signed_Weighted_Residue_Note.pdf   compiled with pdflatex (TeX Live 2023)
            template/...template.tex           source with placeholders, filled by code/build_note.py
    code/   wr_core.py              q-series, F_{p^2} arithmetic, supersingular data, j-maps
            wr_pairs.py             per-(N,p) computation and all checks
            run_all.py              driver (certified tier and Kaneko–Zagier tier)
            verify_normalization.py exact Z-checks of T_N, j-maps, Fricke action
            hecke_check.py          Hecke polynomial Psi_{N,p} mod p^2 cross-check
            eta_multiplier_check.py exact Dedekind-sum check of the eta multiplier
            level1_c_explore.py     Baker congruence and constancy of c(E), p <= 997
            level1_c_formula.py     test of the observed closed form for c_p
            extra/level11_check.py  exploratory run at N = 11 (outside the brief)
            independent_check/      separate re-implementation written during an internal audit:
                                    e2e_bm.py (den R by Berlekamp–Massey, weights from Δ_N^{-k}; 10 pairs),
                                    level1_check.py, mult_check.py (uncertified consistency checks)
            summarize.py, build_note.py
            requirements.txt
    results/
            certified/N??_p????.json   one file per pair, Tier 1 (p <= 211)
            kz/N??_p????.json          one file per pair, Tier 2 (223 <= p <= 1499)
            summary.json, pairs.csv    aggregates; every boolean check; counterexample list
            normalization_checks.json, hecke_polynomial_checks.json,
            eta_multiplier_checks.json, level1_c_checks.json, level1_c_closed_form.json,
            level11_exploratory.json, independent_check.log, table_*.tex, run_*.log
    BRIEF.md            the investigation brief, as supplied
    SHA256SUMS.txt

## What each tier means

* **Tier 1, certified (5 ≤ p ≤ 211).** The q-expansion of T_N mod p is computed to q^{p^3}, which gives
  T|U_p to q^{p^2}. The numerator P is read off using the candidate denominator D_thin, which is built
  only from supersingular data. The certificate checks that D_thin(T)·(T|U_p) − P(T) vanishes through
  q^{p^2−d}. Since den R | T^{p^2} − T a priori (Kronecker congruence), this proves R = P/D_thin
  exactly. For p ≤ 37 the denominator is also recovered with no candidate at all.
* **Tier 2 (223 ≤ p ≤ 1499).** Residues come from the proven double-pole lemma
  r_t = [(T − t)^{−2}] (θT)^{p−1}. This depends on that lemma, not on the conjecture, and agrees
  with Tier 1 wherever both were run.

No computation is used as a premise of any proof.

## Reproduce

    python3 -m pip install -r code/requirements.txt      # python-flint 0.9.0, mpmath
    cd code
    python3 verify_normalization.py 300                  # seconds
    python3 run_all.py --cert-max 29 --pade-max 29       # reproduction range p <= 29, ~1 s
    python3 run_all.py --cert-max 211 --pade-max 37      # full Tier 1, ~40-60 min on one core
    python3 run_all.py --cert-min 100000 --cert-max 211 --kz-max 1500 --hasse-power-max 0   # Tier 2, ~30 min
    python3 hecke_check.py 31                            # ~2 min
    python3 eta_multiplier_check.py                      # seconds
    python3 level1_c_explore.py 1000; python3 level1_c_formula.py 1000   # ~25 s
    python3 extra/level11_check.py 61                    # optional, ~5 min
    python3 summarize.py; python3 build_note.py          # tables, summary.json, PDF

Every JSON file stores each test as an explicit boolean. `summary.json` gives `failed_checks` and
`counterexamples` (both empty). Elements of F_{p^2} are printed in python-flint's representation
F_p[z]/(m(z)), with m recorded per pair as `Fp2_modulus`.

## Totals

* Tier 1: 222 pairs (5 ≤ p ≤ 211), 6,246 thin points (4,696 non-rational).
* Tier 2: 960 pairs (223 ≤ p ≤ 1499), 233,336 thin points (210,326 non-rational).
* In every pair the ratio set is a single value, equal to −(−N/p). No check failed (`summary.json`).

## Reproduction of the inherited report

For p ∈ {5,…,29} there are 37 pairs, 135 thin points and 60 non-rational thin points. Of the pairs,
26 have ≥ 2 thin points, 7 have one and 4 have none. Every ratio is −(−N/p), and at p = 29 the
constants are +1,+1,−1,−1,−1 in level order. All of this matches the brief exactly.

## Caveats

* The proof imports standard facts (Kronecker congruence, Hasse invariant and Kodaira–Spencer,
  moduli of X_1(M) and diamond operators, Deuring models, the Gordon–Hughes–Newman theorem,
  connectivity of isogeny graphs) and Baker's theorem. Section 11 of the note lists the steps a
  specialist should check.
* The closed form for c_p and the N = 11 runs are exploratory.
* The literature search was limited (see Section 10 of the note). Not finding a prior statement
  does not establish priority.
