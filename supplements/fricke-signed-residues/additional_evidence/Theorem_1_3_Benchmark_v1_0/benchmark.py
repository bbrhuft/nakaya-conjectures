#!/usr/bin/env python3
"""Exact Theorem 1.3 benchmark; no inherited files modified.
Requires python-flint==0.9.0 and gcc on Linux x86-64. See README.md.
"""
import ctypes as ct, pathlib, subprocess, time, statistics, json, random, platform, sys, os, math, csv
import flint
from flint import nmod_poly, fq_default_ctx, fq_default_poly_ctx
ROOT=pathlib.Path(__file__).resolve().parent
LIB=next(pathlib.Path(flint.__file__).parent.parent.glob('python_flint.libs/libflint*'))
subprocess.run(['gcc','-O3','-DNDEBUG','-shared','-fPIC',str(ROOT/'native.c'),str(LIB),'-Wl,-rpath,'+str(LIB.parent),'-o',str(ROOT/'native.so')],check=True)
C=ct.CDLL(str(ROOT/'native.so')); U=ct.c_ulong; L=ct.c_long; UP=ct.POINTER(U); V=ct.c_void_p
for name, args, res in [('fast_fac',[U,U],U),('loop_fac',[U,U],U),('poly_new',[UP,L,U],V),('poly_free',[V],None),('evaluate',[V,U,U,U,U,U,U,ct.c_int],U),('run',[V,UP,UP,L,U,U,U,U,ct.c_int,L],U),('run_batch',[V,UP,UP,L,U,U,U,L],U)]:
 f=getattr(C,name);f.argtypes=args;f.restype=res
C.run_dedup.argtypes=C.run_batch.argtypes;C.run_dedup.restype=U

def measure(fn, target=.025, rounds=7):
 """Warm up; calibrate iterations; median/IQR of seven repeated blocks."""
 fn(); n=1
 while True:
  t=time.perf_counter_ns()
  for _ in range(n):fn()
  elapsed=(time.perf_counter_ns()-t)*1e-9
  if elapsed>=target/3:break
  n*=max(2,min(32,int(target/max(elapsed,1e-9)/3)))
 samples=[]
 for _ in range(rounds):
  t=time.perf_counter_ns()
  for _ in range(n):fn()
  samples.append((time.perf_counter_ns()-t)*1e-9/n)
 return {'median_s':statistics.median(samples),'min_s':min(samples),'max_s':max(samples),'iqr_s':statistics.quantiles(samples,n=4)[2]-statistics.quantiles(samples,n=4)[0],'iterations':n,'samples_s':samples}

def coeffs(p,target=None):
 """P such that [x^(p-2)] W^h = a^r b^s P(a^3/b^2).
 Uses multinomials, not the factorial theorem. Four FLINT factorials
 initialize c0, and batch inversion gives the rest in O(degree) operations.
 """
 h=(p-1)//2;target=p-2 if target is None else target
 i=max(0,(target-h+1)//2);j=target-3*i;k=h-i-j
 d=target//3-i
 c=C.fast_fac(h,p)*pow(C.fast_fac(i,p)*C.fast_fac(j,p)%p*C.fast_fac(k,p)%p,-1,p)%p
 den=[(i+t+1)*(k+2*t+1)*(k+2*t+2)%p for t in range(d)]
 pre=[1]
 for v in den:pre.append(pre[-1]*v%p)
 inv=pow(pre[-1],-1,p); dinv=[0]*d
 for t in range(d-1,-1,-1):dinv[t]=inv*pre[t]%p;inv=inv*den[t]%p
 cs=[c]
 for t in range(d):
  jt=j-3*t;c=c*jt*(jt-1)*(jt-2)*dinv[t]%p;cs.append(c)
 return list(reversed(cs)),j-3*d,k+2*d

CM=[(-3,0),(-4,1728),(-7,-3375),(-8,8000),(-11,-32768),(-19,-884736),(-43,-884736000),(-67,-147197952000),(-163,-262537412640768000)]
def models(p):
 """Known inert CM seed, then normalized 2-isogenies; roots over Fp^2.
 No use of Theorem 1.3 to select or certify the curves.
 """
 rng=random.Random(20261105+p);F=fq_default_ctx(p,2,'z');R=fq_default_poly_ctx(F)
 disc,j=next((D,j%p) for D,j in CM if pow(D%p,(p-1)//2,p)==p-1)
 j=F(j)
 def from_j(j):
  if j==0:e4,e6=F(0),F(1)
  elif j==F(1728):e4,e6=F(1),F(0)
  else:e4,e6=j*(j-1728),j*(j-1728)**2
  return -e4/3,2*e6/27
 a,b=from_j(j);pool={};base={}
 for D,jj in CM:
  if pow(D%p,(p-1)//2,p)==p-1 and jj%p not in [0,1728%p]:
   base[str(F(jj%p))]=from_j(F(jj%p))
 for _ in range(600):
  D=-(4*a**3+27*b**2)/256
  e4=-3*a;j=e4**3/D
  if not a.is_zero() and not b.is_zero():
   pool[str(j)]=(a,b)
   if j.frobenius()==j:base[str(j)]=from_j(j)
  if len(pool)>=32 and len(base)>=4:break
  roots=R([b,a,0,1]).roots();assert len(roots)==3
  rr=roots[rng.randrange(3)][0]
  a,b=-4*a-15*rr**2,-22*rr**3-8*a*rr
 # Make 32 nontrivially rescaled models, keeping unique-j counts explicit.
 assert pool and base,(p,len(pool),len(base))
 def rescaled(items,n,extension):
  vals=list(items.values());out=[]
  for i in range(n):
   aa,bb=vals[i%len(vals)];u=F([rng.randrange(1,p),rng.randrange(1,p)]) if extension else F(rng.randrange(1,p))
   out.append((aa*u**4,bb*u**6))
  return out
 return F,R,rescaled(base,32,False),rescaled(pool,32,True),{'seed_CM_discriminant':disc,'available_distinct_j':len(pool),'available_Fp_j':len(base),'Fq_distinct_j_used':min(32,len(pool)),'Fp_distinct_j_used':min(32,len(base)),'field_modulus':str(F.modulus())}

def as_int(x):
 v=x.to_list();assert len(v)<=1 or all(t==0 for t in v[1:]);return int(v[0]) if v else 0

def verify_small(p,cs,r,s):
 """Against explicit polynomial powering, on ALL nonsingular (a,b)
 for tiny p; B=3*c_(p-2) is used only on supersingular curves."""
 h=(p-1)//2;k=(p*p-1)//24;cp=C.loop_fac(h,p)*int(pow(6,h,p))%p;n=0
 for a in range(p):
  for b in range(p):
   D=-(4*a**3+27*b*b)*pow(256,-1,p)%p
   if not D:continue
   W=nmod_poly([b,a,0,1],p)**h
   if int(W[p-1]):continue
   expected=pow(3*int(W[p-2])%p,h,p)
   assert expected==cp*pow(D,k,p)%p
   n+=1
 return n

def run(p):
 assert p<2**31
 h=(p-1)//2;k=(p*p-1)//24
 t=time.perf_counter();cs,r,s=coeffs(p);construction=time.perf_counter()-t
 cp=C.fast_fac(h,p)*pow(6,h,p)%p
 assert cp==C.loop_fac(h,p)*pow(6,h,p)%p
 cc=(U*len(cs))(*cs);poly=C.poly_new(cc,len(cs),p)
 F,R,bases,exts,meta=models(p)
 aa=(U*len(bases))(*(as_int(a) for a,b in bases));bb=(U*len(bases))(*(as_int(b) for a,b in bases))
 for a,b in zip(aa,bb):
  assert C.evaluate(poly,a,b,p,r,s,cp,0)==C.evaluate(poly,a,b,p,r,s,cp,1)
 assert C.run_batch(poly,aa,bb,len(bases),p,r,s,1)==C.run(poly,aa,bb,len(bases),p,r,s,cp,0,1)
 assert C.run_dedup(poly,aa,bb,len(bases),p,r,s,1)==C.run(poly,aa,bb,len(bases),p,r,s,cp,0,1)
 Q=R(cs);inv256=F(256).inverse()
 def baseline(a,b):
  bv=3*a**r*b**s*Q(a**3/(b*b))
  return bv**h
 def theorem(a,b):return cp*(-(4*a**3+27*b*b)*inv256)**k
 for a,b in exts:assert baseline(a,b)==theorem(a,b)
 # Independent Hasse evaluation for EVERY timed model, at EVERY prime.
 ac,ar,ass=coeffs(p,p-1);AQ=R(ac)
 for a,b in bases+exts:
  assert (a**ar*b**ass*AQ(a**3/(b*b))).is_zero()
 # Explicit Hasse and coefficient checks at p <= 1009, including extension models.
 if p<=1009:
  for a,b in bases[:4]+exts[:4]:
   W=R([b,a,0,1])**h
   assert W[p-1]==0
   assert (3*W[p-2])**h==theorem(a,b)
   assert 3*W[p-2]==3*a**r*b**s*Q(a**3/(b*b))
 result={'p':p,'cp':int(cp),'degree_P':len(cs)-1,'r':r,'s':s,'coefficient_construction_s':construction,'polynomial_coefficient_payload_bytes':8*len(cs),'verification':'PASS','Hasse_checks':len(bases)+len(exts),'models':meta,
 'inputs':{'field_modulus_coefficients':[int(t) for t in F.modulus().coeffs()],
 'Fp':[[as_int(a),as_int(b)] for a,b in bases],
 'Fq':[[[int(t) for t in a.to_list()],[int(t) for t in b.to_list()]] for a,b in exts],
 'Fp_outputs':[int(C.evaluate(poly,a,b,p,r,s,cp,1)) for a,b in zip(aa,bb)],
 'Fq_outputs':[[int(t) for t in theorem(a,b).to_list()] for a,b in exts]}}
 for mode,name in [(0,'Fp_scalar_baseline'),(1,'Fp_theorem')]:
  fn=lambda mode=mode:C.run(poly,aa,bb,len(bases),p,r,s,cp,mode,1)
  result[name]=measure(fn)
  result[name]['per_curve_s']=result[name]['median_s']/len(bases)
 # Batch includes all polynomial evaluation and prefactors, same input models.
 result['Fp_batch_baseline']=measure(lambda:C.run_batch(poly,aa,bb,len(bases),p,r,s,1))
 result['Fp_batch_baseline']['per_curve_s']=result['Fp_batch_baseline']['median_s']/len(bases)
 result['Fp_dedup_baseline']=measure(lambda:C.run_dedup(poly,aa,bb,len(bases),p,r,s,1))
 result['Fp_dedup_baseline']['per_curve_s']=result['Fp_dedup_baseline']['median_s']/len(bases)
 for name,fun in [('Fq_scalar_baseline',baseline),('Fq_theorem',theorem)]:
  def fn(fun=fun):
   for a,b in exts:fun(a,b)
  result[name]=measure(fn);result[name]['per_curve_s']=result[name]['median_s']/len(exts)
 result['factorial_FLINT_fast']=measure(lambda:C.fast_fac(h,p))
 result['factorial_native_loop']=measure(lambda:C.loop_fac(h,p))
 result['Fp_speedup_vs_best_tested']=min(result[n]['per_curve_s'] for n in ['Fp_scalar_baseline','Fp_batch_baseline','Fp_dedup_baseline'])/result['Fp_theorem']['per_curve_s']
 result['Fq_speedup']=result['Fq_scalar_baseline']['per_curve_s']/result['Fq_theorem']['per_curve_s']
 C.poly_free(poly)
 return result

if __name__=='__main__':
 os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
 primes=[int(t) for t in sys.argv[1:]] or [101,1009,10007,100003,1000003]
 checks={p:verify_small(p,*coeffs(p)) for p in [5,7,11,13,17,19,23,29,31,37,41,43]}
 data={'meta':{'date':'2026-11-05','python':sys.version,'python_flint':flint.__version__,'FLINT':flint.__FLINT_VERSION__,'platform':platform.platform(),'processor':platform.processor(),'compiler':subprocess.check_output(['gcc','--version'],text=True).splitlines()[0],'seed':20261105,'rounds':7,'small_exhaustive_checks':checks,'cpu_affinity':sorted(os.sched_getaffinity(0))},'results':[]}
 for p in primes:
  print('Running',p,flush=True);rec=run(p);data['results'].append(rec)
  (ROOT/'results.json').write_text(json.dumps(data,indent=2))
  print(json.dumps({k:rec[k] for k in ['p','degree_P','Fp_speedup_vs_best_tested','Fq_speedup','coefficient_construction_s']}),flush=True)
 fields=['p','degree_P','Fp_scalar_baseline_us','Fp_batch_baseline_us','Fp_dedup_baseline_us','Fp_theorem_us','Fq_scalar_baseline_us','Fq_theorem_us','factorial_fast_ms','factorial_loop_ms','coefficient_construction_s','Fp_speedup','Fq_speedup']
 with (ROOT/'summary.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for x in data['results']:
   row={k:x[k] for k in ['p','degree_P','coefficient_construction_s']}
   for n in ['Fp_scalar_baseline','Fp_batch_baseline','Fp_dedup_baseline','Fp_theorem','Fq_scalar_baseline','Fq_theorem']:row[n+'_us']=x[n]['per_curve_s']*1e6
   row.update(factorial_fast_ms=x['factorial_FLINT_fast']['median_s']*1e3,factorial_loop_ms=x['factorial_native_loop']['median_s']*1e3,Fp_speedup=x['Fp_speedup_vs_best_tested'],Fq_speedup=x['Fq_speedup']);w.writerow(row)
