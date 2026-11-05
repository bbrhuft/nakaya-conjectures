# Supplement: supersingular poles and signed residues of prime-level Fricke Hauptmoduln

Journal draft v1.9 (4 November 2026) of a separate paper by David Jordan, with its computational evidence.

**Main theorem (Theorem 1.1).** For each of the fifteen prime levels N ∈ {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71} with X<sub>0</sub>(N)<sup>+</sup> of genus zero, and every prime p ≥ 5 with p ≠ N, the paper determines the poles and residues of the rational function R<sub>N,p</sub> representing T<sub>N</sub>|U<sub>p</sub> modulo p. Here T<sub>N</sub> = q<sup>−1</sup> + O(q) is the normalized Hauptmodul for Γ<sub>0</sub>(N)<sup>+</sup>. The poles are exactly the supersingular values with effective ramification index one. At such a value t<sub>i</sub>, the residue times ∏<sub>j≠i</sub>(t<sub>i</sub> − t<sub>j</sub>)<sup>(p+1)/e<sub>j</sub></sup> equals −(−N/p). An integral-coordinate lemma (Lemma 2.1) builds T<sub>N</sub> over ℤ[1/(6N)], so X<sub>0</sub>(N) itself need not have genus zero.

**Factorial evaluation (Theorem 1.3, proved).** For every prime p ≥ 5 and every supersingular elliptic curve, E<sub>p+1</sub><sup>(p−1)/2</sup> = (6/p)·((p−1)/2)!·Δ<sup>(p²−1)/24</sup>. The proof applies an iterated theta operator to η<sup>p+1</sup> at full level twelve. It recovers Baker's congruence (Corollary 1.4).

**Signed discriminant ratio (Theorem 1.5).** With Robert's isogeny identity, the factorial evaluation gives (Δ(τ)/Δ(ℓτ))<sup>(p²−1)/24</sup> = (ℓ/p) at every supersingular point of X<sub>0</sub>(ℓ), for every prime ℓ ≠ p. Corollary 6.1 extends this to isogenies of any degree prime to p.

This supplement is **separate from the main paper** (`paper/`), which is unchanged. At the five eta-coordinate levels N ∈ {2, 3, 5, 7, 13}, the supersingular values are those of Nakaya's polynomials ss<sub>p</sub><sup>(N\*)</sup> after a shift of coordinate (paper, equation (1.3)).

> **Status: draft, not yet reviewed by a specialist.** AI systems assisted in developing the arguments, checking calculations and preparing the manuscript and the evidence, including the factorial-evaluation argument and its verification code, as stated in the paper. This assistance is not independent specialist refereeing. The paper makes no claim that the exponent (p²−1)/24 itself, or the isogeny transformation of E<sub>p+1</sub>, originates here.

## What changed since v1.4

| v1.4 | v1.9 |
|---|---|
| Residue theorem at five levels, N ∈ {2, 3, 5, 7, 13} | All fifteen prime Fricke levels, via the new integral-coordinate Lemma 2.1. The eta formulas, Nakaya shifts and elliptic-value table stay five-level applications. |
| Factorial evaluation of c<sub>p</sub> was Conjecture 1.5 | Proved for every p ≥ 5 as Theorem 1.3 (new Section 5) |
| Sign from an eta-character calculation (Theorem 1.3) | Sign from the factorial evaluation and Robert's identity (now Theorem 1.5, Section 6) |
| — | New: Remark 2.5 (Faber polynomials and replication), Remark 5.3 (a p = 17 example showing that higher-root constancy fails), Corollary 6.1 (arbitrary prime-to-p isogenies) |
| Certificates at five levels, p ≤ 211 | Same, plus certificates at the ten new levels for p ≤ 47 and a fresh five-level regression (Section 8, Table 4) |

v1.4 remains in the Git history, and its source is also inside `additional_evidence/Factorial_Conjecture_Result_v1_0/manuscript/`.

## Contents

| Path | Contents |
|---|---|
| `Fricke_Signed_Residues_Journal_v1_9.pdf` | The paper (20 pages) |
| `Fricke_Signed_Residues_Journal_v1_9.tex` | LaTeX source (compile with `pdflatex` twice; no external files needed) |
| `computational_evidence/` | Original evidence bundle v1.0, unchanged: `Signed_Weighted_Residue_v1_0` and `Eta_Frobenius_Lemma_Audit_v1_0`, with recorded results, provenance, a SHA-256 manifest and reproduction scripts. See its [`README.md`](computational_evidence/README.md) and [`CLAIMS_AND_FILES.md`](computational_evidence/CLAIMS_AND_FILES.md), keeping in mind the note below. |
| `additional_evidence/` | The two packages added in v1.9: `Factorial_Conjecture_Result_v1_0` (Theorem 1.3) and `Fricke_Fifteen_Levels_Extension_v1_0` (the ten new levels). Start with its [`README.md`](additional_evidence/README.md), which maps v1.9's claims to files. |

**Reading the original bundle against v1.9.** `computational_evidence/` was packaged against draft v1.3 and is committed byte-for-byte, so its documents still describe the older paper. Where they differ from v1.9, the paper and this README take precedence:

- Its "still conjectural" factorial evaluation and "Conjecture 1.5" are now **Theorem 1.3, proved**. The 166-prime `level1_c_closed_form.json` check remains finite evidence for it, not part of the proof.
- Its "Theorem 1.3" (eta/Frobenius sign) is now Theorem 1.5.
- Its five-level scope describes the original computations, not the current theorem. Its level-11 experiments are exploratory and are not the level-11 evidence for v1.9; the N = 11 certificates are in `additional_evidence/Fricke_Fifteen_Levels_Extension_v1_0/results/new_levels_p47.json`.
- Section 8 and Proposition 8.1 (finite certificate) keep their numbers.

Its `PROVENANCE.json` records the SHA-256 of the v1.3 `.tex` and is not updated, so its manifest stays intact.

## Evidence levels

| Computation | Recorded range | What it checks | Location |
|---|---|---|---|
| Certified q-expansion reconstruction, five levels | 222 admissible (N, p) pairs, p ≤ 211 | Exact identities for R<sub>N,p</sub> via the finite certificate (Proposition 8.1); 6246 thin values, 4696 non-rational | `computational_evidence/` |
| Certified reconstruction, ten new levels | 122 pairs, 5 ≤ p ≤ 47 | Same certificate, using SageMath's stored models of X<sub>0</sub>(N) and indices from the model's geometry; 4056 thin values, 3222 non-rational (Table 4) | `additional_evidence/` |
| Fresh five-level regression | 62 pairs, p ≤ 47 | Rerun of the original levels; 402 thin values, 226 non-rational. With the row above: 184 pairs, 4458 thin values, 3448 non-rational | `additional_evidence/` |
| Kaneko–Zagier derivative route | 960 pairs, 223 ≤ p ≤ 1499, five levels | Signed products via the derivative lemma; **not** an independent reconstruction from T|U<sub>p</sub> | `computational_evidence/` |
| Hecke polynomial modulo p² | p ≤ 31, five levels | Symmetry, Kronecker congruence and residue criterion at every element of 𝔽<sub>p²</sub> | `computational_evidence/` |
| Normalized Vélu quotients | 647 (ℓ, p) pairs, ℓ ≤ 47, p ≤ 199 | 127541 cyclic-kernel checks of the discriminant-ratio sign, counted on chosen curve representatives, not distinct coarse points | `computational_evidence/` |
| Factorial evaluation (Theorem 1.3) | 166 primes, 5 ≤ p ≤ 997 | Exact remainders and evaluations at 6430 supersingular j-values (4734 outside 𝔽<sub>p</sub>), with three rescaled models each and Legendre and Weierstrass routes; the negated constant fails at every prime; the proof's theta identities checked at p = 23, 47, 71, 167 | `additional_evidence/` (the older 166-prime check is in `computational_evidence/`) |

These are finite checks of the implementation and normalizations. The theorems rest on the proofs in the paper, and the computations are not used in them. The large five-level sweeps were not rerun when the original bundle was packaged; a bounded fresh rerun is in `computational_evidence/verification/smoke_run/`.

## Checking and reproducing

Both checks need only Python's standard library. They verify hashes and recorded totals against the paper without rerunning the mathematics:

```sh
cd computational_evidence && python scripts/verify_evidence.py     # expected: "status": "PASS"
cd ../additional_evidence && python verify_additional.py          # expected: "status: PASS"
```

To rerun computations:

| Evidence | Requirements | Instructions |
|---|---|---|
| Original bundle | Python 3.12, python-flint 0.9.0, mpmath 1.3.0 | `computational_evidence/REPRODUCTION.md`; e.g. `python scripts/run_reproduction.py smoke` (writes to a new `reproduced/` directory) |
| Ten new levels and regression | Python ≥ 3.11, python-flint 0.9.0 | `additional_evidence/README.md`, Reproduction |
| Factorial evaluation | Python ≥ 3.11, cypari2 2.2.4 (PARI/GP 2.17.2), mpmath 1.3.0 | `additional_evidence/Factorial_Conjecture_Result_v1_0/new_work/run_all.sh` |

The additional packages' scripts write to their own `results/` folders, so run them on a copy.

## Historical material

These files are earlier AI-assisted drafts, audits and research documents. They are kept for provenance and checksum integrity, and **v1.9 supersedes them**:

- `computational_evidence/packages/Signed_Weighted_Residue_v1_0/note/`, `computational_evidence/packages/Eta_Frobenius_Lemma_Audit_v1_0/AUDIT_REPORT.*` and `.../replacement_section/`. The JSON key `matches_conjecture` there is a historical name for the signed product, now Theorem 1.1(e).
- `additional_evidence/Factorial_Conjecture_Result_v1_0/`: `VERDICT.md`, `note/factorial_constant_proof.*`, `SOURCE_PRIORITY_ASSESSMENT.md`, `RESEARCH_PROMPT.md` and the v1.4 manuscript. These call the result "Conjecture 1.5".
- `additional_evidence/Fricke_Fifteen_Levels_Extension_v1_0/`: `research/integral_coordinate.tex` and the v1.6 and v1.7 manuscripts.

Three third-party paper PDFs and two duplicate archives from the factorial package are not committed; see `additional_evidence/README.md`.

## Licence

The code and computational records in `computational_evidence/` and `additional_evidence/` are MIT-licensed; see the repository [`LICENSE`](../../LICENSE). The paper and the historical documents listed above are all rights reserved.
