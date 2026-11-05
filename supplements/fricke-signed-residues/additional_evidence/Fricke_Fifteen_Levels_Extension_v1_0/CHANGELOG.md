# Changes from manuscript v1.6 to v1.7

- Extended Theorem 1.1, with all six parts and its reconstruction corollary, from the five eta-coordinate levels to all fifteen prime levels with genus-zero Fricke quotient.
- Added Lemma 2.1, constructing the integral Fricke coordinate by tame quotient formation and relative Riemann–Roch. The proof supplies both Fourier integrality at the allowed primes and a coordinate on each good special fibre.
- Replaced the global five-level definition of T by its normalized quotient-coordinate definition; kept the eta formulas explicitly restricted to N in {2,3,5,7,13}.
- Wrote the Hecke construction over Lambda_N=Z[1/(6N)], the ring supplied by the geometric coordinate lemma. This suffices for every p in the theorem. The proof does not require importing stronger global integer-coefficient assertions from moonshine.
- Explained symmetry of the Hecke polynomial by comparison of its two monic leading coefficients, avoiding reliance on primitive polynomials over Z after the ring change.
- Retained the inertia, Hasse-derivative and weighted-product proofs, which do not require a global coordinate on X_0(N). Removed the last uses of the explicit five-level u-coordinate from the general setup.
- Retained Theorems 1.3 and 1.5 and the factorial proof. Their scope and arithmetic formulas are unchanged. The eta-coordinate restatement of Theorem 1.5 remains explicitly five-level.
- Retained the Nakaya shift table, explicit elliptic-value polynomials, level-two vanishing criterion and examples as five-level or level-two applications. No unsupported higher-level analogue of the fixed elliptic-value table was added.
- Extended the geometric interpretation to the same fifteen levels; its proof works with arbitrary prime-to-p auxiliary prime level N.
- Added exact certificates at all ten new levels through p=47 (122 pairs, 4056 thin values, 3222 non-rational), and reran all five old levels through p=47 (62 pairs, 402 thin values, 226 non-rational). The fresh combined run covers 184 admissible pairs, 4458 thin values and 3448 non-rational thin values.
- Kept the pre-existing larger computational ranges explicitly scoped to the five original levels. Added the new-level model recipe, verification table and source provenance separately.
- Cited Ogg's original classification and the SageMath source of the classical modular models. Updated the further-directions section: the fifteen-level extension is now part of the theorem; composite levels and positive-genus quotients remain separate questions.

The main theorem remains numbered 1.1. The factorial and signed discriminant-ratio statements remain numbered 1.3 and 1.5. Subsequent section-2 result numbers shift because of the new coordinate lemma; all cross-references are generated from labels.

The source compiles to 19 pages with pdfLaTeX. Citations and cross-references resolve, and no overfull boxes remain. No PDF is needed to use the standalone TeX source.

The new proof and code are available for specialist scrutiny; this revision is not an independent expert referee report. The data repository URL is still to be set by the author after a public deposit.
