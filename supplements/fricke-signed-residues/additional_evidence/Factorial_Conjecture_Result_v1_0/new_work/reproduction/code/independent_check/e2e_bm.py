"""Independent end-to-end check of r_i W_i = -(-N/p).
den R from Berlekamp-Massey on the 1/T expansion of T|U_p (no supersingular input);
supersingular T-values and weights from factoring S(T)=Delta_N^{-k} (Prop. S) written in T."""
import sys
from flint import nmod_poly, fq_default_ctx, fq_default_poly_ctx

AB = {2: (24, 4096), 3: (12, 729), 5: (6, 125), 7: (4, 49), 13: (2, 13)}

def euler(L, p, step=1):
    c = [0]*L
    # prod (1-q^{step n}) via pentagonal numbers
    k = 0
    while True:
        done = True
        for kk in ([k, -k] if k else [0]):
            e = step*(kk*(3*kk-1)//2)
            if e < L:
                c[e] = (c[e] + (-1)**abs(kk)) % p; done = False
        if done and k > 0: break
        k += 1
    return nmod_poly(c, p)

def T_series(N, p, L):
    """returns tau = q*T as nmod_poly mod q^L (tau = 1 + 0 q + ...)."""
    a, b = AB[N]
    E1 = euler(L+2, p); EN = euler(L+2, p, N)
    # u*q = (E1/EN)^a
    r = E1.mul_low(EN.inverse_series_trunc(L+2), L+2)
    uq = r.pow_trunc(a, L+2)
    # b/u = b*q/(uq)
    inv = uq.inverse_series_trunc(L+2)
    # tau = uq + a q + b q^2 * inv
    tau = uq + nmod_poly([0, a], p) + nmod_poly([0, 0, b], p).mul_low(inv, L+2)
    return tau.truncate(L)

def BM(s, p):
    # Berlekamp-Massey over F_p; returns connection polynomial C (C[0]=1) and length Lc
    C = [1]; B = [1]; Lc = 0; m = 1; bb = 1
    for n in range(len(s)):
        d = s[n]
        for i in range(1, Lc+1):
            d = (d + C[i]*s[n-i]) % p
        if d == 0:
            m += 1; continue
        coef = d*pow(bb, -1, p) % p
        Cn = C + [0]*max(0, len(B)+m-len(C))
        for i, x in enumerate(B):
            Cn[i+m] = (Cn[i+m] - coef*x) % p
        if 2*Lc <= n:
            B = C; Lc = n+1-Lc; bb = d; m = 1
        else:
            m += 1
        C = Cn
    return C[:Lc+1], Lc

def leg(a, p):
    a %= p
    return 1 if pow(a, (p-1)//2, p) == 1 else -1

def run(N, p):
    a, b = AB[N]
    k = (p*p-1)//24
    M = (N+1)*k
    # --- den R via BM ---
    nterms = 2*((N+1)*(p-1)//24 + 6) + 10
    LT = p*(nterms+2) + 2
    tau = T_series(N, p, LT)
    tc = [int(x) for x in tau.coeffs()] + [0]*LT
    # T|U_p coefficients c_n = coeff of q^{pn} in T = coeff of q^{pn+1} in tau
    f = [tc[p*n+1] % p if p*n+1 < LT else None for n in range(nterms+2)]
    assert f[0] == 0
    # series w = 1/T = q/tau ; reversion q(w)
    Ls = nterms+2
    tauL = tau.truncate(Ls)
    # q = w * tau(q): fixed point iteration
    qw = nmod_poly([0, 1], p)
    for _ in range(Ls):
        qw = nmod_poly([0, 1], p).mul_low(tauL.compose(qw).truncate(Ls), Ls)
    fpoly = nmod_poly(f[:Ls], p)
    Rw = fpoly.compose(qw).truncate(Ls)       # R as series in w, R = sum_{n>=1} r_n w^n
    rseq = ([int(x) for x in Rw.coeffs()] + [0]*Ls)[1:Ls]
    C, d = BM(rseq, p)
    # D(T) monic of degree d : C(w) = w^d D(1/w)
    Dt = nmod_poly(list(reversed(C + [0]*(d+1-len(C)))), p)
    Dw = nmod_poly(C, p)
    Pw = [int(x) for x in Dw.mul_low(Rw, d+1).coeffs()] + [0]*(d+2)
    P = nmod_poly([Pw[d-m] for m in range(d)], p) if d else nmod_poly([0], p)
    # --- S(T) from Delta_N^{-k} ---
    LS = M + 1
    E1 = euler(LS+1, p); EN = euler(LS+1, p, N)
    G = E1.mul_low(EN, LS+1).inverse_series_trunc(LS+1).pow_trunc(24*k, LS+1)  # q^M Delta_N^{-k}
    Gc = [int(x) for x in G.coeffs()] + [0]*(LS+1)
    # coefficient list g[i] = coeff of q^{-M+i}
    g = Gc[:LS]
    tauS = tau.truncate(LS+1) if tau.length() > LS else tau
    # need tau^m mod q^{m+1}; compute iteratively
    Scoef = [0]*(M+1)
    # we eliminate from top: S = sum s_m T^m, T^m = q^{-m} tau^m
    # coefficient of q^{-M+i} in T^m = coeff of q^{m-M+i}... handle via full array
    taupow = [None]*(M+1)
    tp = nmod_poly([1], p)
    taus = tau.truncate(M+2)
    for m in range(M+1):
        taupow[m] = tp
        tp = tp.mul_low(taus, M+2)
    rem = g[:]  # rem[i] coeff of q^{-M+i}, i=0..M
    for m in range(M, -1, -1):
        i = M - m
        s = rem[i] % p
        Scoef[m] = s
        if s:
            tcf = [int(x) for x in taupow[m].coeffs()] + [0]*(M+2)
            # T^m = sum_j tcf[j] q^{j-m}; q^{j-m} = q^{-M + (M-m+j)}
            for j in range(0, m+1):
                idx = M - m + j
                if idx <= M:
                    rem[idx] = (rem[idx] - s*tcf[j]) % p
    assert all(x % p == 0 for x in rem)
    S = nmod_poly(Scoef, p)
    F = fq_default_ctx(p, 2); RP = fq_default_poly_ctx(F)
    Sroots = RP([F(int(c)) for c in S.coeffs()]).roots()
    mult = {str(t): (t, m) for t, m in Sroots}
    thin = [t for t, m in Sroots if m == p+1]
    assert all((p+1) % m == 0 for _, m in Sroots), "multiplicity not (p+1)/e"
    mass_ok = sum(m for _, m in Sroots) == M
    Dq = RP([F(int(c)) for c in Dt.coeffs()])
    Drts = Dq.roots()
    Dset = sorted(str(t) for t, _ in Drts)
    thinset = sorted(str(t) for t in thin)
    Pq = RP([F(int(c)) for c in P.coeffs()]) if d else None
    dD = Dq.derivative() if d else None
    vals = set()
    for t, _ in Drts:
        r = Pq(t)/dD(t)
        W = F(1)
        for t2, m2 in Sroots:
            if t2 != t:
                W *= (t - t2)**m2
        vals.add(str(r*W))
    pred = -leg(-N, p) % p
    return dict(N=N, p=p, d=d, s=len(Sroots), thin=len(thin), den_eq_thin=(Dset == thinset),
                all_simple=all(m == 1 for _, m in Drts) and Dq.degree() == len(Drts),
                mass_ok=mass_ok, vals=vals, pred=pred)

if __name__ == "__main__":
    pairs = [(13, 7), (7, 11), (2, 29), (5, 19), (3, 23), (13, 17), (7, 29), (13, 29), (2, 31), (5, 37)]
    for N, p in pairs:
        r = run(N, p)
        ok = r['den_eq_thin'] and r['all_simple'] and r['mass_ok'] and r['vals'] <= {str(r['pred'])} and len(r['vals']) == (1 if r['thin'] else 0)
        print(r, "OK" if ok else "FAIL", flush=True)
