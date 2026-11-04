# Supplement: supersingular poles and signed residues of prime-level Fricke Hauptmoduln

Journal draft v1.4 (4 November 2026) of a separate paper by David Jordan, with its computational evidence bundle.

For N ∈ {2, 3, 5, 7, 13} and every prime p ≥ 5, p ≠ N, the paper determines the poles and residues of the rational function R<sub>N,p</sub> representing T<sub>N</sub>|U<sub>p</sub> modulo p, where T<sub>N</sub> is the normalized Hauptmodul for Γ<sub>0</sub>(N)<sup>+</sup>. The poles are exactly the supersingular values with effective ramification index one. At such a value t<sub>i</sub>, the residue times ∏<sub>k≠i</sub>(t<sub>i</sub> − t<sub>k</sub>)<sup>(p+1)/e<sub>k</sub></sup> equals −(−N/p) (Theorem 1.1). The sign comes from an eta-character calculation, which gives (Δ(τ)/Δ(ℓτ))<sup>(p²−1)/24</sup> = (ℓ/p) at every supersingular point of X<sub>0</sub>(ℓ), for every prime ℓ ≠ p (Theorem 1.3). The factorial evaluation of the constant c<sub>p</sub> (Conjecture 1.5) remains a conjecture.

This supplement is **separate from the main paper** (`paper/`), which is unchanged. Its supersingular values are those of Nakaya's polynomials ss<sub>p</sub><sup>(N\*)</sup> after a shift of coordinate (paper, equation (1.3)).

> **Status: draft, not yet reviewed by a specialist.** AI systems assisted in developing the arguments, checking calculations and preparing the manuscript and the evidence bundle, as stated in the paper. This assistance is not independent specialist refereeing. The paper makes no claim that the exponent (p²−1)/24 itself, or the isogeny transformation of E<sub>p+1</sub>, originates here.

## Contents

| Path | Contents |
|---|---|
| `Fricke_Signed_Residues_Journal_v1_4.pdf` | The paper (19 pages) |
| `Fricke_Signed_Residues_Journal_v1_4.tex` | LaTeX source (compile with `pdflatex` twice; no external files needed) |
| `computational_evidence/` | Computational evidence bundle v1.0: the two packages named in the paper's Data and software paragraph (`Signed_Weighted_Residue_v1_0`, `Eta_Frobenius_Lemma_Audit_v1_0`), recorded results, provenance, a SHA-256 manifest and reproduction scripts. Start with its [`README.md`](computational_evidence/README.md) and [`CLAIMS_AND_FILES.md`](computational_evidence/CLAIMS_AND_FILES.md) |

The bundle was packaged against journal draft v1.3, and `computational_evidence/PROVENANCE.json` records the SHA-256 of that earlier `.tex` file (it is not updated for v1.4, so the manifest stays intact). v1.4 revises proofs, attribution and presentation; it reports the same computational ranges and does not assert a new rerun. The bundle is committed byte-for-byte as supplied; its `GITHUB_UPLOAD.md` describes a standalone repository layout and is kept only because the manifest covers it.

## Evidence levels

| Computation | Recorded range | What it checks |
|---|---|---|
| Certified q-expansion reconstruction | 222 admissible (N, p) pairs, p ≤ 211 | Exact identities for R<sub>N,p</sub> via the finite certificate (Proposition 8.1); 6246 thin values, 4696 non-rational |
| Kaneko–Zagier derivative route | 960 pairs, 223 ≤ p ≤ 1499 | Signed products via the derivative lemma; **not** an independent reconstruction from T|U<sub>p</sub> |
| Hecke polynomial modulo p² | p ≤ 31 | Symmetry, Kronecker congruence and residue criterion at every element of 𝔽<sub>p²</sub> |
| Normalized Vélu quotients | 647 (ℓ, p) pairs, ℓ ≤ 47, p ≤ 199 | 127541 cyclic-kernel checks of the eta/Frobenius sign, counted on chosen curve representatives, not distinct coarse points |
| Factorial formula for c<sub>p</sub> | 166 primes, 5 ≤ p ≤ 997 | Finite evidence for Conjecture 1.5; not a proof |

The large sweeps were not rerun when the bundle was packaged. A bounded fresh rerun is recorded in `computational_evidence/verification/smoke_run/`. Finite agreement checks the implementation and normalizations; it is not a substitute for the proofs.

## Checking and reproducing

From `computational_evidence/`, this needs only Python's standard library. It verifies the release hashes and the recorded totals against the paper, without rerunning the mathematics:

```sh
python scripts/verify_evidence.py      # expected: "status": "PASS"
```

To rerun computations (Python 3.12, python-flint 0.9.0, mpmath 1.3.0), see `computational_evidence/REPRODUCTION.md`:

```sh
python -m pip install -r requirements.txt
python scripts/run_reproduction.py smoke
```

The wrapper writes to a new `reproduced/` directory and leaves the archived evidence untouched.

## Historical material

`packages/Signed_Weighted_Residue_v1_0/note/`, `packages/Eta_Frobenius_Lemma_Audit_v1_0/AUDIT_REPORT.*` and `packages/Eta_Frobenius_Lemma_Audit_v1_0/replacement_section/` are earlier AI-assisted drafts and audits. They are kept for provenance and checksum integrity. They predate repairs in the journal draft and are **superseded by it**. The JSON key `matches_conjecture` is a historical name for the signed product, which is now Theorem 1.1(e). The level-11 files in that package lie outside the paper's five-level theorem.

## Licence

The code and computational records in `computational_evidence/` are MIT-licensed; see the repository [`LICENSE`](../../LICENSE). The paper and the historical documents listed above are all rights reserved.
