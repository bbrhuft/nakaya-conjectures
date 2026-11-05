import cypari2, sys
pari = cypari2.Pari(); pari.allocatemem(2*10**9)
pari('ssroots(H,p)=my(t=ffgen(ffinit(p,2),\'t),F=factor(H*t^0)[,1]); vector(#F,i,-polcoef(F[i],0)/polcoef(F[i],1))')
pari('''legc(p)=my(h=(p-1)/2,k=(p^2-1)/24,H=sum(i=0,h,binomial(h,i)^2*'x^i),R=ssroots(H,p),dH=deriv(H),v);
 v=vector(#R,i,my(l=R[i]); kronecker(6,p)*2^(8*k)*(l*(1-l))^(h-2*k)*subst(dH,'x,l)^h);
 [Set(v), Mod(kronecker(6,p)*h!,p)]''')
for p in [int(a) for a in sys.argv[1:]]:
    print(p, pari(f"legc({p})"))
