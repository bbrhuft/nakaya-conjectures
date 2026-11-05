import json,pathlib
R=pathlib.Path(__file__).resolve().parent
d=json.loads((R/'results.json').read_text());v=json.loads((R/'verification.json').read_text());mem=json.loads((R/'memory.json').read_text())
rs=d['results']
lines=['# Corollary 1.2: reconstruction and full-cost benchmarks','',
'5 November 2026. Based on the authoritative v1.9 manuscript.','',
'## Main finding','',
'The reconstruction formula gives a practical speedup against the tested q-expansion routes. Acquisition costs matter: the supersingular method loses at the smallest tested characteristics, then wins as p increases. With p=1009, its complete calculation is 19.4-25.1 times faster across the five tested levels. With the supersingular data supplied, its reconstruction is 64.7-107.9 times faster than a q-expansion control that is already supplied the thin denominator. These are implementation-specific measurements, not global optimality claims.','',
'The scope is the five eta-coordinate levels N=2,3,5,7,13, not all fifteen levels covered by Theorem 1.1. Seven primes were tested at each level: 11,29,59,101,211,509,1009. The two zero cases at N=2, p=5,7 were added as correctness cases.','',
'## Fair comparison and precision','',
'The original evidence verifier generates T_N through source precision of order p^3 for a conservative certificate based on denominator dividing T^(p^2)-T. That verifier is not timed as the main baseline. Instead, this experiment uses the stronger degree bound already available from the pole theorem and mass identity: degree D <= M=floor((N+1)(p-1)/24). It obtains the complete rational function without knowing any supersingular values or residue signs.','',
'There are four timed quantities:','',
'1. Reconstruction only: field context and all supersingular values/indices are supplied; building the thin denominator, its derivative values, weighted residues, numerator and descent to Fp are included.','2. Conditional q-expansion control: the thin denominator D is supplied. Compute T|U_p to q^d, where d=degree D, convert to w=1/T and recover P. This control requires less input information than the residue route: it receives D rather than the full weighted locus.','3. Complete supersingular route: construct Fp^2, compute the supersingular j-locus, acquire every level-N value and its effective index, then reconstruct. No j-locus is cached across levels or timing calls.','4. Complete q-only route: use only N,p and the scalar degree bound M; generate the necessary source expansion, convert to w=1/T and perform Padé reconstruction. No supersingular values, denominator or residues are supplied.','',
'Why the q-only precision is sufficient: R(T)=P(T)/D(T) is proper with degree D<=M. Then R(1/w) has numerator and denominator of degrees at most M and denominator nonzero at w=0. Its first 2M+1 coefficients uniquely determine that rational function: the difference of two candidates has numerator degree at most 2M and vanishes to order 2M+1. The driver computes those coefficients, checks the Padé congruence, and reverses the resulting polynomials. The required source length for S=q*T is 2pM+2, of order p^2 for fixed N, not p^3. For zero cases, M is replaced by one for a short nontrivial expansion.','',
'For the conditional q control, d+1 coefficients determine the numerator once D is supplied, requiring source length pd+2 (with a short expansion for d=0). Exact equality with the complete q-only output checks this reconstruction.','',
'## Implementations','',
'All arithmetic is exact. Supersingular j-values are obtained by constructing the short-Weierstrass Hasse polynomial in z=a^3/b^2 (degree approximately p/12), factoring it over Fp^2, mapping roots to j=6912z/(4z+27), and adjoining the appropriate elliptic values j=0,1728. The known j-map P_N(u)/u^N then gives the level-N fibres. Multiplicities over j=0,1728 and fixed points u^2=b_N determine effective indices. The mass identity and exponent integrality are checked. This acquisition uses no q-expansion and no signed residue formula.','',
'The corollary implementation builds a subproduct tree for D. Remainder-tree multipoint evaluation gives D\'(t_i); its norm is D\'(t_i)^(p+1). The thick-point factors give W_i and the residues r_i=-(-N/p)/W_i. A tree combines the simple fractions into P/D and descends coefficients to Fp. It does not construct the much larger weighted Hasse polynomial of degree of order p^2.','',
'The q-expansion implementation uses Euler pentagonal series and the eta expression T=u+a+b/u, using FLINT truncated polynomial multiplication, powering and Newton series inverses. FLINT compiled compositional reversion gives q(w) for w=1/T; compiled truncated composition gives R(w). Euclidean Padé reconstruction uses FLINT polynomial arithmetic. Slow Python fixed-point compositional reversion and the original p^3 certificate are deliberately avoided.','',
'## Hardware and protocol','',
'Virtualized AMD EPYC 9V74, Linux x86-64, Python 3.12.14, python-flint 0.9.0 / FLINT 3.6.0, GCC 13.3.0 -O3. The timed driver is pinned to CPU 0. Library import and C compilation are outside the clocks. Each route is warmed up and repeated in five blocks for p<=211 and three blocks for p>=509; short routes use calibrated repetition. Medians are reported; all raw samples are saved. Factorization randomness, shared-host load and clock variation remain possible. Acquisition and complete-route times are independently measured, so their medians need not add exactly.','',
'## Full calculation: milliseconds','',
'Both routes start without supersingular data. Complete means the mathematical computation after imports/compilation, not process startup.','',
'| p | Level N | Supersingular route | Q-only route | Q-only / supersingular |',
'|---:|---:|---:|---:|---:|']
for x in rs:
 lines.append(f"| {x['p']:,} | {x['N']} | {x['ss_end_to_end']['median_s']*1e3:.3f} | {x['q_free']['median_s']*1e3:.3f} | {x['full_speedup']:.2f}x |")
lines += ['',
'At p=11 and p=29 the q-only method is faster at every tested level. At p=59 the comparison is close, including an essentially tied level-three case. At p>=101 the supersingular route wins throughout this sample. This is an observed crossover in these implementations, not a universal threshold. Ratios for the empty pole cases p=5,7 do not represent substantial computational workloads.','',
'## Conditional reconstruction: milliseconds','',
'The corollary receives the full weighted supersingular data; the q control receives the denominator only. Acquisition is excluded from both columns.','',
'| p | N | Corollary reconstruction | Q control, known D | Speedup |',
'|---:|---:|---:|---:|---:|']
for x in rs:
 lines.append(f"| {x['p']:,} | {x['N']} | {x['reconstruction_only']['median_s']*1e3:.3f} | {x['q_known_denominator']['median_s']*1e3:.3f} | {x['conditional_speedup']:.2f}x |")
lines += ['',
'## Acquisition breakdown at p=1009','',
'| N | Distinct supersingular j | Thin T-values | Thick T-values | Acquisition (ms) | Reconstruction (ms) | Source q-series length, complete q route |',
'|---:|---:|---:|---:|---:|---:|---:|']
for x in rs:
 if x['p']==1009:
  lines.append(f"| {x['N']} | {x['n_ss_j']} | {x['n_thin']} | {x['n_thick']} | {x['acquisition']['median_s']*1e3:.3f} | {x['reconstruction_only']['median_s']*1e3:.3f} | {x['source_precision_q_free']:,} |")
lines += ['',
'## Correctness and evidence','',
f"All {len(rs)} rational functions agree exactly between the printed-formula implementation and the independent q-only/Padé route. They cover {sum(x['n_thin'] for x in rs):,} thin supersingular values. All stored weighted data replay to the same numerator and monic denominator. At small primes, a separate quadratic-time implementation of the printed pairwise product formula agrees with the tree implementation.",'',
f"All {v['historical_matches']} overlapping pairs also agree with the original archive's independently recorded p^3-precision q-expansion certificates, whose certificate flags were checked. Those historical entries are read unchanged; their paths and hashes are in verification.json. The ten p=509,1009 pairs have fresh degree-bound q-only verification here rather than a new p^3 rerun.", '',
'These finite computations validate the tested implementations and cases. They are not new proofs of the uniform theorem, and they do not replace a specialist proof audit.','',
'## Memory observations','',
'Separate fresh processes measured one complete route at p=1009. Peak RSS includes Python, FLINT and allocator overhead. Input generation and rational reconstruction are included. The elapsed times in these probes are not the main benchmark medians.','',
'| N | Route | Peak process RSS (MiB) | Increase from initial peak (MiB) |',
'|---:|---|---:|---:|']
for x in mem:lines.append(f"| {x['N']} | {x['route']} | {x['final_peak_KiB']/1024:.2f} | {(x['final_peak_KiB']-x['initial_peak_KiB'])/1024:.2f} |")
lines += ['',
'The largest q-series has 1,186,586 coefficients (N=13, p=1009), while the output denominator degree is 587. This illustrates the practical difference in intermediate representation size. RSS figures are coarse observations, not tight space bounds.','',
'## Scope and limitations','',
'- Five eta-coordinate levels were benchmarked, not the other ten Fricke genus-zero levels.','- Neither supersingular-locus acquisition nor q-series reconstruction is claimed to be the globally fastest possible implementation. Specialized hypergeometric Fricke supersingular polynomials, direct computation over Fp, and avoiding root splitting could improve the supersingular route. Other modular-function algorithms could improve the q route.','- Default FLINT field contexts were used; small fields may use Zech-log tables, whose construction is charged to acquisition. Selecting another field backend can change small-prime crossover points.','- The q-only route uses the pole-theorem degree bound, but not the signed residue formula or precomputed supersingular values. Its correctness is conditional only on the same v1.9 mathematical results under comparison.','- The conditional comparison provides different cached information to the two methods, stated explicitly above. It is not a comparison of arbitrary black-box functions with identical input objects.','- No supersingular j-cache is shared across levels in the complete supersingular times. Such sharing would help when processing many N at one p.','- There is no new-prime setup involving the factorial constant c_p here: the corollary sign is simply -(-N/p).','- SageMath, PARI/GP and Magma were not available as executables and were not timed. Both methods use FLINT.','- No claim about cryptographic performance, Cartier-Miller hybrids, or all-fifteen-level benchmark performance is made.','',
'## Assessment','',
'The corollary has a demonstrated computational use beyond assigning residues: it constructs the entire reduced rational function from weighted supersingular data. In this experiment, that advantage survives the cost of obtaining the data for the larger tested primes and reduces intermediate memory substantially. The smaller-prime losses show why reconstruction-only timings should not be presented as full-cost timings. The manuscript and earlier evidence remain unchanged.']
(R/'REPORT.md').write_text('\n'.join(lines)+'\n')
