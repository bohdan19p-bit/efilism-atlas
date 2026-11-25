from itertools import product
from collections import Counter

def run():
    # Exact integer comparisons; values are hypothetical, not measured experience.
    weights=range(1,10)
    grid=[dict(a=a,b=b,difference=2*b-a) for a,b in product(weights,repeat=2)]
    outcomes=dict(Counter('X' if r['difference']>0 else 'Y' if r['difference']<0 else 'tie' for r in grid))
    # Dominance: for differences in [0,2] (not both zero), all positive weights preserve strict ranking.
    dominance=[a*x+b*y>0 for x,y in product(range(3),repeat=2) if x or y for a,b in product(weights,repeat=2)]
    # Purely logical independence of four stipulated claims. Not a model of moral reality.
    rows=[dict(zip('DART',v)) for v in product([False,True],repeat=4)]
    tests=[]
    for premise,conclusion in [('D','A'),('D','R'),('D','T'),('R','T'),('A','T')]:
        eligible=[r for r in rows if r[premise]]
        counter=[r for r in eligible if not r[conclusion]]
        tests.append(dict(premise=premise,conclusion=conclusion,eligible=len(eligible),countermodels=len(counter),example=counter[0]))
    # History preservation vs later compensation, model of two distinct variables.
    histories=[dict(past_harm=h,later_benefit=g,net=g-h) for h,g in product(range(4),repeat=2)]
    return dict(scale_grid=grid,scale_counts=outcomes,dominance_checks=len(dominance),dominance_failures=dominance.count(False),asymmetry_models=len(rows),asymmetry_tests=tests,history_cases=len(histories),positive_net_with_past_harm=[r for r in histories if r['past_harm']>0 and r['net']>0])

if __name__=='__main__':
    import json
    print(json.dumps(run(),ensure_ascii=False,indent=2))
