#!/usr/bin/env python3
"""Independent exact verification of Conjecture 1.5 (now Theorem):
    c_p := E_{p+1}^{(p-1)/2} / Delta^{(p^2-1)/24}  on the supersingular locus  =  (6/p) ((p-1)/2)!  in F_p.

Four computational routes, all exact finite-field arithmetic (no floating point):
  IV  polynomial divisibility  E_{p-1} | E_{p+1}^h - c Delta^k  in F_p[E4,E6], via the exact j-line
      reduction  R(j) := E_{p+1}^h/Delta^k mod ss_p(j)  (equivalence proved in the note, Lemma 2.2).
  I   evaluation of E_{p+1} (as a polynomial in E4,E6) at every supersingular j in F_{p^2}, on several
      randomly rescaled models (E4,E6) -> (u^4 E4, u^6 E6), u random in F_{p^2}^*.
  II  Legendre route: c = (6/p) 2^{8k} (l(1-l))^{h-2k} H'(l)^h at every root l of the Deuring polynomial
      H(l) = sum binom(h,i)^2 l^i  (no Eisenstein series used).
  III Weierstrass/Hasse-Witt route: on y^2 = x^3+ax+b with omega = dx/y,
      c = (3/p) * ([x^{p-2}](x^3+ax+b)^h)^h / Delta^k,  Delta = -(4a^3+27b^2)/256  (no E_{p+1} used).
Also checked: B(E,dx/y) = 3 [x^{p-2}] f^h at supersingular points, the supersingular counts (Eichler-Deuring),
and that the Legendre j-values coincide with the roots of ss_p(j).
Usage: python3 -I verify_factorial.py PMAX [PMIN] [--models M] [--seed S] [--out FILE]
"""
import sys, os, json, time, random, argparse, platform
import cypari2

ap = argparse.ArgumentParser()
ap.add_argument("pmax", type=int)
ap.add_argument("pmin", type=int, nargs="?", default=5)
ap.add_argument("--models", type=int, default=3, help="random rescaled models per supersingular j (route I)")
ap.add_argument("--seed", type=int, default=20261104)
ap.add_argument("--out", default=None)
ap.add_argument("--no-legendre", action="store_true")
ap.add_argument("--no-weierstrass", action="store_true")
ap.add_argument("--negate", action="store_true", help="negative control: test -(6/p)h! instead (every route should FAIL)")
args = ap.parse_args()

here = os.path.dirname(os.path.abspath(__file__))
pari = cypari2.Pari()
pari.allocatemem(2 * 10**9)

pari(f'read("{os.path.join(here, "modp_lib.gp")}")')
random.seed(args.seed)

def primes(a, b):
    return [n for n in range(max(a, 5), b + 1) if all(n % d for d in range(2, int(n**0.5) + 1))]

def run(p):
    t0 = time.time()
    h, k = (p - 1) // 2, (p * p - 1) // 24
    rec = {"p": p, "p_mod_12": p % 12}
    pari(f"p={p}; h={h}; k={k}; A=epoly(p-1,p); B=epoly(p+1,p); S=sspoly(A,p);")
    pari("cpred = Mod(kronecker(6,p)*h!, p);")
    if args.negate: pari("cpred = -cpred;")
    rec["c_pred"] = int(pari("lift(cpred)"))
    # supersingular polynomial: monic, squarefree, expected degree
    deg = int(pari("poldegree(S)"))
    expected = p // 12 + {1: 0, 5: 1, 7: 1, 11: 2}[p % 12]
    rec["n_ss_j"] = deg
    rec["ss_count_ok"] = (deg == expected)
    rec["ss_monic_squarefree"] = bool(pari("pollead(S)==1 && poldegree(gcd(S,deriv(S)))==0"))
    # ---- Route IV: exact divisibility via j-line remainder
    pari("tB = wdec(p+1); bj = jpart(B, p+1, p);")
    pari("Rm = Mod('j,S)^(h*tB[2]/3) * Mod('j-1728,S)^(h*tB[3]/2) * Mod(bj,S)^h;")
    rem = pari("lift(Rm)")
    rec["IV_remainder_is_constant"] = bool(pari("poldegree(lift(Rm)) <= 0"))
    rec["IV_divisibility_ok"] = bool(pari("lift(Rm) == lift(cpred)*Mod(1,p)"))
    # ---- roots of ss_p in F_{p^2}
    pari("J = rootsFq(S, p); nJ = #J; nJFp = sum(i=1,nJ, J[i]^p==J[i]);")
    rec["n_ss_j_in_Fp"] = int(pari("nJFp"))
    rec["n_ss_j_not_in_Fp"] = int(pari("nJ - nJFp"))
    # ---- Route I: evaluate E_{p+1} poly on random models
    allI = True; cvals = set(); B3ok = True; IIIok = True
    for i in range(1, int(pari("nJ")) + 1):
        pari(f"j0 = J[{i}];")
        pari("if(j0==0, e4b=0*j0; e6b=1+0*j0, if(j0==1728, e4b=1+0*j0; e6b=0*j0, e4b=j0*(j0-1728); e6b=j0*(j0-1728)^2));")
        for m in range(args.models):
            a0, a1 = random.randrange(p), random.randrange(p)
            if a0 == 0 and a1 == 0: a0 = 1
            pari(f"u = {a0} + {a1}*ffgen(J[1]); if(u==0,u=1+0*u); e4 = u^4*e4b; e6 = u^6*e6b; D = (e4^3-e6^2)/1728;")
            pari("Av = subst(subst(A,'X,e4),'Y,e6); Bv = subst(subst(B,'X,e4),'Y,e6); cv = Bv^h/D^k;")
            ok = bool(pari("Av == 0 && cv == cpred && D != 0 && e4^3/D == j0"))
            allI &= ok
            cvals.add(str(pari("cv")))
            if not args.no_weierstrass:
                # Route III on y^2 = x^3 + a x + b with E4(E,dx/y) = -3a, E6(E,dx/y) = 27b/2
                pari("aa = -e4/3; bb = 2*e6/27; DW = -(4*aa^3+27*bb^2)/256;")
                pari("c2 = polcoef(('x^3+aa*'x+bb)^h, p-2, 'x); cW = kronecker(3,p)*c2^h/DW^k;")
                IIIok &= bool(pari("DW == D && cW == cpred"))
                B3ok &= bool(pari("Bv == 3*c2"))
    rec["I_all_models_ok"] = allI
    rec["I_distinct_values"] = sorted(cvals)
    rec["I_models_per_j"] = args.models
    if not args.no_weierstrass:
        rec["III_hasse_witt_route_ok"] = IIIok
        rec["B_equals_3c_{p-2}_ok"] = B3ok
    # ---- Route II: Legendre / Deuring polynomial
    if not args.no_legendre:
        pari("H = sum(i=0,h,binomial(h,i)^2*'j^i); L = rootsFq(H*Mod(1,p), p); dH = deriv(H);")
        pari("cL = vector(#L, i, my(l=L[i]); kronecker(6,p)*2^(8*k)*(l*(1-l))^(h-2*k)*subst(dH,'j,l)^h);")
        rec["II_n_lambda"] = int(pari("#L"))
        rec["II_legendre_ok"] = bool(pari("#L==h && vecmin(vector(#L,i,cL[i]==cpred))==1"))
        pari("JL = Set(vector(#L,i, my(l=L[i]); 256*(l^2-l+1)^3/(l^2*(l-1)^2)));")
        rec["II_j_sets_agree"] = bool(pari("JL == Set(J)"))
    rec["seconds"] = round(time.time() - t0, 3)
    keys = ["ss_count_ok", "ss_monic_squarefree", "IV_remainder_is_constant", "IV_divisibility_ok", "I_all_models_ok"]
    if not args.no_weierstrass: keys += ["III_hasse_witt_route_ok", "B_equals_3c_{p-2}_ok"]
    if not args.no_legendre: keys += ["II_legendre_ok", "II_j_sets_agree"]
    rec["all_ok"] = all(rec[x] for x in keys)
    return rec

out = []
T0 = time.time()
for p in primes(args.pmin, args.pmax):
    r = run(p)
    out.append(r)
    print(p, p % 12, "ss_j:", r["n_ss_j"], "(non-F_p:", r["n_ss_j_not_in_Fp"], ")", "c_p:", r["c_pred"],
          "ALL_OK" if r["all_ok"] else "FAIL", r["seconds"], "s", flush=True)
meta = {"pmin": args.pmin, "pmax": args.pmax, "n_primes": len(out),
        "all_ok": all(r["all_ok"] for r in out), "failures": [r["p"] for r in out if not r["all_ok"]],
        "total_seconds": round(time.time() - T0, 1), "seed": args.seed, "models_per_j": args.models,
        "python": sys.version.split()[0], "pari": str(pari("version()")), "cypari2": __import__("importlib.metadata").metadata.version("cypari2"),
        "platform": platform.platform()}
print(json.dumps(meta))
if args.out:
    json.dump({"meta": meta, "records": out}, open(args.out, "w"), indent=1)
