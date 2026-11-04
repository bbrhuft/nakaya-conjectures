#!/usr/bin/env python3
"""Run supplied computations in fresh copies without overwriting archived evidence."""
import argparse
import datetime
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SIGNED = 'Signed_Weighted_Residue_v1_0'
ETA = 'Eta_Frobenius_Lemma_Audit_v1_0'
ELLS = '2,3,5,7,11,13,17,19,23,29,31,37,41,43,47'

def run(suite, out):
    for name,version in [('python-flint','0.9.0'),('mpmath','1.3.0')]:
        actual=importlib.metadata.version(name)
        if actual!=version:
            raise SystemExit(f'{name}=={version} required by this wrapper; found {actual}. Install requirements.txt.')
    out.mkdir(parents=True,exist_ok=False)
    for pkg in (SIGNED,ETA):
        shutil.copytree(ROOT/'packages'/pkg/'code',out/pkg/'code',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        (out/pkg/'results').mkdir()
    signed=out/SIGNED/'code'; eta=out/ETA/'code'
    jobs=[]
    def add(label,folder,*args):jobs.append((label,folder,[sys.executable,*args]))
    if suite=='smoke':
        add('normalization',signed,'verify_normalization.py','300')
        add('certified-small',signed,'run_all.py','--cert-max','29','--pade-max','29')
        add('hecke-small',signed,'hecke_check.py','11')
        add('velu-small',eta,'velu_sign_check.py','31','2,3,5,7,11,13')
        add('level1-small',signed,'level1_c_explore.py','100')
        add('factorial-small',signed,'level1_c_formula.py','100')
    if suite in ('certified','all'):
        add('normalization',signed,'verify_normalization.py','300')
        add('certified-full',signed,'run_all.py','--cert-max','211','--pade-max','37')
    if suite in ('kz','all'):
        add('kz-full',signed,'run_all.py','--cert-min','100000','--cert-max','211','--kz-max','1500','--hasse-power-max','0')
    if suite in ('hecke','all'):add('hecke-full',signed,'hecke_check.py','31')
    if suite in ('eta-multiplier','all'):
        add('eta-multiplier-original',signed,'eta_multiplier_check.py')
        add('eta-multiplier-audit',eta,'eta_multiplier_audit.py')
    if suite in ('velu','all'):add('velu-full',eta,'velu_sign_check.py','199',ELLS)
    if suite in ('level1','all'):
        add('level1-full',signed,'level1_c_explore.py','1000')
        add('factorial-full',signed,'level1_c_formula.py','1000')
    metadata={'suite':suite,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'python':sys.version,'platform':platform.platform(),
              'dependencies':{n:importlib.metadata.version(n) for n in ['python-flint','mpmath']},'runs':[]}
    env=dict(os.environ,PYTHONHASHSEED='0',PYTHONDONTWRITEBYTECODE='1')
    for label,folder,cmd in jobs:
        log=out/(label+'.log'); start=time.monotonic()
        print(f'Running {label}; output: {log}',flush=True)
        with log.open('w',encoding='utf8') as f:
            completed=subprocess.run(cmd,cwd=folder,env=env,stdout=f,stderr=subprocess.STDOUT)
        metadata['runs'].append({'label':label,'command':[Path(cmd[0]).name,*cmd[1:]],'working_directory':str(folder.relative_to(out)),
                                'log':log.name,'exit_code':completed.returncode,'elapsed_seconds':round(time.monotonic()-start,3)})
        (out/'RUN_METADATA.json').write_text(json.dumps(metadata,indent=2)+'\n')
        if completed.returncode:raise SystemExit(f'{label} failed; see {log}')
    comparisons=compare(out)
    metadata['comparisons']=comparisons
    metadata['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (out/'RUN_METADATA.json').write_text(json.dumps(metadata,indent=2)+'\n')
    if comparisons['mismatches']:raise SystemExit('Recorded-output comparison failed; see RUN_METADATA.json.')
    print(json.dumps(comparisons,indent=2),flush=True)
    print('Completed. Archived package results were not modified.',flush=True)

def compare(out):
    mismatches=[];counts={}
    signed=out/SIGNED/'results'; original=ROOT/'packages'/SIGNED/'results'
    fields=['N','p','n_ss_T_values','n_thin','n_thin_nonrational','expected_constant','R_numerator','D_thin','certificate_ok','matches_conjecture']
    for tier in ('certified','kz'):
        n=0
        for f in sorted((signed/tier).glob('*.json')):
            current=json.loads(f.read_text()); expected=json.loads((original/tier/f.name).read_text());n+=1
            for k in fields:
                if k in expected and current.get(k)!=expected[k]:mismatches.append(f'{tier}/{f.name}: {k}')
        if n:counts[tier+'_pairs']=n
    for filename,keys in [
        ('hecke_polynomial_checks.json',['N','p','kronecker_mod_p','H_symmetric','residue_equals_minus_H_all_Fp2','hecke_form_of_conjecture']),
        ('normalization_checks.json',None),
        ('level1_c_checks.json',['p','baker_ok','c_constant','n_ss_j','c_p']),
        ('level1_c_closed_form.json',['p','c_p','pred','match'])]:
        if not (signed/filename).exists():continue
        a=json.loads((signed/filename).read_text());b=json.loads((original/filename).read_text())
        if keys is None:
            if a!=b:mismatches.append(filename)
            counts['normalization_levels']=len(a['levels'])
        else:
            index={(r.get('N'),r['p']):r for r in b}
            for r in a:
                e=index[(r.get('N'),r['p'])]
                for k in keys:
                    if r.get(k)!=e.get(k):mismatches.append(f'{filename} N={r.get("N")} p={r["p"]}: {k}')
            counts[filename.removesuffix('.json')+'_records']=len(a)
    vf=out/ETA/'results/velu_sign_checks.json'
    if vf.exists():
        d=json.loads(vf.read_text());e=json.loads((ROOT/'packages'/ETA/'results/velu_sign_checks.json').read_text())
        index={(r['ell'],r['p']):r for r in e['pairs']}
        for r in d['pairs']:
            expected=index[(r['ell'],r['p'])]
            for k in ['n_ss_j','n_points','theorem_C_ok','legendre_ell_p','values_D_ell_pow_k','ono_m_power_all_1','robert_B_relation_ok','baker_ok','c_constant_ok']:
                if r[k]!=expected[k]:mismatches.append(f'Velu ell={r["ell"]} p={r["p"]}: {k}')
        counts['velu_pairs']=len(d['pairs']);counts['velu_kernel_checks']=sum(r['n_points'] for r in d['pairs'])
    ef=out/ETA/'results/eta_multiplier_audit.json'
    if ef.exists():
        a=json.loads(ef.read_text());b=json.loads((ROOT/'packages'/ETA/'results/eta_multiplier_audit.json').read_text())
        for group in a:
            if len(a[group])!=len(b[group]):mismatches.append('eta audit category length: '+group)
        for r in a['G_character']:
            if not r['nu_G']==r['kronecker_ell_d']==r['chi_disc_d']:mismatches.append('eta audit G character')
        for r in a['y_lemma']:
            if r['nu_y']!=r['kronecker_ell_d']:mismatches.append('eta audit y character')
        if any(r['abs_error']>1e-35 for r in a['numeric_validation']):mismatches.append('eta audit numerical validation')
        counts['eta_audit_G_character_records']=len(a['G_character'])
    ef=signed/'eta_multiplier_checks.json'
    if ef.exists():
        a=json.loads(ef.read_text())
        for r in a['class_checks']:
            if r['nu']!=r['kronecker_N_delta']:mismatches.append('original eta multiplier character')
        if any(r['abs_error']>1e-30 for r in a['numeric_validation']):mismatches.append('original eta numerical validation')
        counts['eta_original_character_records']=len(a['class_checks'])
    return {'compared_record_totals':counts,'mismatches':mismatches,
            'comparison_note':'Timings, random choices and finite-field root enumeration order are not compared; invariant counts, fractions and indicated checks are compared.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('suite',choices=['smoke','certified','kz','hecke','eta-multiplier','velu','level1','all'])
    parser.add_argument('--out',type=Path,help='A new output directory; existing directories are refused.')
    args=parser.parse_args()
    stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    run(args.suite,(args.out or ROOT/'reproduced'/(stamp+'_'+args.suite)).resolve())
