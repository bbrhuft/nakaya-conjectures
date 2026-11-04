"""
Fill the numerical placeholders and tables of note/Signed_Weighted_Residue_Note.tex from
results/summary.json and the generated table files, write the final .tex to
note/build/, and compile it with pdflatex (twice).
"""
import json, os, re, subprocess, shutil
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(here, "..")
res = os.path.join(root, "results")
src = open(os.path.join(root, "note", "template", "Signed_Weighted_Residue_Note.template.tex")).read()
S = json.load(open(os.path.join(res, "summary.json")))
c, z = S["certified_all"], S["kz_all"]
rep = {
    "@@NCERTPAIRS@@": str(c["pairs"]), "@@PCERT@@": str(c["pmax"]),
    "@@NCERTTHIN@@": f"{c['thin_points']:,}".replace(",", "{,}"),
    "@@NCERTNONRAT@@": f"{c['nonrational_thin_points']:,}".replace(",", "{,}"),
    "@@NKZPAIRS@@": str(z["pairs"]), "@@PKZ@@": str(z["pmax"]), "@@PKZMIN@@": str(z["pmin"]),
    "@@NKZTHIN@@": f"{z['thin_points']:,}".replace(",", "{,}"),
    "@@NKZNONRAT@@": f"{z['nonrational_thin_points']:,}".replace(",", "{,}"),
}
for k, v in rep.items():
    src = src.replace(k, v)

def lt(fn, caption, label):
    lines = open(os.path.join(res, fn)).read().splitlines()
    i = lines.index(r"\endhead")
    head = lines[1:i]                      # toprule, header, midrule
    out = [lines[0], r"\caption{" + caption + r"}\label{" + label + r"}\\"] + head + [r"\endfirsthead"] \
          + head + [r"\endhead"] + lines[i + 1:]
    return "{\\small\n" + "\n".join(out) + "\n}\n"

tab_levels = open(os.path.join(res, "table_levels.tex")).read()
tab_levels = ("\\begin{table}[ht]\\centering\\small\n" + tab_levels +
              "\\caption{All runs by level. Tier~1 = certified reconstruction of $R_{N,p}$; Tier~2 = residues from the "
              "proven double-pole lemma. Every pair has a single ratio value, equal to $-\\left(\\frac{-N}{p}\\right)$.}"
              "\\label{tab:levels}\n\\end{table}\n")
src = src.replace("@@TABLE_LEVELS@@", tab_levels)
src = src.replace("@@TABLE_P29@@", lt("table_p_le_29.tex",
    "Reproduction range $p\\le29$ (certified). $\\#j_{ss}$: supersingular $j$; $\\#x$: supersingular points of "
    "$X_0(N)$; $s$: supersingular $T$-values; weights written $e^{\\text{count}}$; last two columns: observed ratio set and the predicted constant.",
    "tab:p29"))
src = src.replace("@@TABLE_NONTHIN@@", lt("table_nonthin_small.tex",
    "All non-thin supersingular values for $p\\le13$. Elements of $\\mathbb F_{p^2}\\setminus\\mathbb F_p$ are written in "
    "python-flint's basis $z$ (minimal polynomial recorded per prime in the JSON output).", "tab:nonthin"))
assert "@@" not in src, re.findall(r"@@\w+@@", src)
out = os.path.join(root, "note", "build")  # scratch build dir; final files copied to note/
os.makedirs(out, exist_ok=True)
fn = os.path.join(out, "Signed_Weighted_Residue_Note.tex")
open(fn, "w").write(src)
for _ in range(3):
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "Signed_Weighted_Residue_Note.tex"],
                       cwd=out, capture_output=True, text=True)
    if r.returncode:
        print(r.stdout[-3000:])
        raise SystemExit("pdflatex failed")
log = open(os.path.join(out, "Signed_Weighted_Residue_Note.log")).read()
warn = [l for l in log.splitlines() if "Warning" in l or "Overfull" in l or "undefined" in l]
for ext in (".tex", ".pdf"):
    shutil.copy(os.path.join(out, "Signed_Weighted_Residue_Note" + ext), os.path.join(root, "note"))
print("built:", os.path.join(root, "note", "Signed_Weighted_Residue_Note.pdf"))
print("warnings:", len(warn))
for w in warn[:30]:
    print("  ", w)
