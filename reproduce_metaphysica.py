from itertools import product
import json

def run():
    # two worlds, two candidate laws; membership in each world
    modal=[]
    for m in product((0,1),repeat=4):
        local=bool((m[0] or m[1]) and (m[2] or m[3]))
        common=bool((m[0] and m[2]) or (m[1] and m[3]))
        modal.append((m,local,common))
    # p at two times in each of two worlds; invariance in actual world vs modal invariance
    temporal=[]
    for m in product((0,1),repeat=4):
        temporal.append((m,bool(m[0] and m[1]),all(m)))
    # all deterministic maps on four microstates; partition {0,1}, {2,3}
    macro=[]
    for f in product(range(4),repeat=4):
        closed=all(f[2*i]//2==f[2*i+1]//2 for i in range(2))
        # independent verification: existence of a commuting deterministic macro map
        exists=any(all(g[x//2]==f[x]//2 for x in range(4)) for g in product(range(2),repeat=2))
        assert closed==exists
        macro.append((f,closed))
    # illustrate divergence, not a proof of chaos
    a,b=.2,.200001
    trajectory=[]
    for t in range(31):
        trajectory.append(dict(t=t,a=a,b=b,distance=abs(a-b)))
        a,b=4*a*(1-a),4*b*(1-b)
    return dict(modal=dict(models=len(modal),local=sum(l for _,l,c in modal),common=sum(c for _,l,c in modal),countermodels=[list(m) for m,l,c in modal if l and not c]),temporal=dict(models=len(temporal),countermodels=[list(m) for m,t,u in temporal if t and not u]),macro=dict(models=len(macro),closed=sum(c for _,c in macro),not_closed=sum(not c for _,c in macro),example_closed=[2,3,0,1],example_open=[0,2,1,3]),logistic=dict(initial=[.2,.200001],r=4,trajectory=trajectory,precision='double; illustrative'))

if __name__=='__main__': print(json.dumps(run(),ensure_ascii=False,indent=2))
