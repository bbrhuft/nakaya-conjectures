#!/usr/bin/env python3
"""
Independent check of the eta/Frobenius lemma (Theorem C of the Signed Weighted Residue Note)
WITHOUT eta functions, q-expansions of X_0(ell), or any Hauptmodul:

    D_ell(x)^{(p^2-1)/24} = (ell/p)   at every geometric supersingular point x = (E, C) of X_0(ell),

where, moduli-theoretically,  D_ell(E, C) = ell^12 * Delta(E, phi^* omega') / Delta(E', omega'),
phi : E -> E' = E/C the quotient isogeny.  Vélu's formulas give E' together with the differential
omega' normalised by phi^* omega' = omega, so  D_ell(E,C) = ell^12 * Delta(E)/Delta(E')  for the Vélu
models.  Since ell^{12 k} = 1 in F_p (k = (p^2-1)/24), the claim is  (Delta(E)/Delta(E'))^k = (ell/p).

For every supersingular j over F_{p^2}, a model E/F_{p^2} with scalar p^2-Frobenius is used, so all
ell+1 kernel polynomials are F_{p^2}-rational; the ell+1 subgroups are found from the ell-division
polynomial.  This covers every geometric point (E, C), including j = 0 and j = 1728.

Also checked at the same points, independently of the inherited code:
  * Ono (arXiv:2509.16175v2) Thm 1.2:  (Delta(E)/Delta(E'))^{(p^2-1)/12} = 1
  * Robert/Baker (Acta Arith. 1998, Lemma 2.2 with lambda = 1):  B(E') = ell * B(E),  B = E_{p+1} mod p
  * Baker Thm 1.4:  B(E)^{p-1} / Delta(E)^{(p^2-1)/12} = -(-1/p)
  * constancy of c(E) = B(E)^{(p-1)/2} / Delta(E)^{(p^2-1)/24} along every ell-isogeny (Corollary D)
  * for N in {2,3,5,7,13}: the Vélu values D_N(E,C) agree with {u^{N-1} : P_N(u) = j u^N}, which ties
    the moduli normalisation to the Hauptmodul normalisation of the note (u_N^{N-1} = Delta/Delta(N tau)).
  * Ono v2 Thm 1.3 on a Deuring model (pi = [-p]):  Delta(E,omega)^{(p^2-1)/12} = (-1)^{(p+1)/2},
    and the consequence (with Baker) B(E,omega)^{p-1} = 1, i.e. B(E,omega) in F_p.

Usage:  python3 velu_sign_check.py [pmax] [ell list, comma separated] [outdir]
"""
import sys, os, json, time, random
from math import gcd
import flint

# ----------------------------------------------------------------------------- number theory helpers
def primes_upto(n):
    s = bytearray([1]) * (n + 1); s[0] = s[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(n + 1) if s[i]]

def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1

# ----------------------------------------------------------------------------- q-expansions mod p
def sigma_list(k, L, p):
    s = [0] * (L + 1)
    for d in range(1, L + 1):
        dk = pow(d, k, p)
        for m in range(d, L + 1, d):
            s[m] = (s[m] + dk) % p
    return s

def eis_qexp(k, L, p):
    """Normalised E_k mod p (k = 4, 6, and the targets 1 for k=p-1, E_2 for k=p+1)."""
    if k == 4:
        c = 240
    elif k == 6:
        c = -504
    else:
        raise ValueError
    s = sigma_list(k - 1, L, p)
    return [1] + [(c * s[n]) % p for n in range(1, L + 1)]

def mul_series(a, b, L, p):
    out = [0] * (L + 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j in range(0, L + 1 - i):
            out[i + j] = (out[i + j] + ai * b[j]) % p
    return out

_cache = {}
def level1_forms(p):
    """E_{p-1} mod p (q-expansion 1) and E_{p+1} mod p (q-expansion E_2 = 1 - 24 sum sigma(n) q^n),
    each as {(a,b): c} meaning sum c E4^a E6^b, solved by linear algebra on q-expansions."""
    if p in _cache:
        return _cache[p]
    out = {}
    for k, target_kind in ((p - 1, 'one'), (p + 1, 'E2')):
        monos = [(a, (k - 4 * a) // 6) for a in range(k // 4 + 1) if (k - 4 * a) % 6 == 0]
        L = len(monos) + 6
        E4 = eis_qexp(4, L, p); E6 = eis_qexp(6, L, p)
        pw4 = [[1] + [0] * L]; pw6 = [[1] + [0] * L]
        for _ in range(k // 4 + 1):
            pw4.append(mul_series(pw4[-1], E4, L, p))
        for _ in range(k // 6 + 1):
            pw6.append(mul_series(pw6[-1], E6, L, p))
        cols = [mul_series(pw4[a], pw6[b], L, p) for (a, b) in monos]
        if target_kind == 'one':
            tgt = [1] + [0] * L
        else:
            s1 = sigma_list(1, L, p)
            tgt = [1] + [(-24 * s1[n]) % p for n in range(1, L + 1)]
        # solve the (overdetermined, consistent) system by rref of the augmented matrix
        aug = []
        for i in range(L + 1):
            aug.extend([cols[j][i] for j in range(len(monos))] + [tgt[i]])
        A = flint.nmod_mat(L + 1, len(monos) + 1, aug, p)
        R, rank = A.rref()
        assert rank == len(monos), (k, rank, len(monos))
        sol = {}
        for i in range(rank):
            # pivot column
            row = [int(R[i, j]) for j in range(len(monos) + 1)]
            piv = next(j for j, v in enumerate(row) if v != 0)
            assert piv < len(monos)
            sol[monos[piv]] = row[-1]
        # verify consistency (rows beyond rank must be zero)
        for i in range(rank, L + 1):
            assert all(int(R[i, j]) == 0 for j in range(len(monos) + 1))
        out[k] = sol
    _cache[p] = (out[p - 1], out[p + 1])
    return _cache[p]

def eval_form(form, E4v, E6v, Fzero):
    acc = Fzero
    for (a, b), c in form.items():
        if c:
            acc += c * E4v ** a * E6v ** b
    return acc

# ----------------------------------------------------------------------------- supersingular j
def supersingular_j(F, p):
    R = flint.fq_default_poly_ctx(F)
    m = (p - 1) // 2
    coeffs = [pow(flint.fmpz(m).bin(i) if hasattr(flint.fmpz(m), 'bin') else _binom(m, i), 2, p) for i in range(m + 1)]
    D = R(coeffs)
    js = set()
    for lam, _ in D.roots():
        j = 256 * (lam * lam - lam + 1) ** 3 / (lam * lam * (lam - 1) ** 2)
        js.add(j)
    expected = p // 12 + (1 if p % 3 == 2 else 0) + (1 if p % 4 == 3 else 0)
    assert len(js) == expected, (p, len(js), expected)
    return sorted(js, key=lambda z: str(z))

def _binom(n, k):
    from math import comb
    return comb(n, k)

# ----------------------------------------------------------------------------- curve utilities
def model_for_j(F, j):
    """Short Weierstrass y^2 = x^3 + a x + b with the given j; for j = 0, 1728 the F_p-curves
    y^2 = x^3 + 1, y^2 = x^3 + x (scalar p^2-Frobenius -p when supersingular)."""
    if j == F(0):
        return F(0), F(1)
    if j == F(1728):
        return F(1), F(0)
    a = 3 * j * (1728 - j)
    b = 2 * j * (1728 - j) ** 2
    return a, b

def invariants(F, a, b):
    E4 = -48 * a
    E6 = 864 * b
    D = -16 * (4 * a ** 3 + 27 * b ** 2)
    assert D == (E4 ** 3 - E6 ** 2) / 1728
    return E4, E6, D

def j_of(F, a, b):
    return 1728 * 4 * a ** 3 / (4 * a ** 3 + 27 * b ** 2)

def division_polys(R, a, b, nmax):
    """P_n with psi_n = P_n (n odd), psi_n = y P_n (n even), y^2 = x^3 + a x + b."""
    x = R.gen()
    Fx = x ** 3 + a * x + b
    P = [R(0), R(1), R(2), 3 * x ** 4 + 6 * a * x ** 2 + 12 * b * x - a * a,
         4 * (x ** 6 + 5 * a * x ** 4 + 20 * b * x ** 3 - 5 * a * a * x * x - 4 * a * b * x - 8 * b * b - a ** 3)]
    while len(P) <= nmax:
        n = len(P)
        if n % 2 == 1:
            m = (n - 1) // 2
            if m % 2 == 0:
                P.append(Fx ** 2 * P[m + 2] * P[m] ** 3 - P[m - 1] * P[m + 1] ** 3)
            else:
                P.append(P[m + 2] * P[m] ** 3 - Fx ** 2 * P[m - 1] * P[m + 1] ** 3)
        else:
            m = n // 2
            P.append(P[m] * (P[m + 2] * P[m - 1] ** 2 - P[m - 2] * P[m + 1] ** 2) / 2)
    return P, Fx

def kernel_polynomials(R, F, a, b, ell):
    """All ell+1 kernel polynomials h_C(x) = prod_{Q in (C-0)/±} (x - x_Q) over F = GF(p^2).
    Requires all C to be F-rational (true when the p^2-Frobenius is scalar)."""
    x = R.gen()
    if ell == 2:
        Fx = x ** 3 + a * x + b
        rts = Fx.roots()
        assert len(rts) == 3 and all(m == 1 for _, m in rts), "2-torsion not rational"
        return [x - e for e, _ in rts]
    d = (ell - 1) // 2
    P, Fx = division_polys(R, a, b, ell + 1 if ell + 1 > d + 2 else d + 2)
    Pl = P[ell]
    assert Pl.degree() == (ell * ell - 1) // 2
    _, facs = Pl.factor()
    facs = [g.monic() for g, m in facs for _ in range(m)]
    assert sum(g.degree() for g in facs) == Pl.degree()
    degs = set(g.degree() for g in facs)
    assert len(degs) == 1, ("mixed factor degrees", degs)
    r = degs.pop()
    if r == d:
        kernels = facs
    else:
        assert d % r == 0
        unused = list(facs)
        kernels = []
        while unused:
            g = unused.pop(0)
            group = [g]
            # x([m]P) mod g for m = 2..d, P a point with x(P) = x mod g
            for m in range(2, d + 1):
                if m % 2 == 1:
                    num = (Fx * P[m - 1] * P[m + 1]) % g
                    den = (P[m] * P[m]) % g
                else:
                    num = (P[m - 1] * P[m + 1]) % g
                    den = (Fx * P[m] * P[m]) % g
                xm = (x - num * den.inverse_mod(g)) % g
                for g2 in list(unused):
                    if g2.compose_mod(xm, g).is_zero():
                        unused.remove(g2); group.append(g2)
            h = R(1)
            for g2 in group:
                h *= g2
            assert h.degree() == d, (h.degree(), d, r)
            kernels.append(h)
    assert len(kernels) == ell + 1, (len(kernels), ell + 1)
    return kernels

def velu(F, a, b, h, ell):
    """Vélu/Kohel: E' = E/C from the kernel polynomial h; phi^*(dx'/y') = dx/y."""
    d = h.degree()
    c = h.coeffs()  # low to high, monic
    assert c[-1] == F(1) and d == (ell - 1) // 2 if ell > 2 else d == 1
    e1 = -c[d - 1] if d >= 1 else F(0)
    e2 = c[d - 2] if d >= 2 else F(0)
    e3 = -c[d - 3] if d >= 3 else F(0)
    s1 = e1
    s2 = e1 * s1 - 2 * e2
    s3 = e1 * s2 - e2 * s1 + 3 * e3
    if ell == 2:
        e = s1
        t = 3 * e * e + a
        w = e * t
    else:
        t = 6 * s2 + 2 * a * d
        w = 10 * s3 + 6 * a * s1 + 4 * b * d
    return a - 5 * t, b - 7 * w

# ----------------------------------------------------------------------------- Hauptmodul j-maps (note / brief)
JMAP = {
    2: lambda u: (u + 256) ** 3,
    3: lambda u: (u + 27) * (u + 243) ** 3,
    5: lambda u: (u * u + 250 * u + 3125) ** 3,
    7: lambda u: (u * u + 13 * u + 49) * (u * u + 245 * u + 2401) ** 3,
    13: lambda u: (u * u + 5 * u + 13) * (u ** 4 + 247 * u ** 3 + 3380 * u * u + 15379 * u + 28561) ** 3,
}

# ----------------------------------------------------------------------------- group law for the Deuring check
def ec_add(F, a, P, Q):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P; x2, y2 = Q
    if x1 == x2:
        if y1 == -y2:
            return None
        lam = (3 * x1 * x1 + a) / (2 * y1)
    else:
        lam = (y2 - y1) / (x2 - x1)
    x3 = lam * lam - x1 - x2
    return (x3, lam * (x1 - x3) - y1)

def ec_mul(F, a, n, P):
    Rr = None; Q = P
    while n:
        if n & 1: Rr = ec_add(F, a, Rr, Q)
        Q = ec_add(F, a, Q, Q); n >>= 1
    return Rr

def random_point(F, a, b, R):
    x = R.gen()
    while True:
        x0 = F.random_element() if hasattr(F, 'random_element') else F(random.randrange(F.prime()))
        rhs = x0 ** 3 + a * x0 + b
        rts = (x * x - rhs).roots()
        if rts:
            return (x0, rts[0][0])

def deuring_model(F, a, b, R, p):
    """Return (a,b) of an F_{p^2}-model with pi_{p^2} = [-p] (twist if needed), or None."""
    def ok(a_, b_):
        for _ in range(6):
            P = random_point(F, a_, b_, R)
            if ec_mul(F, a_, p + 1, P) is not None:
                return False
        return True
    if ok(a, b):
        return a, b
    # quadratic twist by a non-square u of F_{p^2}
    while True:
        u = F.random_element()
        if u == F(0): continue
        if u ** ((p * p - 1) // 2) != F(1):
            break
    a2, b2 = a * u * u, b * u ** 3
    if ok(a2, b2):
        return a2, b2
    return None

# ----------------------------------------------------------------------------- main per-(ell,p) routine
def check_pair(ell, p, do_deuring=True):
    F = flint.fq_default_ctx(p, 2)
    R = flint.fq_default_poly_ctx(F)
    k = (p * p - 1) // 24
    m = (p * p - 1) // 12
    chi = legendre(ell, p)
    Aform, Bform = level1_forms(p)
    js = supersingular_j(F, p)
    rec = {"ell": ell, "p": p, "n_ss_j": len(js), "n_points": 0, "ell_12k_is_1": pow(ell, 12 * k, p) == 1,
           "legendre_ell_p": chi, "values_D_ell_pow_k": set(), "ono_m_power_all_1": True,
           "robert_B_relation_ok": True, "baker_ok": True, "c_constant_ok": True, "hasse_zero_ok": True,
           "velu_j_supersingular_ok": True, "hauptmodul_match_ok": None, "deuring_kappa_ok": None,
           "deuring_B_in_Fp_ok": None, "j0_present": any(j == F(0) for j in js),
           "j1728_present": any(j == F(1728) for j in js), "n_points_j0": 0, "n_points_j1728": 0}
    jset = set(str(j) for j in js)
    c_values = set()
    hm_ok = True
    for j in js:
        a, b = model_for_j(F, j)
        E4, E6, D = invariants(F, a, b)
        A = eval_form(Aform, E4, E6, F(0)); B = eval_form(Bform, E4, E6, F(0))
        if A != F(0): rec["hasse_zero_ok"] = False
        assert B != F(0)
        beta = B ** (p - 1) / D ** m
        if beta != F(-legendre(-1, p)): rec["baker_ok"] = False
        cE = B ** ((p - 1) // 2) / D ** k
        c_values.add(str(cE))
        kernels = kernel_polynomials(R, F, a, b, ell)
        dvals = []
        for h in kernels:
            a2, b2 = velu(F, a, b, h, ell)
            E4b, E6b, D2 = invariants(F, a2, b2)
            j2 = j_of(F, a2, b2)
            if str(j2) not in jset: rec["velu_j_supersingular_ok"] = False
            r = D / D2                      # = ell^{-12} D_ell(E,C)
            if r ** m != F(1): rec["ono_m_power_all_1"] = False
            v = r ** k
            rec["values_D_ell_pow_k"].add(str(v))
            B2 = eval_form(Bform, E4b, E6b, F(0))
            if B2 != ell * B: rec["robert_B_relation_ok"] = False
            c2 = B2 ** ((p - 1) // 2) / D2 ** k
            if c2 != cE: rec["c_constant_ok"] = False
            dvals.append(F(ell) ** 12 * r)
            rec["n_points"] += 1
            if j == F(0): rec["n_points_j0"] += 1
            if j == F(1728): rec["n_points_j1728"] += 1
        if ell in JMAP:
            # compare multiset {D_N(E,C)} with {u^{N-1} : P_N(u) = j u^N}
            x = R.gen()
            poly = JMAP[ell](x) - j * x ** ell
            rts = poly.roots()
            uset = sorted(str(u ** (ell - 1)) for u, mult in rts for _ in range(mult))
            dset = sorted(str(v) for v in dvals)
            if uset != dset:
                hm_ok = False
    rec["values_D_ell_pow_k"] = sorted(rec["values_D_ell_pow_k"])
    rec["theorem_C_ok"] = (rec["values_D_ell_pow_k"] == [str(F(chi))])
    rec["c_values"] = sorted(c_values)
    rec["c_constant_over_all_ss"] = len(c_values) == 1
    if ell in JMAP:
        rec["hauptmodul_match_ok"] = hm_ok
    if do_deuring:
        okk = True; okB = True
        for j in js:
            a, b = model_for_j(F, j)
            dm = deuring_model(F, a, b, R, p)
            if dm is None:
                okk = None; break
            a, b = dm
            E4, E6, D = invariants(F, a, b)
            kappa = D ** m
            if kappa != F((-1) ** ((p + 1) // 2)): okk = False
            B = eval_form(Bform, E4, E6, F(0))
            if B ** (p - 1) != F(1): okB = False
        rec["deuring_kappa_ok"] = okk
        rec["deuring_B_in_Fp_ok"] = okB
    return rec

if __name__ == "__main__":
    pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    ells = [int(t) for t in sys.argv[2].split(",")] if len(sys.argv) > 2 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    outdir = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
    os.makedirs(outdir, exist_ok=True)
    random.seed(2026)
    recs = []; t0 = time.time()
    fails = []
    for ell in ells:
        for p in primes_upto(pmax):
            if p < 5 or p == ell: continue
            t1 = time.time()
            rec = check_pair(ell, p, do_deuring=(p <= 211))
            rec["seconds"] = round(time.time() - t1, 2)
            recs.append(rec)
            flag = "OK " if rec["theorem_C_ok"] else "FAIL"
            if not rec["theorem_C_ok"]: fails.append((ell, p))
            print(f"ell={ell:2d} p={p:4d} ss_j={rec['n_ss_j']:3d} points={rec['n_points']:4d} "
                  f"D^k values={rec['values_D_ell_pow_k']} (ell/p)={rec['legendre_ell_p']:+d} {flag} "
                  f"ono12={rec['ono_m_power_all_1']} robert={rec['robert_B_relation_ok']} baker={rec['baker_ok']} "
                  f"c_const={rec['c_constant_over_all_ss']} hm={rec['hauptmodul_match_ok']} "
                  f"kappa={rec['deuring_kappa_ok']} BinFp={rec['deuring_B_in_Fp_ok']} j0={rec['n_points_j0']} j1728={rec['n_points_j1728']} "
                  f"[{rec['seconds']}s]", flush=True)
    summary = {"pmax": pmax, "ells": ells, "n_pairs": len(recs), "n_points": sum(r["n_points"] for r in recs),
               "n_points_j0": sum(r["n_points_j0"] for r in recs), "n_points_j1728": sum(r["n_points_j1728"] for r in recs),
               "theorem_C_failures": fails,
               "all_theorem_C_ok": all(r["theorem_C_ok"] for r in recs),
               "all_ono_12_ok": all(r["ono_m_power_all_1"] for r in recs),
               "all_robert_ok": all(r["robert_B_relation_ok"] for r in recs),
               "all_baker_ok": all(r["baker_ok"] for r in recs),
               "all_c_constant_ok": all(r["c_constant_ok"] and r["c_constant_over_all_ss"] for r in recs),
               "all_hauptmodul_match_ok": all(r["hauptmodul_match_ok"] in (True, None) for r in recs),
               "all_deuring_kappa_ok": all(r["deuring_kappa_ok"] in (True, None) for r in recs),
               "all_deuring_B_in_Fp_ok": all(r["deuring_B_in_Fp_ok"] in (True, None) for r in recs),
               "seconds": round(time.time() - t0, 1)}
    with open(os.path.join(outdir, "velu_sign_checks.json"), "w") as f:
        json.dump({"summary": summary, "pairs": recs}, f, indent=1)
    print(json.dumps(summary, indent=1))
