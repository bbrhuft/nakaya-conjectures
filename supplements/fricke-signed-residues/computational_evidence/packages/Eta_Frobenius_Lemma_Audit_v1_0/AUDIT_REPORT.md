# Audit of the eta/Frobenius lemma (Theorem C) of the *Signed Weighted Residue Note*

**Audit package v1.0 — 3 November 2026.** AI-assisted referee-style audit (Claude, Anthropic), prepared at the request of D. Jordan. Not a substitute for specialist refereeing. The inherited package `Signed_Weighted_Residue_v1_0` was read but **not modified**; this audit lives in a separate tree.

---

## 0. Verdict

**Correct after specified repairs.** No mathematical error was found in the lemma or in the proof strategy. Every step either (a) is proved here in full from fixed conventions, or (b) is a precisely cited standard import. The repairs are foundational/expository, not corrections of a wrong claim:

| # | Repair | Why it was needed |
|---|---|---|
| R1 | Replace the Gordon–Hughes–Newman citation by a complete derivation of the character of $G=\eta(24\ell\tau)/\eta(24\tau)$ from the Petersson/Knopp closed form of the eta multiplier (§2). | The sign $\left(\frac{\ell}{p}\right)$ is the entire content of the lemma; it should not rest on a cited character formula whose conventions ($d<0$, Kronecker vs Jacobi, $\ell=2$) are not spelled out. |
| R2 | Fix the diamond-operator and Frobenius conventions once and for all: $\langle d\rangle(E,\iota)=(E,\iota\circ[d])$, $G\circ\langle d\rangle=\chi_\ell(d)G$ (no inverse), $\sigma(\tilde x)=\langle -p^{-1}\rangle\tilde x$ (§4). | The note wrote $d^{\pm1}$ and $-p^{\mp1}$; harmless here because $\chi_\ell$ is even and quadratic, but a proof should not contain unresolved signs. |
| R3 | Replace the descent/integrality sentence of Fact I5 by: (i) a two-line $q$-expansion principle at the $\mathbb Z[1/M]$-rational cusp of the $\mu_M$-model giving $G\in\mathbb Q(X_1(M))$; (ii) the moduli description $D_\ell(E,C)=\ell^{12}\Delta(E,\pi^*\omega')/\Delta(E',\omega')$ as a unit on $Y_0(\ell)_{\mathbb Z[1/\ell]}$; (iii) the moduli definition of the degeneracy map $\delta$ with $G^{24}=\delta^*D_\ell^{-1}$; (iv) normality of $Y_1(M)_{\mathbb Z_{(p)}}$ plus the monic equation $T^{24}-\delta^*D_\ell^{-1}$ to get $G\in\mathcal O(Y_1(M)_{\mathbb Z_{(p)}})^\times$ (§3). | Fact I5 said "a function on this model defined over $\mathbb Z_{(p)}$" without saying where it is regular, and invoked unit leading coefficients at *all* cusps, which were never computed. The monic-equation route (suggested in the brief) needs only the cusp $\infty$. |
| R4 | Replace "$E_1$ is 24-isogenous to $E$, so it has a Deuring model" by "$E_1$ is supersingular, so $j(E_1)$ has a model with $\pi=[-p]$", with a proof that $\pi_{p^2}=p\cdot u$, $u\in\mathrm{Aut}(E)$, for every supersingular model over $\mathbb F_{p^2}$ (§4). | The 24-isogeny is irrelevant; what matters is that changing the model of $E_1$ does not change the geometric point $\tilde x$ or the value $G(\tilde x)$, and that $\iota$ need not be $\mathbb F_{p^2}$-rational. |
| R5 | State explicitly which object "$\Delta(\tau)/\Delta(\ell\tau)$ evaluated at $x$" is (eq. (7.2) of the replacement section), so the claim is about the weight-0 moduli function and not about discriminants of independently chosen models. | Requested by the brief; the note's Lemma `Bisog` already implies it but the lemma statement did not say so. |

The replacement LaTeX section (`replacement_section/eta_section_replacement.tex`) incorporates R1–R5 and compiles against the note's preamble (`standalone_wrapper.pdf`).

**Priority.** The exact signed statement $D_\ell^{(p^2-1)/24}=\left(\frac{\ell}{p}\right)$ at all geometric supersingular points was **not found** in any inspected source. Ono (2026, v2, 3 July 2026) proves the $(p^2-1)/12$ statement (his Thm 1.2), proves $\Delta(E,\omega)^{(p^2-1)/12}=(-1)^{(p+1)/2}$ on Deuring models (Thm 1.3), and in Remark 4 explicitly observes that the $(p^2-1)/24$ power can be $-1$ without giving a formula. The $(p^2-1)/12$ statement for $\mathbb F_{p^2}$-isogenous curves is older: Baker (1998, §2), from the Gross–Landweber congruence. The isogeny relation $B(E')=\ell\,B(E)$ (the note's Lemma `Bisog`) is Robert (1980, Théorème B/Lemme 7) as quoted in Baker (1998, Lemma 2.2). The constancy of $c(E)=E_{p+1}^{(p-1)/2}/\Delta^{(p^2-1)/24}$ was not found either. **An unsuccessful search does not establish novelty**; Robert (1980) could not be read in full (see §6).

---

## 1. The exact target

For primes $p\ge5$, $\ell\ne p$, $k=(p^2-1)/24$, and $x=(E,C)$ a geometric supersingular point of $X_0(\ell)$,

$$D_\ell(x)^{k}=\left(\frac{\ell}{p}\right),\qquad D_\ell(E,C):=\ell^{12}\,\frac{\Delta(E,\pi^*\omega')}{\Delta(E',\omega')},\quad \pi:E\to E'=E/C .$$

$D_\ell$ is independent of $\omega'$ (both discriminants have weight 12), is an invertible function on $Y_0(\ell)$ over $\mathbb Z[1/\ell]$, and its $q$-expansion at the cusp $(\mathrm{Tate}(q),\mu_\ell)$ is $\Delta(q)/\Delta(q^\ell)$ (Tate curve: $\pi^*(dt'/t')=\ell\,dt/t$). So $D_\ell$ *is* the weight-0 modular function $\Delta(\tau)/\Delta(\ell\tau)$ in the only sense in which it can be evaluated at a point of $X_0(\ell)_{\overline{\mathbb F}_p}$. Since $\ell^{12k}=\ell^{(p^2-1)/2}=1$ in $\mathbb F_p$, the target is equivalent to $(\Delta(E,\pi^*\omega')/\Delta(E',\omega'))^k=\left(\frac{\ell}{p}\right)$, i.e. **the Vélu-normalised discriminant ratio is a 24th power in $\mathbb F_{p^2}^\times$ iff $\left(\frac{\ell}{p}\right)=1$.** The audit of Theorem C below is independent of the weighted-residue theorem (no residue, Hecke polynomial or Kaneko–Zagier input is used).

---

## 2. The analytic multiplier calculation

### 2.1 The eta-quotient theorem and its hypotheses

The note invoked Gordon–Hughes–Newman in the form of Ono (2004, Thm 1.64): for $f=\prod_{\delta\mid N}\eta(\delta\tau)^{r_\delta}$ with $k=\tfrac12\sum r_\delta\in\mathbb Z$, $\sum\delta r_\delta\equiv0$ and $\sum (N/\delta)r_\delta\equiv0\pmod{24}$, one has $f(\gamma\tau)=\chi(d)(c\tau+d)^k f(\tau)$ on $\Gamma_0(N)$ with $\chi(d)=\left(\frac{(-1)^k s}{d}\right)$, $s=\prod\delta^{r_\delta}$. Negative $r_\delta$ are allowed; $k=0$ is allowed. For $G$: $N=576\ell$, $\delta\in\{24,24\ell\}$, $r_{24}=-1$, $r_{24\ell}=1$: $k=0$; $\sum\delta r_\delta=24(\ell-1)$; $\sum(N/\delta)r_\delta=24-24\ell$; $s=\ell$. All hypotheses hold, including for $\ell=2,3$ (where $s\mid 24$). The level $576\ell$ is necessary for the second congruence: with $N=24\ell$ one gets $1-\ell\not\equiv0$. **The citation is correct as used.**

### 2.2 Complete derivation (replacement for the citation)

Petersson/Knopp closed form (Knopp, 1970, Ch. 4 §4.1; Dedekind-sum form in Apostol, 1990, Thm 3.4): for $c>0$, $\eta(\gamma\tau)=\nu(\gamma)(c\tau+d)^{1/2}\eta(\tau)$ with
$$\nu(\gamma)=\begin{cases}\left(\frac dc\right)e\!\left(\frac{(a+d)c-bd(c^2-1)-3c}{24}\right)&c\text{ odd}\\ \left(\frac cd\right)e\!\left(\frac{(a+d)c-bd(c^2-1)+3d-3-3cd}{24}\right)&c\text{ even}\end{cases}$$
(Kronecker symbols). *Verification:* this closed form agrees with the exact Dedekind-sum multiplier on 400 random matrices, both parities of $c$ and both signs of $d$ (they differ by the fixed branch constant $e(1/8)$ from $(-i)^{1/2}$), and the Dedekind-sum multiplier agrees with 50-digit `mpmath` numerics to $3\times10^{-50}$ (`results/eta_multiplier_audit.json`).

For $\gamma\in\Gamma_0(576\ell)$, $c>0$: $24\gamma\tau=\gamma_1(24\tau)$ and $24\ell\gamma\tau=\gamma_2(24\ell\tau)$ with $\gamma_1=\begin{pmatrix}a&24b\\ c/24&d\end{pmatrix}$, $\gamma_2=\begin{pmatrix}a&24\ell b\\ c/(24\ell)&d\end{pmatrix}$, identical automorphy factors $(c\tau+d)^{1/2}$. Both lower-left entries are divisible by 24 (even), so the even-$c$ line applies to both. In $\nu(\gamma_2)/\nu(\gamma_1)$ every term of the exponent is a multiple of 24 ($24\mid c_i$ kills $(a+d)(c_2-c_1)$ and $3d(c_2-c_1)$; $24\mid b_i$ kills the middle term), so the exponentials cancel, and the symbols give $\left(\frac{c_2}{d}\right)\left(\frac{c_1}{d}\right)=\left(\frac{\ell c_2^2}{d}\right)=\left(\frac{\ell}{d}\right)$ since $c_1=\ell c_2$, $\gcd(c_2,d)=1$. The cases $c=0$ and $c<0$ reduce to this ($G$ has an integral $q$-expansion; $-\gamma$ acts as $\gamma$; $\left(\frac{\ell}{-1}\right)=1$). **Hence $G(\gamma\tau)=\left(\frac{\ell}{d}\right)G(\tau)$ on $\Gamma_0(576\ell)$**, with the Kronecker symbol, for every prime $\ell$ including 2 and 3.

### 2.3 The character

$\chi_\ell(d)=\left(\frac{\ell}{d}\right)$ on $(\mathbb Z/576\ell)^\times$ is, by quadratic reciprocity, the Kronecker character of $\mathbb Q(\sqrt\ell)$: conductor $\ell$ ($\ell\equiv1\bmod4$), $4\ell$ ($\ell\equiv3\bmod4$), $8$ ($\ell=2$), all dividing $576\ell=2^6\cdot3^2\cdot\ell$. It is even (real quadratic field; directly $\left(\frac{\ell}{-1}\right)=1$; and necessarily so since $-I$ acts trivially), quadratic, and $\chi_\ell(p)=\left(\frac{\ell}{p}\right)$ is the Legendre symbol for the prime $p\nmid M$. Verified exhaustively for all $d$ mod $576\ell$, $\ell\le47$ (`eta_multiplier_audit.json: kronecker_character_identification`).

### 2.4 The change of variables $24\tau$

The note's Lemma `mult` is stated for $y=\eta(\tau)/\eta(\ell\tau)$ and $\gamma$ with $24\ell\mid c$, $24\mid b$: $y(\gamma\tau)=\left(\frac{\ell}{d}\right)y(\tau)$. Since $y(\tau)=1/G(\tau/24)$ and $\gamma\tau/24=\tilde\gamma(\tau/24)$ with $\tilde\gamma=\begin{pmatrix}a&b/24\\24c&d\end{pmatrix}\in\Gamma_0(576\ell)$, this is equivalent to §2.2 (using $\chi_\ell^{-1}=\chi_\ell$). Verified on 20 random matrices per $\ell\le47$. **Negative control:** with $24\ell\mid c$ but $24\nmid b$ the multiplier of $y$ is *not* $\left(\frac{\ell}{d}\right)$ in 24–29 of 30 random cases per level, so the hypothesis $24\mid b$ (equivalently the level $576\ell$ rather than $24\ell$) is needed.

### 2.5 Diamond convention

Fixed in §3.2 below: $x_{\gamma\tau}=\langle d\rangle x_\tau$ with $\langle d\rangle(E,\iota)=(E,\iota\circ[d])$, so $G\circ\langle d\rangle=\chi_\ell(d)G$ with **no inverse**. (With the convention $\langle d\rangle(E,\iota)=(E,\iota\circ[d^{-1}])$ one would get $\chi_\ell(d^{-1})$ and $\sigma=\langle -p\rangle$; the product is the same. The replacement section uses one convention throughout.)

---

## 3. Algebraicity, descent and reduction

### 3.1 Which model

The $\mu_M$-model: $Y_1(M)$, $M=576\ell\ge4$, the fine moduli scheme over $\mathbb Z[1/M]$ of pairs $(E,\iota:\mu_M\hookrightarrow E)$, with smooth proper compactification $X_1(M)$ (Deligne & Rapoport, 1973, IV–V; Katz, 1976, §1 "$\Gamma_{00}(N)^{\rm arith}$"; Gross, 1990, §2, Prop. 2.1 — *verified from the text*: "pairs $(E,\alpha)$ … $\alpha:\mu_N\to E_N$ an embedding of group schemes"; the Tate curve with $\mathrm{Id}:\mu_N\to\mathbb G_m/q^{\mathbb Z}$ gives a $\mathbb Z[1/N]$-section $\infty$ with formal parameter $q$). Analytically $\tau\mapsto(E_\tau,\iota_\tau)$, $\iota_\tau(\zeta_M)=1/M$; under $E_\tau\cong\mathbb C^\times/q^{\mathbb Z}$ this is the canonical embedding, so Fourier expansions are $q$-expansions at $\infty$.

Relation to the point model $X_1(M)'$ (pairs $(E,P)$): isomorphic over $\mathbb Z[1/M]$ via $(E,P)\mapsto(E/\langle P\rangle,\ \mu_M\cong E[M]/\langle P\rangle)$ (Weil pairing); Gross (1990, §7, p. 470) also records that $X$ and $X'$ become isomorphic over $\mathbb Z[1/N][\zeta_N]$ by the identity-type identification. Neither isomorphism commutes with the uniformisations by $\mathfrak H$ in the way one might hope, which is why rationality statements cannot be transferred verbally.

### 3.2 Field of definition of $G$ and the $q$-expansion principle

**$\mu_M$-model.** $G$ is holomorphic, non-vanishing on $\mathfrak H$, $\Gamma_1(M)$-invariant (§2.2 with $d\equiv1$), meromorphic at cusps, with $q$-expansion $q^{\ell-1}\prod(1-q^{24\ell n})/(1-q^{24n})\in q^{\ell-1}\mathbb Z[[q]]$. Descent theorem used: *the cusp $\infty$ and its formal parameter $q$ are $\mathbb Q$-rational*; hence for $\sigma\in\mathrm{Gal}(\overline{\mathbb Q}/\mathbb Q)$, $G^\sigma-G$ has zero expansion at $\infty$ and vanishes. So $G\in\mathbb Q(X_1(M))$. (Replacement section, Lemma 7.4.)

**Point model — the note's assertion verified, not assumed.** In $X_1(M)'$ the cusp $(\mathrm{Tate}(q),\zeta_M)$ is only a $\mathbb Z[1/M,\zeta_M]$-section (Conrad, n.d., Ex. 2.3: "for the cusp ∞ we have only obtained it as a section over $\mathbb Z[1/N,\zeta_N]$"; Loeffler, n.d., §3.5: "$Y_1(N)$ is not characterised over $\mathbb Q$ by having $q$-expansions" in $\mathbb Q((q))$). $\sigma_a$ moves $\infty$ to $(\mathrm{Tate}(q),\zeta_M^a)=\langle a\rangle'\infty$, so the Galois argument gives $G^{\sigma_a}=\chi_\ell(a)^{-1}G$: $G$ is defined over the fixed field of $\ker\chi_\ell$, i.e. over $\mathbb Q(\sqrt\ell)$, and its reduction over $\mathbb F_p(\sqrt\ell)\subseteq\mathbb F_{p^2}$. **The note's parenthetical claim is correct.** It is also unnecessary once the $\mu_M$-model is used, and in either model the $p^2$-Frobenius fixes the field of definition of $\overline G$, so the Frobenius computation goes through verbatim.

### 3.3 Extension as an invertible function over $\mathbb Z_{(p)}$ (the repair suggested in the brief)

1. $D_\ell$ is a unit on $Y_0(\ell)_{\mathbb Z[1/\ell]}$ by its moduli definition (§1): $\Delta(E,\omega)$ is a unit on any base for any elliptic curve.
2. $\delta:(E,\iota)\mapsto(E/\iota(\mu_{24}),\ \iota(\mu_{24\ell})/\iota(\mu_{24}))$ is a $\mathbb Z[1/M]$-morphism $Y_1(M)\to Y_0(\ell)$; on $\mathbb C$-points it is $\tau\mapsto24\tau$ (multiplication by 24 maps $E_\tau\to E_{24\tau}$ with kernel $\langle1/24\rangle=\iota_\tau(\mu_{24})$ and carries $\langle 1/(24\ell)\rangle$ onto $\langle1/\ell\rangle$). Hence $G^{24}=\delta^*D_\ell^{-1}$ in $\mathbb Q(X_1(M))$ (equal on $\mathbb C$-points). **Verified moduli-theoretically; surjectivity on $\overline{\mathbb F}_p$-points is constructed explicitly** (replacement Lemma 7.6): given $(E,C)$, take $E_1=E/K$ for a cyclic $K$ of order 24 and a cyclic $Z\subset E_1$ of order $M$ with $Z[24]=E[24]/K$ and image $\ell$-part $C$.
3. $R=\mathcal O(Y_1(M)_{\mathbb Z_{(p)}})$ is a normal domain (smooth over $\mathbb Z_{(p)}$; flat with integral generic fibre). $G\in\mathrm{Frac}(R)$ is a root of the monic $T^{24}-F$, $F=\delta^*D_\ell^{-1}\in R^\times$. So $G\in R$ and $G^{-1}=G^{23}F^{-1}\in R$.

**What this proves:** $\overline G\in\mathcal O(Y_1(M)_{\mathbb F_p})^\times$, an $\mathbb F_p$-rational function, with $\overline G\circ\langle d\rangle=\chi_\ell(d)\overline G$ and $\overline G^{24}=\delta^*\overline D_\ell^{-1}$ (identities in $R$ reduce). **What it still imports:** existence and smoothness of the $\mu_M$-model with its $\mathbb Z[1/M]$-rational cusp (DR/KM/Katz/Gross), the identification of the complex points with $\Gamma_1(M)\backslash\mathfrak H$ compatible with the $\mu_M$-structure (standard; recomputed in Lemma 7.3), representability of $\langle d\rangle$ and $\delta$ over $\mathbb Z[1/M]$. The note's "all cusps" formulation is *also* correct (divisor argument on the regular arithmetic surface with irreducible special fibre, where the expansion at $\infty$ alone shows the vertical multiplicity is 0), but it was not carried out; the monic-equation argument is shorter and is the one adopted.

---

## 4. Supersingular lift and Frobenius

### 4.1 Deuring models without changing the point

Let $\tilde x=(E_1,\iota)$ be any lift. $E_1$ is isogenous to $E$ (through $\delta$), hence supersingular. Replacing $(E_1,\iota)$ by an isomorphic pair does not change the geometric point of the fine moduli scheme nor $\overline G(\tilde x)$. **Claim:** every supersingular $j$ has a model over $\mathbb F_{p^2}$ with $\pi_{p^2}=[-p]$. *Proof recorded in Lemma 7.8:* for any model over $\mathbb F_{p^2}$, $F:E\to E^{(p)}$ and $V:E^{(p)}\to E$ are both purely inseparable of degree $p$, so $F^{(p)}=u\circ V$ with $u\in\mathrm{Aut}(E)$ and $\pi_{p^2}=F^{(p)}F=u\,[p]$. For $j\ne0,1728$, $u=\pm1$ and a quadratic twist flips the sign; for $j=0$ ($p\equiv2\bmod3$) and $j=1728$ ($p\equiv3\bmod4$) the curves $y^2=x^3+1$, $y^2=x^3+x$ over $\mathbb F_p$ have trace 0, so $\pi_{p^2}=\pi_p^2=[-p]$ (Deuring, 1941; Waterhouse, 1969; Ono, 2026, Lemma 4.3). The level structure $\iota$ is **not** required to be $\mathbb F_{p^2}$-rational, and in general it is not (it is defined over $\mathbb F_{p^{2r}}$, $r$ the order of $-p^{-1}$ in $(\mathbb Z/M)^\times$). The "24-isogenous" phrase of the note is replaced by "supersingular".

### 4.2 Three actions distinguished

* **Frobenius on points.** $\sigma\in\mathrm{Gal}(\overline{\mathbb F}_p/\mathbb F_{p^2})$, $u\mapsto u^{p^2}$, acts on $E_1(\overline{\mathbb F}_p)$ through the $\mathbb F_{p^2}$-structure, i.e. as the endomorphism $\pi_{E_1}=[-p]$; on $\mu_M(\overline{\mathbb F}_p)$ as $\zeta\mapsto\zeta^{p^2}$.
* **Galois action on the level structure.** $\iota^\sigma=\sigma_{E_1}\circ\iota\circ\sigma_{\mu_M}^{-1}$, so $\iota^\sigma(\zeta)=[-p]\iota(\zeta^{p^{-2}})=[-p^{-1}]\iota(\zeta)$: $\sigma(\tilde x)=\langle -p^{-1}\rangle\tilde x$ in the $\mu_M$-convention (fixed; the point convention would give $\langle-p\rangle'$).
* **Pull-back on functions.** $\overline G$ is $\mathbb F_p$-rational, so $\overline G(\sigma\tilde x)=\sigma(\overline G(\tilde x))=\overline G(\tilde x)^{p^2}$; and $\overline G\circ\langle d\rangle=\chi_\ell(d)\overline G$.

Hence $\overline G(\tilde x)^{p^2}=\chi_\ell(-p^{-1})\overline G(\tilde x)=\chi_\ell(p)\overline G(\tilde x)$, using only *afterwards* that $\chi_\ell$ is even and quadratic. Because $\overline G$ is a unit, $\overline G(\tilde x)^{p^2-1}=\left(\frac{\ell}{p}\right)$ — **with no coefficient-field factor**: the only Galois action on coefficients is trivial because $\overline G$ is defined over $\mathbb F_p$ (and would still be trivial for $\sigma$ if $\overline G$ were only defined over $\mathbb F_{p^2}$, as in the point model).

### 4.3 Passage to $D_\ell(x)^k$

$\overline G(\tilde x)^{24}=\overline D_\ell(\delta\tilde x)^{-1}=D_\ell(x)^{-1}$, so $D_\ell(x)^k=\overline G(\tilde x)^{-24k}=\overline G(\tilde x)^{-(p^2-1)}=\left(\frac{\ell}{p}\right)$. For $\ell=N\in\{2,3,5,7,13\}$, $D_N=u_N^{N-1}$ and $(N-1)k=(p^2-1)/a_N$.

**$\ell=2,3$, small $p$, $j=0,1728$.** The argument is uniform: $M=576\ell$ is prime to $p\ge5$ for every $\ell\ne p$; the fine moduli scheme $Y_1(M)$ has no stacky points, so $j=0,1728$ cause no difficulty; $D_\ell(x)$ is defined by the moduli formula regardless of $\mathrm{Aut}(E,C)$. Computationally (§8) the identity was verified at **every** geometric supersingular point of $X_0(\ell)$ for all $\ell\le47$, $5\le p\le199$, $p\ne\ell$, including all points over $j=0$ and $j=1728$ and the cases $\ell=2,3$ with $p=5,7$.

A consistency remark that the lemma predicts and Ono's Remark 4 observes: $\overline G(\tilde x)\in\mathbb F_{p^4}\setminus\mathbb F_{p^2}$ exactly when $\left(\frac{\ell}{p}\right)=-1$ (e.g. $p=11,\ell=2$: "generate $\mathbb F_{11^4}$").

---

## 5. The immediate corollary (constancy of $c(E)$)

$c(E)=B(E,\omega)^{(p-1)/2}/\Delta(E,\omega)^{(p^2-1)/24}$ has weight $\tfrac{(p+1)(p-1)}2-12\cdot\tfrac{p^2-1}{24}=0$, so it is independent of $\omega$ and of the model — **invariance under isomorphism holds**. The inherited code evaluates it on $y^2=4x^3-g_2x-g_3$ with $(E_4,E_6)=(12g_2,-216g_3)$, which is the correct normalisation for $\omega=dx/y$ (it matches $c_4=12g_2$, $c_6=216g_3$, $E_6=-c_6$); any rescaling $(\lambda^4E_4,\lambda^6E_6)$ leaves $c$ unchanged anyway.

**Isogeny comparison.** Lemma `Bisog`: $B(E',\omega')=\ell\,B(E,\omega)$ for $\omega=\pi^*\omega'$ at supersingular points. The note's $q$-expansion proof is sound ($E_2-\ell E_2(\ell\tau)$ is a holomorphic weight-2 form on $\Gamma_0(\ell)$ with integral $q$-expansion; $B\equiv E_2$ mod $p$ by Kummer; $q$-expansion principle; $A=0$ at $x$; $\ell^{p-1}=1$). It is moreover a known result: Robert (1980, Théorème B/Lemme 7) as quoted in Baker (1998, Lemma 2.2): $B(E_2)=\lambda^{-(p+1)}\deg\phi\,B(E_1)$ for $\phi^*\omega_2=\lambda\omega_1$ — our case is $\lambda=1$. Verified numerically at every point of §8 (`robert_B_relation_ok`).

**Graph connectivity.** The $\ell$-isogeny graph on supersingular $j$-invariants over $\overline{\mathbb F}_p$ is connected for every prime $\ell\ne p$ (Mestre, 1986; Pizer, 1990; Kohel, 1996) — standard.

**Conclusion.** With Theorem C for one prime $\ell$: $c(E')/c(E)=\ell^{(p-1)/2}\,(\ell^{-12}D_\ell(x))^{k}=\left(\frac{\ell}{p}\right)\cdot1\cdot\left(\frac{\ell}{p}\right)=1$ along every $\ell$-isogeny, so $c$ is constant by connectivity; $c^2=\beta=-\left(\frac{-1}{p}\right)$ by Baker, hence $c\in\mathbb F_p$. **Corollary D is valid.** Conversely constancy of $c$ for one $\ell$ implies Theorem C for that $\ell$, and constancy for all $\ell$ is equivalent to Theorem C for all $\ell$ (given Lemma `Bisog`). **Alternative route:** none found. Ono's Theorem 1.3 controls only $\Delta^{(p^2-1)/12}$ (12th powers); the sign of the 24th-root question is exactly what his method cannot see (his Remark 4). No independent level-one argument for the constancy of $c$ was found, so Corollary D does not currently provide a second proof of Theorem C. (The conjectural evaluation $c_p=\left(\frac6p\right)\left(\frac{p-1}2\right)!$ was not investigated, as instructed; no literature statement of it was encountered.)

---

## 6. Literature and priority audit

| Source (version inspected) | Where | Exact statement / normalisation | Relation to our identity |
|---|---|---|---|
| Ono, K. *Modular forms for chromatic homotopy: Supersingular congruences*, arXiv:2509.16175 **v2, 3 July 2026** (arXiv abs page lists v2 as current; PDF header "arXiv:2509.16175v2 [math.AT] 3 Jul 2026"; v1 (19 Sep 2025) has none of the items below). | Thm 1.2 | $R_\ell(\tilde P)^m=1$, $m=(p^2-1)/12$, $R_\ell=V_\ell(\Delta)/\Delta=\Delta(\ell\tau)/\Delta(\tau)=D_\ell^{-1}$, every supersingular point of $X_0(\ell)$, $p\ge5$, $\ell\ne p$. | The square of our identity. |
| | Thm 1.3 | $\kappa(E)=\Delta(E,\omega)^{(p^2-1)/12}=(-1)^{(p+1)/2}$ for $E/\mathbb F_{p^2}$ supersingular with $\pi_E=[-p]$, $\omega$ $\mathbb F_{p^2}$-rational. | Different object (weight $p^2-1$ on Deuring models); **verified numerically here** (`deuring_kappa_ok`). With Baker it gives $B(E,\omega)^{p-1}=1$ on Deuring models (also verified). |
| | §4.1–4.2, Lemma 4.3, Lemma 4.4 | Vélu-normalised $\Delta^{[\ell]}(E,C,\omega)=\ell^{-12}\Delta(E',\omega')$; $R_\ell(\tilde P)^m=\kappa(E')/\kappa(E)$; Deuring models. | Same moduli normalisation as ours (so $R_\ell=D_\ell^{-1}$ exactly). |
| | Remark 4 | $(p^2-1)/24$ power can be $-1$: $p=11,\ell=2$, $R_2\in\{6,7,2\}$; values of $g_\ell=\eta(\ell z)/\eta(z)$ need not lie in $\mathbb F_{p^2}$; proofs descending $\Delta^{1/24}$ or $\Delta^{1/12}$ to $\mathbb F_{p^2}$ must fail. | **Does not state our identity, nor any formula for the sign.** Our result requires a substantive additional argument (diamond characters on $X_1(576\ell)$), and is consistent with every example there. |
| Baker, A. (1998). *Acta Arith.* 86(1), 91–100 (author's copy read). | Thm 1.4 | $B^{p-1}\equiv-\left(\frac{-1}p\right)\Delta^{(p^2-1)/12}\pmod{(p,A)}$, $B=E_{p+1}$, $A=E_{p-1}$. | Imported as Fact I3; **verified numerically** at every point of §8. No $(p^2-1)/24$ or $B^{(p-1)/2}$ statement. |
| | §2 | For $E_1,E_2$ separably isogenous over $\mathbb F_{p^2}$: $\left(\left(\frac{-1}p\right)\Delta(E_i)\right)^{(p^2-1)/12}$ coincide (from Gross–Landweber). | Isogeny-invariance of Ono's $\kappa$ over $\mathbb F_{p^2}$; with Ono's Lemma 4.4 it gives his Thm 1.2. Square of ours. |
| | Lemma 2.2, Cor. 2.3 (= Robert 1980, Thm B / Lemme 7) | $B(E_2)=\lambda^{-(p+1)}\deg\phi\,B(E_1)$ if $\phi^*\omega_2=\lambda\omega_1$; $B(E_2)^{p-1}=\lambda^{-(p^2-1)}B(E_1)^{p-1}$. | **Precedent for the note's Lemma `Bisog`** (which should cite it). Does not involve $\Delta$-ratios. |
| | (0.1) "Gross–Landweber congruence" | $u_2\equiv\left(\frac{-1}p\right)\Delta^{(p^2-1)/12}\bmod(p,u_1)$, attributed to Gross & Landweber in the text, cited as Landweber (1988, LNM 1326, 69–93). | Source of the $(p^2-1)/12$ statements; not the $/24$ one. |
| Robert, G. (1980). *Invent. Math.* 61, 103–158. | Thm B / Lemme 7 | Known only through Baker's quotation. | **Full text not accessible in this session** (GDZ link not fetchable). Must be inspected for any half-exponent statement; flagged. |
| Kaneko & Zagier (1998), §10, full text read. | (35)–(40) | (39) de Shalit's signed residue formula at level 1; (40) $ss_p'(j)^{p-1}=\dots$ (proved by Baker). | Exponents $p\pm1$ only; no $/24$, no eta quotients, no level $N$. |
| de Shalit (1994) | Thm 1, Cor. 3 | level-1 signed formula via $p$-adic periods. | Not about $D_\ell$. |
| Landweber (1988), LNM 1326, 69–93 | — | Congruences for Legendre polynomials / $u_2$ | Not inspected directly (title/pages from Baker's bibliography). |
| Behrens (2009), *Geom. Topol.* 13, 319–357; Larson (2020), *Topology Appl.* 273, 107094 | — | Divided $\beta$ family; Larson's conjecture (proved by Ono v2 Thm 1.1). | Not inspected beyond Ono's bibliography; the brief's "Behrens and Larson" appears to mean these two separate works. |
| Gordon & Hughes (1993); Newman (1959); Ono (2004) Thm 1.64; Ligozat (1975) | — | Eta-quotient transformation law with character $\left(\frac{(-1)^ks}{d}\right)$. | Citation correct as used (§2.1); replaced by a complete derivation. |
| Knopp (1970) Ch. 4 §4.1; Apostol (1990) Thm 3.4; Rademacher (1931) | — | Closed form / Dedekind-sum form of the eta multiplier. | Import for §2.2; cross-checked exactly. |
| Katz (1976) §1; Gross (1990) §2 (read); Deligne–Rapoport (1973); Katz–Mazur (1985); Conrad (n.d.) handout (read); Loeffler (n.d.) §3.5 (read) | — | $\mu_M$-model, rational cusp, $q$-expansion principle; point-model caveat. | Imports for §3. |
| Deuring (1941); Waterhouse (1969) | — | Deuring models / Frobenius $\pi=pu$. | Import for §4.1 (with an elementary proof recorded). |
| Mestre (1986); Pizer (1990); Kohel (1996) | — | Connectivity of the supersingular $\ell$-isogeny graph. | Import for §5. |
| Betina–Lecouturier (TAMS 2019 final text); Robert (1980) full text; Landweber (1988); Behrens (2009); Larson (2020); Sakai (2011) | — | — | **Not inspected / inaccessible in this session.** |

**Separation of correctness from priority.** Correctness of Theorem C and Corollary D is established above modulo the listed imports. On priority: the exact signed identity (and equivalently the constancy of $c(E)$) was not found in Ono v2, Baker, Kaneko–Zagier, de Shalit, or the eta-character literature; Ono v2 explicitly stops short of it. The closest statements are the $(p^2-1)/12$ results (Gross–Landweber → Baker §2 → Ono Thm 1.2). This is **not** a proof of novelty: Robert (1980) and the homotopy-theoretic literature (Behrens, Larson, Landweber) were not read in full.

---

## 7. Dependency table

| Step | Statement | Status | Source |
|---|---|---|---|
| 1 | $G$ holomorphic, non-vanishing on $\mathfrak H$, $q$-expansion in $q^{\ell-1}\mathbb Z[[q]]$ | proved (trivial) | — |
| 2 | Petersson/Knopp closed form of $\nu_\eta$ | **import** | Knopp 1970 Ch.4 §4.1; Apostol 1990 Thm 3.4; verified exactly vs Dedekind sums (400 matrices) and numerics |
| 3 | $G(\gamma\tau)=\left(\frac{\ell}{d}\right)G(\tau)$ on $\Gamma_0(576\ell)$ | proved (§2.2) | from 2; verified exactly for $\ell\le47$, all classes of $d$ |
| 4 | $\chi_\ell$ = Kronecker character of $\mathbb Q(\sqrt\ell)$, even, quadratic, $\chi_\ell(p)=\left(\frac{\ell}{p}\right)$ | proved (reciprocity) | verified exhaustively mod $576\ell$ |
| 5 | $\mu_M$-model of $Y_1(M)$, $X_1(M)$: fine, smooth over $\mathbb Z[1/M]$, cusp $\infty$ a $\mathbb Z[1/M]$-section with parameter $q$, $\langle d\rangle$ and $\delta$ defined over $\mathbb Z[1/M]$, special fibre irreducible | **import** | DR 1973; KM 1985; Katz 1976 §1; Gross 1990 §2 |
| 6 | $x_{\gamma\tau}=\langle d\rangle x_\tau$; $f\circ\langle d\rangle=\chi(d)f$ | proved (lattice computation) | — |
| 7 | $q$-expansion principle ⇒ $G\in\mathbb Q(X_1(M))$ | proved (2 lines) from 5 | — |
| 8 | $D_\ell$ moduli-theoretic unit on $Y_0(\ell)_{\mathbb Z[1/\ell]}$ with expansion $\Delta(q)/\Delta(q^\ell)$ | proved (Tate curve) | — |
| 9 | $\delta$ is $\tau\mapsto24\tau$; $G^{24}=\delta^*D_\ell^{-1}$; $\delta$ surjective on $\overline{\mathbb F}_p$-points | proved | — |
| 10 | $G\in\mathcal O(Y_1(M)_{\mathbb Z_{(p)}})^\times$ | proved (normality + monic equation) from 5,7,8,9 | — |
| 11 | Deuring model for every supersingular $j$; subgroups rational; quotients keep $\pi=[-p]$ | proved (Lemma 7.8) modulo existence of trace-0 curves at $j=0,1728$ | Deuring 1941; Waterhouse 1969 |
| 12 | $\sigma(\tilde x)=\langle -p^{-1}\rangle\tilde x$ | proved | fine moduli (5) |
| 13 | $\overline G(\tilde x)^{p^2-1}=\left(\frac{\ell}{p}\right)$ | proved from 3,4,6,10,12 | — |
| 14 | $D_\ell(x)^k=\left(\frac{\ell}{p}\right)$ | proved from 9,13 | — |
| 15 | Lemma `Bisog`: $B(E')=\ell B(E)$, $\Delta(\ell\tau)(x)=\ell^{-12}\Delta(E',\omega')$ | proved in note; also **known** | Robert 1980 Lemme 7 via Baker 1998 Lemma 2.2 |
| 16 | Baker's congruence $c^2=-\left(\frac{-1}p\right)$ | **import** | Baker 1998 Thm 1.4 (verified numerically) |
| 17 | connectivity of $\ell$-isogeny graphs | **import** | Mestre 1986; Pizer 1990; Kohel 1996 |
| 18 | Corollary D | proved from 14,15,16,17 | — |

---

## 8. Targeted reproducible checks

`code/velu_sign_check.py` (python-flint 0.9.0) computes, **without eta functions or Hauptmoduln**, for every supersingular $j\in\mathbb F_{p^2}$, a model with scalar $p^2$-Frobenius, all $\ell+1$ kernel polynomials from the $\ell$-division polynomial, Vélu's normalised quotient $E'$, and $r=\Delta(E)/\Delta(E')=\ell^{-12}D_\ell(E,C)$. Checks per point: $r^{(p^2-1)/12}=1$ (Ono), $r^{(p^2-1)/24}=\left(\frac{\ell}{p}\right)$ (Theorem C), $B(E')=\ell B(E)$ (Robert/Baker, with $B=E_{p+1}\bmod p$ recomputed from scratch by linear algebra on $q$-expansions), Baker's congruence, $c(E')=c(E)$, $j(E')$ supersingular, $A(E)=0$; per $(\ell,p)$: $c$ constant over all supersingular $j$; for $N\in\{2,3,5,7,13\}$: the multiset $\{D_N(E,C)\}$ equals $\{u^{N-1}:P_N(u)=ju^N\}$, which ties the Vélu normalisation to the note's $u_N^{N-1}=\Delta/\Delta(N\tau)$; on Deuring models: Ono's $\kappa(E)=(-1)^{(p+1)/2}$ and $B(E,\omega)\in\mathbb F_p$.

**Sweep:** levels ℓ ∈ {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}, primes 5 ≤ p ≤ 199, p ≠ ℓ: 647 pairs, **127541 geometric supersingular points (E, C)** (7709 over j = 0, 7701 over j = 1728). Theorem C failures: none. Wall time 3804.4 s.

| ℓ | pairs | p range | points | points j=0 | points j=1728 | D_ℓ^k ∈ {±1} and = (ℓ/p) | Ono (p²−1)/12 power = 1 | B(E′)=ℓB(E) | Baker | c constant | Hauptmodul match | κ (Ono 1.3) | B ∈ F_p (Deuring) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 44 | 5–199 | 1125 | 69 | 69 | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ |
| 3 | 44 | 5–199 | 1500 | 92 | 92 | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ |
| 5 | 43 | 7–199 | 2244 | 132 | 138 | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ |
| 7 | 43 | 5–199 | 2992 | 184 | 176 | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ |
| 11 | 43 | 5–199 | 4476 | 264 | 264 | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | n/a | all ✓ | all ✓ |
| 13 | 43 | 5–199 | 5236 | 322 | 322 | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ |
| 17 | 43 | 5–199 | 6714 | 396 | 414 | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | n/a | all ✓ | all ✓ |
| 19 | 43 | 5–199 | 7460 | 460 | 440 | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | n/a | all ✓ | all ✓ |
| 23 | 43 | 5–199 | 8928 | 528 | 528 | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | n/a | all ✓ | all ✓ |
| 29 | 43 | 5–199 | 11160 | 660 | 690 | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | n/a | all ✓ | all ✓ |
| 31 | 43 | 5–199 | 11904 | 736 | 704 | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | n/a | all ✓ | all ✓ |
| 37 | 43 | 5–199 | 14136 | 874 | 874 | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | n/a | all ✓ | all ✓ |
| 41 | 43 | 5–199 | 15582 | 924 | 966 | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | n/a | all ✓ | all ✓ |
| 43 | 43 | 5–199 | 16324 | 1012 | 968 | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | n/a | all ✓ | all ✓ |
| 47 | 43 | 5–199 | 17760 | 1056 | 1056 | all ✓ | all ✓ | all ✓ | all ✓ | all ✓ | n/a | all ✓ | all ✓ |

Pairs with (ℓ/p) = −1 (so D_ℓ^k = −1 at every point): 346 of 647; with (ℓ/p) = +1: 301. In every pair the set of values of D_ℓ^k over all points is a single element, equal to (ℓ/p).

Small cases (ℓ ∈ {2,3}, p ∈ {5,7,11,13}):

| ℓ | p | points | D_ℓ^k values | (ℓ/p) | j=0 pts | j=1728 pts |
|---|---|---|---|---|---|---|
| 2 | 5 | 3 | ['4'] | -1 | 3 | 0 |
| 2 | 7 | 3 | ['1'] | +1 | 0 | 3 |
| 2 | 11 | 6 | ['10'] | -1 | 3 | 3 |
| 2 | 13 | 3 | ['12'] | -1 | 0 | 0 |
| 3 | 5 | 4 | ['4'] | -1 | 4 | 0 |
| 3 | 7 | 4 | ['6'] | -1 | 0 | 4 |
| 3 | 11 | 8 | ['1'] | +1 | 4 | 4 |
| 3 | 13 | 4 | ['1'] | +1 | 0 | 0 |

`code/eta_multiplier_audit.py`: see §2 (exact Dedekind sums vs closed form vs numerics; character of $G$ for $\ell\le47$ on random $\gamma\in\Gamma_0(576\ell)$ covering all unit classes of $d$ modulo the conductor, both signs; triviality on $\Gamma_1(576\ell)$; evenness/quadraticity/identification with the Kronecker character exhaustively mod $576\ell$; the note's Lemma `mult`; negative control).

Reproduce: `pip install python-flint==0.9.0 mpmath`; `python3 code/eta_multiplier_audit.py` (≈10 min, Dedekind sums are exact); `python3 code/velu_sign_check.py 31 2,3,5,7,11,13` (seconds) or `python3 code/velu_sign_check.py 199 2,3,5,7,11,13,17,19,23,29,31,37,41,43,47` (≈1 h). Every check is a boolean in `results/*.json`.

---

## 9. Residual points for a specialist

1. The imports in rows 2, 5, 11, 16, 17 of §7 are standard but were cited at section level (Knopp §4.1; DR IV–V; Gross §2 Prop. 2.1, verified from the text); the exact theorem numbers in Deligne–Rapoport and Katz–Mazur for the $\mu_M$-model and its Tate-curve cusp were not checked line by line.
2. Robert (1980) should be read in full for (a) the precise statement of Lemme 7 (to cite it for Lemma `Bisog`), and (b) any statement involving $E_{p+1}^{(p-1)/2}$ or 24th roots of discriminant ratios.
3. The replacement section assumes the note's Lemma `Bisog` (unchanged) for the final sentence about $\Delta(\ell\tau)(x)$; the moduli definition (7.2) makes that sentence a definition rather than a lemma.
4. No new moonshine claims, no large-prime survey, and no investigation of Conjecture E were undertaken (as instructed).

---

## 10. Files

```
AUDIT_REPORT.md / .pdf            this report
README.md                         layout, reproduction, verdict in one paragraph
replacement_section/
    eta_section_replacement.tex   drop-in replacement for Section 7 of the note (+ comments listing the edits to Facts I4/I5 and new bib entries)
    standalone_wrapper.tex/.pdf   compile test with the note's preamble
code/
    eta_multiplier_audit.py       §2 checks
    velu_sign_check.py            §8 checks
    make_tables.py                summary tables from the JSON
results/
    eta_multiplier_audit.json, velu_sign_checks.json, velu_sign_run.log, velu_sign_table.md
literature/
    sources_inspected.md          every source, version/URL inspected, what was read
SHA256SUMS.txt
```

---

## References (APA)

Apostol, T. M. (1990). *Modular functions and Dirichlet series in number theory* (2nd ed., GTM 41). Springer.

Baker, A. (1998). A supersingular congruence for modular forms. *Acta Arithmetica, 86*(1), 91–100. https://doi.org/10.4064/aa-86-1-91-100 (author's copy: https://www.maths.gla.ac.uk/~ajb/dvi-ps/modforms.pdf)

Behrens, M. (2009). Congruences between modular forms given by the divided β family in homotopy theory. *Geometry & Topology, 13*(1), 319–357.

Conrad, B. (n.d.). *Math 248B: Algebraic theory of q-expansions* [Course handout]. Stanford University. https://virtualmath1.stanford.edu/~conrad/248BPage/handouts/qexp.pdf

de Shalit, E. (1994). Kronecker's polynomial, supersingular elliptic curves, and p-adic periods of modular curves. *Contemporary Mathematics, 165*, 135–148.

Deligne, P., & Rapoport, M. (1973). Les schémas de modules de courbes elliptiques. In *Modular functions of one variable II* (LNM 349, pp. 143–316). Springer.

Deuring, M. (1941). Die Typen der Multiplikatorenringe elliptischer Funktionenkörper. *Abhandlungen aus dem Mathematischen Seminar der Universität Hamburg, 14*, 197–272.

Gordon, B., & Hughes, K. (1993). Multiplicative properties of η-products II. *Contemporary Mathematics, 143*, 415–430.

Gross, B. H. (1990). A tameness criterion for Galois representations associated to modular forms (mod p). *Duke Mathematical Journal, 61*(2), 445–517.

Kaneko, M., & Zagier, D. (1998). Supersingular j-invariants, hypergeometric series, and Atkin's orthogonal polynomials. In *Computational perspectives on number theory* (AMS/IP Stud. Adv. Math. 7, pp. 97–126). AMS. (Full text: https://people.mpim-bonn.mpg.de/zagier/files/ams/stud-adv-math/7/fulltext.pdf)

Katz, N. M. (1976). p-adic interpolation of real analytic Eisenstein series. *Annals of Mathematics, 104*, 459–571.

Katz, N. M., & Mazur, B. (1985). *Arithmetic moduli of elliptic curves* (Annals of Mathematics Studies 108). Princeton University Press.

Knopp, M. I. (1970). *Modular functions in analytic number theory*. Markham.

Kohel, D. (1996). *Endomorphism rings of elliptic curves over finite fields* [Doctoral dissertation, UC Berkeley].

Landweber, P. S. (1988). Supersingular elliptic curves and congruences for Legendre polynomials. In *Elliptic curves and modular forms in algebraic topology* (LNM 1326, pp. 69–93). Springer.

Larson, D. M. (2020). Explicit modular forms from the divided beta family. *Topology and its Applications, 273*, 107094.

Ligozat, G. (1975). Courbes modulaires de genre 1. *Bulletin de la SMF, Mémoire 43*.

Loeffler, D. (n.d.). *Modular curves* [Lecture notes]. University of Warwick. https://warwick.ac.uk/fac/sci/maths/people/staff/david_loeffler/teaching/modularcurves/lecture_notes.pdf

Mestre, J.-F. (1986). La méthode des graphes: Exemples et applications. In *Proceedings of the International Conference on Class Numbers and Fundamental Units of Algebraic Number Fields* (pp. 217–242). Nagoya University.

Newman, M. (1959). Construction and application of a class of modular functions II. *Proceedings of the London Mathematical Society (3), 9*, 373–387.

Ono, K. (2004). *The web of modularity: Arithmetic of the coefficients of modular forms and q-series* (CBMS 102). AMS.

Ono, K. (2026). *Modular forms for chromatic homotopy: Supersingular congruences* (arXiv:2509.16175v2, 3 July 2026). https://arxiv.org/abs/2509.16175

Pizer, A. (1990). Ramanujan graphs and Hecke operators. *Bulletin of the AMS (N.S.), 23*(1), 127–137.

Robert, G. (1980). Congruences entre séries d'Eisenstein, dans le cas supersingulier. *Inventiones Mathematicae, 61*, 103–158. (Not accessible in full in this session.)

Waterhouse, W. C. (1969). Abelian varieties over finite fields. *Annales Scientifiques de l'École Normale Supérieure (4), 2*, 521–560.
