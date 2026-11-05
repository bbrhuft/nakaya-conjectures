# new_work/ — Conjecture 1.5 (supersingular factorial constant): result package v1.0

**Result.** Conjecture 1.5 of D. Jordan, *Supersingular poles and signed residues of prime-level Fricke Hauptmoduln* (v1.4), is **proved for every prime p ≥ 5**:

    E_{p+1}^{(p−1)/2} ≡ (6/p)·((p−1)/2)!·Δ^{(p²−1)/24}  (mod p, E_{p−1}),

i.e. c(E) = (6/p)·((p−1)/2)! for every supersingular E/F̄_p. The proof is uniform in p and covers p ≡ 1 (mod 12). It needs neither Baker's congruence nor constancy, and recovers both as corollaries. See `VERDICT.md` for a one-page summary and `note/factorial_constant_proof.pdf` for the proof.

## Contents
| Path | What it is |
|---|---|
| `VERDICT.md` | Verdict, and what is proved, imported, computational or conjectural |
| `note/factorial_constant_proof.tex`, `.pdf` | Standalone proof note (8 pp.): theorem, proof, corollaries, audit, suggested manuscript text, references |
| `SOURCE_PRIORITY_ASSESSMENT.md` | What Baker, Robert, Landweber, Kaneko–Zagier and Ono actually state (with theorem and page numbers), the priority classification, and the normalization audit |
| `code/modp_lib.gp` | PARI/GP library: E_k mod p as polynomials in E4, E6; ss_p(j); exact divisibility test by E_{p−1} |
| `code/verify_factorial.py` | Independent exact verification, routes I–IV (see below), with a `--negate` negative control |
| `code/corollary_check.py` | Exact checks of A = c_{p−1} and B = 3c_{p−2} in F_p[a,b], the signed KZ (40) formula, and the Legendre/Deuring form |
| `code/mechanism_check.py` | Symbolic check of the two proof identities in F_p[E4,E6] for p ≡ 23 (mod 24), where η^{p+1} has level one |
| `code/eta2_gamma12_check.py` | Numerical check (60 digits) that η² has trivial character on Γ(12) |
| `results/` | JSON and logs of all runs |
| `reproduction/`, `reproduction_*.log` | Copy of the inherited `quick_start/` and its rerun logs. The inherited scripts overwrite files in the copy only. |
| `explore/` | Exploratory scripts from the proof search; not needed for reproduction |
| `run_all.sh` | One command that regenerates every result |
| `requirements.txt` | Environment |
| `SHA256SUMS_new_work.txt` | Checksums of every file in new_work/ |

## Verification routes (all exact arithmetic over F_p and F_{p²}; no floating point)
- **IV, divisibility.** R(j) = E_{p+1}^h/Δ^k reduced modulo ss_p(j) equals (6/p)·h!. This is equivalent to divisibility in F_p[E4,E6] (note, Lemma 2.2).
- **I, point evaluation.** E_{p+1}(E4, E6) is evaluated at every supersingular j in F_{p²}, including non-rational ones, on three random rescalings (u⁴E4, u⁶E6) each.
- **II, Legendre route.** (6/p)·2^{8k}·(λ(1−λ))^{h−2k}·H′(λ)^h at every root of the Deuring polynomial. No Eisenstein series are used, and the resulting j-set is cross-checked against ss_p.
- **III, Hasse–Witt route.** (3/p)·c_{p−2}^h/Δ^k on y² = x³ + ax + b. E_{p+1} is not used.

**Outcome.** All 166 primes 5 ≤ p ≤ 997 pass all four routes: 36, 44, 44 and 42 primes in the classes 1, 5, 7 and 11 (mod 12). This covers 6430 supersingular j-values, 4734 of them outside F_p, and 19 290 models. The supersingular counts agree with Eichler–Deuring. The negative control −(6/p)·h! fails all 166 primes. The corollary checks pass for p ≤ 997, with the F_p[a,b] identities checked for p ≤ 200. The mechanism identities hold for p = 23, 47, 71 and 167. The inherited script reproduces 166/166 matches. Finite checks support the proof but do not replace it.

## Commands
```sh
cd new_work
pip install -r requirements.txt   # add --break-system-packages on some systems
./run_all.sh                      # about 12 min on one core
```
Individual runs: `python3 -I code/verify_factorial.py 997 [--negate] [--models M] --out results/x.json`.

## Environment and timings (this run)
Linux x86_64, 2 cores, 7 GB RAM; Python 3.13.18; cypari2 2.2.4 with PARI/GP 2.17.2; mpmath 1.3.0; python-flint 0.9.0 (inherited scripts only); TeX Live pdflatex.

| Run | Time |
|---|---|
| verify p ≤ 997 | 170 s |
| corollaries p ≤ 997 | 125 s |
| mechanism check (p = 167 alone) | 283 s |
| inherited `level1_c_formula.py 997` | 7.7 s |
| inherited brute-force check, p ≤ 73 | 53 s |

## Inherited files
The handoff files outside `new_work/` are unchanged. Their `SHA256SUMS.txt` was re-verified before packaging; see `results/inherited_sha256_check.log`.
