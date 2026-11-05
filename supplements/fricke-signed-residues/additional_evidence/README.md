# Additional evidence for the journal draft (v1.9 and v1.10)

These are the four packages that journal drafts v1.9 and v1.10 added to the *Data and software* paragraph (Section 8):

| Package | Supports | Paper location |
|---|---|---|
| [`Factorial_Conjecture_Result_v1_0/`](Factorial_Conjecture_Result_v1_0/) | The supersingular factorial evaluation B<sup>h</sup> = (6/p)·h!·Δ<sup>k</sup>, now **proved** as Theorem 1.3 | Section 5 (proof); Section 8, final paragraph (computations) |
| [`Fricke_Fifteen_Levels_Extension_v1_0/`](Fricke_Fifteen_Levels_Extension_v1_0/) | Theorem 1.1 at the ten additional levels N ∈ {11, 17, 19, 23, 29, 31, 41, 47, 59, 71}, plus a fresh regression at the original five levels | Lemma 2.1 (integral coordinate); Section 8, Table 4 |
| [`Corollary_1_2_Reconstruction_Benchmark_v1_0/`](Corollary_1_2_Reconstruction_Benchmark_v1_0/) (v1.10) | Timings of the Corollary 1.2 reconstruction against a q-expansion/Padé route at N ∈ {2, 3, 5, 7, 13} | Section 8.1, Table 5 |
| [`Theorem_1_3_Benchmark_v1_0/`](Theorem_1_3_Benchmark_v1_0/) (v1.10) | Timings of the cached factorial evaluation of B<sup>h</sup> against coefficient-polynomial baselines | Section 8.1 |

The original two packages (`Signed_Weighted_Residue_v1_0`, `Eta_Frobenius_Lemma_Audit_v1_0`) are unchanged in [`../computational_evidence/`](../computational_evidence/).

In every case the computations are finite checks. The proofs are in the paper; the computations are not used in them. The benchmark timings measure the tested implementations on one host; they are not optimality claims. Read each benchmark's `REPORT.md` first.

`verify_additional.py` covers the two v1.9 packages. Each benchmark package has its own `SHA256SUMS.txt` (check with `sha256sum -c SHA256SUMS.txt`) and an exact replay script, `verify_saved.py`.

## Quick check

Standard library only. This verifies all three package manifests and recounts every total that v1.9 reports for these packages. It does not rerun the mathematics.

```sh
python verify_additional.py        # expected last line: "status: PASS"
```

## Paper claims and files

Let `F` abbreviate `Factorial_Conjecture_Result_v1_0/new_work` and `X` abbreviate `Fricke_Fifteen_Levels_Extension_v1_0`.

| Claim in v1.9 | Evidence | Code |
|---|---|---|
| Section 8, Table 4: 122 admissible pairs at the ten new levels, 5 ≤ p ≤ 47, 4056 thin values, 3222 non-rational, all certificates pass | `X/results/new_levels_p47.json`, `.log` | `X/code/verify_extension.py`, model data `X/code/hyperelliptic_data.json` |
| Section 8: fresh regression at N ∈ {2, 3, 5, 7, 13} through p = 47, 62 pairs, 402 thin values, 226 non-rational | `X/results/five_level_regression_p47.json`, `.log` | `X/code/regression_five.py` (loads the unchanged copies `X/code/inherited_wr_*.py`) |
| Section 8: combined fifteen-level run, 184 pairs, 4458 thin values, 3448 non-rational | Sum of the two rows above | — |
| Lemma 2.1, integral Fricke coordinate | Proof draft `X/research/integral_coordinate.tex` (historical; the paper's version supersedes it) | — |
| Section 8, final paragraph: factorial evaluation at all 166 primes 5 ≤ p ≤ 997, 6430 supersingular j-values (4734 outside 𝔽<sub>p</sub>), three rescaled models per value, plus Legendre and Weierstrass routes | `F/results/verify_factorial_p5_997.json`, `.log` | `F/code/verify_factorial.py`, `F/code/modp_lib.gp` |
| Same paragraph: the negated constant fails at every prime in range | `F/results/negative_control_p5_997.json`, `.log` | `verify_factorial.py --negate` |
| Same paragraph: the two theta identities of the proof, as polynomial identities in 𝔽<sub>p</sub>[E<sub>4</sub>, E<sub>6</sub>] at p = 23, 47, 71, 167 | `F/results/mechanism_check_p23mod24_le167.log` | `F/code/mechanism_check.py` |
| Corollary 1.4 and the Kaneko–Zagier/Legendre forms (auxiliary) | `F/results/corollary_check.log` | `F/code/corollary_check.py` |
| Section 5, η² on Γ(12) (auxiliary numerical check) | `F/results/eta2_gamma12_check.log` | `F/code/eta2_gamma12_check.py` |

### How the ten-level verifier works

Each new level uses SageMath's stored model v² = f<sub>N</sub>(u) of X<sub>0</sub>(N), with w<sub>N</sub>(u, v) = (u, −v). The coordinate is T<sub>N</sub> = u − s<sub>N</sub>; its q-expansion comes from Newton inversion of α<sub>N</sub>(u(q)) = j(q) + j(q<sup>N</sup>). The ramification indices e<sub>i</sub> come from the geometry of the model, not from the residue formula or the weighted Hasse polynomial. Numerators are reconstructed from the q-expansion and certified by Proposition 8.1. Model provenance, including the SHA-256 of the SageMath source file, is in `X/README.md`.

### Level 11

Level 11 is now inside the theorem. Its certificates are the N = 11 records in `X/results/new_levels_p47.json`. The older level-11 files are exploratory and predate the theorem's extension; they are not the paper's evidence:

- `../computational_evidence/packages/Signed_Weighted_Residue_v1_0/` (level-11 experiments noted in that bundle's `CLAIMS_AND_FILES.md`);
- `Factorial_Conjecture_Result_v1_0/quick_start/code/extra/level11_check.py` and `t11_probe.py`.

## Reproduction

| Package | Requirements | Command (from the package directory) | Recorded time |
|---|---|---|---|
| Fifteen levels | Python ≥ 3.11, `python-flint==0.9.0` | `python3 code/verify_extension.py --pmax 47 --out results/new_levels_p47.json` then `python3 code/regression_five.py` | about 3 minutes for the ten-level run |
| Factorial | Python ≥ 3.11, `cypari2==2.2.4` (bundles PARI/GP 2.17.2), `mpmath==1.3.0`; `python-flint==0.9.0` for the inherited scripts; `pdflatex` to rebuild the note | `cd new_work && pip install -r requirements.txt && ./run_all.sh` | about 12 minutes |

Both scripts overwrite their package's own `results/` files. Run them on a copy to keep the committed baseline intact. Don't run the fifteen-level scripts with `python -O`, because they rely on assertions. SageMath isn't needed: the model coefficients are bundled.

## Files not committed

Five files listed in `Factorial_Conjecture_Result_v1_0/SHA256SUMS.txt` are not in this repository. `verify_additional.py` skips them by name.

| File | Reason |
|---|---|
| `sources/Robert 1980.pdf`, `sources/Landweber 1988.pdf`, `sources/Kaneko & Zagier 1998.pdf` | Third-party publisher copies of the cited papers; not redistributable. See the paper's bibliography. |
| `evidence/Signed_Weighted_Residue_v1_0.zip`, `evidence/Eta_Frobenius_Lemma_Audit_v1_0.zip` | Byte-identical duplicates of the original archives. Their SHA-256 values match `../computational_evidence/PROVENANCE.json`, and their extracted contents are in `../computational_evidence/packages/`. |

## Naming and historical material

- The factorial package unpacks as `Factorial_Conjecture_Research_Handoff_v1_0/`. It is committed here as `Factorial_Conjecture_Result_v1_0/`, the name used in the paper. The contents are unchanged.
- The factorial package refers to the factorial evaluation as **Conjecture 1.5** of draft v1.4. In v1.9 it is **Theorem 1.3**. The v1.4 Theorem 1.3 (eta quotient at supersingular points) is now Theorem 1.5. The package's `VERDICT.md`, `note/factorial_constant_proof.*` and `SOURCE_PRIORITY_ASSESSMENT.md` are AI-assisted research documents that predate v1.9. The paper supersedes them.
- `Factorial_Conjecture_Result_v1_0/manuscript/` (draft v1.4), `Fricke_Fifteen_Levels_Extension_v1_0/input/` (v1.6) and `.../manuscript/` (v1.7) are earlier drafts kept so the package manifests verify. Draft v1.9 at `../` supersedes them.
- Later revisions (v1.8–v1.9) added Remark 2.5 (Faber polynomials), Remark 5.3 (the p = 17 limit to higher-root constancy) and Corollary 6.1 (arbitrary prime-to-p isogenies). No package computation was rerun for these. Remark 5.3 is a small explicit calculation written out in the paper.

## Licence

The code and computational records here are MIT-licensed; see the repository [`LICENSE`](../../../LICENSE). The manuscripts, notes and research documents (`*.tex`, `*.pdf`, `VERDICT.md`, `SOURCE_PRIORITY_ASSESSMENT.md`, `RESEARCH_PROMPT.md`) are all rights reserved.
