#!/usr/bin/env python3
"""Separate-process RSS probes; includes Python and allocator overhead.
These are observed process measurements, NOT algorithmic space bounds.
"""
import sys,json,resource,gc,ctypes as ct,time
import benchmark as b
def rss():
 for line in open('/proc/self/status'):
  if line.startswith('VmRSS:'):return int(line.split()[1])
mode=sys.argv[1];p=int(sys.argv[2]);gc.collect()
start=rss();peak0=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
t0=time.perf_counter()
if mode=='baseline':
 cs,r,s=b.coeffs(p);arr=(b.U*len(cs))(*cs);poly=b.C.poly_new(arr,len(cs),p)
elif mode=='factorial':
 cp=b.C.fast_fac((p-1)//2,p)
elif mode=='theorem_cached':
 # Same compiled function as the timing run; polynomial not used in mode 1.
 arr=(b.U*1)(1);poly=b.C.poly_new(arr,1,p)
 cp=b.C.fast_fac((p-1)//2,p)
 peak0=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;start=rss()
 for i in range(10000):b.C.evaluate(poly,2,3,p,0,0,cp,1)
 # Here these arbitrary coefficients measure arithmetic allocation only;
 # correctness/supersingularity is checked on the actual benchmark dataset.
else:raise ValueError(mode)
print(json.dumps({'mode':mode,'p':p,'elapsed_s':time.perf_counter()-t0,'initial_rss_KiB':start,'final_rss_KiB':rss(),'initial_peak_KiB':peak0,'final_peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'note':'Separate process; coarse OS RSS including runtime/allocator overhead. Cached-theorem memory probe excludes setup; elapsed time includes setup and loop.'}))
