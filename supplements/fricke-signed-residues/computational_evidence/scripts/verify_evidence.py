#!/usr/bin/env python3
"""Verify release hashes and recompute inventory totals from archived JSON (stdlib only)."""
import argparse
import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SIGNED=ROOT/'packages/Signed_Weighted_Residue_v1_0'
ETA=ROOT/'packages/Eta_Frobenius_Lemma_Audit_v1_0'
LEVELS=[2,3,5,7,13]

def primes(n):
    return [p for p in range(2,n+1) if all(p%d for d in range(2,int(p**.5)+1))]
def chi(a,p):return 1 if pow(a%p,(p-1)//2,p)==1 else -1
def load(p):return json.loads(p.read_text(encoding='utf8'))
def require(condition,message):
    if not condition:raise ValueError(message)

def check_manifest(root,filename,skip_self=False):
    checked=0;skipped=[]
    for line in (root/filename).read_text().splitlines():
        if not line.strip():continue
        h,rel=line.split(maxsplit=1);rel=rel.lstrip('*')
        if rel.startswith('./'):rel=rel[2:]
        if skip_self and rel==filename:skipped.append(rel);continue
        p=root/rel
        require(p.resolve().is_relative_to(root.resolve()),'Manifest path escapes package')
        require(p.is_file(),f'Missing manifest entry: {p.relative_to(ROOT)}')
        require(hashlib.sha256(p.read_bytes()).hexdigest()==h,f'Hash mismatch: {p.relative_to(ROOT)}')
        checked+=1
    return {'verified_files':checked,'excluded_self_entries':skipped}

def verify(skip_release=False):
    report={'scope':'Integrity and recorded-result validation; this does not rerun the mathematical algorithms.'}
    if not skip_release:report['release_manifest']=check_manifest(ROOT,'SHA256SUMS.txt')
    report['original_manifests']={
        'signed':check_manifest(SIGNED,'SHA256SUMS.txt'),
        'eta':check_manifest(ETA,'SHA256SUMS.txt',skip_self=True),
        'eta_self_entry_note':'The inherited eta manifest includes an invalid hash of itself. Its original bytes are preserved; the new release manifest independently hashes that file.'}
    rows=[]
    for tier,lo,hi,expected_count in [('certified',5,211,222),('kz',223,1499,960)]:
        recs=[load(p) for p in sorted((SIGNED/'results'/tier).glob('*.json'))]
        require(len(recs)==expected_count,f'{tier} record count')
        expected={(N,p) for N in LEVELS for p in primes(hi) if p>=lo and p!=N}
        require({(r['N'],r['p']) for r in recs}==expected,f'{tier} prime/level coverage')
        for r in recs:
            require(r['matches_conjecture'] is True,f'{tier} signed formula failed')
            require(r['n_thin']==len(r['thin']),f'{tier} thin count')
            require(r['n_thin_nonrational']==sum(not t['rational'] for t in r['thin']),f'{tier} non-rational count')
            require(r['expected_constant']==-chi(-r['N'],r['p']),f'{tier} sign')
            require(r['ratio_set_signed']==([r['expected_constant']] if r['n_thin'] else []),f'{tier} ratio set')
            if tier=='certified':
                require(r['certificate_ok'] is True,'Certificate flag')
                require(len(r['D_thin'])-1==r['n_thin'],'Reduced denominator degree')
                if r['p']<=37:require(r['pade_den_equals_D_thin'] is True,'Candidate-free denominator flag')
                if r['n_thin']:require(r['gcd_P_D_is_1'] is True and r['deg_P_lt_deg_D'] is True,'Reduced fraction flags')
        table=[]
        for N in LEVELS:
            a=[r for r in recs if r['N']==N]
            row={'tier':tier,'N':N,'pairs':len(a),'thin_values':sum(r['n_thin'] for r in a),'nonrational_thin_values':sum(r['n_thin_nonrational'] for r in a),'p_min':min(r['p'] for r in a),'p_max':max(r['p'] for r in a)}
            table.append(row);rows.append(row)
        report[tier]={'pairs':len(recs),'thin_values':sum(r['n_thin'] for r in recs),'nonrational_thin_values':sum(r['n_thin_nonrational'] for r in recs),'empty_pole_pairs':[(r['N'],r['p']) for r in recs if not r['n_thin']],'by_level':table}
    require(report['certified']['thin_values']==6246 and report['certified']['nonrational_thin_values']==4696,'Paper table totals')
    require(report['kz']['thin_values']==233336 and report['kz']['nonrational_thin_values']==210326,'KZ totals')
    stored=load(SIGNED/'results/summary.json')
    require(stored['failed_checks']==[] and stored['counterexamples']==[],'Archived summary failures')
    for name,key in [('certified','certified_all'),('kz','kz_all')]:
        for a,b in [('pairs','pairs'),('thin_values','thin_points'),('nonrational_thin_values','nonrational_thin_points')]:require(report[name][a]==stored[key][b],f'Archive summary {key}/{b}')
    hecke=load(SIGNED/'results/hecke_polynomial_checks.json')
    require({(r['N'],r['p']) for r in hecke}=={(N,p) for N in LEVELS for p in primes(31) if p>=5 and p!=N},'Hecke coverage')
    for r in hecke:
        require(all(v for k,v in r.items() if isinstance(v,bool)),'Hecke flags')
    report['hecke']={'pairs':len(hecke),'p_max':31,'all_recorded_checks_pass':True}
    c=load(SIGNED/'results/level1_c_closed_form.json')
    require({r['p'] for r in c}=={p for p in primes(997) if p>=5},'Factorial conjecture coverage')
    for r in c:
        p=r['p'];f=1
        for j in range(1,(p-1)//2+1):f=f*j%p
        require(r['match'] and r['c_p']==r['pred']==chi(6,p)*f%p,'Recorded factorial conjecture value')
    report['factorial_conjecture']={'primes':len(c),'p_max':max(r['p'] for r in c),'all_recorded_matches':True,'status':'Computational evidence only; the journal draft leaves this formula conjectural.'}
    v=load(ETA/'results/velu_sign_checks.json');vs=v['summary'];vp=v['pairs']
    expected={(ell,p) for ell in primes(47) for p in primes(199) if p>=5 and p!=ell}
    require({(r['ell'],r['p']) for r in vp}==expected and len(vp)==647,'Velu coverage')
    for r in vp:
        require(r['n_points']==(r['ell']+1)*r['n_ss_j'],'Velu kernel enumeration count')
        require(r['theorem_C_ok'] and r['values_D_ell_pow_k']==[str(chi(r['ell'],r['p'])%r['p'])],'Velu sign')
        for k in ['ono_m_power_all_1','robert_B_relation_ok','baker_ok','c_constant_ok','hasse_zero_ok','velu_j_supersingular_ok','c_constant_over_all_ss']:require(r[k] is True,f'Velu {k}')
    total=sum(r['n_points'] for r in vp)
    require(total==127541==vs['n_points'],'Velu total')
    report['velu']={'pairs':len(vp),'kernel_checks':total,'ell_max':47,'p_max':199,'counting_convention':'Cyclic kernels on chosen representatives, not distinct coarse points.'}
    eta=load(ETA/'results/eta_multiplier_audit.json')
    for r in eta['G_character']:require(r['nu_G']==r['kronecker_ell_d']==r['chi_disc_d'],'G multiplier character')
    for r in eta['y_lemma']:require(r['nu_y']==r['kronecker_ell_d'],'y multiplier character')
    for r in eta['petersson_vs_dedekind']:require(Fraction(r['diff'])==Fraction(1,8),'Eta square-root convention offset')
    report['eta_multiplier_audit']={k:len(v) for k,v in eta.items()}
    report['status']='PASS'
    return report,rows

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--skip-release-manifest',action='store_true',help='For assembling a release before its top-level manifest is written.')
    ap.add_argument('--report',type=Path,help='Write a JSON report outside the baseline evidence directories.')
    args=ap.parse_args()
    report,rows=verify(args.skip_release_manifest)
    if args.report:args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
