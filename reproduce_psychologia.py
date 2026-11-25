from itertools import product
from fractions import Fraction as F
import json
def run():
    counts={'higher':0,'lower':0,'equal':0}
    for a,b in product(range(1,5),repeat=2):
        v=F(a,a+b)
        counts['higher' if v>F(1,2) else 'lower' if v<F(1,2) else 'equal']+=1
    invariance=sum(a==c and b==d for a,b,c,d in product([0,1],repeat=4))
    risk=[{'n':n,'no_event_if_1pct':float(F(99,100)**n),'no_event_if_5pct':float(F(95,100)**n),'posterior_high':float(F(95,100)**n/(F(99,100)**n+F(95,100)**n))} for n in [0,10,50,100]]
    return {'selection':{'models':16,'counts':counts},'label_switch':{'models':16,'invariant':invariance,'noninvariant':16-invariance},'risk':risk}
if __name__=='__main__': print(json.dumps(run(),ensure_ascii=False,indent=2))
