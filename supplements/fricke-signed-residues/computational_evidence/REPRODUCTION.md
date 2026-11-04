# Reproduction commands

Python 3.12 was used for the bounded fresh rerun. Install `requirements.txt`
into an environment of your choice; the pinned versions are python-flint 0.9.0
and mpmath 1.3.0. Binary wheel availability varies by Python and operating system;
the package contains source code, not vendored dependency binaries.

Run commands from the supplement root, for example:

```text
python scripts/verify_evidence.py
python scripts/run_reproduction.py smoke
```

No symbolic-algebra system, Sage, PARI or LaTeX installation is required for
these computational suites. The optional historical PDF builder requires TeX,
but it is not used by the reproduction wrapper.

| Suite | Command | Scope |
| --- | --- | --- |
| Bounded fresh reproduction | `python scripts/run_reproduction.py smoke` | Five normalizations, 37 certificates, 13 Hecke cases, 50 Velu pairs, and level-one checks through p = 97 |
| Full certified tier | `python scripts/run_reproduction.py certified` | All 222 pairs, p <= 211; candidate-free recovery through p = 37 |
| Full derivative tier | `python scripts/run_reproduction.py kz` | 960 pairs, 223 <= p <= 1499 |
| Full Hecke checks | `python scripts/run_reproduction.py hecke` | 42 pairs, p <= 31 |
| Eta multipliers | `python scripts/run_reproduction.py eta-multiplier` | Original five-level checks and the separate character audit through ell = 47 |
| Full Velu sweep | `python scripts/run_reproduction.py velu` | 647 pairs, ell <= 47 and p <= 199 |
| Level-one constant | `python scripts/run_reproduction.py level1` | Constancy and factorial checks at 166 primes through p = 997 |
| All of the above full suites | `python scripts/run_reproduction.py all` | Long reproduction of the paper's reported sweeps |

These are substantive exact calculations. The archived instructions estimate
roughly 40–60 minutes for the certified tier, about 30 minutes for the derivative
tier, and about an hour for the full Velu sweep on their original machine.
These are historical estimates, not performance promises for your system.

By default every invocation makes a timestamped directory under `reproduced/`.
Alternatively use `--out /path/to/a/new/directory`. Existing directories are
refused. Outputs include per-case JSON, program logs, commands, package versions,
timings and comparisons with the recorded invariant results. Reproduction does
not edit anything under `packages/`.

For detailed algorithms and optional exploratory commands, consult the original
package READMEs. Running their scripts directly writes to their own `results/`
directories; use the wrapper or a separate copy if preserving the baseline.

The root checksum manifest is for this immutable release. Editing a bundled
file changes its hash. `.gitattributes` disables automatic text conversion in
this supplement to preserve bytes across Windows and Unix Git checkouts.
