"""
Check of the eta-quotient multiplier used in the proof of the Frobenius statement
      u_N(x)^{(p^2-1)/a_N} = (N/p)   at supersingular points.

  y(tau) = eta(tau)/eta(N tau),  y^{a_N} = u_N,  y(gamma tau) = nu(gamma) y(tau) on Gamma_0(N).

Dedekind/Rademacher (Apostol, Modular Functions and Dirichlet Series, Thm 3.4): for c > 0,
  eta(gamma tau) = exp(pi i [(a+d)/(12c) + s(-d,c)]) (-i(c tau + d))^{1/2} eta(tau).
Since eta(N gamma tau) = eta(gamma' (N tau)) with gamma' = [[a, N b],[c/N, d]] and the
same automorphy factor, nu(gamma) = eps(a,b,c,d)/eps(a,Nb,c/N,d) EXACTLY (rational
exponent).  We verify
  (0) the implementation against mpmath numerics for small c;
  (a) nu(gamma) = 1 for gamma = I (mod 24N);
  (b) nu(gamma) = (N/delta) (Kronecker character of Q(sqrt N)) for
      gamma = diag(delta, delta^{-1}) (mod 24N), for every unit delta mod 24N and
      several lifts each.
"""
import json, os, random, sys
from fractions import Fraction
from math import gcd, floor
import mpmath as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wr_core import LEVELS

mp.mp.dps = 40


def saw(x):
    if x.denominator == 1:
        return Fraction(0)
    return x - floor(x) - Fraction(1, 2)


def dedekind_s(h, k):
    return sum((Fraction(r, k) * saw(Fraction(h * r, k)) for r in range(1, k)), Fraction(0))


def eps_exponent(a, b, c, d):
    """eps(gamma) = exp(2 pi i * E), returns E mod 1 (c > 0)."""
    assert c > 0 and a * d - b * c == 1
    return (Fraction(a + d, 24 * c) + dedekind_s(-d, c) / 2) % 1


def nu_exponent(N, a, b, c, d):
    assert c % N == 0 and c > 0
    return (eps_exponent(a, b, c, d) - eps_exponent(a, N * b, c // N, d)) % 1


def eta(tau):
    q = mp.exp(2j * mp.pi * tau)
    return mp.exp(2j * mp.pi * tau / 24) * mp.qp(q)


def kron(N, m):
    m = abs(m)
    if m == 1:
        return 1
    a, n, s = N % m, m, 1
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


rng = random.Random(2026)
out = {"numeric_validation": [], "class_checks": []}
# (0) numeric validation of the exact formula
tau = mp.mpc("0.137", "0.91")
for N in LEVELS:
    cnt = 0
    while cnt < 6:
        c = N * rng.randint(1, 3)
        d = rng.randint(-7, 7)
        if gcd(c, d) != 1:
            continue
        a = pow(d, -1, c) if c > 1 else 1
        b = (a * d - 1) // c
        if a * d - b * c != 1:
            continue
        g = (a * tau + b) / (c * tau + d)
        nu_num = (eta(g) / eta(N * g)) / (eta(tau) / eta(N * tau))
        E = nu_exponent(N, a, b, c, d)
        nu_ex = mp.exp(2j * mp.pi * mp.mpf(E.numerator) / E.denominator)
        err = abs(nu_num - nu_ex)
        assert err < mp.mpf(10) ** (-25), (N, a, b, c, d, nu_num, nu_ex)
        out["numeric_validation"].append({"N": N, "gamma": [a, b, c, d], "nu_exponent": str(E),
                                          "abs_error": float(err)})
        cnt += 1
print("exact multiplier formula agrees with mpmath numerics on", len(out["numeric_validation"]), "matrices")

# (a),(b)
for N in LEVELS:
    M = 24 * N
    for delta in [x for x in range(1, M) if gcd(x, M) == 1]:
        dinv = pow(delta, -1, M)
        vals = set()
        for _ in range(3):
            while True:
                c = M * rng.randint(1, 3)
                d = dinv + M * rng.randint(0, 5)
                if gcd(c, d) != 1:
                    continue
                a = pow(d, -1, c)
                b = (a * d - 1) // c
                for t in range(M):
                    if (b + t * a) % M == 0:
                        b, d = b + t * a, d + t * c
                        break
                if a % M == delta and d % M == dinv and b % M == 0:
                    break
            E = nu_exponent(N, a, b, c, d)
            vals.add(E)
        assert len(vals) == 1, (N, delta, vals)
        E = vals.pop()
        sign = 1 if E == 0 else (-1 if E == Fraction(1, 2) else None)
        exp = kron(N, delta)
        assert sign == exp, (N, delta, E, exp)
        out["class_checks"].append({"N": N, "delta": delta, "nu_exponent": str(E), "nu": sign,
                                    "kronecker_N_delta": exp})
    print(f"N={N}: nu(gamma) = (N/delta) for all {sum(1 for r in out['class_checks'] if r['N']==N)} unit classes delta mod {M} (3 lifts each); delta=1 gives nu=1")
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
with open(os.path.join(base, "eta_multiplier_checks.json"), "w") as f:
    json.dump(out, f, indent=1)
print("eta multiplier checks passed")
