"""Exact tests of the ten new Fricke levels. See README for source and limits.
No signed-residue identity is used to reconstruct the U_p rational function.
"""
import json,sys,time
from pathlib import Path
from fractions import Fraction
from flint import nmod_poly, fmpz_poly
from inherited_wr_core import (Field, primes_upto, legendre, euler_coeffs,
    inflate, ss_j_deuring, ss_j_hasse, horner_series, poly_in_T_from_series)

DATA=json.loads(Path(__file__).with_name('hyperelliptic_data.json').read_text())

def j_series(p,L):
    sig=[0]*L
    for d in range(1,L):
        v=pow(d,3,p)
        for i in range(d,L,d):sig[i]=(sig[i]+v)%p
    E4=nmod_poly([1]+[240*x%p for x in sig[1:]],p)
    E=nmod_poly(euler_coeffs(L),p)
    return E4.pow_trunc(3,L).mul_low(E.pow_trunc(24,L).inverse_series_trunc(L),L)

def qT(N,p,L):
    """Newton inverse of alpha(u)=j(q)+j(q^N), u=T+shift."""
    d=DATA[str(N)];a=d['alpha'];ap=[i*a[i] for i in range(1,len(a))]
    J=j_series(p,L)
    rhs=(J.left_shift(N-1)+nmod_poly(inflate(J.coeffs(),N,L),p)).truncate(L)
    U=nmod_poly([1],p);n=1
    while n<L:
        n=min(2*n,L)
        H=horner_series(a,U,n,p)
        Hp=horner_series(ap,U,n,p)
        U=(U-(H-rhs.truncate(n)).mul_low(Hp.inverse_series_trunc(n),n)).truncate(n)
    assert horner_series(a,U,L,p)==rhs
    return (U-nmod_poly([0,d['shift']],p)).truncate(L),U,J

def run(N,p):
    st=time.monotonic();data=DATA[str(N)];F=Field(p)
    aa=F.poly_from_ints(data['alpha']);Q=F.poly_from_ints(data['Q'])
    ff=F.poly_from_ints(data['hyper_poly'])
    assert ff.gcd(ff.derivative()).degree()==0,'singular hyperelliptic model'
    js,_=ss_j_deuring(F);assert set(js)==set(ss_j_hasse(F))
    points={}
    for j in js.values():
        H=Q-j*aa+j*j
        roots=H.roots();assert sum(mu for _,mu in roots)==N+1
        for u,mu in roots:
            branch=ff(u)==0
            aut=3 if j==F.el(0) else 2 if j==F.el(1728) else 1
            if aut==1:m=1
            else:
                both=(aa(u)==2*j)
                numerator=aut*(2 if both and not branch else 1)
                assert numerator%mu==0,(N,p,F.fmt(u),mu,numerator)
                m=numerator//mu
                assert m in [1,2,3]
            e=m*(2 if branch else 1)
            t=u-F.el(data['shift']);key=F.key(t)
            if key in points:assert points[key]['e']==e
            points[key]={'t':t,'u':u,'e':e}
    pts=list(points.values());thin=[x for x in pts if x['e']==1]
    assert all((p+1)%x['e']==0 for x in pts)
    assert sum((Fraction(1,x['e']) for x in pts),Fraction())==Fraction((N+1)*(p-1),24)
    k=(p*p-1)//24;M=(N+1)*k
    # Enough coefficients for the existing universal certificate, plus padding.
    L=max(p**3+2,M+20,2*N+45)
    S,U,J=qT(N,p,L)
    assert int(S[0])==1 and int(S[1])==0
    # Independent q-expansion check of the second modular relation.
    C=2*N+30
    qQ=horner_series(data['Q'],U,C,p)
    qjj=J.mul_low(nmod_poly(inflate(J.coeffs(),N,C),p),C)
    assert qQ==qjj,('product relation',N,p)
    # Weighted Hasse polynomial from the cusp expansion, compared with geometry.
    C=M+16
    E=nmod_poly(euler_coeffs(C),p)
    EN=nmod_poly(inflate(E.coeffs(),N,C),p)
    series=E.mul_low(EN,C).pow_trunc(24*k,C).inverse_series_trunc(C)
    Sco=poly_in_T_from_series(S,series,M,p)
    assert horner_series(Sco,S,C,p)==series
    SP=F.poly_from_ints(Sco)
    geom=F.P([F.el(1)])
    for x in pts:geom*=F.P([-x['t'],F.el(1)])**((p+1)//x['e'])
    assert SP==geom,('Hasse weights',N,p)
    # Reconstruct P without the sign or the weighted-product formula.
    D=F.P([F.el(1)])
    for x in thin:D*=F.P([-x['t'],F.el(1)])
    dc=[F.to_int(c) for c in D.coeffs()];d=len(thin)
    C=p*p+1
    Up=nmod_poly([int(S[p*n+1]) for n in range(C)],p)
    if d:
        qdF=horner_series(dc,S,C,p).mul_low(Up,C)
        pc=poly_in_T_from_series(S,qdF.right_shift(1),d-1,p)
        assert qdF==horner_series(pc,S,C,p).left_shift(1).truncate(C)
    else:
        pc=[0];assert Up.is_zero()
    PP=nmod_poly(pc,p);DP=nmod_poly(dc,p)
    assert PP.gcd(DP).degree()==0
    assert (nmod_poly([0,1],p).pow_mod(p*p,DP)-nmod_poly([0,1],p))%DP==0 if d else True
    ratios=set();expected=-legendre(-N,p)%p
    for x in thin:
        t=x['t'];res=F.eval_nmod(PP,t)/F.eval_nmod(DP.derivative(),t)
        W=F.el(1)
        for y in pts:
            if t!=y['t']:W*=(t-y['t'])**((p+1)//y['e'])
        assert res!=0 and F.in_Fp(res) and F.in_Fp(W)
        assert res*W==F.el(expected)
        ratios.add(F.to_int(res*W))
    return {'N':N,'p':p,'n_supersingular':len(pts),'n_thin':d,
        'n_nonrational_thin':sum(not F.in_Fp(x['t']) for x in thin),
        'weight_counts':{str(e):sum(x['e']==e for x in pts) for e in sorted({x['e'] for x in pts})},
        'certificate':True,'geometric_weights':True,'weighted_polynomial':True,
        'signed_residues':True,'expected':expected,'ratio_set':sorted(ratios),
        'numerator':pc,'denominator':dc,'initial_T_coefficients':[int(S[i]) for i in range(12)],
        'seconds':round(time.monotonic()-st,3)}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--pmax',type=int,default=31)
    ap.add_argument('--levels',default=','.join(DATA));ap.add_argument('--out',default='results.json')
    args=ap.parse_args();rows=[]
    for N in map(int,args.levels.split(',')):
        for p in primes_upto(args.pmax):
            if p<5 or p==N:continue
            row=run(N,p);rows.append(row);print(json.dumps(row),flush=True)
            Path(args.out).write_text(json.dumps(rows,indent=1))
    print('PASS',len(rows),'pairs',sum(r['n_thin'] for r in rows),'thin points',flush=True)
