#!/usr/bin/env python3
"""Symbolic check, in F_p[E4,E6], of the two identities used in the proof, for primes p = 23 (mod 24),
where F = eta^(p+1) = Delta^((p+1)/24) is itself a level-one form (so no level structure is needed):
  (Q)  theta^h F = (6/p) * ( A^m F - chi12(p) F^p )        [q-expansion identity, m=(p+1)/2, h=(p-1)/2]
  (R)  theta^h F = c_h B^h F  (mod A),  c_h = 12^{-h} prod_{i<h}(m+i) = -12^{-h}/h!
theta^h is computed as the iterated modular-form operator  G -> A*serre_derivative(G) + (w/12)*B*G.
Also checks the consequence  A | B^h - (6/p) h! Delta^k  by exact polynomial division in F_p[E4,E6].
Usage: python3 -I mechanism_check.py PMAX
"""
import sys, os, time, cypari2
here = os.path.dirname(os.path.abspath(__file__))
pari = cypari2.Pari(); pari.allocatemem(2 * 10**9)
pari(f'read("{os.path.join(here, "modp_lib.gp")}")')
pari(r'''{mech(p) = my(h=(p-1)/2, m=(p+1)/2, k=(p^2-1)/24, A, B, D, F, G, w, rhsQ, ch, R, qq, r);
  A = epoly(p-1,p)*Mod(1,p); B = epoly(p+1,p)*Mod(1,p); D = ('X^3-'Y^2)*Mod(1/1728,p); F = D^((p+1)/24);
  G = F; w = m; for(i=0, h-1, G = A*sder(G,p) + Mod(w/12,p)*B*G; w += p+1);
  rhsQ = kronecker(6,p)*(A^m*F - kronecker(12,p)*F^p);
  ch = Mod(12,p)^(-h)*prod(i=0,h-1,Mod(m+i,p));
  \\ (R): G - ch*B^h*F divisible by A ; consequence: A | B^h - (6/p)h! D^k
  R = divA(lift(G - ch*B^h*F), p*m, lift(A), p);
  qq = divA(lift(B^h - kronecker(6,p)*h!*D^k), 12*k, lift(A), p);
  [p, G == rhsQ, ch == -Mod(12,p)^(-h)/h!, R, qq, divA(lift(B^h + kronecker(6,p)*h!*D^k), 12*k, lift(A), p)];}''')
pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 200
for p in [q for q in range(23, pmax + 1, 24) if all(q % d for d in range(2, int(q**0.5) + 1))]:
    t = time.time(); r = pari(f"mech({p})")
    print(f"p={p}: (Q) {bool(r[1])}  c_h=-12^-h/h! {bool(r[2])}  (R) {bool(r[3])}  A|B^h-(6/p)h!D^k {bool(r[4])}  (control A|B^h+(6/p)h!D^k: {bool(r[5])})  [{time.time()-t:.1f}s]", flush=True)
