#!/usr/bin/env python3
"""Replay every saved input in its exact field, without timing or new sampling.
Independently compare classical Hasse derivatives with coefficient extraction.
"""
import json
from flint import fq_default_ctx,fmpz_mod_poly_ctx,fq_default_poly_ctx
from benchmark import ROOT,C,coeffs
data=json.loads((ROOT/'results.json').read_text());total=0
for rec in data['results']:
 p=rec['p'];h=(p-1)//2;k=(p*p-1)//24
 F=fq_default_ctx(modulus=fmpz_mod_poly_ctx(p)(rec['inputs']['field_modulus_coefficients']),var='z');R=fq_default_poly_ctx(F)
 cs,r,s=coeffs(p);Q=R(cs);ac,ar,ass=coeffs(p,p-1);A=R(ac);DA=A.derivative()
 cp=C.fast_fac(h,p)*pow(6,h,p)%p
 for field in ['Fp','Fq']:
  for pair,out in zip(rec['inputs'][field],rec['inputs'][field+'_outputs']):
   a,b=map(F,pair);z=a**3/b**2;D=-(4*a**3+27*b*b)/256
   assert not D.is_zero()
   assert A(z).is_zero()
   B=3*a**r*b**s*Q(z)
   # 12*SerreDerivative(H) = 18*b*H_a - 4*a^2*H_b.
   Ha=a**(ar-1)*b**ass*(ar*A(z)+3*z*DA(z))
   Hb=a**ar*b**(ass-1)*(ass*A(z)-2*z*DA(z))
   assert B==18*b*Ha-4*a*a*Hb
   assert B**h==cp*D**k==F(out)
   total+=1
 print(p,'PASS: saved inputs, Hasse=0, classical Hasse derivative, coefficient route, theorem and saved outputs',flush=True)
print('PASS',total,'saved evaluations')
