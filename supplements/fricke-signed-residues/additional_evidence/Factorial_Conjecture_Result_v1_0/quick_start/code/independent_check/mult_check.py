import mpmath as mp, random
mp.mp.dps = 40
def eta(t):
    q = mp.exp(2j*mp.pi*t)
    return mp.exp(2j*mp.pi*t/24)*mp.qp(q)
def kron(a, n):
    # Kronecker symbol (a/n) for n odd positive or general via sympy
    from sympy import jacobi_symbol
    from sympy.ntheory import legendre_symbol
    s = 1
    if n < 0: n = -n  # a>0 so (a/-1)=1
    while n % 2 == 0:
        n //= 2
        s *= {1:1,7:1,3:-1,5:-1}[a % 8] if a % 2 else 0
    return s * jacobi_symbol(a, n)
random.seed(1)
bad = 0; tot = 0
for l in [11, 17, 19, 23]:
    for _ in range(8):
        while True:
            c = 24*l*random.randint(-3, 3); d = random.randint(-60, 60)
            from math import gcd
            if c and gcd(c, d) == 1:
                # need alpha d - beta c = 1 with 24|beta
                # solve alpha*d ≡ 1 mod 24c? choose beta=24*b: alpha d - 24 b c = 1
                g = gcd(d, 24*c)
                if g == 1:
                    alpha = pow(d, -1, 24*abs(c)); b = (alpha*d - 1)//(24*c)
                    beta = 24*b; break
        tau = mp.mpc(0.13, 0.9)/ (1) 
        # move tau so that gamma tau has decent imag part: use tau = -d/c + i/|c|
        tau = mp.mpc(-mp.mpf(d)/c + 0.01, 1.0/abs(c))
        gt = (alpha*tau + beta)/(c*tau + d)
        y = lambda t: eta(t)/eta(l*t)
        r = y(gt)/y(tau)
        pred = kron(l, d)
        tot += 1
        if abs(r - pred) > 1e-15: bad += 1; print("BAD", l, alpha, beta, c, d, r, pred)
print("checked", tot, "bad", bad)
