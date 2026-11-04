# Fresh bounded reproduction

The wrapper was executed using Python 3.12.14, python-flint 0.9.0 and
mpmath 1.3.0. Exact commands, platform, timings and exit codes are recorded in
`smoke_run/RUN_METADATA.json`.

The run recomputed:

- coordinate normalizations at five levels through 300 terms;
- 37 certified reconstructions through p = 29;
- 13 Hecke-polynomial cases through p = 11;
- 50 Velu cases through p = 31, covering 794 cyclic kernels;
- 23 level-one constancy and 23 factorial cases through p = 97.

The wrapper's comparisons found no mismatches in the indicated invariant
outputs. Logs and fresh result JSON are preserved under `smoke_run/`. The code
used is the unchanged code in `packages/`; no dependencies or compiled caches
have been bundled. This rerun is distinct from the integrity/coverage checks
of the full archived sweeps in `ARCHIVE_VALIDATION.json`.

The large sweeps were not rerun during release preparation. The computations
support the stated finite ranges; the factorial formula remains conjectural.
