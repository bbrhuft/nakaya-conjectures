import cypari2, sys
pari = cypari2.Pari(); pari.allocatemem(2*10**9)
pari('read("lib.gp")')
def run(p):
    h=(p-1)//2
    pari(f"p={p}; h={h}; EP=epoly(p+1,p); EM=epoly(p-1,p); L=ssroots(legH(p),p);")
    return pari(r'''vector(#L,i, my(l=L[i], f=('x)*('x-1)*('x-l), g, a4,a6, e4,e6, A,B,c2);
        g=subst(f,'x,'x+(1+l)/3); a4=polcoef(g,1); a6=polcoef(g,0);
        e4=12*(-4*a4)/2^4; e6=-216*(-4*a6)/2^6;
        A=subst(subst(EM,'X,e4),'Y,e6); B=subst(subst(EP,'X,e4),'Y,e6);
        c2=polcoef(('x^3+a4*'x+a6)^h,p-2); [A, B/c2])''')
for p in [int(a) for a in sys.argv[1:]]:
    print(p, run(p))
