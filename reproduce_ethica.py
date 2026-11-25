from itertools import product
import json

def run():
    # Two independent obligations in an abstract two-alternative decision set.
    # p, h: alternative meets prevention and help requirements.
    counts={"both_feasible":0,"conflict":0,"one_requirement_unattainable":0,"neither_attainable":0}
    examples={}
    for p0,h0,p1,h1 in product((False,True),repeat=4):
        alternatives=[(p0,h0),(p1,h1)]
        p=any(x[0] for x in alternatives); h=any(x[1] for x in alternatives)
        joint=any(x[0] and x[1] for x in alternatives)
        key="both_feasible" if joint else "conflict" if p and h else "one_requirement_unattainable" if p or h else "neither_attainable"
        counts[key]+=1; examples.setdefault(key,alternatives)
    # Distinguish no consent, independent justification, and prior consent.
    # A toy disjunctive gate, NOT an ethical rule for real-world permission.
    counter=[]
    for c,j in product((False,True),repeat=2):
        gate=c or j
        if not c and gate: counter.append({"consent":c,"independent_ground":j,"gate":gate})
    return {"compatibility":{"models":16,"counts":counts,"examples":examples},"authorization":{"models":4,"counterexamples_to_no_consent_implies_no_gate":counter}}

if __name__=="__main__": print(json.dumps(run(),ensure_ascii=False,indent=2))
