"""
Driver.  Usage:
  python3 run_all.py --cert-max 211 --kz-max 1009 --pade-max 37 [--levels 2,3,5,7,13]
Writes one JSON per pair to results/certified/ and results/kz/, and a log line per pair.
  certified : R_{N,p} reconstructed from T|U_p and certified by the a priori bound
              den R | T^{p^2}-T (Kronecker congruence); residues read off from R.
  kz        : residues from the proven double-pole lemma r_i = [(T-t_i)^{-2}](theta T)^{p-1};
              cross-validated against 'certified' on the overlap.
"""
import argparse, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wr_core import primes_upto
from wr_pairs import compute_pair

ap = argparse.ArgumentParser()
ap.add_argument("--cert-min", type=int, default=5)
ap.add_argument("--cert-max", type=int, default=101)
ap.add_argument("--kz-max", type=int, default=0)
ap.add_argument("--pade-max", type=int, default=31)
ap.add_argument("--hasse-power-max", type=int, default=211)
ap.add_argument("--levels", type=str, default="2,3,5,7,13")
args = ap.parse_args()
levels = [int(x) for x in args.levels.split(",")]
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
for sub in ("certified", "kz"):
    os.makedirs(os.path.join(base, sub), exist_ok=True)

def run(N, p, mode):
    kw = dict(mode=mode, pade=(mode == "certified" and p <= args.pade_max),
              hasse_power=(p <= args.hasse_power_max))
    r = compute_pair(N, p, **kw)
    fn = os.path.join(base, mode, f"N{N:02d}_p{p:04d}.json")
    with open(fn, "w") as f:
        json.dump(r, f)
    flags = [k for k, v in r.items() if isinstance(v, bool) and not v and k not in ("rational",)]
    print(f"{mode:9s} N={N:2d} p={p:4d} s={r['n_ss_T_values']:3d} thin={r['n_thin']:3d} "
          f"nonrat={r['n_thin_nonrational']:3d} ratios={r['ratio_set_signed']} "
          f"expected={r['expected_constant']:+d} match={r['matches_conjecture']} "
          f"false_flags={flags} t={r['seconds']}s", flush=True)
    return r

for p in primes_upto(args.cert_max):
    if p < args.cert_min:
        continue
    for N in levels:
        if p != N:
            run(N, p, "certified")
for p in primes_upto(args.kz_max):
    if p <= args.cert_max:
        continue
    for N in levels:
        if p != N:
            run(N, p, "kz")
print("DONE")
