import json,math,csv
KW={'Atacar':0,'Protetor':1,'Veloz':1,'Investida':2,'Atingir':2}   # custo em pontos
SPEC={ 'GK01':(5,'Atingir'),'GK02':(3,'Atacar'),'GK03':(3,'Protetor'),'GK04':(4,'Veloz'),'GK05':(1,'Veloz'),
'GK06':(5,'Investida'),'GK07':(1,'Protetor'),'GK08':(1,'Atacar'),'GK09':(4,'Investida'),'GK10':(2,'Atacar'),
'GK11':(1,'Veloz'),'GK12':(6,'Atacar'),'GK13':(1,'Atacar'),'GK14':(2,'Protetor'),'GK15':(2,'Veloz'),
'GK17':(2,'Investida'),'GK18':(4,'Protetor'),'GK19':(8,'Investida'),'GK20':(2,'Protetor'),'GK21':(7,'Veloz'),
'GK22':(3,'Investida'),'GK23':(3,'Atacar'),'GK24':(4,'Atacar'),'GK25':(1,'Atacar'),'GK26':(2,'Atacar'),
'GK28':(3,'Veloz'),'GK29':(5,'Protetor'),'GK30':(6,'Investida'),'GK16':(1,'Protetor'),'GK27':(6,'Veloz')}
def stats(cost,kw,legend=False):
    pts=2*cost+1-KW[kw]+(1 if legend else 0)
    pts=min(pts,20)
    hi=math.ceil(pts*0.6); lo=pts-hi
    if kw in('Veloz','Investida','Atingir'): a,p=hi,lo
    elif kw=='Protetor': a,p=lo,hi
    else: a,p=math.ceil(pts/2),pts//2
    a=max(1,min(10,a)); p=max(1,min(10,p))
    return a,p
d=json.load(open('deck_goku.json'))
for c in d:
    i=c['id']
    if i in SPEC:
        cost,kw=SPEC[i]; c['custo']=cost; c['palavra']=kw
        c['atk'],c['pv']=stats(cost,kw,i=='GK01')
        c['tipo_carta']='unidade'; c['tipo']='Saiyajin'; c.pop('nota',None)
        if i=='GK01': c['estagio']='lendaria'
json.dump(d,open('deck_goku_v2.json','w'),ensure_ascii=False,indent=1)
with open('catalogo_goku_v2.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['id','nome','custo','atk','pv','palavra','fonte'])
    for c in d: w.writerow([c['id'],c['nome'],c['custo'],c.get('atk',''),c.get('pv',''),c.get('palavra',''),c['fonte']])
for c in d: print(c['id'],c['custo'],c.get('atk'),c.get('pv'),c.get('palavra'))
