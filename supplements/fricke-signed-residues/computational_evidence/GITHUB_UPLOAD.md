# Uploading this supplement with the paper

Suggested repository layout:

```text
README.md
Fricke_Signed_Residues_Journal_v1_3.tex
Fricke_Signed_Residues_Journal_v1_3.pdf
computational_evidence/
  README.md
  CLAIMS_AND_FILES.md
  REPRODUCTION.md
  PROVENANCE.json
  SHA256SUMS.txt
  requirements.txt
  scripts/
  verification/
  packages/
```

1. Unzip the supplied release and copy the **contents** of
   `Fricke_Computational_Evidence_v1_0/` into `computational_evidence/`.
2. Keep both original package directories and their filenames. The paper names
   those packages in its Data and software paragraph.
3. Include the supplement's `.gitattributes` and `.gitignore`; they preserve
   checksum bytes and exclude future local reproduction/environment outputs.
4. From `computational_evidence/`, run `python scripts/verify_evidence.py`.
5. Link the root repository README to `computational_evidence/README.md` and
   state which manuscript version accompanies the data.
6. Upload the paper's TeX and PDF separately. A ZIP release asset is optional;
   keep the expanded code and data browsable in the repository too.

The evidence ZIP does not contain the interactive app, its hosting state,
credentials, Python dependencies, or third-party journal PDFs. No GitHub upload
has been performed by the preparation of this supplement. Existing repository
licensing is not changed.

Historical `note/`, `AUDIT_REPORT.*` and `replacement_section/` files are labelled
in the supplement README as superseded background. They should not be presented
as the current manuscript. No edits to the current paper are needed to make its
two named evidence packages available through this directory layout.
