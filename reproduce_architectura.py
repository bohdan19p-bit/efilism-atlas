import json,itertools
from pathlib import Path
d=json.loads(Path(__file__).with_name('architectura.json').read_text(encoding='utf8'))
p=d['principles']; ids=[x['id'] for x in p]; outputs=set(d['output_labels'])
def closure(facts, enabled):
    s=set(facts)
    while True:
        t=s|{x['conclusion'] for x in p if x['id'] in enabled and set(x['antecedents'])<=s}
        if t==s:return s
        s=t
subsets=[set(c) for k in range(len(ids)+1) for c in itertools.combinations(ids,k)]
for case in d['cases']:
    full=closure(case['facts'],ids)&outputs
    assert full==set(case['derived'])
    for test in [t for t in d['tests'] if t['case']==case['id']]:
        good=[ss for ss in subsets if test['target'] in closure(case['facts'],ss)]
        minima=[ss for ss in good if not any(t<ss for t in good)]
        assert {frozenset(x) for x in minima}=={frozenset(x) for x in test['minimal_sets']}
        assert len(good)==test['successful_subsets']
    models=[]
    keys=sorted(outputs)
    for bits in itertools.product([False,True],repeat=len(keys)):
        s=set(case['facts'])|{x for x,b in zip(keys,bits) if b}
        if all(not set(x['antecedents'])<=s or x['conclusion'] in s for x in p):models.append(s)
    assert set.intersection(*models)&outputs==full
for x in p:
    witnesses=[{'case':c['id'],'lost':sorted((closure(c['facts'],ids)-closure(c['facts'],set(ids)-{x['id']}))&outputs)} for c in d['cases']]
    assert [w for w in witnesses if w['lost']]==x['independence_witnesses']
assert {'forbid_action','permit_action'}<=closure(d['stress_test']['facts'],ids)
print('OK:',len(d['cases'])*len(subsets),'subset checks;',len(d['cases'])*2**len(outputs),'semantic valuations;',len(d['tests']),'minimal sets')
