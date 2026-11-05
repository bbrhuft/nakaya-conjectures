"""
Core exact-arithmetic routines for the signed weighted-residue investigation.

Levels N in {2,3,5,7,13}; T_N = u + a_N + b_N/u, u = (eta(tau)/eta(N tau))^{a_N}.
All finite-field arithmetic is exact (python-flint nmod_poly over F_p and
fq_default over F_{p^2}).  Nothing here uses the conjectured residue formula.
"""
from fractions import Fraction
import flint
from flint import nmod_poly, fmpz_poly, fq_default_ctx, fq_default_poly_ctx

LEVELS = {2: (24, 4096), 3: (12, 729), 5: (6, 125), 7: (4, 49), 13: (2, 13)}


def primes_upto(n):
    s = bytearray([1]) * (n + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


# ---------------------------------------------------------------- j-maps
def jmap_numerator(N):
    """Integer polynomial P_N(u) with j = P_N(u)/u^N (as supplied in the brief)."""
    u = fmpz_poly([0, 1])
    if N == 2:
        return (u + 256) ** 3
    if N == 3:
        return (u + 27) * (u + 243) ** 3
    if N == 5:
        return (u ** 2 + 250 * u + 3125) ** 3
    if N == 7:
        return (u ** 2 + 13 * u + 49) * (u ** 2 + 245 * u + 2401) ** 3
    if N == 13:
        return (u ** 2 + 5 * u + 13) * (u ** 4 + 247 * u ** 3 + 3380 * u ** 2 + 15379 * u + 28561) ** 3
    raise ValueError(N)


# ---------------------------------------------------------------- q-series
def euler_coeffs(L):
    """Coefficients of prod_{n>=1}(1-q^n) up to q^{L-1} (pentagonal numbers)."""
    c = [0] * L
    k = 0
    while True:
        done = True
        for kk in ((k, -k) if k else (0,)):
            e = kk * (3 * kk - 1) // 2
            if e < L:
                c[e] += -1 if kk % 2 else 1
                done = False
        if done and k > 0:
            break
        k += 1
    return c


def inflate(coeffs, N, L):
    out = [0] * L
    for i, v in enumerate(coeffs):
        if i * N >= L:
            break
        out[i * N] = v
    return out


def qseries_S_modp(N, p, L):
    """S = q*T_N as an nmod_poly mod p, truncated to length L.
    q*u = E(q)^a / E(q^N)^a,  q*(b/u) = b q^2 E(q^N)^a / E(q)^a."""
    a, b = LEVELS[N]
    E = nmod_poly(euler_coeffs(L), p)
    Ea = E.pow_trunc(a, L)
    EaN = nmod_poly(inflate(Ea.coeffs(), N, L), p)
    U = Ea.mul_low(EaN.inverse_series_trunc(L), L)
    V = EaN.mul_low(Ea.inverse_series_trunc(L), L)
    bq2V = (V * (b % p)).left_shift(2).truncate(L)
    S = U + nmod_poly([0, a % p], p) + bq2V
    return S.truncate(L)


def qseries_S_Z(N, L):
    """S = q*T_N over Z (fmpz_poly), length L."""
    a, b = LEVELS[N]
    E = fmpz_poly(euler_coeffs(L))
    Ea = E.pow_trunc(a, L)
    EaN = fmpz_poly(inflate([int(x) for x in Ea.coeffs()], N, L))
    U = Ea.mul_low(series_inverse_Z(EaN, L), L)
    V = EaN.mul_low(series_inverse_Z(Ea, L), L)
    S = U + fmpz_poly([0, a]) + (V * b).left_shift(2).truncate(L)
    return S.truncate(L), U, V


def series_inverse_Z(f, L):
    """Inverse of a power series with constant term +-1 over Z (Newton)."""
    c0 = int(f[0])
    assert c0 in (1, -1)
    g = fmpz_poly([c0])
    n = 1
    while n < L:
        n = min(2 * n, L)
        e = (f.mul_low(g, n))
        # g <- g*(2 - f g)
        two = fmpz_poly([2])
        g = g.mul_low((two - e).truncate(n), n)
    return g.truncate(L)


# ---------------------------------------------------------------- finite fields
class Field:
    def __init__(self, p):
        self.p = p
        self.F = fq_default_ctx(p, 2)
        self.P = fq_default_poly_ctx(self.F)

    def el(self, n):
        return self.F(int(n) % self.p)

    def in_Fp(self, x):
        return x ** self.p == x

    def to_int(self, x):
        assert self.in_Fp(x)
        lst = x.to_list()
        assert all(int(c) == 0 for c in lst[1:])
        return int(lst[0]) % self.p

    def key(self, x):
        return tuple(int(c) for c in x.to_list())

    def fmt(self, x):
        """Human-readable: integer in [0,p) if in F_p, else c0+c1*z string."""
        if self.in_Fp(x):
            return str(self.to_int(x))
        return str(x)

    def poly_from_ints(self, coeffs):
        return self.P([self.el(c) for c in coeffs])

    def eval_nmod(self, f, x):
        """Evaluate nmod_poly f (over F_p) at x in F_{p^2} (Horner)."""
        acc = self.F(0)
        for c in reversed(f.coeffs()):
            acc = acc * x + self.el(int(c))
        return acc

    def roots_with_mult(self, coeffs):
        f = self.poly_from_ints(coeffs) if not hasattr(coeffs, 'roots') else coeffs
        return f.roots()


# ---------------------------------------------------------------- supersingular j
def ss_j_deuring(Fd):
    """Supersingular j via Deuring's Legendre polynomial; returns dict key->element."""
    p = Fd.p
    h = (p - 1) // 2
    from math import comb
    D = [comb(h, i) ** 2 % p for i in range(h + 1)]
    Dp = Fd.poly_from_ints(D)
    out = {}
    lam_roots = Dp.roots()
    assert sum(m for _, m in lam_roots) == h, "Deuring polynomial not split over F_{p^2}"
    assert all(m == 1 for _, m in lam_roots), "Deuring polynomial not squarefree"
    for lam, m in lam_roots:
        j = Fd.el(256) * (lam ** 2 - lam + 1) ** 3 / (lam ** 2 * (lam - 1) ** 2)
        out[Fd.key(j)] = j
    return out, [l for l, _ in lam_roots]


def ss_j_hasse(Fd):
    """Supersingular j via the Hasse invariant of y^2=x^3+Ax+B, A=3j(1728-j),
    B=2j(1728-j)^2 (valid for j != 0,1728); j=0,1728 tested on y^2=x^3+1, y^2=x^3-x."""
    p = Fd.p
    h = (p - 1) // 2
    from math import factorial
    jj = nmod_poly([0, 1], p)
    A = 3 * jj * (1728 - jj)
    B = 2 * jj * (1728 - jj) ** 2
    H = nmod_poly([0], p)
    for k in range(0, p):
        if (p - 1 - k) % 3:
            continue
        i = (p - 1 - k) // 3
        l = h - i - k
        if i < 0 or l < 0:
            continue
        coef = factorial(h) // (factorial(i) * factorial(k) * factorial(l))
        H += (coef % p) * A ** k * B ** l
    # strip factors j and (j-1728)
    lin0 = nmod_poly([0, 1], p)
    lin1 = nmod_poly([(-1728) % p, 1], p)
    while H.degree() > 0 and int(H[0]) == 0:
        H = H.right_shift(1)
    while H.degree() > 0 and int(H(1728 % p)) == 0:
        H, r = divmod(H, lin1)
    out = {}
    if H.degree() > 0:
        for r, m in Fd.poly_from_ints([int(c) for c in H.coeffs()]).roots():
            out[Fd.key(r)] = r
    # j = 0 : y^2 = x^3 + 1 ; j = 1728 : y^2 = x^3 - x
    def hasse_coeff(f):
        g = f ** h
        return int(g[p - 1]) if g.degree() >= p - 1 else 0
    x = nmod_poly([0, 1], p)
    if hasse_coeff(x ** 3 + 1) == 0:
        out[Fd.key(Fd.el(0))] = Fd.el(0)
    if hasse_coeff(x ** 3 - x) == 0:
        out[Fd.key(Fd.el(1728))] = Fd.el(1728)
    return out


# ---------------------------------------------------------------- level-N supersingular data
def ss_points(N, Fd, jset):
    """Return list of T-values with data: points u over them, m_x, stab, e."""
    p = Fd.p
    a, b = LEVELS[N]
    PN = jmap_numerator(N)
    PNc = [int(c) for c in PN.coeffs()]
    bF = Fd.el(b)
    pts = []  # (u, j, mult, m)
    for jk, j in jset.items():
        coeffs = [Fd.el(c) for c in PNc]
        # P_N(u) - j u^N
        coeffs[N] = coeffs[N] - j
        f = Fd.P(coeffs)
        rts = f.roots()
        tot = sum(mm for _, mm in rts)
        assert tot == N + 1, f"fibre over j not split over F_p^2 (N={N},p={p})"
        if j == Fd.el(0):
            aut = 3
        elif j == Fd.el(1728):
            aut = 2
        else:
            aut = 1
        for u, mult in rts:
            assert u != Fd.F(0)
            assert aut % mult == 0, (N, p, mult, aut)
            m = aut // mult
            if aut == 1:
                assert mult == 1
            pts.append((u, j, mult, m))
    # group by T-value
    groups = {}
    for (u, j, mult, m) in pts:
        t = u + Fd.el(a) + bF / u
        groups.setdefault(Fd.key(t), {"t": t, "pts": []})["pts"].append((u, j, mult, m))
    tvals = []
    for k, g in groups.items():
        us = g["pts"]
        u0 = us[0][0]
        fixed = (u0 * u0 == bF)
        if fixed:
            assert len(us) == 1, ("fixed point with extra points", N, p)
            stab = 2
        else:
            assert len(us) == 2, ("orbit size", N, p, len(us))
            # check the orbit is {u, b/u} and m agrees
            assert us[1][0] == bF / u0
            assert us[0][3] == us[1][3], "m not Fricke invariant"
            stab = 1
        m = us[0][3]
        e = m * stab
        tvals.append({"t": g["t"], "u": [x[0] for x in us], "j": [x[1] for x in us],
                      "mult": [x[2] for x in us], "m": m, "stab": stab, "e": e})
    return tvals


# ---------------------------------------------------------------- Laurent helpers
def poly_in_T_from_series(Sser, f_shifted, n, p):
    """Given S=qT (nmod_poly) and f_shifted = q^n * f where f is (expected) a
    polynomial in T of degree <= n, return coefficients alpha_0..alpha_n by
    matching exponents q^{-n}..q^0 of f.  Only coefficients 0..n of f_shifted are used."""
    L = n + 1
    powS = [nmod_poly([1], p)]
    for k in range(1, n + 1):
        powS.append(powS[-1].mul_low(Sser, L))
    alpha = [0] * (n + 1)
    fc = [int(f_shifted[i]) for i in range(L)]
    # q^n * T^k = q^{n-k} S^k ; coefficient of q^m is [S^k]_{m-n+k}
    for m in range(0, n + 1):
        k = n - m
        val = fc[m]
        for kk in range(k + 1, n + 1):
            idx = m - n + kk
            if 0 <= idx < L:
                val -= alpha[kk] * int(powS[kk][idx])
        alpha[k] = val % p
    return alpha


def horner_series(coeffs_T, Sser, L, p):
    """q^d * P(T) as power series of length L, where P has coefficients coeffs_T
    (low to high), d = deg P, using S = qT."""
    d = len(coeffs_T) - 1
    K = nmod_poly([coeffs_T[d] % p], p)
    for i in range(d):
        c = coeffs_T[d - 1 - i] % p
        K = K.mul_low(Sser, L)
        if c:
            K = K + nmod_poly([0] * (i + 1) + [c], p)
        K = K.truncate(L)
    return K
