# Corollary 1.2 reconstruction benchmark, v1.0

Run date: 5 November 2026. Read REPORT.md first.

This package compares two exact algorithms for R_(N,p)(T), the rational function
representing T_N|U_p modulo p, at N=2,3,5,7,13. It is a separate experiment:
v1.9 of the manuscript and the original evidence archives were not modified.
Current status follows v1.9. Historical conjecture language inside the unchanged
inherited source copies is not the status of the current theorem.

## Reproduce

Requires Linux x86-64, GCC, Python 3.12 and python-flint 0.9.0 (FLINT 3.6.0 wheel).

```
python -m pip install python-flint==0.9.0
python benchmark.py
python verify_saved.py /absolute/path/to/Signed_Weighted_Residue_v1_0.zip
python memory_probe.py 2 1009 ss
python memory_probe.py 2 1009 q
python memory_probe.py 13 1009 ss
python memory_probe.py 13 1009 q
```

An isolated virtual environment is recommended. benchmark.py compiles the small
C bridge on import. It uses locally reproduced public FLINT 3.6 ABI declarations;
do not assume ABI portability to other FLINT releases/platforms. The bridge calls
FLINT's series inversion, compositional reversion and truncated composition.
No SageMath, PARI/GP or Magma installation is needed or was benchmarked.

The default experiment has 35 nonzero cases (five levels and seven primes) plus
the level-two zero cases p=5,7. For a small smoke run:

```
python benchmark.py 2:5 2:7 2:11 3:29 13:31
```

benchmark.py overwrites results.json and summary.csv with the requested run.
Back up the supplied results before running new timings. Sampling of roots can
vary because FLINT uses randomized factoring. Final rational functions are exact
and independent of root ordering. Exact supersingular data are saved in the
original field coordinates for replay.

verify_saved.py checks all saved data against fresh q-only reconstruction.
If the historical archive is supplied, it also verifies all overlapping outputs
against its original p^3-precision certificates. Without that archive, exact replay
still works and the script records that historical matching was unavailable.

## Outputs

- REPORT.md: results, methods, proof of comparison precision and qualifications.
- results.json: all raw timing samples, field moduli, supersingular T-values and
  effective indices, numerator and denominator coefficients.
- summary.csv: compact timings in milliseconds.
- verification.json / verification.txt: saved-data replay and historical matches.
- memory.json: separate-process coarse memory probes.
- INPUT_PROVENANCE.json / SHA256SUMS.txt: input identities and bundle hashes.

The two Python files under inherited/ are unchanged copies from the original
Signed_Weighted_Residue_v1_0 package. Only wr_core.py is imported by the timed
driver. wr_pairs.py is retained to document the original p^3 verifier, which is
not the comparator timed here. No original research evidence is overwritten.
