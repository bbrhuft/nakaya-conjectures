\\ modp_lib.gp -- exact mod-p level-one modular form utilities (PARI/GP >= 2.15)
\\ Conventions: X = E4, Y = E6, Delta = (X^3 - Y^2)/1728, E_k = 1 - (2k/B_k) sum sigma_{k-1}(n) q^n.

eis(k,L) = my(c = -2*k/bernfrac(k)); 1 + c*sum(n=1, L, sigma(n,k-1)*q^n) + O(q^(L+1));

\\ Weight-k level-one form with q-expansion eis(k) reduced mod p, as a polynomial in X,Y over Z (coeffs in [0,p)).
{epoly(k, p) = my(L = k\4 + 12, E4 = eis(4,L), E6 = eis(6,L), T = eis(k,L), B = List(), V, M, s, chk);
  for(a = 0, k\4, if((k - 4*a) % 6 == 0, listput(B, [a, (k - 4*a)/6])));
  V = vector(#B, i, E4^B[i][1] * E6^B[i][2]);
  M = matrix(#B, #B, i, j, polcoef(V[j], i-1, q));
  s = matsolvemod(M, p, vector(#B, i, lift(Mod(polcoef(T, i-1, q), p)))~);
  if(type(s) != "t_COL", error("epoly: no solution"));
  chk = sum(i = 1, #B, s[i]*V[i]) - T;
  for(n = 0, L, if(Mod(polcoef(chk, n, q), p) != 0, error("epoly: q-expansion mismatch at n=", n)));
  sum(i = 1, #B, (s[i] % p) * 'X^B[i][1] * 'Y^B[i][2]);}

\\ Decompose weight w = 12n + 4d + 6e with d in {0,1,2}, e in {0,1}: returns [n,d,e]
wdec(w) = my(e = (w % 4 != 0), d, r); r = w - 6*e; d = (r/4) % 3; [(w - 4*d - 6*e)/12, d, e];

\\ Isobaric P(X,Y) of weight w  ->  polynomial s(j) with P = X^d Y^e Delta^n s(j)  (mod p).
\\ Writing P = X^d Y^e Q(X^3, Y^2) with Q homogeneous of degree n gives s(j) = Q(j, j-1728).
{jpart(P, w, p) = my(t = wdec(w), n = t[1], d = t[2], e = t[3], P1, cf = vector(n+1), a, al, acc, pw);
  P1 = subst(P, 'X, 1);
  for(b = 0, poldegree(P1, 'Y), my(c = polcoef(P1, b, 'Y)); if(c == 0, next);
    a = w - 6*b; if(a % 4, error("jpart: not isobaric")); a /= 4;
    if((a - d) % 3 || (b - e) % 2 || a < d || b < e, error("jpart: bad monomial"));
    al = (a - d)/3; cf[al+1] += c);
  acc = Mod(cf[n+1], p); pw = Mod(1,p);
  forstep(al = n-1, 0, -1, pw *= ('j - 1728); acc = acc*'j + cf[al+1]*pw);
  acc;}

\\ supersingular polynomial ss_p(j) = j^d (j-1728)^e s(j), where A = E_{p-1} = X^d Y^e Delta^n s(j)
sspoly(A, p) = my(t = wdec(p-1)); 'j^t[2] * ('j-1728)^t[3] * jpart(A, p-1, p);

\\ roots in F_{p^2} of a squarefree polynomial over F_p
{rootsFq(P, p) = my(t = ffgen(ffinit(p,2), 't), F = factor(subst(lift(P),'j,'x) * t^0)[,1]);
  vector(#F, i, if(poldegree(F[i]) != 1, error("rootsFq: not split")); -polcoef(F[i],0)/polcoef(F[i],1));}

\\ Serre derivative on F_p[X,Y]: dX = -Y/3, dY = -X^2/2
sder(f, p) = Mod(-1/3,p)*'Y*deriv(f,'X) + Mod(-1/2,p)*'X^2*deriv(f,'Y);

\\ Exact test of divisibility A | P in F_p[X,Y] for isobaric P of weight w, where A = E_{p-1} mod p.
\\ Uses that A is squarefree with irreducible factors X (iff d_A=1), Y (iff e_A=1) and the factors of
\\ s_A(j) homogenized; hence A | P  <=>  (d_A=0 or P(0,Y)=0) and (e_A=0 or P(X,0)=0) and s_A | s_P.
{divA(P, w, A, p) = my(tA = wdec(p-1), sA = jpart(A, p-1, p), sP, ok = 1);
  P = P*Mod(1,p);
  if(P == 0, return(1));
  if(tA[2] == 1 && subst(P,'X,0) != 0, ok = 0);
  if(tA[3] == 1 && subst(P,'Y,0) != 0, ok = 0);
  sP = jpart(lift(P), w, p);
  if(sP % sA != 0, ok = 0);
  ok;}
