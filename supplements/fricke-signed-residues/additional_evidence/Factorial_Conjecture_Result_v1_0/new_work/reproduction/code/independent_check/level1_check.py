"""Independent level-1 check: Baker sign, constancy of c(E)=B^{(p-1)/2}/Delta^k on ss locus,
and c_p vs (6/p)((p-1)/2)!.  Uses only E4,E6 evaluation; supersingular j found by brute force
over F_{p^2} via the Hasse invariant (coefficient of x^{p-1} in f(x)^{(p-1)/2})."""
import sys
from flint import fq_default_ctx, nmod_poly, nmod
from math import factorial

def primes(a, b):
    return [n for n in range(a, b+1) if n > 1 and all(n % d for d in range(2, int(n**.5)+1))]

def sigma(n, k):
    return sum(d**k for d in range(1, n+1) if n % d == 0)

def qexp_mod(coeffs_fn, L, p):
    return [coeffs_fn(n) % p for n in range(L)]

def mul(a, b, L, p):
    c = [0]*L
    for i, x in enumerate(a):
        if x:
            for j in range(L-i):
                c[i+j] = (c[i+j] + x*b[j]) % p
    return c

def E_basis(p):
    """Express E_{p+1} mod p as sum c_i Delta^i E4^a E6^b (4a+6b = w-12i, a<=2,b<=1)."""
    w = p + 1
    L = w//12 + 3
    E4 = [1] + [240*sigma(n, 3) % p for n in range(1, L)]
    E6 = [1] + [(-504*sigma(n, 5)) % p for n in range(1, L)]
    # Delta = (E4^3-E6^2)/1728
    inv1728 = pow(1728, -1, p)
    E43 = mul(mul(E4, E4, L, p), E4, L, p); E62 = mul(E6, E6, L, p)
    D = [((x-y)*inv1728) % p for x, y in zip(E43, E62)]
    # target: E_{p+1} == E_2 mod p : 1 - 24 sum sigma_1 q^n
    tgt = [1] + [(-24*sigma(n, 1)) % p for n in range(1, L)]
    rmin = w % 12
    if rmin == 2: rmin = 14
    n = (w - rmin)//12
    ab = {0: (0, 0), 4: (1, 0), 6: (0, 1), 8: (2, 0), 10: (1, 1), 14: (2, 1)}[rmin]
    terms = [(i, ab[0] + 3*(n-i), ab[1]) for i in range(n+1)]
    # build q-expansions
    def mono(i, a, b):
        f = [1] + [0]*(L-1)
        for _ in range(i): f = mul(f, D, L, p)
        for _ in range(a): f = mul(f, E4, L, p)
        for _ in range(b): f = mul(f, E6, L, p)
        return f
    cols = [mono(*t) for t in terms]
    # triangular solve: Delta^i starts at q^i
    coef = []
    res = tgt[:]
    for idx, t in enumerate(terms):
        i = t[0]
        c = res[i] % p  # leading coefficient of col is 1 at q^i
        coef.append(c)
        res = [(x - c*y) % p for x, y in zip(res, cols[idx])]
    assert all(x == 0 for x in res), "E_{p+1} not in span?"
    return list(zip(coef, terms))

def run(p):
    F = fq_default_ctx(p, 2)
    k = (p*p-1)//24
    rep = E_basis(p)
    # supersingular j: j with Hasse invariant 0; model y^2=x^3+ax+b
    ss = []
    for jj in F.elements() if hasattr(F, 'elements') else []:
        pass
    # enumerate F_{p^2}
    g = F.gen()
    elems = [F(a) + F(b)*g for a in range(p) for b in range(p)]
    def hasse(a, b):
        # coefficient of x^{p-1} in (x^3+ax+b)^{(p-1)/2}
        # do polynomial arithmetic with lists of F elements
        m = (p-1)//2
        poly = [F(1)]
        base = [b, a, F(0), F(1)]
        for _ in range(m):
            new = [F(0)]*(len(poly)+3)
            for i, x in enumerate(poly):
                if x != 0:
                    for j, y in enumerate(base):
                        new[i+j] += x*y
            poly = new
        return poly[p-1]
    for j in elems:
        if j == 0:
            a, b = F(0), F(1)
        elif j == 1728:
            a, b = F(1), F(0)
        else:
            a = 3*j*(1728-j); b = 2*j*(1728-j)**2
        if hasse(a, b) == 0:
            ss.append(j)
    cvals = set(); bvals = set()
    for j in ss:
        if j == 0:
            e4, e6 = F(0), F(1)
        elif j == 1728:
            e4, e6 = F(1), F(0)
        else:
            e4, e6 = j*(j-1728), j*(j-1728)**2
        D = (e4**3 - e6**2)/1728
        B = F(0)
        for c, (i, a, b) in rep:
            B += F(c) * D**i * e4**a * e6**b
        beta = B**(p-1) / D**(2*k)
        c = B**((p-1)//2) / D**k
        bvals.add(str(beta)); cvals.add(str(c))
    leg = lambda a: pow(a % p, (p-1)//2, p)
    baker = (-pow(-1 % p, (p-1)//2, p)) % p
    l6 = 1 if leg(6) == 1 else p-1
    conj = (l6 * factorial((p-1)//2)) % p
    return p, len(ss), bvals, baker, cvals, conj

if __name__ == "__main__":
    for p in primes(5, int(sys.argv[1]) if len(sys.argv) > 1 else 60):
        p, n, bv, bk, cv, cj = run(p)
        ok = (bv == {str(bk)}) and (cv == {str(cj)})
        print(p, "ss=", n, "beta", bv, "baker", bk, "c", cv, "conj", cj, "OK" if ok else "MISMATCH")
