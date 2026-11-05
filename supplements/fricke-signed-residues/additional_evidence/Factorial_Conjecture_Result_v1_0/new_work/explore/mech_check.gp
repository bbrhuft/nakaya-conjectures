\\ Level-one check of the proof mechanism when p = 23 mod 24, so F = eta^(p+1) = Delta^((p+1)/24)
read("lib.gp");
\\ Serre derivative on F_p[X,Y] (X=E4, Y=E6): dX=-Y/3, dY=-X^2/2
sd(f,p)=Mod(-1/3,p)*'Y*deriv(f,'X)+Mod(-1/2,p)*'X^2*deriv(f,'Y);
{mech(p)= my(h=(p-1)/2, m=(p+1)/2, A, B, D, F, G, w, chi12, rhs);
  A=epoly(p-1,p)*Mod(1,p); B=epoly(p+1,p)*Mod(1,p);
  D=('X^3-'Y^2)*Mod(1/1728,p); F=D^((p+1)/24);
  G=F; w=m;
  for(i=0,h-1, G=A*sd(G,p)+Mod(w/12,p)*B*G; w+=p+1);
  chi12=kronecker(12,p);
  rhs=kronecker(6,p)*(A^m*F-chi12*F^p);
  [p, G==rhs];}
for(i=1,4, p=[23,47,71,167][i]; print(mech(p)));
