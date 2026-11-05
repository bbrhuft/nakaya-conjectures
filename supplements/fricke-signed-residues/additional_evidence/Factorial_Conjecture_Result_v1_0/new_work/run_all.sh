#!/usr/bin/env bash
# Reproduce every computation in new_work/ (run from the new_work/ directory).
# Requirements: see requirements.txt (Python >= 3.11, cypari2 with PARI/GP >= 2.15, mpmath; pdflatex for the note).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p results
# 1. Main independent verification, p <= 997: routes I-IV (about 3 min on 1 core)
python3 -I code/verify_factorial.py 997 --models 3 --out results/verify_factorial_p5_997.json | tee results/verify_factorial_p5_997.log
# 2. Negative control: the wrong sign -(6/p)h! must fail at every prime (about 2 min)
python3 -I code/verify_factorial.py 997 --negate --models 1 --no-legendre --out results/negative_control_p5_997.json > results/negative_control_p5_997.log
tail -1 results/negative_control_p5_997.log
# 3. Corollaries: B = 3c_{p-2} and A = c_{p-1} in F_p[a,b] (p <= 200), signed KZ(40) and Legendre form (p <= 997)
python3 -I code/corollary_check.py 997 200 | tee results/corollary_check.log | tail -1
# 4. Proof mechanism at level one (p = 23 mod 24): theta^h F identity, leading term, divisibility (p=167 takes ~5 min)
python3 -I code/mechanism_check.py 170 | tee results/mechanism_check_p23mod24_le167.log
# 5. eta^2 has trivial character on Gamma(12) (numerical, 60 digits)
python3 -I code/eta2_gamma12_check.py | tee results/eta2_gamma12_check.log | tail -1
# 6. Inherited scripts, run on a copy (they overwrite ../results inside the copy only)
( cd reproduction && python3 code/level1_c_formula.py 997 ) | tee reproduction_level1_c_formula_997.log
( cd reproduction && python3 code/independent_check/level1_check.py 73 ) | tee reproduction_level1_check_73.log | tail -1
# 7. Note
( cd note && pdflatex -interaction=nonstopmode factorial_constant_proof.tex >/dev/null && pdflatex -interaction=nonstopmode factorial_constant_proof.tex >/dev/null && echo "note built" )
