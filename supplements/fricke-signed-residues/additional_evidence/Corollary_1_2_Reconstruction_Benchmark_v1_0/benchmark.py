#!/usr/bin/env python3
"""Corollary 1.2 vs q-expansion: exact reconstruction and acquisition costs.
Requires python-flint 0.9.0, FLINT 3.6.0 Linux x86-64 wheel and GCC.
"""
import pathlib,sys,ctypes as ct,subprocess,time,json,statistics,os,platform,math,csv
from fractions import Fraction
import flint
from flint import nmod_poly,fq_default_ctx,fq_default_poly_ctx
ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'inherited'))
from wr_core import Field,ss_points,euler_coeffs,inflate,LEVELS,legendre
LIB=next(pathlib.Path(flint.__file__).parent.parent.glob('python_flint.libs/libflint*'))
subprocess.run(['gcc','-O3','-shared','-fPIC',str(ROOT/'series_bridge.c'),str(LIB),'-Wl,-rpath,'+str(LIB.parent),'-o',str(ROOT/'series_bridge.so')],check=True)
C=ct.CDLL(str(ROOT/'series_bridge.so'));U=ct.c_ulong;UP=ct.POINTER(U)
C.transform.argtypes=[UP,UP,UP,ct.c_long,U];C.transform.restype=None

def measure(fn,rounds=5,target=.015):
 fn();n=1
 while True:
  start=time.perf_counter();fn();elapsed=time.perf_counter()-start
  if elapsed>=target/4:break
  n=min(128,max(1,int(target/max(elapsed,1e-8))))
  break
 samples=[]
 for _ in range(rounds):
  start=time.perf_counter()
  for j in range(n):fn()
  samples.append((time.perf_counter()-start)/n)
 return {'median_s':statistics.median(samples),'min_s':min(samples),'max_s':max(samples),'samples_s':samples,'iterations':n,'rounds':rounds}

def hasse_j(Fd):
 """Build the short-Weierstrass Hasse polynomial in z=a^3/b^2,
 factor over Fp^2, map z to j=6912z/(4z+27), append elliptic values.
 Degree approximately p/12; no q-expansion and no new residue formula.
 """
 p=Fd.p;h=(p-1)//2;t=p-1;i=max(0,(t-h+1)//2);j=t-3*i;k=h-i-j;d=t//3-i
 fac=[1]*(h+1)
 for v in range(2,h+1):fac[v]=fac[v-1]*v%p
 inv=[1]*(h+1);inv[h]=pow(fac[h],-1,p)
 for v in range(h,0,-1):inv[v-1]=inv[v]*v%p
 coeff=[fac[h]*inv[i+v]%p*inv[j-3*v]%p*inv[k+2*v]%p for v in range(d+1)]
 P=Fd.P(list(reversed(coeff)))
 out={}
 for z,m in P.roots():
  assert m==1
  j0=6912*z/(4*z+27);out[Fd.key(j0)]=j0
 for j0,on in [(0,p%3==2),(1728,p%4==3)]:
  if on:out[Fd.key(Fd.el(j0))]=Fd.el(j0)
 expected=p//12+{1:0,5:1,7:1,11:2}[p%12]
 assert len(out)==expected,(p,len(out),expected)
 return out

def acquire(N,p):
 Fd=Field(p);js=hasse_j(Fd);tv=ss_points(N,Fd,js)
 assert sum((Fraction(1,x['e']) for x in tv),Fraction())==Fraction((N+1)*(p-1),24)
 assert all((p+1)%x['e']==0 for x in tv)
 tv.sort(key=lambda x:Fd.key(x['t']))
 return Fd,tv,len(js)

def tree_build(ts,P):
 if len(ts)==1:return (P([-ts[0],1]),None,None)
 mid=len(ts)//2;l=tree_build(ts[:mid],P);r=tree_build(ts[mid:],P)
 return (l[0]*r[0],l,r)

def tree_eval(f,tr):
 if tr[1] is None:return [f[0]]
 return tree_eval(f%tr[1][0],tr[1])+tree_eval(f%tr[2][0],tr[2])

def partial_numerator(rs,tr,offset=0):
 if tr[1] is None:return tr[0].context()([rs[offset]])
 mid=tr[1][0].degree()
 return partial_numerator(rs,tr[1],offset)*tr[2][0]+partial_numerator(rs,tr[2],offset+mid)*tr[1][0]

def descend(poly,Fd):return nmod_poly([Fd.to_int(c) for c in poly.coeffs()],Fd.p)

def reconstruct(Fd,tv):
 thin=[x['t'] for x in tv if x['e']==1];thick=[x for x in tv if x['e']!=1];p=Fd.p
 if not thin:return nmod_poly([],p),nmod_poly([1],p)
 tr=tree_build(thin,Fd.P);vals=tree_eval(tr[0].derivative(),tr)
 const=Fd.el(-legendre(-CURRENT_N,p))
 rs=[]
 for t,v in zip(thin,vals):
  # v^(p+1) is its norm; thick values remain essential in W.
  W=v*v.frobenius()
  for x in thick:W*= (t-x['t'])**((p+1)//x['e'])
  rr=const/W
  assert rr.frobenius()==rr and not rr.is_zero()
  rs.append(rr)
 return descend(partial_numerator(rs,tr),Fd),descend(tr[0],Fd)

def qS(N,p,L):
 """Optimized eta-quotient expansion: one forward ratio U and its inverse.
 Exact mod p, so valid past precision p without division by indices.
 """
 a,b=LEVELS[N];E=nmod_poly(euler_coeffs(L),p);Ea=E.pow_trunc(a,L)
 EaN=nmod_poly(inflate(Ea.coeffs(),N,L),p)
 Uq=Ea.mul_low(EaN.inverse_series_trunc(L),L)
 invU=Uq.inverse_series_trunc(L-2) if L>2 else nmod_poly([1],p)
 return (Uq+nmod_poly([0,a],p)+(b*invU).left_shift(2)).truncate(L)

def q_to_w(S,p,L):
 ss=(U*L)(*(int(S[i]) for i in range(L)))
 gg=(U*L)(*(int(S[p*i+1]) for i in range(L)))
 out=(U*L)();C.transform(out,ss,gg,L,p)
 return nmod_poly(list(out),p)

def reverse_fixed(f,d,p):return nmod_poly([int(f[d-i]) for i in range(d+1)],p)

def q_known(N,p,D):
 d=D.degree()
 # Even if d=0, do a short expansion rather than using a zero shortcut.
 L=max(2,d+1);S=qS(N,p,p*(L-1)+2);Rw=q_to_w(S,p,L)
 Dw=reverse_fixed(D,d,p);Aw=Dw.mul_low(Rw,d+1)
 assert int(Aw[0])==0
 P=reverse_fixed(Aw,d,p)
 return P,D

def rational_reconstruct(f,M,L,p):
 if f.is_zero():return nmod_poly([],p),nmod_poly([1],p)
 r0=nmod_poly([0]*L+[1],p);r1=f;t0=nmod_poly([],p);t1=nmod_poly([1],p)
 while r1.degree()>M:
  q,r=divmod(r0,r1);r0,r1=r1,r;t0,t1=t1,t0-q*t1
 assert not r1.is_zero() and t1.degree()<=M and int(t1[0])!=0
 fac=pow(int(t1[0]),-1,p);num=r1*fac;den=t1*fac
 assert (den.mul_low(f,L)-num).truncate(L).is_zero()
 assert int(num[0])==0
 d=max(num.degree(),den.degree())
 return reverse_fixed(num,d,p),reverse_fixed(den,d,p)

def q_free(N,p):
 M=max(1,(N+1)*(p-1)//24);L=2*M+1
 S=qS(N,p,p*(L-1)+2);Rw=q_to_w(S,p,L)
 return rational_reconstruct(Rw,M,L,p)

def equal_rat(x,y):return x[0]*y[1]==y[0]*x[1]

def reference_residues(Fd,tv,N):
 """Small-p independent O(s^2) evaluation of the printed product formula."""
 P=Fd.P([0]);D=Fd.P([1]);ts=[x['t'] for x in tv if x['e']==1]
 for t in ts:D*=Fd.P([-t,1])
 for t in ts:
  W=Fd.F(1)
  for x in tv:
   if x['t']!=t:W*=(t-x['t'])**((Fd.p+1)//x['e'])
  P+=(-legendre(-N,Fd.p)/W)*(D//Fd.P([-t,1]))
 return descend(P,Fd),descend(D,Fd)

def run_pair(N,p):
 global CURRENT_N;CURRENT_N=N
 Fd,tv,nj=acquire(N,p);ans=reconstruct(Fd,tv);known=q_known(N,p,ans[1]);free=q_free(N,p)
 assert equal_rat(ans,known) and equal_rat(ans,free)
 assert ans[0]==free[0] and ans[1]==free[1]
 assert ans[0].gcd(ans[1]).degree()==0
 if p<=31:assert reference_residues(Fd,tv,N)==ans
 # Build all complete routes inside the clock; acquisition repeated, no j-cache.
 def end_to_end():
  fd,tvs,_=acquire(N,p);return reconstruct(fd,tvs)
 res={'N':N,'p':p,'n_ss_j':nj,'n_ss_values':len(tv),'n_thin':ans[1].degree(),'n_thick':sum(x['e']>1 for x in tv),'nonrational_values':sum(not Fd.in_Fp(x['t']) for x in tv),'P':[int(c) for c in ans[0].coeffs()],'D':[int(c) for c in ans[1].coeffs()],'Fp2_modulus':[int(c) for c in Fd.F.modulus().coeffs()],
 'ss_data':[{'t':[int(c) for c in x['t'].to_list()],'e':x['e']} for x in tv],'verification':'PASS',
 'source_precision_q_known':p*(max(2,ans[1].degree()+1)-1)+2,'source_precision_q_free':p*(2*max(1,(N+1)*(p-1)//24))+2}
 for name,fn in [('acquisition',lambda:acquire(N,p)),('reconstruction_only',lambda:reconstruct(Fd,tv)),('ss_end_to_end',end_to_end),('q_known_denominator',lambda:q_known(N,p,ans[1])),('q_free',lambda:q_free(N,p))]:
  res[name]=measure(fn,rounds=3 if p>=509 else 5)
 res['conditional_speedup']=res['q_known_denominator']['median_s']/res['reconstruction_only']['median_s']
 res['full_speedup']=res['q_free']['median_s']/res['ss_end_to_end']['median_s']
 return res

if __name__=='__main__':
 os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
 pairs=[(N,p) for p in [11,29,59,101,211,509,1009] for N in LEVELS if N!=p]+[(2,5),(2,7)]
 if len(sys.argv)>1:pairs=[tuple(map(int,s.split(':'))) for s in sys.argv[1:]]
 out={'meta':{'date':'2026-11-05','python':sys.version,'python_flint':flint.__version__,'FLINT':flint.__FLINT_VERSION__,'platform':platform.platform(),'compiler':subprocess.check_output(['gcc','--version'],text=True).splitlines()[0],'cpu_affinity':sorted(os.sched_getaffinity(0)),'levels':list(LEVELS),'note':'No claim of optimal acquisition or fastest possible q-route. No persistent j cache across levels.'},'results':[]}
 for N,p in pairs:
  print('Running',N,p,flush=True);r=run_pair(N,p);out['results'].append(r)
  (ROOT/'results.json').write_text(json.dumps(out,indent=2))
  print(json.dumps({k:r[k] for k in ['N','p','n_thin','conditional_speedup','full_speedup']}),flush=True)
 with (ROOT/'summary.csv').open('w') as f:
  fields=['N','p','n_thin','acquisition_ms','reconstruction_ms','ss_end_to_end_ms','q_known_ms','q_free_ms','conditional_speedup','full_speedup']
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for r in out['results']:
   row={k:r[k] for k in ['N','p','n_thin','conditional_speedup','full_speedup']}
   for key,col in [('acquisition','acquisition_ms'),('reconstruction_only','reconstruction_ms'),('ss_end_to_end','ss_end_to_end_ms'),('q_known_denominator','q_known_ms'),('q_free','q_free_ms')]:row[col]=1e3*r[key]['median_s']
   w.writerow(row)
