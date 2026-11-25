from itertools import product
# Two natural profiles n=0,1; two contexts a=0,1 (evaluative attitudes).
# Each map is a toy interpretation of value V and reason R, not a metaethical theory.
def run():
 maps=list(product([0,1],repeat=4)); rows=[]
 def superv(f): return f[0]==f[1] and f[2]==f[3]
 def identity(f): return f==(0,0,1,1)
 def nontriv(f): return len(set(f))==2
 def bridge(v,r): return all(not x or y for x,y in zip(v,r))
 tests=[('M-T1','Супервентность V не влечёт тождество V=N',lambda v,r:superv(v),lambda v,r:identity(v)),('M-T2','Нетривиальная супервентность V не влечёт именно V=N',lambda v,r:superv(v) and nontriv(v),lambda v,r:identity(v)),('M-T3','Тождество V=N влечёт супервентность V',lambda v,r:identity(v),lambda v,r:superv(v)),('M-T4','Тождество V=N не влечёт мост V→R',lambda v,r:identity(v),lambda v,r:bridge(v,r)),('M-T5','Супервентность V и R не влечёт мост V→R',lambda v,r:superv(v) and superv(r),lambda v,r:bridge(v,r)),('M-T6','Тождество V=N и мост V→R влекут N→R',lambda v,r:identity(v) and bridge(v,r),lambda v,r:bridge((0,0,1,1),r))]
 for i,t,p,c in tests:
  eligible=[(v,r) for v in maps for r in maps if p(v,r)]; bad=[(v,r) for v,r in eligible if not c(v,r)]
  rows.append(dict(id=i,title=t,models=len(maps)**2,premise_models=len(eligible),countermodels=len(bad),valid=not bad,first_countermodel=dict(V=bad[0][0],R=bad[0][1]) if bad else None))
 return rows
if __name__=='__main__':
 import json
 print(json.dumps(run(),ensure_ascii=False,indent=2))
