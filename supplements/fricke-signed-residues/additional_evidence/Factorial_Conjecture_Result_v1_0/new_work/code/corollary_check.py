#!/usr/bin/env python3
"""Exact checks of corollaries stated in the note (all finite-field arithmetic):
 (W)  E_{p-1}(-3a,27b/2) = [x^{p-1}](x^3+ax+b)^h  and  E_{p+1}(-3a,27b/2) = 3 [x^{p-2}](x^3+ax+b)^h
      as polynomial identities in F_p[a,b]   (i.e. A, B on (y^2=x^3+ax+b, dx/y)).
 (J)  signed j-line formula: for every supersingular j0 not in {0,1728},
      ss_p'(j0)^h * j0^{(1-d)(p-1)/3} * (j0-1728)^{(1-e)(p-1)/4} = (-2/p) h!,   p-1 = 12n+4d+6e.
 (L)  Deuring/Legendre form: H'(l)^h = h! 2^{-(p^2-1)/3} (l(1-l))^{(p-1)(p-5)/12} at every root l of H.
Usage: python3 -I corollary_check.py PMAX [PMAX_W]
"""
import sys, os, time, cypari2
here = os.path.dirname(os.path.abspath(__file__))
pari = cypari2.Pari(); pari.allocatemem(2 * 10**9)
pari(f'read("{os.path.join(here, "modp_lib.gp")}")')
pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 300
pmaxW = int(sys.argv[2]) if len(sys.argv) > 2 else 200
pari(r'''{chkW(p) = my(h=(p-1)/2, A=epoly(p-1,p), B=epoly(p+1,p), f=('x^3+'a*'x+'b)*Mod(1,p), fh=f^h,
     sub = P -> subst(subst(P*Mod(1,p),'X,-3*'a),'Y,27*'b/2));
  [sub(A) == polcoef(fh,p-1,'x), sub(B) == 3*polcoef(fh,p-2,'x)];}''')
pari(r'''{chkJ(p) = my(h=(p-1)/2, t=wdec(p-1), d=t[2], e=t[3], A=epoly(p-1,p), S=sspoly(A,p), dS=deriv(S), J=rootsFq(S,p), tgt=Mod(kronecker(-2,p)*h!,p), ok=1, cnt=0);
  for(i=1,#J, my(j0=J[i]); if(j0==0 || j0==1728, next); cnt++;
     if(subst(lift(dS),'j,j0)^h * j0^((1-d)*(p-1)/3) * (j0-1728)^((1-e)*(p-1)/4) != tgt, ok=0));
  [ok, cnt];}''')
pari(r'''{chkL(p) = my(h=(p-1)/2, k=(p^2-1)/24, H=sum(i=0,h,binomial(h,i)^2*'j^i), L=rootsFq(H*Mod(1,p),p), dH=deriv(H), ok=1);
  for(i=1,#L, my(l=L[i]); if(subst(dH,'j,l)^h != h! * 2^(-8*k) * (l*(1-l))^(2*k-h), ok=0)); ok;}''')
primes = [q for q in range(5, pmax + 1) if all(q % d for d in range(2, int(q**0.5) + 1))]
allok = True; T = time.time()
for p in primes:
    w = list(pari(f"chkW({p})")) if p <= pmaxW else None
    j = pari(f"chkJ({p})"); l = bool(pari(f"chkL({p})"))
    ok = (w is None or all(bool(x) for x in w)) and bool(j[0]) and l
    allok &= ok
    print(p, p % 12, "W:", None if w is None else [bool(x) for x in w], "J:", bool(j[0]), f"({int(j[1])} ss j)", "L:", l, "OK" if ok else "FAIL", flush=True)
print("ALL_OK" if allok else "SOME_FAIL", f"primes 5..{pmax} (W up to {pmaxW})", f"{time.time()-T:.1f}s")
