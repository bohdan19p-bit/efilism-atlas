from fractions import Fraction as F
from itertools import product

def run():
    grid=[]
    for p,a,b in product([F(i,10) for i in range(1,10)],repeat=3):
        post=p*a/(p*a+(1-p)*b)
        grid.append((p,a,b,post))
    # Exact: sign of posterior-prior equals sign of likelihood difference.
    sign=lambda x:(x>0)-(x<0)
    tests={'grid':len(grid),'equal_likelihood':sum(a==b for p,a,b,q in grid),'equal_unchanged':sum(a==b and p==q for p,a,b,q in grid),'direction_failures':sum(sign(q-p)!=sign(a-b) for p,a,b,q in grid)}
    # Same accuracy and mean confidence, different alignment with correctness.
    y=[1,1,0,0]; samples={'aligned':[.9,.8,.6,.5],'reversed':[.5,.6,.8,.9]}
    scores={k:{'mean_confidence':sum(v)/4,'accuracy':sum(y)/4,'brier':sum((p-o)**2 for p,o in zip(v,y))/4} for k,v in samples.items()}
    # Independent truth and justification: toy logical countermodels.
    worlds=list(product([False,True],repeat=2))
    return dict(bayes=tests,calibration=scores,logic={'models':len(worlds),'truth_without_justification':sum(t and not j for t,j in worlds),'justification_without_truth':sum(j and not t for t,j in worlds)})
if __name__=='__main__':
    import json
    print(json.dumps(run(),ensure_ascii=False,indent=2))
