"""
Independent cross-check through the Hecke (modular) polynomial.

For level N and small p, build Psi_{N,p}(X,Y) = prod_gamma (X - T(gamma tau)), Y = T(tau),
modulo p^2 from power sums  P_m = T(q^p)^m + p (T^m | U_p)  and Newton's identities
(computed modulo p^3; the division by k = p loses one p-adic digit).  Then
  (i)   Kronecker:  Psi == (X^p - Y)(X - Y^p)  (mod p);
  (ii)  H := (Psi - (X^p-Y)(X-Y^p))/p  is symmetric mod p;
  (iii) for every t in F_{p^2}:  -H(t^p,t) == Res_{T=t} R_{N,p}  (taken from the
        certified computation; zero unless t is thin);
  (iv)  for thin t: H(t^p,t) == (-N/p) W_t^{-1}   (the conjecture in Hecke form).
Usage: python3 hecke_check.py PMAX
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flint import nmod_poly
from wr_core import LEVELS, primes_upto, qseries_S_modp, Field, legendre, horner_series
from wr_pairs import compute_pair


def poly_in_T_mod(Sser, f_shifted, n, M):
    L = n + 1
    powS = [nmod_poly([1], M)]
    for k in range(1, n + 1):
        powS.append(powS[-1].mul_low(Sser, L))
    alpha = [0] * (n + 1)
    fc = [int(f_shifted[i]) for i in range(L)]
    for m in range(0, n + 1):
        k = n - m
        val = fc[m]
        for kk in range(k + 1, n + 1):
            idx = m - n + kk
            if 0 <= idx < L:
                val -= alpha[kk] * int(powS[kk][idx])
        alpha[k] = val % M
    return alpha


def hecke_poly_mod_p2(N, p):
    M = p ** 3
    V0 = p * (p + 1)          # max pole order of the power sums
    LS = (p + 1) ** 2 + p + 5
    S = qseries_S_modp(N, p, LS)            # placeholder mod p, replaced below
    S = qseries_S_mod(N, M, LS)
    Sc = [int(c) for c in S.coeffs()] + [0] * LS
    # S^m coefficients
    Spow = [nmod_poly([1], M)]
    for m in range(1, p + 2):
        Spow.append(Spow[-1].mul_low(S, LS))
    Spc = [[int(c) for c in sp.coeffs()] + [0] * (LS) for sp in Spow]
    # power sums P_m as Laurent, exponents [-V0, p+1], stored with offset V0
    P = [None]
    for m in range(1, p + 2):
        co = [0] * (V0 + p + 2)
        for e in range(-V0, p + 2):
            v = 0
            if e % p == 0 and e // p + m >= 0:
                v += Spc[m][e // p + m]
            if p * e + m >= 0:
                v += p * Spc[m][p * e + m]
            co[e + V0] = v % M
        P.append(nmod_poly(co, M))
    # e_k: polynomial in T (coeff list) and Laurent expansion with offset p+1,
    # exponents [-(p+1), V0]
    LE = (p + 1) + V0 + 1
    Strunc = S.truncate(LE)
    epoly = [[1]]
    eser = [nmod_poly([0] * (p + 1) + [1], M)]
    for k in range(1, p + 2):
        acc = [0] * (p + 2)  # exponents -(p+1)..0 of k e_k
        for i in range(1, k + 1):
            prod = eser[k - i] * P[i]
            sgn = 1 if i % 2 == 1 else -1
            for eps in range(-(p + 1), 1):
                idx = eps + (p + 1) + V0
                acc[eps + p + 1] += sgn * int(prod[idx]) if idx <= prod.degree() else 0
        acc = [x % M for x in acc]
        if k % p == 0:
            assert all(x % p == 0 for x in acc), "Newton numerator not divisible by p"
            acc = [(x // p) % (p * p) for x in acc]
            kk = k // p
            inv = pow(kk, -1, p * p)
            acc = [x * inv % (p * p) for x in acc]
        else:
            inv = pow(k, -1, M)
            acc = [x * inv % M for x in acc]
        # acc[i] is coefficient of q^{i-(p+1)}; as q^{p+1} e_k power series
        f_sh = nmod_poly(acc, M)
        al = poly_in_T_mod(Strunc, f_sh, p + 1, M)
        epoly.append(al)
        ser = horner_series(al, Strunc, LE, M)   # q^{p+1} e_k(T) (degree <= p+1)
        eser.append(ser)
    # Psi(X,Y) = sum_k (-1)^k e_k(Y) X^{p+1-k}, reduce mod p^2 ; dict (i,j)->coef of X^i Y^j
    Psi = {}
    for k in range(p + 2):
        sgn = 1 if k % 2 == 0 else -1
        for jdeg, c in enumerate(epoly[k]):
            c = (sgn * c) % (p * p)
            if c:
                Psi[(p + 1 - k, jdeg)] = (Psi.get((p + 1 - k, jdeg), 0) + c) % (p * p)
    return Psi


def qseries_S_mod(N, M, L):
    from wr_core import euler_coeffs, inflate
    a, b = LEVELS[N]
    E = nmod_poly(euler_coeffs(L), M)
    Ea = E.pow_trunc(a, L)
    EaN = nmod_poly(inflate([int(c) for c in Ea.coeffs()], N, L), M)
    U = Ea.mul_low(EaN.inverse_series_trunc(L), L)
    Vv = EaN.mul_low(Ea.inverse_series_trunc(L), L)
    return (U + nmod_poly([0, a % M], M) + (Vv * (b % M)).left_shift(2)).truncate(L)


def check(N, p):
    Psi = hecke_poly_mod_p2(N, p)
    K = {(p + 1, 0): 1, (p, p): -1, (1, 1): -1, (0, p + 1): 1}
    # Kronecker mod p
    keys = set(Psi) | set(K)
    kron = all((Psi.get(k, 0) - K.get(k, 0)) % p == 0 for k in keys)
    H = {k: ((Psi.get(k, 0) - K.get(k, 0)) % (p * p)) // p for k in keys}
    H = {k: v % p for k, v in H.items() if v % p}
    sym = all(H.get((j, i), 0) == v for (i, j), v in H.items())
    deg_ok = all(i <= p + 1 and j <= p + 1 for (i, j) in H)
    r = compute_pair(N, p, mode="certified", hasse_power=False, kz=False)
    Fd = Field(p)
    F = Fd.F
    rdict = {}
    for e in r["thin"]:
        rdict[e["t"]] = e["r"]
    Wd = {e["t"]: e["W"] for e in r["thin"]}
    # enumerate F_{p^2}
    z = F.gen()
    ok_res, ok_conj, n_nonzero = True, True, 0
    Hl = list(H.items())
    legmN = legendre(-N, p)
    for c0 in range(p):
        for c1 in range(p):
            t = Fd.el(c0) + Fd.el(c1) * z
            tp = t ** p
            val = F(0)
            for (i, j), c in Hl:
                val += Fd.el(c) * tp ** i * t ** j
            key = Fd.fmt(t)
            if key in rdict:
                n_nonzero += 1
                ok_res &= (Fd.fmt(-val) == rdict[key])
                # conjecture: H(t^p,t) == (-N/p) / W_t
                ok_conj &= (Fd.fmt(val) == Fd.fmt(Fd.el(legmN) / parse(Fd, Wd[key])))
            else:
                ok_res &= (val == F(0))
    return {"N": N, "p": p, "kronecker_mod_p": kron, "H_symmetric": sym, "H_bidegree_le_p+1": deg_ok,
            "residue_equals_minus_H_all_Fp2": ok_res, "thin_count": n_nonzero,
            "hecke_form_of_conjecture": ok_conj}


def parse(Fd, s):
    # inverse of Field.fmt for strings produced by fmt
    if s.lstrip('-').isdigit():
        return Fd.el(int(s))
    F = Fd.F
    z = F.gen()
    # format like 'a*z + b' or 'z + b' or 'a*z'
    s2 = s.replace(' ', '')
    val = F(0)
    for term in s2.replace('-', '+-').split('+'):
        if not term:
            continue
        if 'z' in term:
            co = term.replace('*z', '').replace('z', '')
            co = 1 if co in ('', '+') else (-1 if co == '-' else int(co))
            val += Fd.el(co) * z
        else:
            val += Fd.el(int(term))
    return val


if __name__ == "__main__":
    pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 23
    out = []
    for p in primes_upto(pmax):
        if p < 5:
            continue
        for N in LEVELS:
            if N == p:
                continue
            res = check(N, p)
            print(res, flush=True)
            out.append(res)
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
    with open(os.path.join(base, "hecke_polynomial_checks.json"), "w") as f:
        json.dump(out, f, indent=1)
    assert all(all(v for k, v in r.items() if isinstance(v, bool)) for r in out)
    print("all Hecke-polynomial checks passed")
