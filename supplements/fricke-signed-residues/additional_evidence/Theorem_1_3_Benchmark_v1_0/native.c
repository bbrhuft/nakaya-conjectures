#include <stdint.h>
#include <stdlib.h>
#include <time.h>
/* Minimal public FLINT 3.x ABI declarations. This file is compiled against
   the FLINT shared library bundled with python-flint; see README. */
typedef unsigned long U;
typedef struct { U n,ninv,norm; } nmod_t;
typedef struct { U *coeffs; long alloc,length; nmod_t mod; } poly_t;
extern void nmod_poly_init(poly_t*,U);
extern void nmod_poly_clear(poly_t*);
extern void nmod_poly_set_coeff_ui(poly_t*,long,U);
extern U nmod_poly_evaluate_nmod(const poly_t*,U);
extern void nmod_poly_evaluate_nmod_vec_fast(U*,const poly_t*,const U*,long);
extern U n_preinvert_limb(U);
extern U n_factorial_fast_mod2_preinv(U,U,U);
static U mul(U a,U b,U p){return a*b%p;} /* benchmark p < 2^31 */
static U pw(U a,U e,U p){U r=1;while(e){if(e&1)r=mul(r,a,p);a=mul(a,a,p);e>>=1;}return r;}
static U inv256;
U fast_fac(U n,U p){return n_factorial_fast_mod2_preinv(n,p,n_preinvert_limb(p));}
U loop_fac(U n,U p){U r=1;for(U i=2;i<=n;i++)r=mul(r,i,p);return r;}
void *poly_new(U *c,long n,U p){inv256=pw(256,p-2,p);poly_t *f=malloc(sizeof(poly_t));nmod_poly_init(f,p);for(long i=0;i<n;i++)nmod_poly_set_coeff_ui(f,i,c[i]);return f;}
void poly_free(void *f){nmod_poly_clear(f);free(f);}
/* Return the independent B^h and theorem results, including prefactors and
   discriminant construction. Formula uses omega=dx/y throughout. */
U evaluate(void *poly,U a,U b,U p,U r,U s,U cp,int mode){
 U h=(p-1)/2,k=(p*p-1)/24,a3=mul(mul(a,a,p),a,p),b2=mul(b,b,p),B;
 if(mode==1){U D=mul((p-(4*a3%p+27*b2%p)%p)%p,inv256,p);return mul(cp,pw(D,k,p),p);}
 poly_t *f=poly;
 if(b==0){/* only k=0 monomial can survive */
   long d=f->length-1;U kmin=s-2*d;
   B=kmin?0:mul(3* f->coeffs[d]%p,pw(a,r+3*d,p),p);
 }else{
   U z=mul(a3,pw(b2,p-2,p),p);
   B=mul(3*pw(a,r,p)%p,pw(b,s,p),p);
   B=mul(B,nmod_poly_evaluate_nmod(f,z),p);
 }
 return pw(B,h,p);
}
U run(void *poly,U *aa,U *bb,long n,U p,U r,U s,U cp,int mode,long reps){
 U acc=0;for(long j=0;j<reps;j++)for(long i=0;i<n;i++)acc^=evaluate(poly,aa[i],bb[i],p,r,s,cp,mode);return acc;
}
/* Batch polynomial evaluation, then identical prefactor/powering arithmetic.
   Caller supplies b != 0; allocation and evaluation are included. */
U run_batch(void *poly,U *aa,U *bb,long n,U p,U r,U s,long reps){
 U *z=malloc(n*sizeof(U)),*v=malloc(n*sizeof(U)),acc=0;
 for(long j=0;j<reps;j++){
  for(long i=0;i<n;i++){U b2=mul(bb[i],bb[i],p);z[i]=mul(mul(mul(aa[i],aa[i],p),aa[i],p),pw(b2,p-2,p),p);}
  nmod_poly_evaluate_nmod_vec_fast(v,poly,z,n);
  for(long i=0;i<n;i++){U B=mul(3*pw(aa[i],r,p)%p,pw(bb[i],s,p),p);B=mul(B,v[i],p);acc^=pw(B,(p-1)/2,p);}
 }
 free(z);free(v);return acc;
}
/* Reuse polynomial values at repeated z=a^3/b^2 within one input batch.
   This handles repeated j-invariants fairly without using Theorem 1.3. */
U run_dedup(void *poly,U *aa,U *bb,long n,U p,U r,U s,long reps){
 U *zs=malloc(n*sizeof(U)),*vs=malloc(n*sizeof(U)),acc=0;
 for(long rep=0;rep<reps;rep++){
  long count=0;
  for(long i=0;i<n;i++){
   U z=mul(mul(mul(aa[i],aa[i],p),aa[i],p),pw(mul(bb[i],bb[i],p),p-2,p),p);long j;
   for(j=0;j<count && zs[j]!=z;j++);
   if(j==count){zs[count]=z;vs[count]=nmod_poly_evaluate_nmod(poly,z);count++;}
   U B=mul(3*pw(aa[i],r,p)%p,pw(bb[i],s,p),p);B=mul(B,vs[j],p);acc^=pw(B,(p-1)/2,p);
  }
 }
 free(zs);free(vs);return acc;
}
