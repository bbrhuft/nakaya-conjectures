#include <stdlib.h>
typedef unsigned long U;
typedef struct {U n,ninv,norm;} nmod_t;
typedef struct {U *coeffs;long alloc,length;nmod_t mod;} poly_t;
extern void nmod_poly_init(poly_t*,U);
extern void nmod_poly_clear(poly_t*);
extern void nmod_poly_set_coeff_ui(poly_t*,long,U);
extern void nmod_poly_inv_series(poly_t*,const poly_t*,long);
extern void nmod_poly_shift_left(poly_t*,const poly_t*,long);
extern void nmod_poly_truncate(poly_t*,long);
extern void nmod_poly_revert_series(poly_t*,const poly_t*,long);
extern void nmod_poly_compose_series(poly_t*,const poly_t*,const poly_t*,long);
/* S=q*T(q), G=(T|U_p)(q). Output G(q(w)), where w=1/T.
   FLINT's optimized series reversion and composition; no residue formula. */
void transform(U *out,const U *ss,const U *gg,long n,U p){
 poly_t S,G,inv,w,q,R;
 nmod_poly_init(&S,p);nmod_poly_init(&G,p);nmod_poly_init(&inv,p);
 nmod_poly_init(&w,p);nmod_poly_init(&q,p);nmod_poly_init(&R,p);
 for(long i=0;i<n;i++){nmod_poly_set_coeff_ui(&S,i,ss[i]);nmod_poly_set_coeff_ui(&G,i,gg[i]);}
 nmod_poly_inv_series(&inv,&S,n);
 nmod_poly_shift_left(&w,&inv,1);nmod_poly_truncate(&w,n);
 nmod_poly_revert_series(&q,&w,n);
 nmod_poly_compose_series(&R,&G,&q,n);
 for(long i=0;i<n;i++)out[i]=i<R.length?R.coeffs[i]:0;
 nmod_poly_clear(&S);nmod_poly_clear(&G);nmod_poly_clear(&inv);
 nmod_poly_clear(&w);nmod_poly_clear(&q);nmod_poly_clear(&R);
}
