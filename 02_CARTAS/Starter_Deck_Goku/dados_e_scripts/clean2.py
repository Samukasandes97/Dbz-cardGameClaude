import cv2,numpy as np,sys,os
os.makedirs('clean',exist_ok=True)
LEADER={1,2,3,4,5,6,19,22}; EXTRA={15,26}
def kind(i): return 'L' if i in LEADER else 'E' if i in EXTRA else 'B'
RECT={'L':(20,0,545,742),'B':(46,26,556,724),'E':(30,28,552,722)}
PAN={0:(497,707),1:(495,648),2:(495,652),3:(495,645),4:(497,705),5:(495,655),6:(495,600),7:(673,706),8:(640,705),
10:(490,560),11:(610,708),12:(490,595),13:(495,538),14:(580,708),15:(495,600),16:(610,708),17:(495,650),18:(510,685),19:(495,620),
20:(578,708),21:(490,598),22:(505,705),23:(495,565),24:(495,705),25:(495,705),26:(490,600),28:(530,665),29:(575,705)}
LOGO={10:[(385,608,550,702)],18:[(330,478,550,528)],22:[(330,436,556,496)],26:[(330,656,550,708)],28:[(46,476,275,524)],8:[(40,568,262,632)]}
H=[]
for i in range(30):
    g=cv2.cvtColor(cv2.imread(f'src/{i:02d}.png'),cv2.COLOR_BGR2GRAY).astype(np.float32)
    H.append(g-cv2.GaussianBlur(g,(0,0),2.5))
med=np.median(np.array(H),axis=0)
_b=np.zeros(med.shape,np.float32)
_d=np.array([530,-430],np.float32); _d/=np.linalg.norm(_d); _n=np.array([-_d[1],_d[0]])
_p0=np.array([40,560],np.float32); _p1=np.array([600,70],np.float32)
cv2.fillPoly(_b,[np.array([(_p0+_n*95).astype(int),(_p1+_n*95).astype(int),(_p1-_n*95).astype(int),(_p0-_n*95).astype(int)])],1.0)
TT=np.clip(med,-30,30)*_b
def poly(m,pts): cv2.fillPoly(m,[np.array(pts,np.int32)],255)
def process(i):
    k=kind(i); x0,y0,x1,y1=RECT[k]
    im=cv2.imread(f'src2/{i:02d}.png'); f=im.astype(np.float32); h,w=im.shape[:2]
    mask=np.zeros((h,w),np.uint8)
    px0,px1=(52,552) if k=='B' else (40,562) if k=='L' else (44,556)
    info=None
    if i in PAN:
        py0,py1=PAN[i]; gg=f.mean(axis=2)
        def band(ya,yb): return gg[ya:yb,px0+8:px1-8]
        top=np.median(band(py0+2,py0+6)/np.maximum(band(py0-6,py0-2),12))
        bot=np.median(band(py1-6,py1-2)/np.maximum(band(py1+2,py1+6),12)) if py1+6<y1 else top
        a=float(np.clip((top+bot)/2,.5,1.0)); info=(py0,py1,round(float(top),2),round(float(bot),2),round(a,2))
        if False:
            gain=np.ones((h,w),np.float32); gain[py0:py1,px0:px1]=1/a
            gain=cv2.GaussianBlur(gain,(0,0),1.5) if False else gain
            f=np.clip(f*gain[...,None],0,255)
        u=f.astype(np.uint8)
        g=cv2.cvtColor(u,cv2.COLOR_BGR2GRAY)
        sub=g[py0:py1,px0:px1]
        diff=np.abs(sub.astype(np.int16)-cv2.medianBlur(sub,13).astype(np.int16))
        hsv=cv2.cvtColor(u[py0:py1,px0:px1],cv2.COLOR_BGR2HSV)
        tm=((diff>34)&(sub>190)&(hsv[...,1]<90)).astype(np.uint8)*255
        sat=((hsv[...,1]>105)&(hsv[...,2]>115)).astype(np.uint8)
        satc=cv2.morphologyEx(sat,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))
        n,lab,st,_=cv2.connectedComponentsWithStats(satc,connectivity=8)
        for j in range(1,n):
            x,y,ww,hh,ar=st[j]
            if 20<=ww<=240 and 14<=hh<=38 and ar/(ww*hh)>.5 and x<420: tm[max(y-3,0):y+hh+3,max(x-3,0):x+ww+3]=255
        tm=cv2.dilate(tm,np.ones((5,5),np.uint8))
        pass
    ov=np.zeros((h,w),np.uint8)
    if k=='B':
        poly(ov,[(0,0),(128,0),(128,70),(112,126),(0,126)]); poly(ov,[(396,0),(600,0),(600,118),(452,118)])
    if k=='L': poly(ov,[(372,0),(600,0),(600,114),(430,114)])
    if k=='E': poly(ov,[(0,0),(126,0),(126,122),(0,122)])
    wm=(np.abs(med)>7).astype(np.uint8)*255
    wm=cv2.morphologyEx(wm,cv2.MORPH_OPEN,np.ones((2,2),np.uint8)); wm=cv2.dilate(wm,np.ones((5,5),np.uint8))
    _g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(np.float32); _m=cv2.blur(_g,(9,9)); _s=np.sqrt(np.maximum(cv2.blur(_g*_g,(9,9))-_m*_m,0))
    wm=cv2.bitwise_and(wm,((_s<20).astype(np.uint8)*255))
    cm=np.zeros_like(mask); cm[y0:y1,x0:x1]=255; mask=cv2.bitwise_and(mask,cm); mask=np.maximum(mask,ov)
    u=np.clip(f,0,255).astype(np.uint8)
    out=cv2.inpaint(u,mask,3,cv2.INPAINT_TELEA)
    fs=min([PAN[i][0]]+[l[1] for l in LOGO.get(i,[]) if l[1]<PAN.get(i,(9999,))[0]]) if i in PAN else None
    art=out[y0:y1,x0:x1].copy()
    if fs is not None:
        hh=art.shape[0]; fy=fs-y0-16
        bl=cv2.GaussianBlur(art,(0,0),18).astype(np.float32)
        yy=np.arange(hh,dtype=np.float32)[:,None,None]
        t=np.clip((yy-fy)/38.0,0,1); t=t*t*(3-2*t)
        u=np.clip((yy-fy)/max(hh-fy,1),0,1)
        shade=1-0.95*(u**0.7)
        art=(art.astype(np.float32)*(1-t)+bl*t)*shade
        art=np.clip(art,0,255).astype(np.uint8)
    cv2.imwrite(f'clean/{i:02d}_art.png',art); cv2.imwrite(f'clean/{i:02d}_mask.png',mask[y0:y1,x0:x1])
    return k,info
if __name__=='__main__':
    ids=[int(a) for a in sys.argv[1:]] or range(30)
    for i in ids: print(i,process(i),flush=True)
