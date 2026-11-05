# Verdict: Conjecture 1.5 is proved for every prime p ≥ 5

**Statement.** Let p ≥ 5, h = (p−1)/2 and k = (p²−1)/24. Then

    E_{p+1}^{(p−1)/2} ≡ (6/p)·((p−1)/2)!·Δ^{(p²−1)/24}   (mod p, E_{p−1})   in Z_(p)[E4,E6].

Equivalently, c(E) = B(E,ω)^h/Δ(E,ω)^k equals (6/p)·h! for every supersingular E over F̄_p and every nonzero invariant differential ω. This holds in all four classes mod 12, including p ≡ 1 (mod 12), and at non-rational supersingular j. The note proves the equivalence of the two forms, including the factors E4 and E6 at j = 0 and j = 1728 (Lemma 2.2).

**Type of result.** This is a uniform proof, not a partial one. It needs none of the manuscript's constancy result (Cor. 1.4), Baker's congruence, isogeny-graph connectivity, the eta–Frobenius theorem (Thm 1.3) or CM evaluations. All of these follow from it except Robert's isogeny identity, which is still used to deduce Thm 1.3. No counterexample exists.

**Idea, in four lines.** F = η^{p+1} is a weight-(p+1)/2 form on Γ(12), and F ≡ η(τ)η(pτ) mod p. Its quadratic twist is therefore explicit:

    θ^h F = (6/p)(A^{(p+1)/2} F − χ₁₂(p) F^p)

as mod-p forms, by the q-expansion principle. Iterating θf = A∂f + (w/12)Bf shows that θ^h F ≡ −(1/h!)(B/12)^h F mod A. At a supersingular point A = 0 and F ≠ 0, and F^{p−1} = Δ^k. Hence B^h = (6/p)·χ₁₂(p)·12^h·h!·Δ^k = (6/p)·h!·Δ^k, because χ₁₂(p)·12^h = (3/p)² = 1.

## What is proved, imported, computational or conjectural

| Item | Status |
|---|---|
| Theorem (Conjecture 1.5), all p ≥ 5 | **Proved** (note §3), given the standard inputs below |
| Equivalence of the point form and the divisibility form (j = 0, 1728) | **Proved** (Lemma 2.2), using squarefreeness of A (imported) |
| η² ∈ M₁(Γ(12)) | **Proved** from the Petersson multiplier formula; also checked numerically |
| Constancy of c, Baker's congruence, eta character (manuscript Thm 1.3) | **Corollaries**; Robert's isogeny identity is imported for the last |
| Signed Kaneko–Zagier (40); B = 3·[x^{p−2}](x³+ax+b)^h | **Proved** here and checked exactly |
| Legendre/Deuring form H′(λ)^h = h!·2^{−(p²−1)/3}·(λ(1−λ))^{(p−1)(p−5)/12} | Classical Γ(2) theta identities **imported**; checked exactly for p ≤ 997 |
| Imported inputs | q-expansion principle at level Γ(12) (Katz 1973, §1.6); A = Hasse invariant with simple zeros (Katz 1973 §2.1; Baker 1998 Thm 1.2; Kaneko–Zagier 1998); Kummer congruence E_{p+1} ≡ E₂; Serre derivative; Euler's pentagonal identity |
| Computational | All 166 primes 5 ≤ p ≤ 997 agree along four independent exact routes, and a negative control fails |
| Conjectural content remaining | **None** for Conjecture 1.5 |

## Caveats

- The proof has been checked by the author of this note and by computation. It has **not** been refereed by an independent human expert, and should be before publication.
- **Priority is not established.** No published signed evaluation was found in Baker 1998, Robert 1980, Landweber 1988, Kaneko–Zagier 1998, Ono 2025 or several recent arXiv papers. De Shalit 1994 was not accessible. The mechanism is Serre's functional equation (Robert 1980, Théorème 2) moved to the self-dual weight (p+1)/2 via η^{p+1}, so specialists may know the result. See `SOURCE_PRIORITY_ASSESSMENT.md`.
