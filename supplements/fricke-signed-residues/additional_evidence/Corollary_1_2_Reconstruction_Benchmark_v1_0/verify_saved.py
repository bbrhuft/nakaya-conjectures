#!/usr/bin/env python3
"""Replay exact supersingular data, compare q-only reconstruction, and compare
overlapping outputs to the original independent p^3 certificate archive.
"""
import json,pathlib,zipfile,hashlib,sys
import benchmark as b
from flint import nmod_poly,fmpz_mod_poly_ctx,fq_default_ctx,fq_default_poly_ctx
data=json.loads((b.ROOT/'results.json').read_text());out=[]
archive=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else b.ROOT.parent/'handoff/Fricke_Paper_Conversation_Handoff_v1_0/evidence/Signed_Weighted_Residue_v1_0.zip'
z=zipfile.ZipFile(archive) if archive.exists() else None
for rec in data['results']:
 N,p=rec['N'],rec['p'];b.CURRENT_N=N
 fd=b.Field(p);fd.F=fq_default_ctx(modulus=fmpz_mod_poly_ctx(p)(rec['Fp2_modulus']));fd.P=fq_default_poly_ctx(fd.F)
 tv=[{'t':fd.F(x['t']),'e':x['e']} for x in rec['ss_data']]
 stored=nmod_poly(rec['P'],p),nmod_poly(rec['D'],p)
 replay=b.reconstruct(fd,tv);q=b.q_free(N,p)
 assert stored==replay==q
 row={'N':N,'p':p,'replay_and_q_free':'PASS'}
 name=f'Signed_Weighted_Residue_v1_0/results/certified/N{N:02d}_p{p:04d}.json'
 if z is not None and name in z.namelist():
  old=json.loads(z.read(name));oldrat=nmod_poly(old['R_numerator'],p),nmod_poly(old['D_thin'],p)
  assert old['certificate_ok'] and stored==oldrat
  row.update(historical_certificate='PASS',historical_entry=name,historical_entry_sha256=hashlib.sha256(z.read(name)).hexdigest())
 out.append(row);print(N,p,'PASS',row.get('historical_certificate',''),flush=True)
(b.ROOT/'verification.json').write_text(json.dumps({'records':out,'all_ok':True,'historical_matches':sum('historical_certificate' in r for r in out),'archive_available':z is not None},indent=2))
print('PASS',len(out),'saved rational functions;',sum('historical_certificate' in r for r in out),'historical p^3 certificate matches')
