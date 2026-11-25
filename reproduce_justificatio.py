from itertools import product
V='F I B H R E K A C T P U G L X Y'.split()
TESTS=[
('T01','Факт и независимость не влекут антиценность',lambda m:m['F'] and m['I'],lambda m:m['B']),
('T02','Антиценность не влечёт практическое основание',lambda m:m['B'] and m['H'],lambda m:m['R']),
('T03','Равный учёт и признанный критерий условно сохраняют основание',lambda m:m['R'] and m['E'] and m['K'] and (not(m['R'] and m['E'] and m['K']) or m['A']),lambda m:m['A']),
('T04','Признанное основание без нормы учёта не влечёт долг',lambda m:m['R'] and m['A'],lambda m:m['C']),
('T05','Риск и отсутствие авторизации сами по себе не влекут запрет',lambda m:m['H'] and m['T'] and not m['P'],lambda m:m['L']),
('T06','Непригодность одного оправдания не доказывает запрет',lambda m:not m['G'],lambda m:m['L']),
('T07','Запрет следует при явном защитном принципе и его условиях',lambda m:m['H'] and m['T'] and not m['P'] and (not(m['H'] and m['T'] and not m['P']) or m['L']),lambda m:m['L']),
('T08','Универсальное правило не влечёт полный охват',lambda m:m['U'],lambda m:m['X']),
('T09','Полный охват и правило влекут заключение при заданном правиле перехода',lambda m:m['U'] and m['X'] and (not(m['U'] and m['X']) or m['L']),lambda m:m['L']),
('T10','Отсутствие установленного запрета не влечёт положительную авторизацию',lambda m:not m['L'],lambda m:m['Y'])]
def run():
 out=[]
 for i,t,p,c in TESTS:
  relevant=[]; models=0; counter=0; first=None
  for vals in product([False,True],repeat=len(V)):
   m=dict(zip(V,vals))
   if p(m):
    models+=1
    if not c(m):
     counter+=1
     if first is None:first=m.copy()
  out.append(dict(id=i,title=t,valuations=2**len(V),premise_models=models,countermodels=counter,first_countermodel=first,valid=counter==0))
 return out
if __name__=='__main__':
 import json
 print(json.dumps(run(),ensure_ascii=False,indent=2))
