# Python 3. Конкретные контрмодели; не доказательство философских посылок.
worlds=[{'L1'},{'L2'}]
assert all(worlds) and not set.intersection(*worlds)
assert len(set([1,-1]))>1
value,authorization=True,False
assert value and not authorization
assert sum([-2,3])>0 and min([-2,3])<0
assert all(x==x*x for x in [0,1]) and 2!=2*2
prohibition,permission=False,False
assert not prohibition and not permission
print('6/6 countermodels reproduced')
