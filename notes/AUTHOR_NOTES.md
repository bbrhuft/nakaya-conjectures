# Notes for the human author

## Status and contribution

The manuscript is an eighteen-page journal-style draft before any venue-specific reformatting, covering both Nakaya's Conjecture 5 (linear factors) and Conjecture 6 (degree); the two were merged into one article on 27 October 2026, and the title was changed to "Nakaya's conjectures on the linear factors and degree of Fricke supersingular polynomials". The author block gives David Jordan, Maynooth University. The mathematical contribution is framed as an explicit uniform deduction of Nakaya's formula from classical modular-curve geometry, Aricheta's theorem, and the fixed-point class-number formula. The arbitrary-level statement is made precise, but is itself a formal consequence of older general results. Beneish–Wen's Theorem 6.5 already implies the same geometric identity for squarefree total levels Np after Riemann–Hurwitz, although their preprint does not mention Nakaya. Morton's E7 paper (Ramanujan J. 63 (2024), Section 3) had reduced the N = 7 case to his Conjectures 1–3, proving Conjecture 1 as Theorem A; the article settles N = 7 unconditionally, without proving his Conjectures 2–3. A novelty assessment by a specialist is essential before presenting the article as original research. No priority claim is made.

The proof uses the single-involution simplification supplied in the revision instructions. The cyclic-stabilizer explanation remains in the lifting lemma, where it is required. The flat proper quotient and structure-sheaf argument replaces the earlier resolution discussion. The article explicitly handles rational quotient points whose lifts are swapped by Frobenius.

The main 827-case verification passed, as did the supplementary 60-case level-two run. An extended run under PARI 2.17.2 using the stored relations (verification/run_extended.py) passed all 4,201 pairs with p ≤ 2000. Corollary 5.2 (all odd prime levels) was checked independently by verification/verify_general.gp: 526 pairs at 21 levels, 296 of them at 16 levels outside Nakaya's set, no mismatches. The title stays focused on Nakaya's conjectures rather than advertising the general-level results. The worked example N=11, p=13 was also checked by Atkin–Lehner traces on the characteristic-zero cusp-form space. These computations verify the requested finite range and the implementation; they are not a replacement for the geometric proof.

## Citation sign-off

Read SOURCE_AUDIT.md before submission. Katz–Mazur Theorem 13.1.3 has now been checked on the original page (p. 390). The proof itself cites the inspected original Deligne–Rapoport theorem directly. Morton's E7 paper is cited as Ramanujan Journal 63 (2024), 339–385, with theorem, conjecture, section and page numbers checked against the published article (27 October 2026); they agree with arXiv:2206.09801v5, so the separate arXiv citation was dropped. Aricheta, Ogg and Beneish–Wen were re-checked against the primary texts in a second pass (26 October 2026).

Aricheta's complete hypotheses and conclusion have been restated faithfully, with a short verbatim definition, rather than reproducing the entire theorem as a long quotation. All uses are of quotient-curve geometric points, not of rational lifts. This is explicit in the source audit.

The statement about Morton's finer E7 formulas is limited to what this article does not prove and what the published abstract calls conjectural. It does not assert that a comprehensive later-literature search has established their current open status.

## Human review, authorship, and AI disclosure

The disclosure in the manuscript records substantive OpenAI ChatGPT/Codex assistance with mathematical exposition, literature retrieval, code preparation and execution, and editing, and Anthropic Claude assistance with source checking, the extended verification run, and copy-editing. It does not pretend that the assistance was confined to grammar. AI is not an author. A human author must review the sources, take responsibility for every argument and calculation, confirm the final text, and supply their actual details. Those approvals have not been performed by this workflow.

A number theorist with experience in modular curves should read the draft. In particular, have the reader independently check the arbitrary-level coarse-model argument, the Hauptmodul descent, the normalization conventions, and the prior-art assessment. Coauthorship should reflect an actual scholarly contribution, rather than being offered solely as a substitute for review.

Elsevier's current official journal policy requires disclosure of substantive AI use and human responsibility. Its policy was checked on 26 October 2026: https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals . It permits AI support for literature synthesis and organization under human oversight, so the disclosure should accurately describe the assistance actually used.

The Ramanujan Journal's current official instructions say that LLMs do not satisfy authorship criteria, substantive use should be documented, and final text requires human accountability: https://link.springer.com/journal/11139/submission-guidelines . Its copy-editing exemption does not describe the assistance used here. Its instructions also ask for 150–250 abstract words, 4–6 keywords, numeric citations, and DOI links where available; adapt the final file to the selected journal's exact template. Confirm competing-interest, funding, contribution, and data-availability statements with the actual authors instead of inventing them.

After the human review is genuinely complete, the author may adapt the publisher's standard declaration to say that they reviewed and edited the AI-assisted material and accept full responsibility. Do not assert completed human review before it has occurred.

## Possible venues

Journal of Number Theory has the closest direct publication history for Nakaya and Morton's E5 work. The Ramanujan Journal has the published E7 paper and a related readership. Research in Number Theory and International Journal of Number Theory are also plausible subjects for a presubmission assessment. Proceedings of the American Mathematical Society would generally require a crisp original contribution, so it should not be selected on the basis of length alone. These are subject-fit suggestions, not predictions of acceptance. The prior-art overlap may mean that the appropriate form is an expository note or a short clarification rather than a new-research article.

Before choosing a venue, settle whether the explicit all-level deduction is already recorded elsewhere and how much originality the editor requires. A presubmission enquiry can describe the exact contribution without claiming a new Frobenius mechanism. No external submission, publication, or message has been sent.

## Revision of 27 October 2026 (ChatGPT review)

- Remark 5.3 now applies formula (4.1) only to squarefree composite N; other levels need the full fixed-point formula (Im–Jeon–Kim, Proposition 2.1). Theorem 1.1 itself holds for every N prime to p.
- New Lemma 3.2 derives Aricheta's identity g(B) = g(X) + (D − λ)/2 directly from the quotient model, with attribution kept. The former Lemmas 3.2 and 3.3 are now 3.3 and 3.4.
- Shorter abstract; previous work condensed, with the Morton N = 7 detail in Remark 7.3.
- New Appendix A.1 with Table 1 (command, PARI version, reconstructed or stored Hauptmoduli, expected output for each survey). Later appendix subsections moved down by one; the PARI 2.17.2 note is now A.5 and is worded as an observed failure, not a claimed PARI defect.
- New code-and-data availability statement giving the repository URL, recommending a tagged release or commit, and stating that no DOI has been assigned.
- The AI declaration now says "the author".

Open: the second implementation (`conjecture6_second_implementation/`) rebuilds the Hauptmoduli and was run only under PARI 2.15.4; it probably meets the same 2.17 failure but has not been tested there. No tagged release exists yet.

## Revision of 27 October 2026 (literature review)

Section 3.1 was expanded after reading Furumoto–Hasegawa, Xue, Accola and Padurariu–Park–Voight directly (see SOURCE_AUDIT.md, third pass). Xue (2009, Theorem 2) already proves the level-one case of Theorem 1.1 by the same route; this is now credited. Aricheta is credited for the quadratic-factor count in the abstract, introduction and Corollary 6.3. Contact details moved to the end of the paper.

## Revision of 27 October 2026 (before arXiv)

Following a review by Google Gemini, Appendix A was condensed: the former survey table (commands and expected outputs) and the reproduction instructions moved to the README, A.1 is now a short "Software and scope" paragraph, and the PARI/GP 2.17.2 diagnosis moved to the README, leaving a one-paragraph "Extended check" (A.4). Later appendix subsections moved up one; the representative-checks table is now Table 1. One sentence in "Relation to previous work" contrasts Morton's level-by-level proofs (Hasse invariants of E5, E7; explicit relations between j and j_N*) with the uniform argument. The AI declaration was left unchanged, by the author's decision. The PDF in paper/ was compiled here with pdflatex from the same source the author downloaded.

## Conjecture 6 (added in the merged version)

The degree formula follows from Lemma 3.1 (D = 1 + g(X_0(Np)/<w_N>) in genus zero), Riemann-Hurwitz, the genus formula for X_0(Np), and the fixed-point counts of w_N (formula (4.1) for N >= 5; the exceptional Q = 3 term of Im-Jeon-Kim, Proposition 2.1, for N = 3). Nakaya proved N = 3; Morton proved N = 5 (JNT 227 (2021), Section 7) and N = 7 (IJNT 19 (2023), Section 3). Proposition 6.2 gives the total count at every prime level N >= 5, and Corollary 6.3 the factorization type over F_p. The degree checks are in verification/c6_degrees.py, verification/c6_direct.gp and verification/conjecture6_second_implementation/; all agreed (see README).

## Revision of 29 October 2026 (Section 7 scrutiny; release v1.2)

A source check of Section 7 against Morton's proofs, a step-by-step review of the argument, and a check of the Conjecture 4 package (see SOURCE_AUDIT.md, fourth pass) led to these changes:

- Abstract: the Conjecture 4 sentence now refers to the double cover X_0(N) → X_0(N)^+, not "the same model".
- Proof of Proposition 7.1: Deuring's criterion, as stated by Morton, replaces the citation of Beneish–Wen, Proposition 3.16; a clause justifies that b_N is monic (Nakaya states this only for a_N).
- Remark 6.4: credits Morton (JNT 218, Theorem 6.1) and Hajouji (Proposition 2.9(1), Section 2.5) for Question 1; the argument here is presented as another route.
- Remark 8.4: credits Morton's Theorem 6 for Conjecture 2, and Hajouji's Table 1 and its observed symmetry, which Corollary 6.3 explains for N, p ≥ 5; reports the 105-pair agreement.
- Appendix A.7: the degree at N = 2 is compared with the value from Proposition 7.1, not Corollary 1.3; the 246 flagged pairs are split into 239 and 7; the discriminant of E_N has no prime factor other than 2, 3 and N.
- Remarks 6.4 and 8.4 use 𝔖 instead of S. The bibliography adds Hajouji and states that Morton's Fricke-paper numbers are from arXiv v1.
- AI declaration: ChatGPT-6.1 Sol is credited with investigating and drafting Section 7; Claude with the comparison with Hajouji's table.
- The two \newpage commands were removed, since the new text left nearly empty pages.

Remark numbers in earlier entries above (for example "Remark 7.3") refer to the numbering before Section 7 was added; that remark is now 8.3.


## Revision of 14 November 2026 (release v1.3)

Changes to the manuscript (now 24 pages):

- Introduction: defines Nakaya's supersingular polynomial explicitly from R_N; adds a "Contribution" paragraph and a separate "Relation to previous work" paragraph; states that Theorem 1.1 needs no squarefree hypothesis on N.
- Section 2: explains the two uses of the hypothesis p ≥ 5 (tame averaging, and automorphism groups at j = 0 = 1728 in characteristic 2 and 3).
- Lemma 3.1: cites Bars and Dalal (J. Algebra 672 (2025), Lemma 30) for the same total-count identity.
- Lemma 3.3: the cyclic-stabilizer argument is spelled out.
- Proposition 5.1: restructured into three parts (integral coordinate; norm identity Norm(X − j) = R_N over Z_(p); identification of the roots), with the integrality of the Fourier coefficients proved directly rather than taken from moonshine.
- Corollary 8.3 (new): Morton's Conjectures 2 and 3 for the Tate normal form E_7, deduced from Corollary 1.2 at N = 7 and Morton's Theorem 1, Theorem A and Section 3. It replaces the former Remark 8.3 ("What the count does not determine"); Remark 8.4 now explains why the finer counts follow at level seven. This supersedes the statement under "Status and contribution" above that the article does not prove Morton's Conjectures 2–3.
- Remark 8.5 (new): the two terms of the linear-factor formula as rational points lifting to X_0(N) and points with an N-isogeny to the Frobenius conjugate (Chenu–Smith, Arpin). Hajouji's Table 1 remark is now 8.6.
- Appendix A condensed into four subsections; the general-level check is now A.3 and the survey summary A.4.
- Code and data availability: cites the Zenodo concept DOI 10.5281/zenodo.23698276 instead of a version DOI.
- AI declaration: adds Gemini Hydrogen and Claude Fable 5.2.

The verification code and results are unchanged from v1.2.

### Open source checks (moved from comments in the .tex)

- Theorem 1.1 is stated for every N prime to p, not only squarefree N. Confirm that Deligne–Rapoport VI 6.9 and Ribet Proposition 3.8 are stated in that generality; only prime N is needed for the corollaries.
- Corollary 8.3: the pinpoint references to Morton's E_7 paper (Theorem 1; Theorem A; Section 3, Lemma 1 and Proposition 1; Conjectures 2 and 3 in Section 2) were checked against arXiv:2206.09801, not the published version.
- Corollary 8.3 uses Morton's Section 3, Proposition 1 as stated; parts of its proof there are brief. A specialist should confirm that it is unconditional. A Google Gemini Hydrogen review (November 2026) asserts that it is, but that assertion has not been checked against Morton's proof.
- Remark 8.5: the statements of Arpin's paper relevant to it (reported as Theorem 4.13 and Proposition 5.3) have not been checked against the source; add pinpoint references once they are.
- Morton's Fricke-group paper (IJNT 19 (2023)): theorem and section numbers are taken from arXiv:2105.14532v1; check them against the published version before submission.

### Zenodo labelling of v1.2

The GitHub tag and release for v1.2 are correctly named, but the Zenodo record doi:10.5281/zenodo.23778165 was published with the version label "v5" by mistake; the label was corrected to "v1.2" on Zenodo on 14 November 2026 (the DOI and files are unchanged). From v1.3, `.zenodo.json` sets the version explicitly.
