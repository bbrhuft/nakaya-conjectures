# Eta/Frobenius lemma audit — package v1.0 (3 November 2026)

Independent referee-style audit of **Theorem C** of the *Signed Weighted Residue Note* (package
`Signed_Weighted_Residue_v1_0`, 3 Nov 2026):

    (Δ(τ)/Δ(ℓτ))^{(p²−1)/24} = (ℓ/p)   at every geometric supersingular point of X_0(ℓ),  p ≥ 5, ℓ ≠ p prime,

together with its corollary that c(E) = E_{p+1}^{(p−1)/2}/Δ^{(p²−1)/24} is constant on the supersingular locus.
AI-assisted (Claude, Anthropic), at the request of D. Jordan; not refereed by a specialist. The inherited
package was **not modified** (its SHA-256 is recorded below for reference).

## Verdict in one paragraph

**Correct after specified repairs.** No error was found in the statement or in the proof strategy. The
repairs are foundational: (R1) the character of G = η(24ℓτ)/η(24τ) on Γ₀(576ℓ) is now derived completely from
the Petersson/Knopp closed form of the eta multiplier (and is the Kronecker character of Q(√ℓ), even and
quadratic, including ℓ = 2, 3); (R2) the diamond and Frobenius conventions are fixed with no ± signs
(⟨d⟩(E,ι) = (E, ι∘[d]), G∘⟨d⟩ = χ_ℓ(d) G, σ(x̃) = ⟨−p⁻¹⟩x̃); (R3) descent and integrality of G are proved via the
q-expansion principle at the Z[1/M]-rational cusp of the μ_M-model, the moduli description of D_ℓ as a unit on
Y₀(ℓ), the moduli definition of the degeneracy map δ (G²⁴ = δ*D_ℓ⁻¹) and normality of Y₁(M) over Z_(p) (monic
equation T²⁴ − δ*D_ℓ⁻¹); (R4) the Deuring model is chosen for E₁ because E₁ is supersingular, with a proof that
π_{p²} = p·u, u ∈ Aut(E), and without changing the geometric point; (R5) "Δ(τ)/Δ(ℓτ) at x" is defined as
ℓ¹²Δ(E,π*ω′)/Δ(E′,ω′). The note's claim that in the point convention G is only defined over Q(√ℓ) was verified
(it is correct and not needed). **Priority:** the signed identity is not in Ono's arXiv:2509.16175 **v2 (3 July
2026)**, which proves the (p²−1)/12 statement (Thm 1.2) and notes in Remark 4 that the (p²−1)/24 power can be −1
without giving a formula; the (p²−1)/12 statement for F_{p²}-isogenies is already in Baker (1998, §2) via
Gross–Landweber; the note's Lemma on B(E′) = ℓ B(E) is Robert (1980, Lemme 7) as quoted by Baker (Lemma 2.2).
No source stating the signed identity or the constancy of c(E) was found; Robert (1980) could not be read in full,
so this is not a proof of novelty.

## Layout

    AUDIT_REPORT.md / AUDIT_REPORT.pdf    the audit (verdict, complete proof with repairs, dependency table,
                                          literature comparison, computations, residual points, APA references)
    README.md                             this file
    replacement_section/
        eta_section_replacement.tex       drop-in replacement for Section 7 (\label{sec:eta}) of the note; comments
                                          list the edits to Imported Facts I4/I5 and the new bibliography entries
        standalone_wrapper.tex / .pdf     compile test with the note's preamble (pdflatex, TeX Live)
    code/
        eta_multiplier_audit.py           exact Dedekind-sum multiplier vs mpmath; Petersson closed form vs Dedekind
                                          sums; character of G on Γ₀(576ℓ) for ℓ ≤ 47 (all classes of d, both signs);
                                          Kronecker-character identification; the note's Lemma; negative control
        velu_sign_check.py                Vélu-based verification of Theorem C at every geometric supersingular point
                                          of X₀(ℓ) (ℓ ≤ 47, p ≤ 199), with Ono Thm 1.2/1.3, Robert/Baker, Baker,
                                          constancy of c, and Hauptmodul-normalisation cross-checks
        make_tables.py                    builds results/velu_sign_table.md
    results/
        eta_multiplier_audit.json         every matrix tested, with exact exponents
        velu_sign_checks.json             every (ℓ,p) pair, every check as a boolean, the set of values of D_ℓ^k
        velu_sign_run.log, velu_sign_table.md
    literature/
        sources_inspected.md              each source with the copy/version inspected and what was read
    SHA256SUMS.txt

## Reproduce

    python3 -m pip install python-flint==0.9.0 mpmath
    python3 code/eta_multiplier_audit.py                     # ~10 min (exact Dedekind sums for c up to ~8·10^4)
    python3 code/velu_sign_check.py 31 2,3,5,7,11,13         # seconds: 50 pairs, 794 points
    python3 code/velu_sign_check.py 199 2,3,5,7,11,13,17,19,23,29,31,37,41,43,47   # ~1 h: full sweep
    python3 code/make_tables.py
    cd replacement_section && pdflatex standalone_wrapper.tex && pdflatex standalone_wrapper.tex

The Vélu check uses no eta functions and no Hauptmodul: it enumerates supersingular j over F_{p²}, takes a
model with scalar p²-Frobenius, finds all ℓ+1 kernel polynomials from the ℓ-division polynomial, applies
Vélu's normalised formulas, and tests (Δ(E)/Δ(E′))^{(p²−1)/24} = (ℓ/p). It therefore tests the lemma at every
geometric point, including those over j = 0 and j = 1728, and at levels far outside {2,3,5,7,13}.

## Inherited package (unchanged)

    c6776e79-Signed_Weighted_Residue_v1_0.zip   SHA-256: d4b0ac057c84f344fb047dd7f70c591c334fa3adb7764c2118c10ad5c2e8b009
