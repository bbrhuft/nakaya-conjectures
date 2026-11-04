"""Test the observed closed form  c_p = (6/p) * ((p-1)/2)!  (mod p)  for the constant value of
c(E) = E_{p+1}^{(p-1)/2}/Delta^{(p^2-1)/24} on the supersingular locus.  Exploratory only."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wr_core import Field, primes_upto, legendre, ss_j_deuring
from wr_pairs import level1_data, baker_c
pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 600
res = []
for p in primes_upto(pmax):
    if p < 5: continue
    Fd = Field(p)
    jD, _ = ss_j_deuring(Fd)
    Ep1, Em1, ok = level1_data(p)
    cs = set()
    for j in jD.values():
        cs.add(Fd.key(baker_c(Fd, j, Ep1, Em1)[3]))
    assert len(cs) == 1
    k = list(cs)[0]
    assert all(x == 0 for x in k[1:])
    c = k[0] % p
    h = (p - 1) // 2
    f = 1
    for i in range(1, h + 1): f = f * i % p
    pred = legendre(6, p) * f % p
    res.append({"p": p, "c_p": c, "pred": pred, "match": c == pred})
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
json.dump(res, open(os.path.join(base, "level1_c_closed_form.json"), "w"), indent=0)
bad = [r["p"] for r in res if not r["match"]]
print("primes tested:", len(res), "pmax:", res[-1]["p"], "mismatches:", bad[:20])
