# Theorem 1.3 exact-evaluation benchmark, v1.0

Run date: 5 November 2026. Read REPORT.md for results and qualifications.
This is a separate experiment; the v1.9 manuscript and inherited ZIPs were not modified.

## Reproduce

On Linux x86-64 with GCC and Python 3.12:

```
python -m pip install python-flint==0.9.0
python benchmark.py
python verify_saved.py
python memory_probe.py factorial 1000003
python memory_probe.py baseline 1000003
python memory_probe.py theorem_cached 1000003
```

The first command may need a virtual environment. The benchmark script compiles
native.c into native.so, linking the FLINT shared library bundled with python-flint.
Native code uses public FLINT 3.6 nmod_poly ABI declarations reproduced locally
because the wheel has no development headers. The tested combination is
python-flint 0.9.0 / FLINT 3.6.0 / Linux x86-64 (64-bit unsigned long).
Do not assume the local declarations are portable to another ABI or platform.
The native arithmetic deliberately requires p < 2^31; benchmark.py enforces this.

The default primes are 101, 1009, 10007, 100003 and 1000003. Alternative prime
arguments may be supplied, but the CM-seed model generator must find an inert
seed in its fixed list, and must find nonspecial base-field models. It is not a
general-purpose arbitrary-prime curve generator. Inputs must be prime.

benchmark.py creates results.json and summary.csv. Each record stores the exact
field modulus, timed curve models, outputs, timings and sample variability.
Curve generation can visit a different walk on another run because FLINT's root
ordering is not fixed by the Python seed. verify_saved.py replays the exact saved
inputs independently of that sampling variation. Timings naturally vary by host.

## Files

- REPORT.md: interpretation, results and limitations.
- benchmark.py, native.c: all timing and input-generation code.
- verify_saved.py: exact replay, including an independent Hasse-derivative route.
- results.json: full timings and exact inputs/outputs.
- summary.csv: compact numeric results (microseconds per curve).
- memory_probe.py, memory.json: coarse separate-process RSS observations.
- verification.txt: recorded successful saved-input verification.
- SHA256SUMS.txt: hashes of this bundle's files other than the manifest itself.

No network access, PARI, SageMath or Magma is needed to reproduce these tests.
Those systems were not benchmarked. No claim of a globally fastest algorithm is made.

## Mathematical normalization

All curves are y^2=x^3+a*x+b with omega=dx/y, so
E4=-3a, E6=27b/2 and Delta=-(4a^3+27b^2)/256.
The conventional route uses B=3[x^(p-2)](x^3+ax+b)^((p-1)/2) on supersingular
curves. The independent replay also checks B=18b*H_a-4a^2*H_b, where
H=[x^(p-1)](x^3+ax+b)^((p-1)/2), i.e. B=12*SerreDerivative(H).
Neither conventional evaluator uses Theorem 1.3's factorial evaluation.

The target is B^((p-1)/2), not B itself. Both implementations receive a known
supersingular curve; input certification is outside the timed regions.
