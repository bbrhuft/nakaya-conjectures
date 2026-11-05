import cypari2, sys
pari = cypari2.Pari(); pari.allocatemem(10**9)
pari('ssroots(H,p)=my(t=ffgen(ffinit(p,2),\'t),F=factor(H*t^0)[,1]); vector(#F,i,-polcoef(F[i],0)/polcoef(F[i],1))')
p=int(sys.argv[1]); h=(p-1)//2
pari(f"H=sum(i=0,{h},binomial({h},i)^2*'x^i)")
R=pari(f"R=ssroots(H,{p})")
print(len(R))
for i in range(len(R)):
    print(pari(f"[R[{i+1}], subst(deriv(H),'x,R[{i+1}])]"))
