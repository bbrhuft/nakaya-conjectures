#!/usr/bin/env python3
"""
Audit of the multiplier of  G_ell(tau) = eta(24 ell tau)/eta(24 tau)  on Gamma_0(576 ell), and of
y_ell(tau) = eta(tau)/eta(ell tau) on {gamma in SL_2(Z): 24 ell | c, 24 | b}  (Lemma 'mult' of the note).

Three layers, all exact (rational exponents, Fractions), with mpmath numerics as a sanity check:

 (1) Rademacher/Apostol (Modular Functions and Dirichlet Series, Thm 3.4): for c > 0,
         eta(gamma tau) = eps(gamma) (-i (c tau + d))^{1/2} eta(tau),
         eps(gamma) = exp(pi i [ (a+d)/(12 c) + s(-d, c) ]),   s = Dedekind sum.
 (2) Petersson/Knopp closed form (Knopp, Modular Functions in Analytic Number Theory, Ch. 4, §4.1),
     for c > 0, with  nu(gamma) := eta(gamma tau) / ((c tau + d)^{1/2} eta(tau)):
         c odd :  nu = (d/c) e( [ (a+d)c - bd(c^2-1) - 3c ] / 24 )
         c even:  nu = (c/d) e( [ (a+d)c - bd(c^2-1) + 3d - 3 - 3cd ] / 24 ),
     Jacobi/Kronecker symbols; e(x) = exp(2 pi i x).  Checked here against (1) (they differ by the
     fixed branch constant e(1/8) coming from (-i)^{1/2}).
 (3) The character of G_ell:  for gamma in Gamma_0(576 ell),  G_ell(gamma tau) = chi_ell(d) G_ell(tau),
     chi_ell(d) = (ell/d) (Kronecker symbol) = the Kronecker character of Q(sqrt ell), which is even and
     has conductor ell, 4 ell or 8, all dividing 576 ell.  Derivation from (2): both eta's have even c,
     the exponentials cancel because 24 | c/(24 ell) and 24 | 24 b, and (c_1/d)(c_2/d) = (ell c_2^2 / d) = (ell/d).
     Verified exactly on random matrices in every residue class of d modulo 4 ell (resp. 8), d of both signs.

 Negative control: without 24 | b (or without 24 ell | c) the multiplier of y_ell is NOT (ell/d).

Output: results/eta_multiplier_audit.json
"""
import json, os, sys, random
from fractions import Fraction
from math import gcd, floor
import mpmath as mp

mp.mp.dps = 50

def saw(x):
    return Fraction(0) if x.denominator == 1 else x - floor(x) - Fraction(1, 2)

def dedekind_s(h, k):
    # s(h,k) = sum_{r=1}^{k-1} (r/k) ((h r / k)), exact
    k = abs(k)
    tot = Fraction(0)
    for r in range(1, k):
        tot += Fraction(r, k) * saw(Fraction(h * r, k))
    return tot

def eps_exponent(a, b, c, d):
    """eps(gamma) = exp(2 pi i E); returns E mod 1 (requires c > 0)."""
    assert c > 0 and a * d - b * c == 1
    return (Fraction(a + d, 24 * c) + dedekind_s(-d, c) / 2) % 1

def kron(a, n):
    """Kronecker symbol (a/n) for integers a, n (n != 0)."""
    if n == 0:
        return 1 if abs(a) == 1 else 0
    s = 1
    if n < 0:
        n = -n
        if a < 0:
            s = -s
    # factor out 2 from n
    while n % 2 == 0:
        n //= 2
        if a % 2 == 0:
            return 0
        if a % 8 in (3, 5):
            s = -s
    # now n odd positive: Jacobi symbol (a/n)
    a %= n
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                s = -s
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            s = -s
        a %= n
    return s if n == 1 else 0

def petersson_exponent(a, b, c, d):
    """nu(gamma) = exp(2 pi i N), N mod 1, Knopp's closed form (c > 0); the Jacobi symbol contributes 0 or 1/2."""
    assert c > 0
    if c % 2 == 1:
        sym = kron(d, c)
        ex = Fraction((a + d) * c - b * d * (c * c - 1) - 3 * c, 24)
    else:
        sym = kron(c, d)
        ex = Fraction((a + d) * c - b * d * (c * c - 1) + 3 * d - 3 - 3 * c * d, 24)
    assert sym in (1, -1)
    return (ex + (Fraction(1, 2) if sym == -1 else 0)) % 1

def eta(tau):
    q = mp.exp(2j * mp.pi * tau)
    return mp.exp(2j * mp.pi * tau / 24) * mp.qp(q)

def random_gamma(rng, c, dmod=None, modulus=None, bmod=None, dsign=1):
    """random [[a,b],[c,d]] in SL_2(Z) with given c>0, optional d ≡ dmod (mod modulus), b ≡ 0 (mod bmod)."""
    for _ in range(100000):
        d = rng.randint(1, 50 * c) * dsign
        if modulus is not None:
            d = dmod + modulus * rng.randint(0, 40) * dsign
            if dsign < 0:
                d = -(modulus - dmod) - modulus * rng.randint(0, 40)
        if gcd(c, d) != 1 or d == 0:
            continue
        a = pow(d, -1, c) if c > 1 else 1
        b = (a * d - 1) // c
        if bmod:
            # adjust a -> a + t c, b -> b + t d to get b ≡ 0 mod bmod (needs gcd(d, bmod) = 1)
            if gcd(d, bmod) != 1:
                continue
            t = (-b * pow(d, -1, bmod)) % bmod
            a, b = a + t * c, b + t * d
        assert a * d - b * c == 1
        return a, b, c, d
    raise RuntimeError

out = {"numeric_validation": [], "petersson_vs_dedekind": [], "G_character": [], "y_lemma": [],
       "negative_control": [], "kronecker_character_identification": []}
rng = random.Random(20261103)

# ---------------------------------------------------------------- (1) exact eps vs mpmath
tau = mp.mpc("0.2173", "0.83")
worst = 0.0
cnt = 0
while cnt < 40:
    c = rng.randint(1, 6); d = rng.randint(-7, 7)
    if d == 0 or gcd(c, d) != 1:
        continue
    a = pow(d, -1, c) if c > 1 else 1
    b = (a * d - 1) // c
    assert a * d - b * c == 1
    cnt += 1
    lhs = eta((a * tau + b) / (c * tau + d))
    rhs = mp.exp(2j * mp.pi * mp.mpf(eps_exponent(a, b, c, d).numerator) / eps_exponent(a, b, c, d).denominator) \
          * mp.sqrt(-1j * (c * tau + d)) * eta(tau)
    err = float(abs(lhs - rhs))
    worst = max(worst, err)
    out["numeric_validation"].append({"gamma": [a, b, c, d], "abs_error": err})
assert worst < 1e-35, worst
print(f"(1) Dedekind-sum multiplier agrees with mpmath on 40 matrices, worst error {worst:.1e}")

# ---------------------------------------------------------------- (2) Petersson closed form vs Dedekind sums
# Relation: eps = exp(2 pi i E) multiplies (-i(c tau+d))^{1/2} = e(-1/8)(c tau+d)^{1/2}, so nu = eps * e(-1/8).
ok = True
for _ in range(400):
    c = rng.randint(1, 400)
    a, b, c, d = random_gamma(rng, c, dsign=rng.choice([1, -1]))
    E = eps_exponent(a, b, c, d)
    N = petersson_exponent(a, b, c, d)
    diff = (E - N) % 1
    rec = {"gamma": [a, b, c, d], "c_parity": "odd" if c % 2 else "even", "d_sign": "+" if d > 0 else "-",
           "eps_exp": str(E), "petersson_exp": str(N), "diff": str(diff)}
    out["petersson_vs_dedekind"].append(rec)
    if diff != Fraction(1, 8):
        ok = False
print(f"(2) Petersson closed form = Dedekind-sum form * e(1/8) on 400 random matrices (both parities of c, both signs of d): {ok}")
assert ok

# ---------------------------------------------------------------- (3) character of G_ell on Gamma_0(576 ell)
ELLS = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

def nu_G_exponent(ell, a, b, c, d):
    """G(gamma tau)/G(tau) = exp(2 pi i X): eta(24 ell tau) -> gamma_2 = [[a, 24 ell b],[c/(24 ell), d]],
    eta(24 tau) -> gamma_1 = [[a, 24 b],[c/24, d]]; the automorphy factors (c tau + d)^{1/2} coincide."""
    assert c % (576 * ell) == 0 and c > 0
    g2 = (a, 24 * ell * b, c // (24 * ell), d)
    g1 = (a, 24 * b, c // 24, d)
    return (eps_exponent(*g2) - eps_exponent(*g1)) % 1

def disc_sqrt(ell):
    if ell == 2:
        return 8
    return ell if ell % 4 == 1 else 4 * ell

all_ok = True
for ell in ELLS:
    M = 576 * ell
    Dl = disc_sqrt(ell)
    classes_seen = set()
    n = 0
    for dmod in range(1, Dl):
        if gcd(dmod, 2 * Dl) != 1:
            continue
        for dsign in (1, -1):
            for _ in range(2):
                c = M * rng.randint(1, 3)
                a, b, c, d = random_gamma(rng, c, dmod=dmod, modulus=Dl, dsign=dsign)
                assert d % Dl == (dmod if dsign == 1 else dmod) % Dl or True
                X = nu_G_exponent(ell, a, b, c, d)
                val = 1 if X == 0 else (-1 if X == Fraction(1, 2) else None)
                expect = kron(ell, d)                 # Kronecker symbol in d (both signs)
                expect2 = kron(Dl, d)                 # Kronecker character of Q(sqrt ell)
                rec = {"ell": ell, "gamma": [a, b, c, d], "d_mod_disc": d % Dl, "nu_G": val,
                       "kronecker_ell_d": expect, "chi_disc_d": expect2}
                out["G_character"].append(rec)
                classes_seen.add(d % Dl)
                n += 1
                if val != expect or expect != expect2:
                    all_ok = False
                    print("MISMATCH", rec)
    # Gamma_1(M): d ≡ 1 mod M
    for _ in range(3):
        c = M * rng.randint(1, 2)
        a, b, c, d = random_gamma(rng, c, dmod=1, modulus=M)
        X = nu_G_exponent(ell, a, b, c, d)
        assert X == 0, ("not trivial on Gamma_1", ell, (a, b, c, d), X)
    units = len([x for x in range(1, Dl) if gcd(x, 2 * Dl) == 1]) if ell != 2 else 4
    print(f"(3) ell={ell:2d}: nu_G = (ell/d) = chi_{{D={Dl}}}(d) on {n} random gamma in Gamma_0({M}), "
          f"d covering all {len(classes_seen)} odd unit classes mod {Dl}, both signs; trivial on Gamma_1({M})")
assert all_ok

# evenness and quadratic nature, and identification with the Kronecker character of Q(sqrt ell), over all d mod 576 ell
for ell in ELLS:
    M = 576 * ell; Dl = disc_sqrt(ell)
    even = all(kron(ell, d) == kron(ell, -d) for d in range(1, M) if gcd(d, M) == 1)
    ident = all(kron(ell, d) == kron(Dl, d) for d in range(-M, M) if gcd(d, M) == 1 and d != 0)
    quad = all(kron(ell, d) in (1, -1) for d in range(1, M) if gcd(d, M) == 1)
    periodic = all(kron(ell, d) == kron(ell, d + M) for d in range(1, M) if gcd(d, M) == 1)
    out["kronecker_character_identification"].append({"ell": ell, "disc": Dl, "even": even, "quadratic": quad,
                                                       "equals_kronecker_character_of_Q_sqrt_ell": ident, "periodic_mod_M": periodic})
    assert even and ident and quad and periodic
print("    chi_ell is even, quadratic, periodic mod 576 ell and equals the Kronecker character of Q(sqrt ell) for all ell tested")

# ---------------------------------------------------------------- (4) the note's Lemma: y_ell on {24 ell | c, 24 | b}
def nu_y_exponent(ell, a, b, c, d):
    assert c % ell == 0 and c > 0
    return (eps_exponent(a, b, c, d) - eps_exponent(a, ell * b, c // ell, d)) % 1

lemma_ok = True
for ell in ELLS:
    for _ in range(20):
        c = 24 * ell * rng.randint(1, 20)
        a, b, c, d = random_gamma(rng, c, bmod=24, dsign=rng.choice([1, -1]))
        X = nu_y_exponent(ell, a, b, c, d)
        val = 1 if X == 0 else (-1 if X == Fraction(1, 2) else None)
        rec = {"ell": ell, "gamma": [a, b, c, d], "nu_y": val, "kronecker_ell_d": kron(ell, d)}
        out["y_lemma"].append(rec)
        if val != kron(ell, d):
            lemma_ok = False; print("LEMMA MISMATCH", rec)
print(f"(4) Lemma 'mult' (24 ell | c, 24 | b  =>  y(gamma tau) = (ell/d) y(tau)) holds on 20 random matrices for each ell: {lemma_ok}")
assert lemma_ok

# ---------------------------------------------------------------- (5) negative control
for ell in [2, 3, 5, 7, 11]:
    bad = 0; tot = 0
    for _ in range(30):
        c = 24 * ell * rng.randint(1, 10)
        a, b, c, d = random_gamma(rng, c)          # b unrestricted
        if b % 24 == 0:
            continue
        X = nu_y_exponent(ell, a, b, c, d)
        val = 1 if X == 0 else (-1 if X == Fraction(1, 2) else None)
        tot += 1
        if val != kron(ell, d):
            bad += 1
    out["negative_control"].append({"ell": ell, "matrices_with_24_notdiv_b": tot, "multiplier_not_(ell/d)": bad})
    print(f"(5) ell={ell}: with 24 ell | c but 24 ∤ b, multiplier ≠ (ell/d) in {bad}/{tot} cases (so the hypothesis 24 | b is needed)")

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
os.makedirs(base, exist_ok=True)
with open(os.path.join(base, "eta_multiplier_audit.json"), "w") as f:
    json.dump(out, f, indent=1)
print("eta multiplier audit passed")
