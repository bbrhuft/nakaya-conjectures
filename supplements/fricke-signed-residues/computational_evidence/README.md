# Computational evidence for the Fricke signed-residue paper

This is the repository-ready computational supplement to David Jordan's
*Supersingular poles and signed residues of prime-level Fricke Hauptmoduln*,
journal draft v1.3 (`Fricke_Signed_Residues_Journal_v1_3.tex`). It supplies the
two evidence packages named in the paper, their original recorded outputs,
source code, integrity checks and safe reproduction commands.

The manuscript and its PDF should be uploaded separately. `PROVENANCE.json`
records the TeX hash against which this supplement was assembled.

## Start here

1. Read `CLAIMS_AND_FILES.md` for the correspondence with the paper.
2. Run `python scripts/verify_evidence.py`. This needs only Python's standard
   library: it verifies release hashes and checks coverage, totals and recorded
   outcomes against the paper. It does **not** rerun the mathematical algorithms.
3. To reproduce calculations, use Python 3.12 and install the two dependencies:

   ```text
   python -m pip install -r requirements.txt
   python scripts/run_reproduction.py smoke
   ```

The wrapper runs computations in new working copies under `reproduced/`. It
refuses to overwrite an existing output directory and leaves the archived
evidence intact. After each run it compares invariant outputs with the archive
and writes logs, dependency versions and `RUN_METADATA.json`.

For a virtual environment, use `python -m venv .venv`, then activate it with
`.venv\Scripts\Activate.ps1` in Windows PowerShell or `source .venv/bin/activate`
on Linux/macOS. Commands may require `python3` instead of `python` on Unix.

## What is included

```text
packages/
  Signed_Weighted_Residue_v1_0/
    code/                 original computational implementations
    results/certified/    222 exact reconstruction records, p <= 211
    results/kz/           960 derivative-formula checks, 223 <= p <= 1499
    results/              auxiliary checks, tables, logs and aggregate files
    note/                 HISTORICAL research note, superseded by journal draft
  Eta_Frobenius_Lemma_Audit_v1_0/
    code/                 independent implementation route using Velu quotients
    results/              647 (ell,p) pairs, 127541 cyclic-kernel checks
    AUDIT_REPORT.*        HISTORICAL AI-assisted audit, retained for provenance
    replacement_section/  HISTORICAL proof replacement, subsequently revised
scripts/
  verify_evidence.py       standard-library integrity and recorded-output checker
  run_reproduction.py      non-destructive driver for fresh calculations
verification/
  ARCHIVE_VALIDATION.json  recomputed inventory and recorded-result checks
  paper_table.csv          table totals recomputed from the individual records
  smoke_run/               bounded fresh rerun: metadata, logs and result JSON
CLAIMS_AND_FILES.md
REPRODUCTION.md
PROVENANCE.json
GITHUB_UPLOAD.md
requirements.txt
SHA256SUMS.txt
```

All files inside `packages/` were extracted byte-for-byte from the two supplied
original ZIPs. No original code, numerical record, note or audit text was edited.
No third-party journal-paper PDFs or app deployment files are included.

## Evidence levels and status

| Computation | Recorded range | What it establishes or checks |
| --- | --- | --- |
| Certified q-expansion reconstruction | 222 admissible (N,p) pairs, p <= 211 | Exact rational-function identities using the paper's a priori denominator bound and finite certificate; includes 6246 thin values, 4696 non-rational |
| Kaneko-Zagier derivative route | 960 pairs, 223 <= p <= 1499 | Signed products computed using the derivative lemma; not an independent q-expansion reconstruction |
| Hecke polynomial modulo p^2 | 42 pairs, p <= 31 | Kronecker congruence, symmetry and residue criterion at every element of F_p^2 |
| Normalized Velu quotients | 647 pairs, ell <= 47 and p <= 199 | 127541 cyclic-kernel checks of the eta/Frobenius sign, plus auxiliary checks |
| Factorial formula for c_p | 166 primes, 5 <= p <= 997 | Finite evidence for Conjecture 1.5; not a proof |

The five residue levels are N = 2,3,5,7,13; primes satisfy p >= 5 and p != N.
Kernel checks are counted on chosen supersingular curve representatives, not as
distinct coarse moduli points. Residues, polynomial coefficients and field
arithmetic are exact; the multiplier scripts also include explicitly labelled
high-precision numerical sanity checks.

The original JSON key `matches_conjecture` is historical: it records the signed
residue product studied before the journal draft promoted that statement to a
theorem. This is distinct from the **still conjectural** factorial evaluation of
c_p. Similarly, exploratory level-11 files are retained but lie outside the
five-level residue theorem in this paper.

## What was verified when preparing this release

The archived coverage and totals were recomputed from all primary records and
agree with the manuscript. A fresh bounded rerun used Python 3.12,
python-flint 0.9.0 and mpmath 1.3.0:

- all five normalization checks through 300 terms;
- 37 certified pairs through p = 29;
- 13 Hecke-polynomial pairs through p = 11;
- 50 Velu pairs through p = 31, involving 794 cyclic kernels;
- 23 level-one constancy checks and 23 factorial checks through p = 97.

The compared invariant outputs agree with the archived results. Fresh logs and
outputs are in `verification/smoke_run/`. The large sweeps were **not** rerun
while packaging; their original outputs and the full reproduction code are
included. These are AI-assisted computations and checks, not independent human
specialist refereeing.

## Provenance and checksum detail

`SHA256SUMS.txt` at this release's root covers all bundled files except itself.
The original signed-residue manifest verifies all 1220 entries. The eta audit's
original manifest has one invalid self-entry for `SHA256SUMS.txt`; its other
15 listed files verify. This self-entry is documented and skipped only by the
original-manifest check. The new release manifest independently covers the
original manifest's bytes too. The inherited files were not silently repaired.

Original research notes and audit reports are preserved as historical material.
Their proof discussions, terminology, source-access statements and priority
comments may predate repairs in journal draft v1.3. Use the journal manuscript
as the mathematical exposition; these historical documents do not supersede it.

This supplement contains no new licence declaration. Retain the repository's
existing licensing arrangements. See `GITHUB_UPLOAD.md` for an upload checklist.
