#!/usr/bin/env python3
"""Numerical cross-check (mpmath, 60 digits) of Lemma 2.1: eta(tau)^2 transforms with trivial
character on Gamma(12), i.e.  eta(g tau)^2 = (c tau + d) eta(tau)^2  for g in Gamma(12).
Random elements with c>0 and c<0 are tested at random points of the upper half-plane.
(The lemma itself is proved from the Petersson/Rademacher multiplier formula in the note.)"""
import random, math, mpmath as mp
mp.mp.dps = 60
def eta(t):
    q = mp.exp(2j * mp.pi * t)
    return mp.exp(2j * mp.pi * t / 24) * mp.qp(q)
def rand_gamma12(rng):
    while True:
        c = 12 * rng.choice([i for i in range(-6, 7) if i])
        d = 1 + 12 * rng.randint(-5, 5)
        if math.gcd(abs(c), abs(d)) != 1: continue
        # extended Euclid: a d - b c = 1
        g, x, y = egcd(d, -c)   # x*d + y*(-c) = 1  -> a = x, b = y
        if g != 1: continue
        a, b = x, y
        t = (-b * pow(d, -1, 12)) % 12
        a, b = a + t * c, b + t * d
        assert a * d - b * c == 1 and a % 12 == 1 and b % 12 == 0 and c % 12 == 0 and d % 12 == 1
        return a, b, c, d
def egcd(a, b):
    if b == 0: return (abs(a), 1 if a > 0 else -1, 0)
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y
rng = random.Random(12)
worst = 0
for trial in range(40):
    a, b, c, d = rand_gamma12(rng)
    y = rng.uniform(0.7, 1.3); x = rng.uniform(-0.3, 0.3)
    t = mp.mpf(-d) / c + mp.mpc(x, y) / abs(c)      # chosen so that Im(t), Im(g t) are both ~ 1/|c|
    gt = (a * t + b) / (c * t + d)
    r = eta(gt) ** 2 / ((c * t + d) * eta(t) ** 2)
    worst = max(worst, abs(r - 1))
    print((a, b, c, d), mp.nstr(r, 15))
print("max |ratio - 1| =", mp.nstr(worst, 5))
