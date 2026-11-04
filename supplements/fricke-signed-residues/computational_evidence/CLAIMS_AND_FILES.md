# Paper claims and their computational files

All paths below are relative to this supplement. Let `S` abbreviate
`packages/Signed_Weighted_Residue_v1_0` and `E` abbreviate
`packages/Eta_Frobenius_Lemma_Audit_v1_0`.

| Location in journal draft v1.3 | Evidence | Reproduction code |
| --- | --- | --- |
| Section 8, certified reconstructions and its five-row table | `S/results/certified/N??_p????.json`, `S/results/summary.json`, `S/results/pairs.csv`; independently recounted in `verification/paper_table.csv` | `S/code/run_all.py`, `wr_pairs.py`, `wr_core.py`; wrapper suite `certified` |
| Section 8, candidate-free denominator recovery through p = 37 | `pade_den_equals_D_thin` in the applicable certified JSONs | Same driver with `--pade-max 37` |
| Section 8, 960 derivative-formula cases | `S/results/kz/N??_p????.json` | Same driver; wrapper suite `kz` |
| Section 8, Hecke polynomial checks through p = 31 | `S/results/hecke_polynomial_checks.json`, `hecke_check.log` | `S/code/hecke_check.py`; wrapper suite `hecke` |
| Section 8, eta/Frobenius sign by Velu quotients | `E/results/velu_sign_checks.json`, `velu_sign_run.log`, `velu_sign_table.md` | `E/code/velu_sign_check.py`; wrapper suite `velu` |
| Eta-character calculation, auxiliary finite checks | `S/results/eta_multiplier_checks.json`, `E/results/eta_multiplier_audit.json` | Original and audit multiplier scripts; wrapper suite `eta-multiplier` |
| Coordinate normalizations in Sections 1 and 3 | `S/results/normalization_checks.json` | `S/code/verify_normalization.py 300`; included in `smoke` and `certified` |
| Section 1.4, Table 1 level-two fractions | `S/results/certified/N02_p0011.json`, `N02_p0013.json`, `N02_p0017.json`, `N02_p0029.json` | Included in `smoke` |
| Corollary 1.4, finite checks of level-one constancy | `S/results/level1_c_checks.json` | `S/code/level1_c_explore.py`; wrapper suite `level1` |
| Conjecture 1.5 and Remark 6.2, factorial formula | `S/results/level1_c_closed_form.json` | `S/code/level1_c_formula.py`; wrapper suite `level1` |

## Exact interpretation

The certified driver reconstructs the numerator from the q-expansion using a
denominator built from supersingular data, then checks the finite bound in
Proposition 8.1. It does not insert the signed residue formula to determine the
numerator. JSON records document the inputs, reconstructed fraction and test
outcomes; rerunning the supplied code recomputes the required q-series. The JSON
files do not themselves contain the full very long q-series.

The derivative tier uses the paper's derivative lemma to evaluate residues.
The Velu route is computationally separate from the eta/Hauptmodul route and
evaluates discriminants of normalized isogeny quotients. It is not a human
referee report or an all-prime computational proof. Its auxiliary Deuring-model
selection routine sets a Python random seed and uses random point tests; the
underlying FLINT random choices are not guaranteed to be identical. Timings,
point choices and field presentations need not be byte-for-byte reproducible. The target finite
field operations and recorded discriminant-ratio tests are exact.

## Historical files outside the paper's claims

The signed package also contains level-11 experiments, internal consistency
scripts, a historical research note, and a template/build script for that note.
These are retained to preserve the original package and its checksums. They are
not additional claims of the journal paper. In particular, do not use the old
note builder to generate the current journal manuscript.

The multiplier audit records an expected `1/8` offset when comparing two eta
multiplier conventions. Its negative-control section intentionally exhibits
failures outside the hypotheses. Neither is a counterexample to the theorem.
