from itertools import product
from fractions import Fraction as F
import json
def run():
    # Transparent content does not logically imply its truth.
    trans=[(t,k,v) for t,k,v in product((0,1),repeat=3)]
    # Proposed Metzinger conditions: necessity only, not sufficiency.
    cond=[m for m in product((0,1),repeat=5) if not m[4] or all(m[:4])]
    # Compare duplicate indicator with independent indicators; prior 1/2, sensitivity 4/5, false-positive rate 1/5.
    p=F(1,2); h=F(4,5); n=F(1,5)
    posterior=lambda a,b:p*a/(p*a+(1-p)*b)
    # In a branching toy model, A=B and A=C imply B=C.
    eq=[]
    for ab,ac,bc in product((0,1),repeat=3):
        valid=not ((ab and ac and not bc) or (ab and bc and not ac) or (ac and bc and not ab))
        eq.append(dict(ab=ab,ac=ac,bc=bc,consistent=valid))
    return dict(transparency=dict(models=len(trans),transparent_false=sum(t and not v for t,k,v in trans),example=[1,0,0]),conditions=dict(all_models=32,consistent=len(cond),all_conditions_without_suffering=sum(all(m[:4]) and not m[4] for m in cond)),evidence=dict(single=str(posterior(h,n)),duplicate=str(posterior(h,n)),independent=str(posterior(h*h,n*n))),identity=dict(models=len(eq),consistent=sum(x['consistent'] for x in eq),counterexamples=[x for x in eq if not x['consistent']]))
if __name__=='__main__': print(json.dumps(run(),ensure_ascii=False,indent=2))
