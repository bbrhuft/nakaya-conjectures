# Fifteen-level Fricke extension

4 November 2026. Research extension of David Jordan's *Supersingular poles and signed residues of prime-level Fricke Hauptmoduln*, version 1.6 to version 1.7.

## Verdict

Theorem 1.1 extends to every prime level

    N = 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71

and every reduction prime p >= 5 with p != N. This is a proof extension, not an inference from the finite checks. The full proof is in the accompanying v1.7 manuscript. No genus-zero hypothesis on X_0(N) itself is needed.

With the normalized quotient coordinate T_N = q^(-1)+O(q), define e_i and W_i exactly as in the manuscript. The poles of the reduced U_p image are precisely the thin supersingular values (e_i=1), each simple, and

    r_i W_i = -(-N/p).

The coefficient ring needed for the proof is Lambda_N = Z[1/(6N)]. The excluded reduction primes remain 2, 3 and N. The level N and reduction characteristic p must not be conflated.

## What changes in the proof

1. The new integral-coordinate lemma constructs X_0(N)/w_N as a smooth proper genus-zero curve over Lambda_N with one cusp section. Tame invariants commute with reduction. Relative Riemann–Roch for the degree-one cusp divisor constructs the unique normalized integral coordinate and proves its reduction remains a coordinate at every admissible prime.
2. The Hecke polynomial argument works over Lambda_N, independently of an eta expression for T_N. Transitivity, the Kronecker congruence, symmetry and the universal denominator bound are unchanged in substance.
3. The inertia indices and the local Kodaira–Spencer calculation do not require a coordinate on X_0(N). They prove exactly the same thin-pole criterion and residue formula.
4. The weighted Hasse polynomial A^(p+1)/(Delta(tau)Delta(Ntau))^k still has its sole pole at the quotient cusp, with the same monic normalization and multiplicities (p+1)/e_i.
5. Robert's isogeny identity and the factorial evaluation then give the signed product exactly as before. Theorem 1.5 and the geometric interpretation already admit the general prime-level arguments.

The five-level eta formulas, Nakaya shifts and explicit elliptic-value table are retained as five-level applications, not asserted for the other ten levels. The factorial theorem and its proof are unchanged.

## Exact checks completed

| Levels | Range | Admissible pairs | Thin values | Non-rational thin values |
| --- | --- | ---: | ---: | ---: |
| Ten new levels | 5 <= p <= 47, p != N | 122 | 4056 | 3222 |
| Five original levels, fresh regression | Same | 62 | 402 | 226 |
| All fifteen | Same | 184 | 4458 | 3448 |

Every pair passes a certificate using the a priori denominator bound T^(p^2)-T. Numerators are reconstructed from the Fourier series without the signed product formula. The supersingular input is checked by two Hasse-polynomial routes. The new-level tests also compare the full weighted Hasse polynomial, independently obtained geometric indices, the mass identity, and all individual signed residue products. No thin point has zero residue. All resulting r_i and W_i lie in F_p.

The smaller pilot and p<=31 files are retained as checkpoints; their pairs overlap the main p<=47 run and must not be counted again. The new verifier does not construct every new Hecke polynomial modulo p^2: its certificate uses the proved general Hecke bound. Thus it verifies a rational-function identity, not an independent numerical proof of the Hecke construction.

## New-level computation and model normalization

The mathematical coefficient data in `code/hyperelliptic_data.json` are extracted from SageMath's `_hyperelliptic_isogeny_data` for the ten levels. The imported classical model and modular map are

    v^2=f(u), w_N(u,v)=(u,-v),
    j=(alpha(u)+beta(u)v)/2,
    Q(u)=(alpha(u)^2-f(u)beta(u)^2)/4=j*(j o w_N).

Here alpha is monic of degree N and Q has degree N+1. Newton inversion of

    alpha(u(q))=j(q)+j(q^N),   q*u(q)=1+O(q)

gives the Fourier expansion at primes p!=N; T_N=u-shift, with shift=-alpha[N-1]/N. The shifts in increasing new-level order are 5,3,2,2,1,2,1,1,1,1. The product relation is separately checked. The input models are standard stored modular data, not newly derived models or consequences of the signed residue theorem.

At a supersingular j0, solve Q-j0*alpha+j0^2=0 over F_(p^2). The roots of f detect Fricke branch points. For j0=0 or 1728, let a=3 or 2, respectively, and let mu be the multiplicity of u in this polynomial. At a branch point the reduced automorphism order is m=a/mu. Away from the branch locus it is m=2a/mu if alpha(u)=2j0, and m=a/mu otherwise. This accounts for the two preimages when both j-values coincide. Set e=m*2 at a branch point and e=m otherwise; for other j0 set m=1. These are geometric ramification calculations and do not use the weighted Hasse polynomial. The verifier checks that all model f have squarefree reduction at each tested prime, that repeated descriptions give the same e, and that the resulting full weighted polynomial agrees with its Fourier expansion.

## Reproduction

Requires Python 3.11 or later and python-flint 0.9.0. No SageMath or PARI installation is required. The included mathematical model data are sufficient; no network is used by the verification scripts.

From the bundle directory:

```bash
python3 -m pip install python-flint==0.9.0
python3 code/verify_extension.py --pmax 47 --out results/new_levels_p47.json
python3 code/regression_five.py
```

The ten-level run took about 191 seconds in the recorded environment. Timing is informational, not a performance claim. The new run and all true regression flags have been checked. Each new record includes the numerator and denominator, coefficient arrays in ascending powers, point counts, index counts and sign checks. The scripts retain their assertions: do not run Python with `-O`.

## Source and provenance

- Input manuscript: v1.6, SHA256 `b3cef967d3d6a2e31cafb47ba32fe07a0a71bb051e2757b79790f754695797d8`. Its bytes are preserved unchanged under `input/`.
- The new arithmetic code is `code/verify_extension.py`.
- `code/inherited_wr_core.py` and `code/inherited_wr_pairs.py` are unchanged copies from the supplied `Signed_Weighted_Residue_v1_0` package. The regression loader only maps the old module name to its preserved copy. `SHA256SUMS.txt` records the included bytes.
- SageMath source: <https://raw.githubusercontent.com/sagemath/sage/develop/src/sage/schemes/elliptic_curves/isogeny_small_degree.py>, retrieved 4 November 2026. Downloaded source SHA256: `e86d3590e525270a542cb1ad240b714a6206768b1bc4369151ff069b353f8bc3`. The original source is not redistributed here; the extracted mathematical coefficients and attribution are included.
- Ogg's classification was checked against the original §3 corollary: <https://www.numdam.org/item/SDPP_1974-1975__16_1_A4_0/>.
- The good-reduction and tame quotient inputs are the standard Deligne–Rapoport/Katz–Mazur theory already cited in the manuscript. The new coordinate construction is written out, including flatness, base change and the principal-part sequence.

## Limits and interpretation

The all-prime statement rests on the proof, not on the bounded numerical run. This work has not undergone independent specialist refereeing. No exhaustive literature-priority claim is made. The extension puts the theorem on the complete classical Ogg prime set; it supplies no new Monster action and does not independently explain the coincidence of that set with the prime divisors of the Monster's order. Composite levels, positive-genus quotients, and the bad characteristics are outside this result.

The manuscript's public data URL remains to be supplied after the evidence is deposited in the author's intended repository. No external publication was performed.
