"""Standard-library only. Run: python reproduce_fundamentalis.py"""
from pathlib import Path
from itertools import combinations, product
import json

def solve(data):
    rules=data['rules']; syms=list(data['symbols']); subsets=[s for n in range(len(rules)+1) for s in combinations(rules,n)]
    def closure(facts, selected):
        out=set(facts)
        while True:
            new=out|{r['conclusion'] for r in selected if set(r['requires'])<=out}
            if new==out: return out
            out=new
    results=[]
    for s in data['scenarios']:
        minimal=[]; valid=0
        for subset in subsets:
            ids=set(r['id'] for r in subset)
            if s['target'] in closure(s['facts'],subset):
                valid+=1
                if not any(set(m)<=ids for m in minimal): minimal.append(sorted(ids))
        results.append({**s,'subsets':len(subsets),'supporting_subsets':valid,'minimal_supports':minimal,'full_closure':sorted(closure(s['facts'],rules))})
    # Exhaustive truth valuations with all base facts fixed and subsets of rules.
    # Verify that semantic entailment matches forward closure for each scenario/subset.
    checks=0; mismatches=[]; witnesses=[]
    for s in data['scenarios']:
        free=[x for x in syms if x not in s['facts']]
        vals=[set(s['facts'])|{x for x,b in zip(free,bits) if b} for bits in product([False,True],repeat=len(free))]
        for subset in subsets:
            counter=None; models=0
            for val in vals:
                checks+=1
                if all(not set(r['requires'])<=val or r['conclusion'] in val for r in subset):
                    models+=1
                    if s['target'] not in val and counter is None: counter=sorted(val)
            entailed=counter is None
            if entailed!=(s['target'] in closure(s['facts'],subset)): mismatches.append([s['id'],s['target'],[r['id'] for r in subset]])
            if len(subset)==len(rules) or len(subset)==len(rules)-1:
                witnesses.append({'scenario':s['id'],'target':s['target'],'rules':[r['id'] for r in subset],'models':models,'countermodel_true':counter,'entailed':entailed})
    return {'results':results,'subset_checks':len(subsets)*len(results),'truth_valuation_checks':checks,'mismatches':mismatches,'witnesses':witnesses}
if __name__=='__main__':
    d=json.loads(Path(__file__).with_name('demonstratio_fundamentalis.json').read_text())
    result=solve(d)
    if 'formal' in d: assert d['formal']==result
    print(json.dumps(result,ensure_ascii=False,indent=2))
