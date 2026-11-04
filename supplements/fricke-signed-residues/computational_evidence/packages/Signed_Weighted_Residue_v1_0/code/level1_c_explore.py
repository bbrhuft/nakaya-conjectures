"""Level-one invariant c(E) = E_{p+1}^{(p-1)/2} / Delta^{(p^2-1)/24} on the supersingular locus.
Checks Baker (c^2 = -(-1/p)) and constancy of c; records c_p for p = 3 mod 4 (then c_p = +-1)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wr_core import Field, primes_upto, legendre, ss_j_deuring
from wr_pairs import level1_data, baker_c
pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 600
out = []
for p in primes_upto(pmax):
    if p < 5: continue
    Fd = Field(p)
    jD, _ = ss_j_deuring(Fd)
    Ep1, Em1, ok = level1_data(p)
    cs = set(); bok = True
    for j in jD.values():
        A, B, beta, c = baker_c(Fd, j, Ep1, Em1)
        bok &= (beta == Fd.el(-legendre(-1, p))) and A == Fd.F(0)
        cs.add(Fd.key(c))
    const = len(cs) == 1
    c = Fd.F(list(cs)[0][0]) if const else None
    rec = {"p": p, "baker_ok": bok, "c_constant": const, "n_ss_j": len(jD)}
    if const and p % 4 == 3:
        rec["c_p"] = 1 if c == Fd.el(1) else -1
    out.append(rec)
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
json.dump(out, open(os.path.join(base, "level1_c_checks.json"), "w"), indent=0)
print("all Baker ok:", all(r["baker_ok"] for r in out), " all c constant:", all(r["c_constant"] for r in out), " primes:", len(out), " pmax:", out[-1]["p"])
print("p=3 mod 4 c_p:", [(r["p"], r["c_p"]) for r in out if "c_p" in r][:40])
