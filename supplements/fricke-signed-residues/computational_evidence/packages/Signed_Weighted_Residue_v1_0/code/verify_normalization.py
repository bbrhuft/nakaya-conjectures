"""
Exact (over Z) verification of the normalizations in the brief:
  * T_N = u + a_N + b_N/u = q^{-1} + 0 + O(q);
  * j = P_N(u)/u^N  (the supplied j-maps);
  * Fricke: j(N tau) = P_N(b_N/u)/(b_N/u)^N, i.e. w_N(u) = b_N/u;
  * first coefficients of T_N (compare with the McKay-Thompson series 2A,3A,5A,7A,13A).
Writes results/normalization_checks.json.
"""
import json, sys, os
from flint import fmpz_poly
sys.path.insert(0, os.path.dirname(__file__))
from wr_core import LEVELS, jmap_numerator, euler_coeffs, inflate, qseries_S_Z, series_inverse_Z

L = int(sys.argv[1]) if len(sys.argv) > 1 else 300
out = {"precision_terms": L, "levels": {}}

# J = q*j = E4^3 / prod(1-q^n)^24
sig3 = [0] * L
for d in range(1, L):
    for m in range(d, L, d):
        sig3[m] += d ** 3
E4 = fmpz_poly([1] + [240 * sig3[n] for n in range(1, L)])
E = fmpz_poly(euler_coeffs(L))
J = (E4 ** 3).truncate(L).mul_low(series_inverse_Z(E.pow_trunc(24, L), L), L)
assert int(J[0]) == 1 and int(J[1]) == 744 and int(J[2]) == 196884

for N, (a, b) in LEVELS.items():
    res = {}
    S, U, V = qseries_S_Z(N, L)
    # T = q^{-1} * S ; constant term of T is S[1]
    res["T_first_coeffs"] = {"q^-1": int(S[0]), "q^0": int(S[1]),
                             **{f"q^{n}": int(S[n + 1]) for n in range(1, 6)}}
    assert int(S[0]) == 1 and int(S[1]) == 0
    # j-map:  J * U^N == sum_k c_k q^{N+1-k} U^k
    PN = jmap_numerator(N)
    lhs = J.mul_low(U.pow_trunc(N, L), L)
    rhs = fmpz_poly([0])
    Uk = fmpz_poly([1])
    for k in range(N + 2):
        c = int(PN[k]) if k <= PN.degree() else 0
        if c:
            rhs += (Uk * c).left_shift(N + 1 - k)
        Uk = Uk.mul_low(U, L)
    rhs = rhs.truncate(L)
    res["jmap_identity_holds"] = (lhs == rhs)
    # Fricke: P_N(b q V) == J(q^N) * b^N * V^N
    bqV = (V * b).left_shift(1).truncate(L)
    lhs2 = fmpz_poly([0])
    pw = fmpz_poly([1])
    for k in range(N + 2):
        c = int(PN[k]) if k <= PN.degree() else 0
        if c:
            lhs2 += pw * c
        pw = pw.mul_low(bqV, L)
    lhs2 = lhs2.truncate(L)
    JN = fmpz_poly(inflate([int(x) for x in J.coeffs()], N, L))
    rhs2 = JN.mul_low(V.pow_trunc(N, L), L) * (b ** N)
    rhs2 = rhs2.truncate(L)
    res["fricke_identity_holds"] = (lhs2 == rhs2)
    # b_N = N^{12/(N-1)}, a_N = 24/(N-1)
    res["a_N_formula"] = (a == 24 // (N - 1)) and (24 % (N - 1) == 0)
    res["b_N_formula"] = (b == N ** (12 // (N - 1)))
    out["levels"][str(N)] = res
    print(N, res)

os.makedirs(os.path.join(os.path.dirname(__file__), "..", "results"), exist_ok=True)
with open(os.path.join(os.path.dirname(__file__), "..", "results", "normalization_checks.json"), "w") as f:
    json.dump(out, f, indent=1)
assert all(v["jmap_identity_holds"] and v["fricke_identity_holds"] for v in out["levels"].values())
print("all normalization checks passed")
