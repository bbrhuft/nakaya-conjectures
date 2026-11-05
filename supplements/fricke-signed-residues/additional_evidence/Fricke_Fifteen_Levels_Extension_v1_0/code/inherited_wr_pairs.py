"""
Per-(N,p) computation:
  A. supersingular data (two independent j-sources), weights, mass identity;
  B. certified reconstruction of R_{N,p} from the q-expansion of T_N|U_p
     (candidate thin denominator + a priori bound den | T^{p^2}-T);
  C. residues r_i, weighted products W_i, ratios r_i W_i, Frobenius tests;
  D. checks of the proof ingredients:
       D1 Hasse-power identity  prod (T-t_k)^{(p+1)/e_k} == Delta_N^{-(p^2-1)/24}  (mod p)
       D2 Kaneko-Zagier double-pole lemma  r_i == coeff of (T-t_i)^{-2} in (theta T)^{p-1}
       D3 eta-quotient Frobenius  u(x)^{(p^2-1)/a_N} == (N/p) at every ss point x
       D4 Baker / c(E):  E_{p+1}^{p-1}/Delta^{(p^2-1)/12} == -(-1/p),
          c(E)=E_{p+1}^{(p-1)/2}/Delta^{(p^2-1)/24} constant on the ss locus,
          and r_i W_i == (N/p) c(E) c(E/C).
Nothing here assumes the conjectured residue formula; the expected constant is
only compared at the end.
"""
from fractions import Fraction
import time
from math import comb
import flint
from flint import nmod_poly, nmod_mat, fmpq
from wr_core import (LEVELS, Field, legendre, ss_j_deuring, ss_j_hasse, ss_points,
                     qseries_S_modp, poly_in_T_from_series, horner_series, jmap_numerator,
                     euler_coeffs, inflate)

_level1_cache = {}


def _sigma(k, L, p):
    s = [0] * L
    for d in range(1, L):
        dk = pow(d, k, p)
        for m in range(d, L, d):
            s[m] = (s[m] + dk) % p
    return s


def eisenstein_modp(k, L, p):
    """q-expansion mod p of E_k = 1 - (2k/B_k) sum sigma_{k-1}(n) q^n (exact B_k)."""
    Bk = fmpq.bernoulli(k)
    c = fmpq(-2 * k) / Bk
    num, den = int(c.p), int(c.q)
    if den % p == 0:
        raise ValueError("non-integral")
    cm = num * pow(den, -1, p) % p
    s = _sigma(k - 1, L, p)
    return [1 % p] + [cm * s[n] % p for n in range(1, L)]


def level1_form_in_E4E6(k, target, p):
    """Write the weight-k form with q-expansion `target` (mod p) as
    sum c_{al,be} E4^al E6^be; returns list of ((al,be),c) and a verification flag."""
    basis = [(al, (k - 4 * al) // 6) for al in range(k // 4 + 1) if (k - 4 * al) % 6 == 0]
    dim = len(basis)
    L = dim + 25
    E4 = nmod_poly(eisenstein_modp(4, L, p), p)
    E6 = nmod_poly(eisenstein_modp(6, L, p), p)
    ser = [E4.pow_trunc(al, L).mul_low(E6.pow_trunc(be, L), L) for (al, be) in basis]
    M = nmod_mat(dim, dim, [int(ser[i][n]) for n in range(dim) for i in range(dim)], p)
    rhs = nmod_mat(dim, 1, [target[n] % p for n in range(dim)], p)
    sol = M.solve(rhs)
    cs = [int(sol[i, 0]) for i in range(dim)]
    comb_ser = nmod_poly([0], p)
    for c, s in zip(cs, ser):
        comb_ser += c * s
    ok = all(int(comb_ser[n]) == target[n] % p for n in range(L))
    return list(zip(basis, cs)), ok


def level1_data(p):
    """E_{p+1} and E_{p-1} mod p as polynomials in E4, E6."""
    if p in _level1_cache:
        return _level1_cache[p]
    L = (p + 1) // 4 + 40
    Ep1, ok1 = level1_form_in_E4E6(p + 1, eisenstein_modp(p + 1, L, p), p)
    Em1, ok2 = level1_form_in_E4E6(p - 1, eisenstein_modp(p - 1, L, p), p)
    _level1_cache[p] = (Ep1, Em1, ok1 and ok2)
    return _level1_cache[p]


def g2g3_for_j(Fd, j):
    if j == Fd.el(0):
        return Fd.el(0), Fd.el(1)
    if j == Fd.el(1728):
        return Fd.el(1), Fd.el(0)
    c = Fd.el(27) * j / (j - Fd.el(1728))
    return c, c


def eval_E4E6(Fd, form, E4v, E6v):
    acc = Fd.F(0)
    for (al, be), c in form:
        if c:
            acc += Fd.el(c) * E4v ** al * E6v ** be
    return acc


def baker_c(Fd, j, Ep1, Em1):
    """Returns (E_{p-1}(E), beta(E)=E_{p+1}^{p-1}/Delta^{(p^2-1)/12}, c(E)=E_{p+1}^{(p-1)/2}/Delta^{(p^2-1)/24})."""
    p = Fd.p
    g2, g3 = g2g3_for_j(Fd, j)
    E4v, E6v = Fd.el(12) * g2, Fd.el(-216) * g3
    Dv = g2 ** 3 - Fd.el(27) * g3 ** 2
    assert Dv != Fd.F(0)
    jj = E4v ** 3 / Dv
    assert jj == j
    A = eval_E4E6(Fd, Em1, E4v, E6v)
    B = eval_E4E6(Fd, Ep1, E4v, E6v)
    beta = B ** (p - 1) / Dv ** ((p * p - 1) // 12)
    c = B ** ((p - 1) // 2) / Dv ** ((p * p - 1) // 24)
    return A, B, beta, c


def compute_pair(N, p, mode='certified', kz=True, hasse_power=True, pade=False, verbose=False):
    certify = (mode == 'certified')
    t0 = time.time()
    a, b = LEVELS[N]
    Fd = Field(p)
    F = Fd.F
    res = {"N": N, "p": p, "mode": mode, "Fp2_modulus": str(F.modulus())}
    rmap = None
    # ---------------- A. supersingular data
    jD, lams = ss_j_deuring(Fd)
    jH = ss_j_hasse(Fd)
    res["ss_j_sources_agree"] = (set(jD.keys()) == set(jH.keys()))
    assert res["ss_j_sources_agree"]
    res["n_ss_j"] = len(jD)
    tv = ss_points(N, Fd, jD)
    res["n_ss_points_X0N"] = sum(len(x["u"]) for x in tv)
    res["n_ss_T_values"] = len(tv)
    mass = sum(Fraction(1, x["e"]) for x in tv)
    res["mass"] = str(mass)
    res["mass_expected"] = str(Fraction((N + 1) * (p - 1), 24))
    res["mass_ok"] = (mass == Fraction((N + 1) * (p - 1), 24))
    assert res["mass_ok"]
    # exponent integrality
    res["exponents_integral"] = all((p + 1) % x["e"] == 0 for x in tv)
    assert res["exponents_integral"]
    ecount = {}
    for x in tv:
        ecount[x["e"]] = ecount.get(x["e"], 0) + 1
    res["weight_counts"] = {str(k): v for k, v in sorted(ecount.items())}
    res["nonthin"] = [{"t": Fd.fmt(x["t"]), "e": x["e"], "m": x["m"], "stab": x["stab"],
                       "j": [Fd.fmt(jj) for jj in x["j"]], "u": [Fd.fmt(u) for u in x["u"]]}
                      for x in tv if x["e"] > 1]
    thin = [x for x in tv if x["e"] == 1]
    d = len(thin)
    res["n_thin"] = d
    res["n_thin_nonrational"] = sum(1 for x in thin if not Fd.in_Fp(x["t"]))
    # D_thin over F_p
    Dq = Fd.P([F(1)])
    for x in thin:
        Dq = Dq * Fd.P([-x["t"], F(1)])
    Dco = [Fd.to_int(c) for c in Dq.coeffs()] if d else [1]
    Dthin = nmod_poly(Dco, p)
    res["D_thin"] = Dco
    # ---------------- B. certified reconstruction of R
    Sser = None
    if certify:
        L = p ** 3 + 2
        Sser = qseries_S_modp(N, p, L)
        Sc = Sser.coeffs()
        Sc += [0] * (L - len(Sc))
        L2 = p * p + 1
        G = nmod_poly([Sc[p * n + 1] for n in range(L2)], p)  # T|U_p, coefficients c_{pn}
        assert int(G[0]) == 0
        S2 = Sser.truncate(L2)
        if d == 0:
            res["R_numerator"] = [0]
            res["certificate_ok"] = G.is_zero()
            alpha = []
        else:
            Cd = horner_series(Dco, S2, L2, p)      # q^d D(T)
            qdF = Cd.mul_low(G, L2)                  # q^d D(T) (T|U_p)
            assert int(qdF[0]) == 0
            alpha = poly_in_T_from_series(S2, qdF.right_shift(1), d - 1, p)
            qdP = horner_series(alpha, S2, L2, p).left_shift(1).truncate(L2)
            res["certificate_ok"] = ((qdF - qdP).truncate(L2).is_zero())
            res["R_numerator"] = alpha
        res["certificate_precision_q_exponent"] = p * p - d
        res["certificate_T_terms"] = L
        assert res["certificate_ok"], (N, p)
        Pnum = nmod_poly(alpha if alpha else [0], p)
        if d:
            res["gcd_P_D_is_1"] = (Pnum.gcd(Dthin).degree() == 0)
            res["deg_P_lt_deg_D"] = (Pnum.degree() < d)
            assert res["gcd_P_D_is_1"] and res["deg_P_lt_deg_D"]
        if pade:
            # Candidate-free determination of den_red R: Htil := (T^{p^2}-T) R(T) is a
            # polynomial of degree <= p^2-1 (a priori bound); recover it from
            # q-series (T(q^{p^2}) - T(q)) * (T|U_p) and take gcd with T^{p^2}-T.
            n = p * p - 1
            Ln = n + 1
            # q^{p^2} T(q^{p^2}) = S(q^{p^2}),  q^{p^2} T(q) = q^{p^2-1} S(q)
            n1 = n + 1
            L1 = n1 + 1
            Sinf = nmod_poly(inflate(S2.truncate(L1).coeffs(), p * p, L1), p)  # S(q^{p^2})
            qT = S2.truncate(L1).left_shift(n1 - 1).truncate(L1)              # q^{n1} T
            X = (Sinf - qT).truncate(L1)                                       # q^{n1}(T^{p^2}-T)
            Hs = X.mul_low(G.truncate(L1), L1)                                 # q^{n1} * Htil
            assert int(Hs[0]) == 0
            hco = poly_in_T_from_series(S2.truncate(L1), Hs.right_shift(1), n, p)
            Ht = nmod_poly(hco, p)
            Fq2 = nmod_poly([0, p - 1] + [0] * (p * p - 2) + [1], p)          # T^{p^2} - T
            gg = Ht.gcd(Fq2)
            den = Fq2 // gg
            den = den * pow(int(den.leading_coefficient()), -1, p)
            res["pade_den_equals_D_thin"] = (den == Dthin)
            res["pade_degree_bound_used"] = n
        # ---------------- C. residues and weighted products
        Dder = Dthin.derivative()
        expected = (-legendre(-N, p)) % p
        res["expected_constant"] = -legendre(-N, p)
        ratios = []
        thin_out = []
        rmap, Wmap = {}, {}
        for x in thin:
            t = x["t"]
            r = Fd.eval_nmod(Pnum, t) / Fd.eval_nmod(Dder, t)
            W = F(1)
            for y in tv:
                if y["t"] == t:
                    continue
                W *= (t - y["t"]) ** ((p + 1) // y["e"])
            rmap[Fd.key(t)] = r
            Wmap[Fd.key(t)] = W
            ratio = r * W
            thin_out.append({"t": Fd.fmt(t), "rational": Fd.in_Fp(t), "r": Fd.fmt(r), "W": Fd.fmt(W),
                             "r_in_Fp": Fd.in_Fp(r), "W_in_Fp": Fd.in_Fp(W),
                             "rW": Fd.fmt(ratio), "j": [Fd.fmt(jj) for jj in x["j"]]})
            ratios.append(ratio)
        res["thin"] = thin_out
        res["all_r_in_Fp"] = all(e["r_in_Fp"] for e in thin_out)
        res["all_W_in_Fp"] = all(e["W_in_Fp"] for e in thin_out)
        rs = sorted(set(Fd.to_int(z) if Fd.in_Fp(z) else -999 for z in ratios))
        res["ratio_set_modp"] = rs
        res["ratio_set_signed"] = [((z + 1) % p) - 1 if z >= 0 else None for z in rs]
        res["ratio_constant"] = (len(rs) <= 1)
        res["matches_conjecture"] = all(z == expected for z in rs)
        # Frobenius conjugation
        frob_ok = True
        for x in thin:
            t = x["t"]
            if Fd.in_Fp(t):
                continue
            tp = t ** p
            kp = Fd.key(tp)
            if kp not in rmap:
                frob_ok = False
                continue
            frob_ok &= (rmap[kp] == rmap[Fd.key(t)] ** p) and (Wmap[kp] == Wmap[Fd.key(t)] ** p)
        res["frobenius_conjugation_ok"] = frob_ok
    if mode == 'kz' and d:
        ng = p - 1 + 2 * d
        Lg = ng + 1 + 100
        S4 = qseries_S_modp(N, p, Lg)
        qthetaT = nmod_poly([((m - 1) * int(S4[m])) % p for m in range(Lg)], p)
        g_sh = qthetaT.pow_trunc(p - 1, Lg)
        C2 = horner_series(Dco, S4, Lg, p)
        f_sh = g_sh.mul_low(C2.mul_low(C2, Lg), Lg)
        poly = poly_in_T_from_series(S4, f_sh, ng, p)
        back = horner_series(poly, S4, Lg, p)
        res["kz_polynomial_identity_ok_to_extra_100_terms"] = ((f_sh - back).truncate(Lg).is_zero())
        Pg = nmod_poly(poly, p)
        Dder = Dthin.derivative()
        expected = (-legendre(-N, p)) % p
        res["expected_constant"] = -legendre(-N, p)
        rmap, Wmap, ratios, thin_out = {}, {}, [], []
        for x in thin:
            t = x["t"]
            r = Fd.eval_nmod(Pg, t) / Fd.eval_nmod(Dder, t) ** 2
            W = F(1)
            for y in tv:
                if y["t"] == t:
                    continue
                W *= (t - y["t"]) ** ((p + 1) // y["e"])
            rmap[Fd.key(t)] = r
            Wmap[Fd.key(t)] = W
            ratios.append(r * W)
            thin_out.append({"t": Fd.fmt(t), "rational": Fd.in_Fp(t), "r": Fd.fmt(r), "W": Fd.fmt(W),
                             "r_in_Fp": Fd.in_Fp(r), "W_in_Fp": Fd.in_Fp(W), "rW": Fd.fmt(r * W)})
        res["thin"] = thin_out
        res["all_r_in_Fp"] = all(e["r_in_Fp"] for e in thin_out)
        res["all_W_in_Fp"] = all(e["W_in_Fp"] for e in thin_out)
        res["all_r_nonzero"] = all(v != F(0) for v in rmap.values())
        rs = sorted(set(Fd.to_int(z) if Fd.in_Fp(z) else -999 for z in ratios))
        res["ratio_set_modp"] = rs
        res["ratio_set_signed"] = [((z + 1) % p) - 1 if z >= 0 else None for z in rs]
        res["ratio_constant"] = (len(rs) <= 1)
        res["matches_conjecture"] = all(z == expected for z in rs)
        frob_ok = True
        for x in thin:
            t = x["t"]
            if Fd.in_Fp(t):
                continue
            kp = Fd.key(t ** p)
            frob_ok &= (kp in rmap) and (rmap[kp] == rmap[Fd.key(t)] ** p) and (Wmap[kp] == Wmap[Fd.key(t)] ** p)
        res["frobenius_conjugation_ok"] = frob_ok
    elif mode == 'kz':
        res["thin"] = []
        res["ratio_set_modp"] = []
        res["ratio_set_signed"] = []
        res["ratio_constant"] = True
        res["matches_conjecture"] = True
        res["expected_constant"] = -legendre(-N, p)
    # ---------------- D1. Hasse-power identity
    if hasse_power:
        k = (p * p - 1) // 24
        Spoly = Dthin ** (p + 1)
        bye = {}
        for x in tv:
            if x["e"] > 1:
                bye.setdefault(x["e"], Fd.P([F(1)]))
                bye[x["e"]] = bye[x["e"]] * Fd.P([-x["t"], F(1)])
        for e, g in bye.items():
            gi = nmod_poly([Fd.to_int(c) for c in g.coeffs()], p)
            Spoly = Spoly * gi ** ((p + 1) // e)
        nS = Spoly.degree()
        res["deg_weighted_ss_poly"] = nS
        assert nS == (N + 1) * k
        LS = nS + 1
        S3 = Sser.truncate(LS) if Sser is not None else qseries_S_modp(N, p, LS)
        lhs = horner_series([int(c) for c in Spoly.coeffs()], S3, LS, p)
        E = nmod_poly(euler_coeffs(LS), p)
        EN = nmod_poly(inflate(E.coeffs(), N, LS), p)
        W24 = E.mul_low(EN, LS).pow_trunc(24 * k, LS)
        rhs = W24.inverse_series_trunc(LS)
        res["hasse_power_identity_ok"] = ((lhs - rhs).truncate(LS).is_zero())
    # ---------------- D2. Kaneko-Zagier double pole lemma
    if kz and certify and d:
        ng = p - 1 + 2 * d
        Lg = ng + 1 + 200
        S4 = Sser.truncate(Lg) if Sser.length() >= Lg else qseries_S_modp(N, p, Lg)
        qthetaT = nmod_poly([((m - 1) * int(S4[m])) % p for m in range(Lg)], p)
        g_sh = qthetaT.pow_trunc(p - 1, Lg)
        C2 = horner_series(Dco, S4, Lg, p)
        f_sh = g_sh.mul_low(C2.mul_low(C2, Lg), Lg)   # q^{ng} g D(T)^2
        poly = poly_in_T_from_series(S4, f_sh, ng, p)
        back = horner_series(poly, S4, Lg, p)
        res["kz_polynomial_identity_ok_to_extra_200_terms"] = ((f_sh - back).truncate(Lg).is_zero())
        Pg = nmod_poly(poly, p)
        Dder = Dthin.derivative()
        kz_ok = True
        for x in thin:
            t = x["t"]
            coef = Fd.eval_nmod(Pg, t) / Fd.eval_nmod(Dder, t) ** 2
            kz_ok &= (coef == rmap[Fd.key(t)])
        res["kz_double_pole_equals_residue"] = kz_ok
        # orders of vanishing at non-thin supersingular values
        PgF = Fd.P([Fd.el(int(c)) for c in Pg.coeffs()])
        ord_ok = True
        for x in tv:
            if x["e"] == 1:
                continue
            lin = Fd.P([-x["t"], F(1)])
            mult = 0
            f = PgF
            while True:
                qq, rr = divmod(f, lin)
                if not rr.is_zero():
                    break
                mult += 1
                f = qq
            exp = ((p - 1) * (x["e"] - 1) - 2)
            ord_ok &= (exp % x["e"] == 0 and mult == exp // x["e"])
        res["kz_orders_at_nonthin_ok"] = ord_ok
    # ---------------- D3 / D4
    Ep1, Em1, okl1 = level1_data(p)
    res["level1_basis_ok"] = okl1
    legN = legendre(N, p)
    U_ok = True
    for x in tv:
        for u in x["u"]:
            v = u ** ((p * p - 1) // a)
            U_ok &= (v == Fd.el(legN))
    res["eta_frobenius_U_ok_all_ss"] = U_ok
    cvals = {}
    baker_ok = True
    hasse_zero_ok = True
    for jk, j in jD.items():
        A, B, beta, c = baker_c(Fd, j, Ep1, Em1)
        hasse_zero_ok &= (A == F(0))
        baker_ok &= (beta == Fd.el(-legendre(-1, p)))
        cvals[jk] = c
    res["E_{p-1}_vanishes_at_ss"] = hasse_zero_ok
    res["baker_beta_ok"] = baker_ok
    cset = set(Fd.key(c) for c in cvals.values())
    res["c_constant_on_ss_locus"] = (len(cset) == 1)
    if d and rmap is not None:
        PN = jmap_numerator(N)
        PNc = [Fd.el(int(cc)) for cc in PN.coeffs()]
        def Jmap(u):
            acc = F(0)
            for cc in reversed(PNc):
                acc = acc * u + cc
            return acc / u ** N
        fac_ok = True
        for x in thin:
            u = x["u"][0]
            j1, j2 = Jmap(u), Jmap(Fd.el(b) / u)
            c1, c2 = cvals[Fd.key(j1)], cvals[Fd.key(j2)]
            fac_ok &= (rmap[Fd.key(x["t"])] * Wmap[Fd.key(x["t"])] == Fd.el(legN) * c1 * c2)
        res["rW_equals_legN_c_c"] = fac_ok
    res["seconds"] = round(time.time() - t0, 2)
    return res
