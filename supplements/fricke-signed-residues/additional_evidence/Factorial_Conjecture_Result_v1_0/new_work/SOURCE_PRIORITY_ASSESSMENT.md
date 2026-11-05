# Source audit and priority assessment

Every statement below was read in the original text: the supplied PDFs (Robert and Landweber by text extraction, Kaneko–Zagier by OCR) or the author's copy of Baker. Page numbers are the printed journal pages. Anything not read is marked **unverified**.

## 1. What each source actually contains, and what may be imported

### Baker, A. (1998). *A supersingular congruence for modular forms.* Acta Arith. 86(1), 91–100
- **Thm 1.4 (p. 94).** B^{p−1} ≡ −(−1/p) Δ^{(p²−1)/12} mod (p, A), with A = E_{p−1}, B = E_{p+1} normalized to constant term 1 and Δ = (Q³−R²)/1728. The same paper gives an elliptic-curve version over F_{p^d}. This is exactly the **square** of the conjectured identity. The normalization matches the manuscript.
- **Prop 1.3 (p. 93).** Mod p, B ≡ ∂A and ∂B ≡ −QA. Baker's ∂ (∂Q = −4R, ∂R = −6Q²) is 12 times the Serre derivative used in the note, so B = 12∂A in the note's normalization.
- **Thm 1.2.** The irreducible factors of A mod p are Q, R, Q³ − αΔ and Q⁶ + βΔQ³ + γΔ², each to multiplicity one. The note imports this squarefreeness for Lemma 2.2.
- **Lemma 2.2.** Quotes Robert's isogeny identity.
- **(6.1), p. 99.** ss_p′(α)^{p−1} = (−1)^{ε−1} α^{2(δ−1)(p−1)/3} (α−1728)^{(ε−1)(p−1)/2}, with p = 12m_p + 4δ + 6ε + 1. This is KZ (40). The note's Corollary 4.1 is a signed square root of it, and agrees with (6.1) after squaring.
- **Method.** Baker reduces to curves over F_p with CM by Q(√−p) and uses Gross–Landweber.
- The paper contains no half-exponent statement, no ((p−1)/2)! and no sign selection.

### Robert, G. (1980). *Congruences entre séries d'Eisenstein, dans le cas supersingulier.* Invent. Math. 61, 103–158
- **Théorème B (p. 106).** E_{p+1}(x′)/E_{p+1}(x) ≡ deg π (mod pN) for a normalized prime-to-p isogeny between supersingular pairs.
- **§3.3, eq. (19) and Lemme 7 (p. 124).** B(E/C, π_*ω) − ℓB(E,ω) = −12A(E,ω)·Σ…, so B(E/C) = ℓ·B(E) when A = 0. This is the manuscript's citation, and it is correct.
- **Théorème 2 (§2.5, p. 119)** is "Serre's functional equation" (Serre's letter of 13/6/78). For even k with 4 ≤ k ≤ p−3 and k̄ = p+1−k, the forms (p−k)!·G_k^p and (E_{p+1}/12)^{k−1}·G_{k̄} have the same image in W_{pk} = M/(p, E_{p−1}). The proof uses θ^{k−1} and the leading coefficient ∏(k̄+i) ≡ −1/(p−k)!. **This is the same mechanism as the note**, applied there to Eisenstein series of even weight at level 1. At the self-dual weight k = k̄ = (p+1)/2, which is even only when p ≡ 3 (mod 4), it yields h!·G_{(p+1)/2}^{p−1} ≡ (B/12)^h. That would still leave a sign evaluation of G_{(p+1)/2}^{p−1}/Δ^k. Robert does not do this, and neither η nor c_p appears.
- **Main theorem (Thm A/Thm 8)** concerns modified Eisenstein series of weights k, k*. It contains no signed evaluation of B^h/Δ^k.

### Landweber, P. S. (1988). *Supersingular elliptic curves and congruences for Legendre polynomials.* LNM 1326, 69–93
- **Thm 2 (Gross).** u₂ = (−1/p) Δ^{(p²−1)/12} for supersingular curves.
- **Thm 3 (p. 72).** For y² = 4∏(x−e_i) supersingular, Δ^{(p²−1)/24} = (e_α−e_β)^{(p²−1)/4}. This is a half-exponent result for Δ alone.
- **Thm 1 (Chudnovsky).** Legendre-polynomial congruences for V₁, V₂.
- The paper says nothing about E_{p+1}^{(p−1)/2}. Combined with the note's theorem it gives E_{p+1}(E, dx/y)^h = (6/p)·h!·(e_α−e_β)^{(p²−1)/4}.

### Kaneko, M. & Zagier, D. (1998). *Supersingular j-invariants, hypergeometric series, and Atkin's orthogonal polynomials.* AMS/IP Stud. Adv. Math. 7, 97–126
- **§3.** E_{p−1} = Δ^m E₄^δ E₆^ε ss̃_p(j). Imported for Lemma 2.2 and Corollary 4.1.
- **§10 (pp. 123–125).** Properties (a)–(d) of the residues of ψ_p = j|U_p. They state de Shalit's conjectural formula (39) and the equivalent (40) for ss_p′(j)^{p−1}, both squared. They also say: "if p ≡ −1 (mod 12), then (40) says simply that ss_p′(j) ∈ F_p … It would be nice to have an elementary proof." The note's Corollary 4.1 gives a signed refinement and this fact as a consequence.

### Ono, K. (2025). arXiv:2509.16175
- Thm 1.2 says the supersingular values of Δ(ℓτ)/Δ(τ) raised to the power (p²−1)/12 equal 1. Remark 4 says the (p²−1)/24 power can be −1. Neither E_{p+1}^{(p−1)/2} nor factorials appear. This was checked through a web summary and the manuscript's remark; the source was not read in full.

### Other sources found by search (checked through summaries of the full text)
- Bringmann–Guerzhoy–Kane–Mertens–Rolen, arXiv:2606.14020 (2026). Not relevant.
- Ringeling, arXiv:2211.01114 (2022). Studies forms congruent to theta series at weight (p+1)/2. No η^{p+1}, no E_{p+1} and no factorial.
- arXiv:2608.21198 (2026), on Legendre polynomials and CM. Nothing on H′ at roots.

### Not checked (unverified)
- de Shalit, E. (1994), *Kronecker's polynomial, supersingular elliptic curves, and p-adic periods of modular curves*. Known only through KZ §10. According to KZ it proves (39) for p ≡ 1 mod 4, and up to sign for p ≡ 3 mod 4. That is the squared quantity.
- Serre's 1978 letter to Robert, the homotopy-theory literature on "v₂^{1/2}", and Gross's unpublished work.

## 2. Classification

| Category | Finding |
|---|---|
| Already published exact formula for the sign of c_p | **None found** in the sources above |
| Immediate corollary of known results | **No.** Known results (Baker, KZ (40), de Shalit (39), Landweber Thm 3) give only c_p² or half-exponents of Δ alone. Choosing the root requires new input. |
| Genuinely additional proof | **Yes.** The note: θ^{(p−1)/2} applied to η^{p+1} on Γ(12) |
| Closest precedent for the method | Robert (1980), Thm 2 (Serre's functional equation); Wilton's congruence for τ(n) mod 23 (the case p = 23) |

**Assessment.** The theorem looks new relative to the literature examined. Its proof is short and uses only standard tools, so the result may be folklore among specialists in mod-p modular forms or elliptic cohomology. Before claiming priority, check de Shalit 1994, the elliptic-cohomology literature (Baker's later papers, Laures) and ask an expert.

## 3. Normalization audit (the "traps")
- **(6/p) versus (−6/p).** The proof produces (24/p) = (6/p) from the exponent 1/24 of η. Exact data through p = 997 confirm (6/p); replacing it by −(6/p) fails at every p (negative control).
- **Factors 12 and 1728.** Δ = (E₄³−E₆²)/1728 = η²⁴. The factor 12^h ≡ (3/p) from B/12 cancels χ₁₂(p) = (3/p).
- **Differential scaling.** Both B^h and Δ^k have weight (p²−1)/2. Random rescalings by u ∈ F_{p²}^× were tested.
- **Inherited code normalization.** E₄ = 12g₂, E₆ = −216g₃ and Δ = g₂³ − 27g₃² for y² = 4x³ − g₂x − g₃ with ω = dx/y. This is consistent with the above.
- **Squared identity.** The proof never takes a square root. Baker's congruence is recovered by squaring and Wilson's theorem.
- **A ≡ 1 versus A = 0.** These are used in different places. The q-expansion principle is applied to an identity between forms of equal weight that keeps A^{(p+1)/2}, and A = 0 is substituted only afterwards, at the points.
- **Circularity.** The proof does not use the manuscript's signed-residue theorem, Baker's congruence or constancy.
