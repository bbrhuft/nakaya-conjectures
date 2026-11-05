import mpmath as mp
from flint import fmpz_poly
import sys; sys.path.insert(0,'..')
from wr_core import euler_coeffs, inflate, series_inverse_Z
L = 60
th = [0]*L
R = 12
for x in range(-R,R+1):
    for y in range(-R,R+1):
        n = x*x+x*y+3*y*y
        if n < L: th[n]+=1
th = fmpz_poly(th)
E = fmpz_poly(euler_coeffs(L)); E11 = fmpz_poly(inflate(euler_coeffs(L),11,L))
eta2 = (E*E11).truncate(L).pow_trunc(2,L)   # (eta eta11)^2 / q
S = th.pow_trunc(2,L).mul_low(series_inverse_Z(eta2,L),L)  # q*T + 6q
T = [int(S[i]) for i in range(L)]
T[1] -= 6
print("q*T coefficients:", T[:12])
# numeric Fricke invariance
mp.mp.dps = 30
def theta(tau):
    q = mp.exp(2j*mp.pi*tau); s = 0
    for x in range(-25,26):
        for y in range(-25,26):
            s += q**(x*x+x*y+3*y*y)
    return s
def eta(tau): return mp.exp(2j*mp.pi*tau/24)*mp.qp(mp.exp(2j*mp.pi*tau))
def Tf(tau): return theta(tau)**2/(eta(tau)*eta(11*tau))**2 - 6
tau = mp.mpc(0.05, 0.31)
print(Tf(tau), Tf(-1/(11*tau)))
