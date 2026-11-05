#!/usr/bin/env python3
"""Coarse separate-process RSS probe: one complete route after imports."""
import resource,time,sys,json
import benchmark as b
N,p=int(sys.argv[1]),int(sys.argv[2]);route=sys.argv[3];b.CURRENT_N=N
def rss():
 for line in open('/proc/self/status'):
  if line.startswith('VmRSS:'):return int(line.split()[1])
start=rss();peak0=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;t=time.perf_counter()
if route=='ss':
 fd,tv,_=b.acquire(N,p);ans=b.reconstruct(fd,tv)
elif route=='q':ans=b.q_free(N,p)
else:raise ValueError(route)
print(json.dumps({'N':N,'p':p,'route':route,'elapsed_s':time.perf_counter()-t,'initial_rss_KiB':start,'final_rss_KiB':rss(),'initial_peak_KiB':peak0,'final_peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'degree_D':ans[1].degree(),'note':'One fresh-process call; OS RSS includes Python/FLINT and allocator overhead. Import/compilation excluded.'}))
