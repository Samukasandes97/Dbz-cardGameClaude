import numpy as np,json,sys,re,os
sys.path.insert(0,'anal')
from feat import load
def f0track(x,sr=16000):
    n=int(.04*sr);h=int(.01*sr);out=[]
    for i in range(0,len(x)-n,h):
        s=x[i:i+n]-x[i:i+n].mean(); e=(s*s).sum()
        if e<2e-3: out.append(0);continue
        ac=np.correlate(s,s,'full')[n-1:]; ac/=ac[0]+1e-9
        lo,hi=int(sr/900),int(sr/110); seg=ac[lo:hi]
        # primeiro pico forte (evita subarmonico)
        pk=[k for k in range(1,len(seg)-1) if seg[k]>seg[k-1] and seg[k]>=seg[k+1] and seg[k]>0.5]
        if not pk: out.append(0);continue
        best=max(seg[k] for k in pk); k=[k for k in pk if seg[k]>0.9*best][0]+lo
        out.append(sr/k)
    return np.array(out)
def clas(x):
    d=len(x)/16000; p=f0track(x); v=p>0; vr=v.mean() if len(p) else 0
    env=np.convolve(np.abs(x),np.ones(400)/400,'same'); pkpos=env.argmax()/len(x)
    pv=p[v]
    if len(pv)>=4:
        a=len(pv)//3; s0,s1,s2=np.median(pv[:a]),np.median(pv[a:2*a]),np.median(pv[2*a:]); top=np.percentile(pv,90)
    else: s0=s1=s2=top=0
    return dict(dur=round(d,2),vr=round(float(vr),2),f_ini=round(float(s0)),f_mid=round(float(s1)),f_fim=round(float(s2)),f_top=round(float(top)),pkpos=round(float(pkpos),2))
def tipo(c):
    if c['dur']>=2.2: return 'fala_longa'
    if c['dur']>1.3: return 'frase'
    if c['vr']<0.3: return 'respiracao_impacto'
    if c['f_ini'] and c['f_fim']<c['f_ini']*0.82 and c['f_top']<650: return 'dor_queda'   # voz cai: dor/esforço
    if c['f_mid']>=c['f_ini']*0.95 and c['f_top']>=450: return 'ataque_grito'  # sobe/arco agudo: grito de ataque
    return 'esforco_neutro'
if __name__=='__main__':
    R={}
    for era,dr,nm in (('E','aud_in','Goku (Z - Early)'),('M','aud_mid','Goku (Z - Mid)')):
        for f in sorted(os.listdir(dr)):
            n=int(re.search(r'_(\d+)\.ogg',f).group(1)); c=clas(load(f'{dr}/{f}')); c['tipo']=tipo(c); R[f'{era}{n}']=c
    json.dump(R,open('anal/cls.json','w'))
    from collections import Counter
    print(Counter(c['tipo'] for k,c in R.items() if k[0]=='E'))
    for t in ('ataque_grito','dor_queda','respiracao_impacto','esforco_neutro'):
        print(t,[int(k[1:]) for k,c in R.items() if k[0]=='E' and c['tipo']==t and c['dur']<1.3][:60])
