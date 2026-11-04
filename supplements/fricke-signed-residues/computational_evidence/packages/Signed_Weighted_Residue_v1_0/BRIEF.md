Investigate an exact signed weighted-residue conjecture for the five prime levels
\[
N\in\{2,3,5,7,13\}.
\]

This is a separate follow-up to our level-two paper, *Supersingular poles of a level-two Hauptmodul modulo primes*. Your task is to reproduce, challenge, and sharpen the proposed uniform formula below, then attempt a proof. Treat all reported computations and inherited arguments as material to audit, not established premises.

**1. Fix the normalization exactly**

Put
\[
a_N=\frac{24}{N-1},\qquad
b_N=N^{12/(N-1)},\qquad
u_N(\tau)=\left(\frac{\eta(\tau)}{\eta(N\tau)}\right)^{a_N},
\]
and
\[
T_N=u_N+a_N+\frac{b_N}{u_N}.
\]
Thus \(T_N=q^{-1}+O(q)\) is the normalized Hauptmodul for
\(\Gamma_0(N)^+=\langle\Gamma_0(N),w_N\rangle\), and
\(w_N(u_N)=b_N/u_N\).

The pairs \((a_N,b_N)\) are
\[
(24,4096),(12,729),(6,125),(4,49),(2,13).
\]
Do not substitute a Hauptmodul with an unrecorded additive or multiplicative change.

For primes \(p\ge5\), \(p\nmid N\), use
\[
\left(\sum_n c_nq^n\right)\big|U_p=\sum_n c_{pn}q^n.
\]
Write
\[
\overline{T_N|U_p}=R_{N,p}(\overline T_N).
\]
First justify the rationality of this expression and that it vanishes at infinity, or clearly identify the theorem supplying these facts.

**2. Define the supersingular weights geometrically**

Let \(t_1,\ldots,t_s\) be the distinct geometric supersingular \(T_N\)-values.

For a point \(x=(E,C_N)\) on \(X_0(N)\) mapping to \(t_i\), define
\[
m_x=\left|\operatorname{Aut}(E,C_N)/\{\pm1\}\right|,
\qquad
e_i=m_x\,\left|\operatorname{Stab}_{\langle w_N\rangle}(x)\right|.
\]

Check that this definition is independent of the representative of the Fricke orbit and correctly measures the effective local quotient action. In particular, distinguish group order from effective inertia.

Call \(t_i\) thin when \(e_i=1\). All products below range over distinct geometric supersingular values, each appearing once. Their weights are recorded in the exponents; do not insert multiplicities a second time.

The expected pole theorem is:
\[
\operatorname{den}_{\mathrm{red}}R_{N,p}(T)
=\prod_{e_i=1}(T-t_i),
\]
with every displayed pole simple and having nonzero residue.

This support statement has a proposed uniform Deligne–Rapoport proof through
\[
X_0(Np)^{\mathrm{DR}}/\langle w_N\rangle.
\]
It is background for this investigation, not permission to assume a proof that has not been supplied.

**3. Investigate the exact signed conjecture**

For every thin \(t_i\), define
\[
r_i=\operatorname{Res}_{T=t_i}R_{N,p}(T),\qquad
W_i=\prod_{k\ne i}(t_i-t_k)^{(p+1)/e_k}.
\]

Verify that every exponent is integral in the stated setting. If it is not, stop and correct the formulation rather than choosing arbitrary roots.

The candidate identity is
\[
\boxed{
r_iW_i=-\left(\frac{-N}{p}\right)
}
\]
or equivalently
\[
\boxed{
r_i=
-\left(\frac{-N}{p}\right)
\prod_{k\ne i}(t_i-t_k)^{-(p+1)/e_k}.
}
\]

Your primary objectives are to determine:

- whether the ratio \(r_iW_i\) is constant across all thin points;
- whether its value is exactly the displayed signed Legendre symbol;
- whether this holds uniformly for all five levels and all admissible primes;
- whether individual residues and weighted products always belong to \(\mathbb F_p\), including at non-rational thin points.

The last property was observed computationally; treat it as a separate assertion requiring explanation.

For level two, the attached manuscript and sign-proof bundle contain the claimed proof. Audit their normalization and hypotheses before using them.

**4. Reproduce and extend the evidence independently**

The preceding investigation reports all admissible pairs with
\[
N\in\{2,3,5,7,13\},\qquad
p\in\{5,7,11,13,17,19,23,29\},\qquad p\ne N.
\]

That gives 37 pairs and 135 thin geometric points, including 60 non-rational thin points. Of the pairs, 26 have at least two thin points, seven have one, and four have none. Every reported ratio matched the candidate sign.

Reproduce these results, then extend the prime range as far as practical—preferably through at least \(p=101\). Report the range actually completed, including failures and exceptions.

Compute \(R_{N,p}\) independently of the conjectured residue formula. In particular, do not construct a rational function from the proposed residues and then count their agreement as independent evidence.

One route is to recover a numerator from the \(q\)-expansion using the candidate thin denominator, then certify the identity using an independently justified degree or pole bound. Separate successful reconstruction from a rigorous certificate.

Use exact finite-field arithmetic. Include non-rational points in \(\mathbb F_{p^2}\), and explicitly test Frobenius conjugation.

Useful \(j\)-maps, with \(u=u_N\), are:
\[
j=\frac{(u+256)^3}{u^2}\quad(N=2),
\]
\[
j=\frac{(u+27)(u+243)^3}{u^3}\quad(N=3),
\]
\[
j=\frac{(u^2+250u+3125)^3}{u^5}\quad(N=5),
\]
\[
j=\frac{(u^2+13u+49)(u^2+245u+2401)^3}{u^7}
\quad(N=7),
\]
\[
j=\frac{(u^2+5u+13)
(u^4+247u^3+3380u^2+15379u+28561)^3}{u^{13}}
\quad(N=13).
\]
Verify these normalizations independently.

Supersingular \(j\)-values can be obtained from the Deuring polynomial
\[
D_p(\lambda)=\sum_{j=0}^{(p-1)/2}
\binom{(p-1)/2}{j}^{2}\lambda^j
\]
and
\[
j(\lambda)=
256\frac{(\lambda^2-\lambda+1)^3}
{\lambda^2(\lambda-1)^2},
\]
or by another independent method.

As a consistency check, test the weighted mass identity
\[
\sum_i\frac1{e_i}=\frac{(N+1)(p-1)}{24}.
\]
Check small-characteristic collisions and exceptional automorphisms explicitly.

For diagnostic comparisons, the reported constant ratios at \(p=29\), in level order \(2,3,5,7,13\), are
\[
+1,+1,-1,-1,-1.
\]

**5. Seek a proof of the constant and its sign**

Keep two questions separate:

1. Why do exactly the thin supersingular points contribute poles?
2. Why do their residues satisfy this particular product formula with this exact constant?

The Deligne–Rapoport model and tame quotient theory can control node thickness and residue vanishing. Thickness alone does not determine the relevant smoothing units, so it does not by itself establish the signed product formula.

Explore direct approaches on \(X_0(N)\) and its Fricke quotient, including:

- Hasse invariants and Kodaira–Spencer identities;
- a Kaneko–Zagier-style calculation of the first Kronecker correction;
- Fricke action on differentials, de Rham or crystalline cohomology;
- de Shalit-style period and smoothing-unit formulas.

In particular, investigate whether the determinant \(N\) of the Fricke isogeny explains the factor \(\left(\frac{-N}{p}\right)\). This is a suggested mechanism, not an established argument.

If a Hecke polynomial is used, fix its normalization and write
\[
\Psi_{N,p}(X,Y)
=(X^p-Y)(X-Y^p)+pH_{N,p}(X,Y).
\]
With the expected residue convention
\[
r_i=-\overline H_{N,p}(t_i^p,t_i),
\]
the conjecture becomes
\[
\overline H_{N,p}(t_i^p,t_i)
=\left(\frac{-N}{p}\right)W_i^{-1}.
\]
Check the minus sign carefully.

Prefer a uniform proof directly from the level-\(N\) geometry. Passing through Legendre coordinates remains acceptable as a comparison or computational tool.

**6. Check the literature and state the outcome precisely**

Search for an existing result implying this exact formula, including its normalization and sign. Distinguish pole-support theorems, formulas only up to sign, rational-point cases, and formulas valid at all geometric supersingular points.

Consult the attached level-two work, de Shalit, Kaneko–Zagier, Baker, Betina–Lecouturier, and relevant work on Fricke-group Hasse invariants and Atkin polynomials. Verify what each source actually proves. Do not infer priority from an unsuccessful search.

Deliver:

1. A precise signed theorem or conjecture, with its exact scope.
2. A reproducible Python or Sage implementation and machine-readable results.
3. A table showing supersingular counts, weights, thin counts, non-rational thin counts, and the observed ratio sets.
4. A proof attempt that identifies every unresolved step explicitly.
5. A concise literature assessment.
6. A self-contained LaTeX research note and a README explaining reproduction.

If the formula fails, prioritize the first counterexample and a corrected statement. If it survives extensive testing without proof, retain conjectural status. Do not modify the existing level-two paper during this investigation.