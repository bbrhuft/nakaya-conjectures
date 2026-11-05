# Factorial constant: Conjecture 1.5

Read INPUT_PROVENANCE.md, SOURCE_GUIDE.md, then RESEARCH_PROMPT.md.
The manuscript is v1.4. The purpose is a proof attempt and priority check, not a larger numerical survey alone.

## Contents
- manuscript/: current standalone TeX and compiled PDF.
- evidence/: two original, unchanged research archives (full five-level context and eta/Frobenius audit).
- quick_start/: unchanged copies of the original signed-residue code tree and two relevant result files, for easy use without nested extraction.
- sources/: supplied Robert, Landweber and Kaneko--Zagier papers.
- FRESH_SMOKE_CHECK.txt: small reproduction run made while preparing this handoff.

## Reproduction
Install `python-flint==0.9.0` and `mpmath==1.3.0`.
Copy quick_start to new_work/reproduction before running: the inherited scripts overwrite files in ../results.
Run from that copied directory:

```sh
python code/level1_c_formula.py 997
python code/independent_check/level1_check.py 43
```

The second implementation enumerates a finite field by brute force: begin with a small bound. The first script checks constancy at every supersingular j and compares the factorial formula. Record future changes and output separately. The supplied p<=997 result covers 166 primes; finite checks are not a uniform proof.

Create new_work/ for your results. Preserve inherited files. SHA256SUMS.txt covers all other files in this handoff.
