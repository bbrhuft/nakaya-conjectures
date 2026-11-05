# Theorem 1.3: timed exact-evaluation benchmark

5 November 2026. Separate experiment based on the v1.9 theorem.

## Finding

The factorial theorem provides a practical speedup for the exact target B^h on known supersingular curves after caching the characteristic-dependent constant. The speedup grows with the characteristic against the tested coefficient-polynomial evaluators. This is not an evaluation of B itself and is not a supersingularity test. No proof of optimality or speed record against all available algorithms is claimed.

## Environment and protocol

AMD EPYC 9V74 (virtualized Linux x86-64); Python 3.12.14; python-flint 0.9.0, bundled FLINT 3.6.0; GCC 13.3.0 -O3. The main run was pinned to CPU 0. Each measurement was warmed up, automatically calibrated, and repeated in seven blocks; reported times are medians. Individual samples and IQRs are in results.json. Hardware sharing and clock variation remain possible.

There are 32 models per prime per field group. The Fp tests run in compiled C, with FLINT nmod_poly evaluation and shared native modular powering. Each Python call times a whole 32-model block. The Fp^2 tests use python-flint fq_default arithmetic and compiled fq_default_poly evaluation, with Python dispatch for the prefactors. Thus absolute times across the two field groups are not directly comparable. In particular, an optimized C implementation of extension-field arithmetic could reduce both extension-field timings.

## Independent baseline

Put h=(p-1)/2 and W=x^3+ax+b. For omega=dx/y, the conventional evaluator computes B=3[x^(p-2)]W^h, then B^h. Multinomial coefficients produce a univariate polynomial P of degree approximately p/12 satisfying B=3*a^r*b^s*P(a^3/b^2). Coefficient construction uses four FLINT factorial calls and batch inversion; it does not use the new factorial evaluation. This avoids constructing an entire general modular-form space or a high-precision characteristic-zero q-expansion.

Three Fp baselines were timed: compiled scalar FLINT polynomial evaluation; FLINT fast multipoint evaluation in blocks of 32; and scalar evaluation with reuse at repeated a^3/b^2 values within a block. Reuse is mathematically valid and does not use Theorem 1.3. It is the fastest of these three in this dataset. There is no persistent cache of evaluated values across timing blocks. Fp^2 measurements use scalar polynomial evaluation.

## Cached evaluation results

All entries below include formation of the discriminant or polynomial prefactors and the final powering. They exclude curve generation, supersingularity checks, field construction, polynomial construction and c_p setup. Units: microseconds per curve.

| p | Fp scalar baseline | Fp best tested baseline | Theorem, Fp | Speedup vs best | Fp^2 scalar baseline | Theorem, Fp^2 | Speedup |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 101 | 0.149 | 0.111 | 0.088 | 1.26x | 3.292 | 2.965 | 1.11x |
| 1,009 | 0.253 | 0.171 | 0.154 | 1.11x | 8.232 | 4.229 | 1.95x |
| 10,007 | 0.673 | 0.382 | 0.144 | 2.66x | 34.828 | 4.513 | 7.72x |
| 100,003 | 3.820 | 0.542 | 0.199 | 2.72x | 311.541 | 4.660 | 66.86x |
| 1,000,003 | 35.178 | 3.532 | 0.257 | 13.76x | 3767.718 | 5.061 | 744.47x |

## Setup costs

Fast-factorial entries are warm-library FLINT calls, not Python computation of the full integer factorial. The native-loop comparator multiplies residues in C and constant working space. Both include a single ctypes call. Legendre-symbol evaluation is not included in these factorial-only entries. Coefficient construction is one observed Python-orchestrated construction, not a statistically repeated optimized construction benchmark.

| p | FLINT fast factorial (ms) | Native factorial loop (ms) | Baseline coefficient construction (ms) | Native coefficient payload |
|---:|---:|---:|---:|---:|
| 101 | 0.0010 | 0.0005 | 0.032 | 72 bytes |
| 1,009 | 0.0029 | 0.0023 | 0.234 | 672 bytes |
| 10,007 | 0.0122 | 0.0201 | 0.782 | 6,680 bytes |
| 100,003 | 0.0626 | 0.2046 | 5.753 | 66,672 bytes |
| 1,000,003 | 0.3695 | 2.0934 | 60.713 | 666,672 bytes |

At p=1,000,003, the warm fast-factorial setup is 0.369 ms. Charging this setup only to the theorem and assuming the baseline polynomial is already prepared gives an approximate arithmetic break-even of 113 curve evaluations against the tested within-block reuse baseline, or 4 blocks of 32. This is a dataset-specific estimate, not a general bound: repeated-j structure and persistent caches change it. Against a single Fp^2 scalar polynomial evaluation, the measured factorial setup is already smaller than the per-curve saving.

A separate fresh-process factorial probe at the largest prime took 0.574 ms for its first fast-factorial call, compared with the warm-library value above. Importing Python/FLINT and process startup are excluded. Thus a claim of logarithmic total time for a new prime would be incorrect: the factorial setup remains a distinct cost.

## Dataset and correctness

Inputs start from inert reductions of class-number-one CM j-invariants and are propagated by explicit normalized 2-isogenies. Nonzero differential rescalings are then applied. The timed dataset excludes j=0 and j=1728 to avoid giving the conventional evaluator a special-value shortcut. All curve coefficients, field moduli and outputs are stored in results.json.

| p | Fp models | Distinct Fp j used | Extension models | Distinct j used in extension group |
|---:|---:|---:|---:|---:|
| 101 | 32 | 6 | 32 | 8 |
| 1,009 | 32 | 8 | 32 | 32 |
| 10,007 | 32 | 13 | 32 | 32 |
| 100,003 | 32 | 3 | 32 | 32 |
| 1,000,003 | 32 | 3 | 32 | 32 |

The extension group includes genuinely non-rational j-invariants and generally has extension-valued coefficients even for rational j, because the differential rescaling is in Fp^2. Counts are not claims of 32 distinct j-invariants in each base-field group.

- 320 timed model evaluations: independent Hasse invariant equals zero, coefficient evaluator agrees with the theorem, and exact replay agrees with saved outputs.
- Independent classical Hasse derivatives also recover B on all 320 saved models: B=18b*H_a-4a^2*H_b, equivalent to B=12*SerreDerivative(H). This strengthens the independence of the conventional route from Theorem 1.3.
- For p<=1009, explicit polynomial powering additionally checks Hasse and selected-coefficient extraction on eight models per prime.
- Exhaustive direct powering on all nonsingular short models at twelve primes 5<=p<=43 checks 630 supersingular models.
- Native FLINT batch checksums agree with scalar evaluations; individual evaluations are checked independently as above.

These are finite reproducible checks, not new proofs of Theorem 1.3.

## Memory

The largest native polynomial has 83,334 coefficients, occupying 666,672 bytes of coefficient payload. Construction and Python objects take additional memory. The cached theorem stores a bounded number of field elements per evaluation.

Fresh-process OS measurements at p=1,000,003 (coarse RSS, including runtime and allocator overhead):

| Probe | Initial RSS (KiB) | Final RSS (KiB) | Increase in peak RSS (KiB) |
|---|---:|---:|---:|
| factorial | 23,264 | 27,464 | 4,084 |
| baseline | 23,276 | 34,452 | 17,896 |
| theorem_cached | 27,564 | 27,568 | 0 |

For the cached-theorem probe, setup is performed before measuring the initial RSS. The arbitrary coefficients used in that allocation-only probe are not presented as supersingular correctness tests. These RSS deltas are observations, not precise algorithmic memory bounds or an allocation trace.

## Limits and interpretation

This establishes a practical evaluation advantage against the tested conventional routes. It does not establish the fastest possible evaluation of B^h. No SageMath, PARI/GP or Magma executable was available, so those systems were not timed. The experiment also does not benchmark a Bostan-Gaudry-Schost implementation for selected coefficients, every possible Hasse-derivative implementation, or specialized half-factorial/class-number algorithms.

The degree and cost of a conventional polynomial grow with p. The theorem replaces this with modular exponentiation once c_p is cached. FLINT is used to implement both approaches: the comparison concerns mathematical evaluation routes, not a claim that a new arithmetic library beats FLINT.

The Fp^2 ratios include generic extension-polynomial and Python-interface costs. They should not be projected onto optimized isogeny cryptography code. Batch sizes larger than 32, richer base-field samples, persistent caches and different processors can change the ranking. No cryptographic application, Cartier-Miller hybrid or manuscript revision is asserted.

## Provenance

Authoritative input: Fricke_Signed_Residues_Journal_v1_9.tex, Theorem 1.3. The independent coefficient route was present in Factorial_Conjecture_Result_v1_0/new_work/code/verify_factorial.py. Its historical conjecture terminology has no bearing on the current theorem status. The new benchmark code is separate and all inherited inputs remain unchanged.
