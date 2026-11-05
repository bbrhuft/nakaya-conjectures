import sys,json,time
from pathlib import Path
import inherited_wr_core
sys.modules['wr_core']=inherited_wr_core
from inherited_wr_pairs import compute_pair
from inherited_wr_core import primes_upto
root=Path(__file__).resolve().parent.parent
out=[]
for N in [2,3,5,7,13]:
 for p in primes_upto(47):
  if p<5 or p==N:continue
  row=compute_pair(N,p,mode='certified',kz=True,hasse_power=True)
  out.append(row);print(N,p,row.get('certificate_ok'),flush=True)
  (root/'results/five_level_regression_p47.json').write_text(json.dumps(out,indent=1,default=str))
print('PASS',len(out),'pairs',flush=True)
