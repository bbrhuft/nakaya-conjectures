# Research assignment: the supersingular factorial constant (Conjecture 1.5)

Act as a careful research mathematician in modular forms modulo primes, supersingular elliptic curves, and explicit congruences. Seek a rigorous proof or exact counterexample to Conjecture 1.5 of David Jordan's *Supersingular poles and signed residues of prime-level Fricke Hauptmoduln*, v1.4. Check whether the statement is already known before claiming novelty. Proceed beyond a plan into source checks, exact computation and a proof attempt.

## Read first

Unpack `Factorial_Conjecture_Research_Handoff_v1_0.zip`. Read `START_HERE.md`, `INPUT_PROVENANCE.md`, `SOURCE_GUIDE.md`, then the manuscript's definitions of A, B, Delta and c(E), Corollary 1.4, Conjecture 1.5, and the proof and subsequent remarks in Section 6. Inspect the supplied implementations before reusing them. The evidence archives are inherited research, not independent refereeing. Preserve all inherited files unchanged and put your work in `new_work/`.

## Exact target and conventions

For every prime p >= 5, put h=(p-1)/2 and k=(p^2-1)/24. Use the usual normalized level-one forms

    A = E_(p-1) mod p,    B = E_(p+1) mod p,
    Delta = q product_(n>=1)(1-q^n)^24 = (E4^3-E6^2)/1728.

Here q=exp(2*pi*i*tau), and E_w has constant coefficient 1. For a supersingular elliptic curve E over an algebraic closure of F_p with a nonzero invariant differential omega, define

    c(E) = B(E,omega)^h / Delta(E,omega)^k.

The weights cancel, so c(E) does not depend on the differential. The manuscript proves that c(E) is constant on the supersingular locus, belongs to F_p, and has square -(-1/p). Denote this constant c_p.

The conjecture is

    c_p = (6/p) * h!   in F_p,

where (a/p) is the Legendre symbol and h! is the ordinary factorial reduced modulo p. Equivalently, prove

    B^h - (6/p) h! Delta^k  belongs to the ideal (A) in F_p[E4,E6].

Both numerator terms have weight (p^2-1)/2. Verify this equivalence, including stack multiplicities at j=0 and j=1728. Baker's congruence and Wilson's theorem determine the same square; reproducing that square does not establish the conjecture's sign.

## 1. Audit and literature

Audit the normalizations and identify exactly what may be imported from Baker (1998), Robert (1980), Landweber (1988), and Kaneko--Zagier (1998). Inspect original statements rather than relying on the manuscript's descriptions. Audit the constancy result to the extent needed; if using it conditionally, say precisely so. Look for an existing signed evaluation, including polynomial congruences, supersingular Eisenstein values, Hasse invariants, hypergeometric/Legendre polynomial identities, and Gauss-factorial or Jacobi-sum formulas.

Record precise theorem/equation/page references, hypotheses and normalization conversions. Separate an already published exact formula, an immediate corollary of known results, and a genuinely additional proof. Unavailable sources remain unverified. Do not infer a result from its title or an AI summary.

## 2. Independent exact checks

Reproduce the inherited factorial data through p=997 if feasible; it contains 166 primes, with no reported mismatch. Independently compute B and the supersingular locus rather than defining c_p using the proposed factorial. Cross-check both elliptic-curve evaluations and modular-form polynomial divisibility at a useful bounded range.

Cover all four classes modulo 12, emphasizing p=13,37,61,73,97 and further p=1 mod 12 examples. At these primes neither j=0 nor j=1728 supplies a supersingular curve. Check non-rational supersingular j-values too, and model/differential independence. Record fields, coefficients, precision bounds, software versions and timings. Finite agreement is not a proof. If a mismatch occurs, certify it exactly and audit normalizations before declaring a counterexample.

## 3. Seek one uniform proof

Compare a few routes, then pursue the strongest rather than accumulating unexplained experiments:

- A modular-form or hypergeometric identity proving the displayed divisibility and retaining its scalar.
- Use constancy and evaluate on a suitable supersingular model for each p, explaining how the model and evaluation are chosen uniformly, including p=1 mod 12.
- A Frobenius/de Rham or crystalline calculation, or a Jacobi-sum/factorial evaluation, with every normalization and sign tracked.

These are suggestions, not assumed facts or required methods. A different short proof is preferable if available. Do not claim a uniform proof from the j=0 and j=1728 cases alone. A solution for some residue classes is a partial result and should be reported as such.

Pay particular attention to these traps:

- The symbol (6/p), rather than (-6/p), and all factors 12, 1728, and differential scalings.
- A squared identity cannot select one of its two roots.
- A has q-expansion 1 modulo p but vanishes at supersingular points: these facts concern different evaluations. Substituting A=0 into a cusp q-expansion argument is not legitimate without a modular-form identity.
- The main signed-residue theorem is already proved without this conjecture. Do not use the desired evaluation as an unacknowledged premise in its own proof.

## 4. Deliverables and stopping point

Return a concise verdict, a standalone proof note in TeX (and PDF if possible), exact reproducible code and outputs, and a source/priority assessment. State which facts are proved, imported, computational or conjectural. If unresolved, identify the strongest partial theorem and the exact missing sign evaluation; do not label the main paper incomplete because this optional conjecture remains open.

Provide a short suggested manuscript replacement only if the proof warrants it; do not edit the inherited manuscript. End with a portable result ZIP containing a README, commands, environment requirements, checksums and all new work. Do not broaden this assignment to higher Fricke levels, moonshine representation constructions or categorical Langlands.
