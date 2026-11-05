\\ Eisenstein series E_k q-expansion to O(q^(L+1))
eis(k,L)=my(c=-2*k/bernfrac(k)); 1+c*sum(n=1,L,sigma(n,k-1)*q^n)+O(q^(L+1));
\\ weight-k level-one form with given q-expansion T, mod p, as polynomial in X=E4, Y=E6
{epoly(k,p)=my(L=k\4+10,E4=eis(4,L),E6=eis(6,L),T=eis(k,L),B=List(),V,M,s);
  for(a=0,k\4,if((k-4*a)%6==0,listput(B,[a,(k-4*a)/6])));
  V=vector(#B,i,E4^B[i][1]*E6^B[i][2]);
  M=matrix(#B,#B,i,j,polcoef(V[j],i-1,q)); s=matsolvemod(M,p,vector(#B,i,lift(Mod(polcoef(T,i-1,q),p)))~);
  if(type(s)!="t_COL",error("nosol"));
  for(n=0,L, if(Mod(polcoef(sum(i=1,#B,s[i]*V[i])-T,n,q),p)!=0,error("bad",n)));
  sum(i=1,#B,(s[i]%p)*'X^B[i][1]*'Y^B[i][2]);}
ssroots(H,p)=my(t=ffgen(ffinit(p,2),'t),F=factor(H*t^0)[,1]); vector(#F,i,-polcoef(F[i],0)/polcoef(F[i],1));
legH(p)=my(h=(p-1)/2); sum(i=0,h,binomial(h,i)^2*'x^i);
