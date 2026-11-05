# Corollary 1.2: reconstruction and full-cost benchmarks

5 November 2026. Based on the authoritative v1.9 manuscript.

## Main finding

The reconstruction formula gives a practical speedup against the tested q-expansion routes. Acquisition costs matter: the supersingular method loses at the smallest tested characteristics, then wins as p increases. With p=1009, its complete calculation is 19.4-25.1 times faster across the five tested levels. With the supersingular data supplied, its reconstruction is 64.7-107.9 times faster than a q-expansion control that is already supplied the thin denominator. These are implementation-specific measurements, not global optimality claims.

The scope is the five eta-coordinate levels N=2,3,5,7,13, not all fifteen levels covered by Theorem 1.1. Seven primes were tested at each level: 11,29,59,101,211,509,1009. The two zero cases at N=2, p=5,7 were added as correctness cases.

## Fair comparison and precision

The original evidence verifier generates T_N through source precision of order p^3 for a conservative certificate based on denominator dividing T^(p^2)-T. That verifier is not timed as the main baseline. Instead, this experiment uses the stronger degree bound already available from the pole theorem and mass identity: degree D <= M=floor((N+1)(p-1)/24). It obtains the complete rational function without knowing any supersingular values or residue signs.

There are four timed quantities:

1. Reconstruction only: field context and all supersingular values/indices are supplied; building the thin denominator, its derivative values, weighted residues, numerator and descent to Fp are included.
2. Conditional q-expansion control: the thin denominator D is supplied. Compute T|U_p to q^d, where d=degree D, convert to w=1/T and recover P. This control requires less input information than the residue route: it receives D rather than the full weighted locus.
3. Complete supersingular route: construct Fp^2, compute the supersingular j-locus, acquire every level-N value and its effective index, then reconstruct. No j-locus is cached across levels or timing calls.
4. Complete q-only route: use only N,p and the scalar degree bound M; generate the necessary source expansion, convert to w=1/T and perform Padé reconstruction. No supersingular values, denominator or residues are supplied.

Why the q-only precision is sufficient: R(T)=P(T)/D(T) is proper with degree D<=M. Then R(1/w) has numerator and denominator of degrees at most M and denominator nonzero at w=0. Its first 2M+1 coefficients uniquely determine that rational function: the difference of two candidates has numerator degree at most 2M and vanishes to order 2M+1. The driver computes those coefficients, checks the Padé congruence, and reverses the resulting polynomials. The required source length for S=q*T is 2pM+2, of order p^2 for fixed N, not p^3. For zero cases, M is replaced by one for a short nontrivial expansion.

For the conditional q control, d+1 coefficients determine the numerator once D is supplied, requiring source length pd+2 (with a short expansion for d=0). Exact equality with the complete q-only output checks this reconstruction.

## Implementations

All arithmetic is exact. Supersingular j-values are obtained by constructing the short-Weierstrass Hasse polynomial in z=a^3/b^2 (degree approximately p/12), factoring it over Fp^2, mapping roots to j=6912z/(4z+27), and adjoining the appropriate elliptic values j=0,1728. The known j-map P_N(u)/u^N then gives the level-N fibres. Multiplicities over j=0,1728 and fixed points u^2=b_N determine effective indices. The mass identity and exponent integrality are checked. This acquisition uses no q-expansion and no signed residue formula.

The corollary implementation builds a subproduct tree for D. Remainder-tree multipoint evaluation gives D'(t_i); its norm is D'(t_i)^(p+1). The thick-point factors give W_i and the residues r_i=-(-N/p)/W_i. A tree combines the simple fractions into P/D and descends coefficients to Fp. It does not construct the much larger weighted Hasse polynomial of degree of order p^2.

The q-expansion implementation uses Euler pentagonal series and the eta expression T=u+a+b/u, using FLINT truncated polynomial multiplication, powering and Newton series inverses. FLINT compiled compositional reversion gives q(w) for w=1/T; compiled truncated composition gives R(w). Euclidean Padé reconstruction uses FLINT polynomial arithmetic. Slow Python fixed-point compositional reversion and the original p^3 certificate are deliberately avoided.

## Hardware and protocol

Virtualized AMD EPYC 9V74, Linux x86-64, Python 3.12.14, python-flint 0.9.0 / FLINT 3.6.0, GCC 13.3.0 -O3. The timed driver is pinned to CPU 0. Library import and C compilation are outside the clocks. Each route is warmed up and repeated in five blocks for p<=211 and three blocks for p>=509; short routes use calibrated repetition. Medians are reported; all raw samples are saved. Factorization randomness, shared-host load and clock variation remain possible. Acquisition and complete-route times are independently measured, so their medians need not add exactly.

## Full calculation: milliseconds

Both routes start without supersingular data. Complete means the mathematical computation after imports/compilation, not process startup.

| p | Level N | Supersingular route | Q-only route | Q-only / supersingular |
|---:|---:|---:|---:|---:|
| 11 | 2 | 0.077 | 0.036 | 0.47x |
| 11 | 3 | 0.089 | 0.027 | 0.30x |
| 11 | 5 | 0.113 | 0.043 | 0.38x |
| 11 | 7 | 0.177 | 0.056 | 0.31x |
| 11 | 13 | 0.240 | 0.081 | 0.34x |
| 29 | 2 | 0.225 | 0.111 | 0.49x |
| 29 | 3 | 0.300 | 0.148 | 0.49x |
| 29 | 5 | 0.456 | 0.271 | 0.59x |
| 29 | 7 | 0.558 | 0.330 | 0.59x |
| 29 | 13 | 0.851 | 0.587 | 0.69x |
| 59 | 2 | 0.580 | 0.690 | 1.19x |
| 59 | 3 | 0.779 | 0.789 | 1.01x |
| 59 | 5 | 0.956 | 1.176 | 1.23x |
| 59 | 7 | 1.175 | 1.740 | 1.48x |
| 59 | 13 | 2.140 | 3.003 | 1.40x |
| 101 | 2 | 1.310 | 1.892 | 1.44x |
| 101 | 3 | 1.454 | 2.644 | 1.82x |
| 101 | 5 | 1.640 | 3.706 | 2.26x |
| 101 | 7 | 1.930 | 4.699 | 2.44x |
| 101 | 13 | 3.030 | 8.965 | 2.96x |
| 211 | 2 | 4.654 | 12.278 | 2.64x |
| 211 | 3 | 4.417 | 15.598 | 3.53x |
| 211 | 5 | 5.331 | 22.846 | 4.29x |
| 211 | 7 | 6.267 | 29.579 | 4.72x |
| 211 | 13 | 9.340 | 55.209 | 5.91x |
| 509 | 2 | 9.465 | 92.280 | 9.75x |
| 509 | 3 | 12.811 | 122.908 | 9.59x |
| 509 | 5 | 18.684 | 173.220 | 9.27x |
| 509 | 7 | 26.323 | 241.004 | 9.16x |
| 509 | 13 | 56.499 | 396.585 | 7.02x |
| 1,009 | 2 | 20.949 | 490.033 | 23.39x |
| 1,009 | 3 | 26.721 | 669.373 | 25.05x |
| 1,009 | 5 | 41.134 | 944.484 | 22.96x |
| 1,009 | 7 | 55.213 | 1069.329 | 19.37x |
| 1,009 | 13 | 102.752 | 1998.450 | 19.45x |
| 5 | 2 | 0.027 | 0.015 | 0.54x |
| 7 | 2 | 0.036 | 0.018 | 0.50x |

At p=11 and p=29 the q-only method is faster at every tested level. At p=59 the comparison is close, including an essentially tied level-three case. At p>=101 the supersingular route wins throughout this sample. This is an observed crossover in these implementations, not a universal threshold. Ratios for the empty pole cases p=5,7 do not represent substantial computational workloads.

## Conditional reconstruction: milliseconds

The corollary receives the full weighted supersingular data; the q control receives the denominator only. Acquisition is excluded from both columns.

| p | N | Corollary reconstruction | Q control, known D | Speedup |
|---:|---:|---:|---:|---:|
| 11 | 2 | 0.012 | 0.020 | 1.60x |
| 11 | 3 | 0.014 | 0.016 | 1.17x |
| 11 | 5 | 0.014 | 0.014 | 1.02x |
| 11 | 7 | 0.034 | 0.048 | 1.42x |
| 11 | 13 | 0.057 | 0.043 | 0.76x |
| 29 | 2 | 0.035 | 0.059 | 1.70x |
| 29 | 3 | 0.041 | 0.069 | 1.71x |
| 29 | 5 | 0.063 | 0.128 | 2.03x |
| 29 | 7 | 0.125 | 0.133 | 1.07x |
| 29 | 13 | 0.172 | 0.292 | 1.70x |
| 59 | 2 | 0.069 | 0.248 | 3.61x |
| 59 | 3 | 0.116 | 0.332 | 2.87x |
| 59 | 5 | 0.179 | 0.446 | 2.48x |
| 59 | 7 | 0.289 | 0.722 | 2.50x |
| 59 | 13 | 0.523 | 1.208 | 2.31x |
| 101 | 2 | 0.116 | 0.761 | 6.54x |
| 101 | 3 | 0.189 | 1.044 | 5.53x |
| 101 | 5 | 0.232 | 1.528 | 6.59x |
| 101 | 7 | 0.339 | 1.918 | 5.65x |
| 101 | 13 | 0.566 | 4.337 | 7.66x |
| 211 | 2 | 0.249 | 6.146 | 24.67x |
| 211 | 3 | 0.338 | 7.969 | 23.59x |
| 211 | 5 | 0.662 | 10.368 | 15.66x |
| 211 | 7 | 0.664 | 13.412 | 20.19x |
| 211 | 13 | 1.566 | 23.416 | 14.95x |
| 509 | 2 | 1.134 | 42.102 | 37.12x |
| 509 | 3 | 1.838 | 56.526 | 30.75x |
| 509 | 5 | 2.070 | 81.784 | 39.50x |
| 509 | 7 | 3.932 | 100.861 | 25.65x |
| 509 | 13 | 7.182 | 179.728 | 25.03x |
| 1,009 | 2 | 2.388 | 217.382 | 91.03x |
| 1,009 | 3 | 2.881 | 310.925 | 107.93x |
| 1,009 | 5 | 4.676 | 425.068 | 90.90x |
| 1,009 | 7 | 6.801 | 469.502 | 69.04x |
| 1,009 | 13 | 13.296 | 860.465 | 64.72x |
| 5 | 2 | 0.001 | 0.013 | 16.80x |
| 7 | 2 | 0.001 | 0.013 | 22.67x |

## Acquisition breakdown at p=1009

| N | Distinct supersingular j | Thin T-values | Thick T-values | Acquisition (ms) | Reconstruction (ms) | Source q-series length, complete q route |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 84 | 126 | 0 | 20.277 | 2.388 | 254,270 |
| 3 | 84 | 168 | 0 | 23.212 | 2.881 | 339,026 |
| 5 | 84 | 252 | 0 | 35.445 | 4.676 | 508,538 |
| 7 | 84 | 336 | 0 | 49.987 | 6.801 | 678,050 |
| 13 | 84 | 587 | 2 | 87.967 | 13.296 | 1,186,586 |

## Correctness and evidence

All 37 rational functions agree exactly between the printed-formula implementation and the independent q-only/Padé route. They cover 2,782 thin supersingular values. All stored weighted data replay to the same numerator and monic denominator. At small primes, a separate quadratic-time implementation of the printed pairwise product formula agrees with the tree implementation.

All 27 overlapping pairs also agree with the original archive's independently recorded p^3-precision q-expansion certificates, whose certificate flags were checked. Those historical entries are read unchanged; their paths and hashes are in verification.json. The ten p=509,1009 pairs have fresh degree-bound q-only verification here rather than a new p^3 rerun.

These finite computations validate the tested implementations and cases. They are not new proofs of the uniform theorem, and they do not replace a specialist proof audit.

## Memory observations

Separate fresh processes measured one complete route at p=1009. Peak RSS includes Python, FLINT and allocator overhead. Input generation and rational reconstruction are included. The elapsed times in these probes are not the main benchmark medians.

| N | Route | Peak process RSS (MiB) | Increase from initial peak (MiB) |
|---:|---|---:|---:|
| 2 | ss | 27.12 | 4.71 |
| 2 | q | 53.44 | 30.68 |
| 13 | ss | 30.58 | 7.89 |
| 13 | q | 144.17 | 121.43 |

The largest q-series has 1,186,586 coefficients (N=13, p=1009), while the output denominator degree is 587. This illustrates the practical difference in intermediate representation size. RSS figures are coarse observations, not tight space bounds.

## Scope and limitations

- Five eta-coordinate levels were benchmarked, not the other ten Fricke genus-zero levels.
- Neither supersingular-locus acquisition nor q-series reconstruction is claimed to be the globally fastest possible implementation. Specialized hypergeometric Fricke supersingular polynomials, direct computation over Fp, and avoiding root splitting could improve the supersingular route. Other modular-function algorithms could improve the q route.
- Default FLINT field contexts were used; small fields may use Zech-log tables, whose construction is charged to acquisition. Selecting another field backend can change small-prime crossover points.
- The q-only route uses the pole-theorem degree bound, but not the signed residue formula or precomputed supersingular values. Its correctness is conditional only on the same v1.9 mathematical results under comparison.
- The conditional comparison provides different cached information to the two methods, stated explicitly above. It is not a comparison of arbitrary black-box functions with identical input objects.
- No supersingular j-cache is shared across levels in the complete supersingular times. Such sharing would help when processing many N at one p.
- There is no new-prime setup involving the factorial constant c_p here: the corollary sign is simply -(-N/p).
- SageMath, PARI/GP and Magma were not available as executables and were not timed. Both methods use FLINT.
- No claim about cryptographic performance, Cartier-Miller hybrids, or all-fifteen-level benchmark performance is made.

## Assessment

The corollary has a demonstrated computational use beyond assigning residues: it constructs the entire reduced rational function from weighted supersingular data. In this experiment, that advantage survives the cost of obtaining the data for the larger tested primes and reduces intermediate memory substantially. The smaller-prime losses show why reconstruction-only timings should not be presented as full-cost timings. The manuscript and earlier evidence remain unchanged.
