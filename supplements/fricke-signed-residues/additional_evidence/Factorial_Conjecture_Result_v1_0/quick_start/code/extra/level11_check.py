"""
Exploratory test beyond the five levels: N = 11, where X_0(11) has genus 1 but
Gamma_0(11)^+ has genus 0.  Hauptmodul (checked: integral, Fricke-invariant numerically):
    T_11 = theta_Q(tau)^2 / (eta(tau) eta(11 tau))^2 - 6,   Q = x^2 + xy + 3y^2,
    T_11 = q^{-1} + 17 q + 46 q^2 + 116 q^3 + ...   (McKay-Thompson 11A).
Supersingular T-values: roots of  P(T) - j s(T) + j^2  over supersingular j, where
s = j(tau)+j(11 tau), P = j(tau) j(11 tau) are polynomials in T.
Weights e_t: from the multiplicity (p+1)/e_t of t in Delta_11^{-(p^2-1)/24} (a polynomial in T);
cross-checked against the mass identity sum 1/e = 12(p-1)/24.
R_{11,p}: certified exactly as for the five levels.  Tests r_t W_t == -(-11/p).
"""
import json, os, sys
from fractions import Fraction
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from flint import nmod_poly
from wr_core import Field, primes_upto, legendre, euler_coeffs, inflate, ss_j_deuring, horner_series, poly_in_T_from_series

N = 11


def T11_S(p, L):
    """S = q*T_11 mod p, length L."""
    R = int((L ** 0.5) * 1.2) + 3
    th = [0] * L
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            n = x * x + x * y + 3 * y * y
            if n < L:
                th[n] += 1
    th = nmod_poly([c % p for c in th], p)
    E = nmod_poly(euler_coeffs(L), p)
    E11 = nmod_poly(inflate(euler_coeffs(L), 11, L), p)
    eta2 = E.mul_low(E11, L).pow_trunc(2, L)
    S = th.pow_trunc(2, L).mul_low(eta2.inverse_series_trunc(L), L)
    S = S - nmod_poly([0, 6 % p], p)
    return S.truncate(L)


def jseries_q(p, L):
    """q*j(q) mod p, length L."""
    sig3 = [0] * L
    for d in range(1, L):
        d3 = pow(d, 3, p)
        for m in range(d, L, d):
            sig3[m] = (sig3[m] + d3) % p
    E4 = nmod_poly([1] + [240 * sig3[n] % p for n in range(1, L)], p)
    E = nmod_poly(euler_coeffs(L), p)
    return E4.pow_trunc(3, L).mul_low(E.pow_trunc(24, L).inverse_series_trunc(L), L)


def run(p):
    Fd = Field(p)
    F = Fd.F
    res = {"N": N, "p": p}
    L = p ** 3 + 2
    S = T11_S(p, L)
    assert int(S[0]) == 1 and int(S[1]) == 0
    # s(T) = j(q)+j(q^11) : pole order 11 ;  P(T) = j(q) j(q^11): pole order 12
    Lj = 40
    J = jseries_q(p, Lj * 11 + 20)
    J11 = nmod_poly(inflate([int(c) for c in J.coeffs()], 11, Lj * 11 + 20), p)
    # q^11 s = q^10 * (qj) + (q^11 j(q^11)) ; q^11 j(q^11) = J11
    Lq = 13 + 30
    qs = (J.left_shift(10) + J11).truncate(Lq)
    qP = J.mul_low(J11, Lq)                         # q^12 j(q) j(q^11)
    s_co = poly_in_T_from_series(S.truncate(Lq), qs, 11, p)
    P_co = poly_in_T_from_series(S.truncate(Lq), qP, 12, p)
    # sanity: re-expand and compare extra coefficients
    ok_s = (horner_series(s_co, S.truncate(Lq), Lq, p) - qs).truncate(Lq).is_zero()
    ok_P = (horner_series(P_co, S.truncate(Lq), Lq, p) - qP).truncate(Lq).is_zero()
    res["s_P_polynomials_ok"] = ok_s and ok_P
    jD, _ = ss_j_deuring(Fd)
    sF = [Fd.el(c) for c in s_co]
    PF = [Fd.el(c) for c in P_co]
    tset = {}
    for j in jD.values():
        co = [PF[i] - j * (sF[i] if i < len(sF) else F(0)) for i in range(13)]
        co[0] += j * j
        rts = Fd.P(co).roots()
        assert sum(m for _, m in rts) == 12
        for t, m in rts:
            tset[Fd.key(t)] = t
    # weights from Delta_11^{-k}
    k = (p * p - 1) // 24
    nS = 12 * k
    LS = nS + 1
    E = nmod_poly(euler_coeffs(LS), p)
    E11 = nmod_poly(inflate(euler_coeffs(LS), 11, LS), p)
    Dk = E.mul_low(E11, LS).pow_trunc(24 * k, LS).inverse_series_trunc(LS)   # q^{nS} Delta_11^{-k}
    Sco = poly_in_T_from_series(S.truncate(LS), Dk, nS, p)
    SF = Fd.P([Fd.el(c) for c in Sco])
    roots = SF.roots()
    res["weighted_poly_splits"] = (sum(m for _, m in roots) == nS)
    rootset = {Fd.key(t): (t, m) for t, m in roots}
    res["roots_match_resultant_set"] = (set(rootset) == set(tset))
    tv = []
    for kk, (t, m) in rootset.items():
        assert (p + 1) % m == 0
        tv.append({"t": t, "e": (p + 1) // m})
    mass = sum(Fraction(1, x["e"]) for x in tv)
    res["mass_ok"] = (mass == Fraction(12 * (p - 1), 24))
    res["weight_counts"] = {}
    for x in tv:
        res["weight_counts"][str(x["e"])] = res["weight_counts"].get(str(x["e"]), 0) + 1
    thin = [x for x in tv if x["e"] == 1]
    d = len(thin)
    res["n_thin"] = d
    res["n_thin_nonrational"] = sum(1 for x in thin if not Fd.in_Fp(x["t"]))
    Dq = Fd.P([F(1)])
    for x in thin:
        Dq = Dq * Fd.P([-x["t"], F(1)])
    Dco = [Fd.to_int(c) for c in Dq.coeffs()]
    Dthin = nmod_poly(Dco, p)
    Sc = S.coeffs() + [0] * L
    L2 = p * p + 1
    G = nmod_poly([int(Sc[p * n + 1]) for n in range(L2)], p)
    S2 = S.truncate(L2)
    if d == 0:
        res["certificate_ok"] = G.is_zero()
        alpha = [0]
    else:
        Cd = horner_series(Dco, S2, L2, p)
        qdF = Cd.mul_low(G, L2)
        alpha = poly_in_T_from_series(S2, qdF.right_shift(1), d - 1, p)
        qdP = horner_series(alpha, S2, L2, p).left_shift(1).truncate(L2)
        res["certificate_ok"] = (qdF - qdP).truncate(L2).is_zero()
    Pn = nmod_poly(alpha, p)
    Dd = Dthin.derivative()
    ratios = set()
    rin = True
    for x in thin:
        t = x["t"]
        r = Fd.eval_nmod(Pn, t) / Fd.eval_nmod(Dd, t)
        W = F(1)
        for y in tv:
            if y["t"] != t:
                W *= (t - y["t"]) ** ((p + 1) // y["e"])
        rin &= Fd.in_Fp(r) and Fd.in_Fp(W)
        ratios.add(Fd.fmt(r * W))
    res["r_and_W_in_Fp"] = rin
    exp = -legendre(-N, p)
    res["expected"] = exp
    res["ratio_set"] = sorted(ratios)
    res["matches"] = all(int(z) == exp % p for z in ratios)
    return res


if __name__ == "__main__":
    pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 47
    out = []
    for p in primes_upto(pmax):
        if p < 5 or p == N:
            continue
        r = run(p)
        print(r, flush=True)
        out.append(r)
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "results")
    json.dump(out, open(os.path.join(base, "level11_exploratory.json"), "w"), indent=1)
    print("all ok:", all(all(v for v in r.values() if isinstance(v, bool)) for r in out))
