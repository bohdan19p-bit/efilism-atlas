import json,itertools,collections
from pathlib import Path
p=Path(__file__).resolve().parent
a=json.loads((p/'architectura.json').read_text()); c=json.loads((p/'critica.json').read_text())
rules=a['principles']; outputs=set(a['output_labels']); allids={r['id'] for r in rules}
def derive(facts,active):
    known=set(facts); trace=[]
    while True:
        new=[r for r in rules if r['id'] in active and set(r['antecedents'])<=known and r['conclusion'] not in known]
        if not new: break
        for r in new: known.add(r['conclusion']); trace.append(r['id'])
    return sorted(known&outputs),trace
def status(out):
    f='forbid_action' in out; p='permit_action' in out
    return 'conflict' if f and p else 'forbidden' if f else 'permitted' if p else 'undetermined'
def compute():
    matrix=[]; subset_stats={}; baseline={case['id']:derive(case['facts'],allids)[0] for case in c['cases']}
    for prof in c['profiles']:
        for case in c['cases']:
            out,trace=derive(case['facts'],allids-set(prof['removed'])); base=baseline[case['id']]
            matrix.append({'profile':prof['id'],'case':case['id'],'outputs':out,'lost':sorted(set(base)-set(out)),'status':status(out),'trace':trace})
    for case in c['cases']:
        counts=collections.Counter(); support=collections.Counter()
        for mask in itertools.product([False,True],repeat=len(rules)):
            out,_=derive(case['facts'],{r['id'] for r,b in zip(rules,mask) if b}); counts[status(out)]+=1; support.update(out)
        subset_stats[case['id']]={'statuses':dict(sorted(counts.items())),'output_counts':dict(sorted(support.items()))}
    return {'matrix':matrix,'subset_statistics':subset_stats,'subset_evaluations':len(c['cases'])*2**len(rules),'profile_evaluations':len(matrix)}
if __name__=='__main__':
    result=compute(); assert result==c['computed']; print(json.dumps({'verified':True,'subset_evaluations':result['subset_evaluations'],'profile_evaluations':result['profile_evaluations']},ensure_ascii=False))
