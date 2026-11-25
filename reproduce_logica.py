import json, itertools as it, shutil, pathlib, re, collections, zipfile
from fractions import Fraction as Q
P=pathlib.Path('/mnt/data'); src=P/'Atlas_Efilismi_v1_3'; out=P/'Atlas_Efilismi_v1_4'; shutil.copytree(src,out,dirs_exist_ok=True)
D=json.loads((src/'atlas_unified.json').read_text()); oldN=len(D['nodes']);oldE=len(D['edges']); tests=[]
def test(id,mod,title,form,models,evalfn,interpret,scope,expect):
    count=eligible=bad=0; witness=None
    for m in models:
        count+=1; premise,conclusion=evalfn(m)
        if premise:
            eligible+=1
            if not conclusion:
                bad+=1
                if witness is None:witness=m
    assert eligible>0 and bool(bad)==expect,(id,bad,eligible)
    tests.append(dict(id=id,module=mod,title=title,formula=form,models=count,premise_models=eligible,countermodels=bad,witness=witness,result='countermodel' if bad else 'bounded_entailment',interpretation=interpret,scope=scope))
def unary(names):
    for n in range(1,4):
        for bits in it.product([False,True],repeat=n*len(names)):
            yield {'domain':list(range(n)),**{p:list(bits[i*n:(i+1)*n]) for i,p in enumerate(names)}}
def allimp(a,b):return all(not x or y for x,y in zip(a,b))
S='Конечные непустые области из 1–3 элементов; одноместные предикаты, все интерпретации. Отсутствие контрмодели в этих границах не доказывает общую валидность.'
test('LOG-T01','LOG-01','От частного случая к универсальному запрету','∃x(Cx ∧ Fx) ⊭ ∀x(Cx → Fx)',unary(['C','F']),lambda m:(any(c and f for c,f in zip(m['C'],m['F'])),allimp(m['C'],m['F'])),'C — создание; F — запрет. Запрет хотя бы одного случая не устанавливает запрет всех случаев.',S,True)
test('LOG-T02','LOG-01','Явное общее правило и охват класса','∀x(Cx → Rx), ∀x(Rx → Fx) ⊨ ∀x(Cx → Fx)',unary(['C','R','F']),lambda m:(allimp(m['C'],m['R']) and allimp(m['R'],m['F']),allimp(m['C'],m['F'])),'R — применимость защитного критерия. Вывод следует по транзитивности импликации для произвольного x; обе универсальные посылки требуют отдельного обоснования.',S,False)
test('LOG-T03','LOG-01','Отсутствие согласия не устанавливает разрешение','∀x(Cx → ¬Sx) ⊭ ∀x(Cx → Px)',unary(['C','S','P']),lambda m:(all(not c or not s for c,s in zip(m['C'],m['S'])),allimp(m['C'],m['P'])),'S — предварительное согласие, P — разрешение. Невозможность получить согласие сама по себе не устанавливает ни разрешение, ни запрет; нужен нормативный принцип.',S,True)
test('LOG-T04','LOG-01','Субъектный и межсубъектный охват','∀x(Hx → Vx), ∃x Hx ⊨ ∃x Vx',unary(['H','V']),lambda m:(allimp(m['H'],m['V']) and any(m['H']),any(m['V'])),'H — переживаемый вред; V — антиценность для субъекта. Следование по инстанцированию; тезис H→V не доказан логикой.',S,False)
def frames(reflexive=False,serial=False,props=('p','q')):
 for n in (1,2):
  for b in it.product([False,True],repeat=n*n):
   R=[list(b[i*n:(i+1)*n]) for i in range(n)]
   if reflexive and not all(R[i][i] for i in range(n)):continue
   if serial and not all(any(row) for row in R):continue
   for vals in it.product([False,True],repeat=n*len(props)):
    yield {'worlds':list(range(n)),'R':R,**{p:list(vals[j*n:(j+1)*n]) for j,p in enumerate(props)}}
def box(m,p,w=0):return all(not r or v for r,v in zip(m['R'][w],p))
M='Все рефлексивные фреймы Крипке с 1–2 мирами и булевыми оценками; выделенный мир 0. Не модель физической Вселенной.'
test('LOG-T05','LOG-02','Фактичность и необходимость','p ⊭ □p',frames(True),lambda m:(m['p'][0],box(m,m['p'])),'Истинность в действительном мире не равна истинности во всех доступных мирах.',M,True)
test('LOG-T06','LOG-02','Необходимость в рефлексивной модели','□p ⊨ p',frames(True),lambda m:(box(m,m['p']),m['p'][0]),'Это аксиома T: действительный мир доступен из самого себя. Не переносится на произвольную деонтическую доступность.',M,False)
test('LOG-T07','LOG-02','Распределение необходимости','□(p → q), □p ⊨ □q',frames(),lambda m:(box(m,[not p or q for p,q in zip(m['p'],m['q'])]) and box(m,m['p']),box(m,m['q'])),'Правило K следует из семантики □; не делает фактическую посылку необходимой.','Все фреймы 1–2 мира, включая пустые отношения доступности.',False)
# deterministic laws: unique successor in each possible initial state, but event may differ across initial states.
models=({'transition':list(f),'event':list(p)} for f in it.product(range(2),repeat=2) for p in it.product([False,True],repeat=2))
test('LOG-T08','LOG-02','Детерминизм и безусловная необходимость','p(f(s₀)) ⊭ ∀s p(f(s))',models,lambda m:(m['event'][m['transition'][0]],all(m['event'][s] for s in m['transition'])),'Даже при одном и том же детерминированном законе f разные допустимые начальные состояния могут давать разные исходы. Это не опровержение детерминизма.','Все функции двух состояний в два состояния и все оценки события.',True)
DE='Сериальные фреймы 1–2 мира; O — истинность во всех нормативно допустимых мирах, Pp := ¬O¬p. Стандартная упрощённая деонтическая семантика.'
test('LOG-T09','LOG-03','Должное и действительное','Op ⊭ p',frames(serial=True),lambda m:(box(m,m['p']),m['p'][0]),'Обязанность может быть нарушена. Нормативная модель не описывает фактическое поведение.',DE,True)
test('LOG-T10','LOG-03','Обязанность и разрешение','Op ⊨ Pp',frames(serial=True),lambda m:(box(m,m['p']),not box(m,[not p for p in m['p']])),'Непустота множества допустимых миров предотвращает одновременную обязательность противоположных состояний.',DE,False)
test('LOG-T11','LOG-03','Разрешение не обязанность','Pp ⊭ Op',frames(serial=True),lambda m:(not box(m,[not p for p in m['p']]),box(m,m['p'])),'Допустимость поступка не делает его обязательным.',DE,True)
test('LOG-T12','LOG-03','Запрет действия и полномочия третьих лиц','O¬p ⊭ Pq',frames(serial=True),lambda m:(box(m,[not p for p in m['p']]),not box(m,[not q for q in m['q']])),'p — исходное действие, q — отдельное вмешательство. Из этического запрета не выводится право принуждения; автономия и ненасилие требуют самостоятельной проверки.',DE,True)
# defeasible classification with explicit priorities (no general default logic engine)
def policies():
 for r,c,b in it.product([False,True],repeat=3):yield {'reason':r,'counter_reason':c,'block':b}
def outcome(m):
 if m['block']:return 'не допустимо по отдельному ограничению'
 if m['reason'] and m['counter_reason']:return 'конфликт; решение открыто'
 if m['reason']:return 'предварительно поддержано'
 if m['counter_reason']:return 'предварительно не поддержано'
 return 'нет достаточных данных'
for m in policies():m['result']=outcome(m)
N='Все 8 состояний иллюстративного приоритетного классификатора; не общая немонотонная логика. Ограничение имеет приоритет по stipulation.'
test('LOG-T13','LOG-04','Пересмотр предварительного вывода','r ⊭ предварительная поддержка при расширении данных',policies(),lambda m:(m['reason'],outcome(m)=='предварительно поддержано'),'Добавление встречного основания или ограничения может отозвать предварительную поддержку; не отменяет первоначальный факт.',N,True)
test('LOG-T14','LOG-04','Приоритет самостоятельного ограничения','block ⊨ отказ по ограничению',policies(),lambda m:(m['block'],outcome(m)=='не допустимо по отдельному ограничению'),'Следует из выбранного порядка правил, не доказывает этическую обязательность такого порядка.',N,False)
test('LOG-T15','LOG-04','Конфликт не равен разрешению','r ∧ c ∧ ¬block ⊭ предварительная поддержка',policies(),lambda m:(m['reason'] and m['counter_reason'] and not m['block'],outcome(m)=='предварительно поддержано'),'Встречные основания без приоритета оставляют решение открытым.',N,True)
# benign toy decision problem: product test, abstract units. Probability grid exact rational.
rows=[]
for p in [Q(0),Q(1,100),Q(1,20),Q(1,10),Q(1,2),Q(1)]:
 for g,l in it.product([1,5,20],[5,20,100]):
  eu=(1-p)*g-p*l
  rows.append({'p':str(p),'gain':g,'loss':l,'EU':str(eu),'eu_positive':eu>0,'upper_bound_pass':p<=Q(1,100)})
R='54 искусственных сценария: 6 вероятностей × 3 выигрыша × 3 потери. Точные дроби; порог 1% выбран только для примера, не нормативная рекомендация.'
test('LOG-T16','LOG-05','Положительное среднее и риск','EU > 0 ⊭ p = 0',rows,lambda m:(m['eu_positive'],Q(m['p'])==0),'Положительное ожидаемое значение совместимо с ненулевым риском. Это логическое различие, не этическая оценка.',R,True)
test('LOG-T17','LOG-05','Среднее и независимое ограничение','EU > 0 ⊭ p ≤ 1/100',rows,lambda m:(m['eu_positive'],m['upper_bound_pass']),'Максимизация среднего и отдельный критерий допустимости риска — разные правила выбора. Обоснование порога остаётся открытым.',R,True)
intervals=[{'lo':str(a),'hi':str(b)} for a,b in it.product([Q(0),Q(1,100),Q(1,10),Q(1)],repeat=2) if a<=b]
test('LOG-T18','LOG-05','Неопределённость и невозможность','p_min = 0 ⊭ p_max = 0',intervals,lambda m:(Q(m['lo'])==0,Q(m['hi'])==0),'Нулевая нижняя оценка не исключает положительную верхнюю. Отсутствие надёжной оценки риска не равнозначно доказательству безопасности.','Все 10 интервалов на сетке {0, 1/100, 1/10, 1}.',True)
refs=[('LOG-R01','Classical Logic','https://plato.stanford.edu/entries/logic-classical/'),('LOG-R02','Modal Logic','https://plato.stanford.edu/entries/logic-modal/'),('LOG-R03','Deontic Logic','https://plato.stanford.edu/entries/logic-deontic/'),('LOG-R04','Non-monotonic Logic','https://plato.stanford.edu/entries/logic-nonmonotonic/'),('LOG-R05','Decision Theory','https://plato.stanford.edu/entries/decision-theory/'),('LOG-R06','Imprecise Probabilities','https://plato.stanford.edu/entries/imprecise-probabilities/')]
mods=[('LOG-01','Logica Praedicatorum — предикатная логика','Отличаем применимость универсального критерия к каждому субъекту от категорического запрета всех действий класса. Квантор ∀ требует явно заданной области. Непустота области не гарантирует существование случаев C.','wiki:C027','wiki:C030','ARG-18'),('LOG-02','Logica Modalis — модальная логика','Разграничиваем фактическую, номологическую и логическую необходимость. Детерминированность при фиксированных законах и условиях не означает необходимость этих условий. Контингентность не тождественна случайности.','wiki:C011','wiki:C012','arch:C009'),('LOG-03','Logica Deontica — деонтическая логика','Различаем первичные практические основания, итоговую обязанность, запрет и разрешение. Запрет добровольного действия не создаёт полномочия принуждать других.','wiki:C030','arch:C019','arch:C020'),('LOG-04','Logica Nonmonotonica — пересмотр выводов','Предварительные основания могут быть пересмотрены при появлении встречных обстоятельств. Различаем изменение фактов, конкуренцию оснований и независимые ограничения.','wiki:C022','wiki:C026','DEM-04'),('LOG-05','Theoria Decisionis — теория решений','Различаем вероятность, неопределённость, ожидаемое значение и независимое условие допустимости. Не присваиваем вероятности реальным жизненным сценариям без данных. Двойной предохранитель требует отдельных критериев профилактики и коррекции.','wiki:C022','ARG-09','DEM-04')]
L={'version':'1.4','scope':'Редакторская реконструкция; не доказательство метаэтики. Конечные тесты и иллюстративные модели.','modules':[{'id':i,'title':t,'body':b,'related':list(anchors)} for i,t,b,*anchors in mods],'references':[{'id':i,'title':t,'url':u,'scope':'Поисковые выдержки SEP; не исчерпывающее чтение'} for i,t,u in refs],'tests':tests,'decision_examples':rows,'nonmonotonic_examples':[dict(m,result=outcome(m)) for m in policies()]}
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
nodeids={n['id'] for n in D['nodes']}
def node(id,title,kind,body,category,status,record=None):
 assert id not in nodeids;nodeids.add(id);D['nodes'].append(dict(id=id,title=title,kind=kind,body=body,category=category,status=status,record=record or {}))
def edge(a,b,typ,label,note=''):
 assert a in nodeids and b in nodeids,(a,b)
 D['edges'].append(dict(id=f'L14:E{len(D["edges"])-oldE+1:04}',source=a,target=b,type=typ,label=label,status='conditional',note=note))
for i,t,b,*anchors in mods:node(i,t,'logica',b,'Логический аппарат','reconstruction')
for i,t,u in refs:node(i,t,'reference','Методологический ориентир Stanford Encyclopedia of Philosophy. Проверены поисковые выдержки, не весь текст.','Logica','selective_review',{'url':u});D['nodes'][-1]['origin']={'url':u}
for i,t,b,*anchors in mods:
 for a in anchors:edge(i,a,'related_to','Тематическое сопоставление','Не логическое следствие')
for i,(m,ref) in enumerate(zip(mods,refs)) :edge(m[0],ref[0],'academic_reference','Методологический ориентир')
edge('LOG-05','LOG-R06','academic_reference','Неопределённость вероятностей')
for t in tests:
 body=f"{t['formula']}\n\n{t['interpretation']}\n\nПроверено моделей: {t['models']}; моделей с истинными посылками: {t['premise_models']}; контрмоделей: {t['countermodels']}.\n{t['scope']}"
 node(t['id'],t['title'],'logica_test',body,'Logica / конечные тесты','countermodel' if t['countermodels'] else 'conditional',t)
 edge(t['module'],t['id'],'contains','Формальный тест')
D.update(version='1.4',edition='Logica Efilismi — расширенный логический аппарат',counts=dict(collections.Counter(n['kind'] for n in D['nodes'])),edge_counts=dict(collections.Counter(e['type'] for e in D['edges'])))
D['history'].append(dict(version='1.4',title='Logica',description='Пять модулей, конечные предикатные, модальные и деонтические модели, приоритетный классификатор и иллюстративная теория решений.'))
D['limits'].append('Logica: конечные модели ограниченного размера, не полноценный универсальный решатель. Этические посылки и пороги не доказаны тестами.')
dump(out/'logica.json',L);dump(out/'atlas_unified.json',D)
# integrate HTML, preserving prior code and embedded data.
h=(src/'Atlas_Efilismi.html').read_text(); h=h.replace('Atlas Efilismi — v1.3','Atlas Efilismi — v1.4').replace('v1.3</','v1.4</')
start=h.index('<script id="atlas-data"'); a=h.index('>',start)+1;b=h.index('</script>',a);h=h[:a]+json.dumps(D,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+h[b:]
h=h.replace("demonstratio_case:'Контекстный пример'}","demonstratio_case:'Контекстный пример',logica:'Логический модуль',logica_test:'Конечный тест'}")
h=h.replace("['catalogue','Указатель'","['logica','Logica',['logica','logica_test']],['catalogue','Указатель'")
h=h.replace("'foundation','demonstratio'].includes(mode)","'foundation','demonstratio','logica'].includes(mode)")
h=h.replace("['demonstratio',c.demonstratio,'Досье Demonstratio']","['demonstratio',c.demonstratio,'Досье Demonstratio'],['logica',c.logica,'Модули Logica']")
h=h.replace("['DEM-01','DEM-02'","['LOG-01','LOG-02','LOG-03','LOG-04','LOG-05','DEM-01','DEM-02'")
h=h.replace("function detailFields(n){let h='';const r=n.record||{},o=n.ontology||{},m=n.mapping||{};","""function detailFields(n){let h='';const r=n.record||{},o=n.ontology||{},m=n.mapping||{};
 if(n.kind==='logica_test'){h+=section('Результат конечной проверки',field('Формула',r.formula)+field('Итог',r.countermodels?'Контрмодель найдена':'В заданных границах контрмодель не найдена')+field('Число моделей',String(r.models))+field('Истинные посылки',String(r.premise_models))+field('Контрмодели',String(r.countermodels))+field('Первый свидетель',r.witness?JSON.stringify(r.witness,null,2):'—')+field('Границы',r.scope));}
 if(n.kind==='logica'){h+=section('Тесты модуля',D.edges.filter(e=>e.source===n.id&&e.type==='contains').map(e=>openBtn(e.target,N.get(e.target)?.title)).join(''));}
""")
(out/'Atlas_Efilismi.html').write_text(h,encoding='utf8')
# report
report=['# Logica Efilismi — v1.4','\n## Метод и ограничения','\nМодели ниже не являются доказательствами истинности философских посылок. Проверка предикатных и модальных схем ограничена малыми конечными областями. Общая валидность T02, T04, T06, T07, T10 следует из указанных правил и семантики; остальные положительные результаты относятся только к заданной модели. Немонотонный модуль — классификатор с заданным приоритетом, а не универсальный вывод. Вероятности и полезности условны. Никаких выводов о допустимости принуждения, насилия или вреда существующим субъектам не следует из этики создания.','\n## Модули']
for i,t,b,*anchors in mods:
 report+=['\n### '+t,b,'Связанные узлы: '+', '.join(anchors)]
 for x in tests:
  if x['module']==i:
   report+=['\n#### '+x['id']+' — '+x['title'],'`'+x['formula']+'`',x['interpretation'],f"Моделей: {x['models']}; удовлетворяют посылкам: {x['premise_models']}; контрмоделей: {x['countermodels']}.",x['scope']]
   if x['witness'] is not None:report+=['Первый свидетель: `'+json.dumps(x['witness'],ensure_ascii=False)+'`']
report+=['\n## Выводы для книги','1. Развести квантор универсального критерия и квантор запрета всех случаев (§33).','2. Явно индексировать необходимость условиями и законами (§24 и главы о модальности).','3. Отличать первоначальное основание от итоговой обязанности, а обязанность от полномочия третьего лица (§30, §32).','4. Уточнить, является ли защитный порог независимым ограничением или компонентом агрегированной оценки; это содержательное нормативное решение, не математическая теорема.','5. Не выводить квалификацию Error Prime из одной фактичности физических процессов.','\n## Академические ориентиры','Выборочная сверка по доступным поисковым выдержкам, а не полное чтение.']+[f'- [{t}]({u})' for _,t,u in refs]
(out/'logica_report.md').write_text('\n\n'.join(report),encoding='utf8')
# preserve readme, add concise intro
read=(src/'README.md').read_text();(out/'README.md').write_text('# Atlas Efilismi v1.4 — Logica\n\nОткрыть Atlas_Efilismi.html. Вкладка Logica: 5 модулей и 18 тестов. logica.json — результаты, logica_report.md — отчёт, validation_v1_4.json — протокол. reproduce_logica.py воспроизводит модели и сборку при наличии исходного каталога v1.3.\n\n---\n\n'+read)
assert D['nodes'][:oldN]==json.loads((src/'atlas_unified.json').read_text())['nodes'];assert len({e['id'] for e in D['edges']})==len(D['edges']);assert all(e['source'] in nodeids and e['target'] in nodeids for e in D['edges']);assert len(nodeids)==len(D['nodes']);assert json.loads(h[h.index('>',h.index('<script id="atlas-data"'))+1:h.index('</script>',h.index('<script id="atlas-data"'))])==D
stats={'version':'1.4','nodes':len(D['nodes']),'edges':len(D['edges']),'added_nodes':len(D['nodes'])-oldN,'added_edges':len(D['edges'])-oldE,'tests':len(tests),'models':sum(t['models'] for t in tests),'with_countermodel':sum(bool(t['countermodels']) for t in tests),'no_countermodel_in_bound':sum(not t['countermodels'] for t in tests),'checks':['unique nodes and edges','valid endpoints','preserved original nodes','HTML embedded JSON equals atlas JSON'],'browser':'not yet tested'}
dump(out/'validation_v1_4.json',stats); print(stats)
