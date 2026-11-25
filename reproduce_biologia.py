from itertools import product
from fractions import Fraction as F
import json
def run():
    counts={"positive":0,"zero":0,"negative":0}; examples={}; residual=0
    for w1,w2,z1,z2 in product(range(1,5),range(1,5),range(4),range(4)):
        w=F(w1+w2,2); z=F(z1+z2,2); new=F(w1*z1+w2*z2,w1+w2)
        cov=F(w1*z1+w2*z2,2)-w*z
        delta=new-z; residual+=delta!=cov/w
        k="positive" if delta>0 else "negative" if delta<0 else "zero";counts[k]+=1
        examples.setdefault(k,dict(w=[w1,w2],z=[z1,z2],delta=str(delta)))
    # Abstract bounded controller, not physiological parameters.
    control={"sufficient":0,"residual":0}
    for d,c in product(range(6),repeat=2):
        r=d-min(d,c);control["sufficient" if r==0 else "residual"]+=1
    # Logical scope, no extra premises: biological function, negative experience, normative prohibition.
    models=list(product((0,1),repeat=3))
    return dict(price=dict(models=sum(counts.values()),counts=counts,examples=examples,identity_failures=residual),regulation=dict(models=36,counts=control),bridges=dict(models=len(models),function_without_experience=sum(f and not h for f,h,n in models),experience_without_prohibition=sum(h and not n for f,h,n in models)))
if __name__=='__main__': print(json.dumps(run(),ensure_ascii=False,indent=2))
