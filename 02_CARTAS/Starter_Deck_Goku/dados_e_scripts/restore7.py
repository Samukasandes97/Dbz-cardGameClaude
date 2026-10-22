import cv2,numpy as np,os,sys
from skimage.filters import sato,apply_hysteresis_threshold
LEADER={1,2,3,4,5,6,19,22}; EXTRA={15,26}
kind=lambda i:'L' if i in LEADER else 'E' if i in EXTRA else 'B'
RECT={'L':(20,0,545,742),'B':(46,26,556,724),'E':(30,28,552,722)}
KS=5
IM={i:cv2.imread(f'src/{i:02d}.png') for i in range(30)}
HP={i:(lambda g:g-cv2.GaussianBlur(g,(0,0),1.5))(cv2.cvtColor(IM[i],cv2.COLOR_BGR2GRAY).astype(np.float32)) for i in range(30)}
os.makedirs('src2',exist_ok=True)
ker=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(KS,KS))
for k in 'BLE':
    ids=[i for i in range(30) if kind(i)==k]
    x0,y0,x1,y1=RECT[k]
    reg=np.zeros(HP[0].shape,bool); reg[y0+4:y1-4,x0+4:x1-4]=1; reg[:140,:]=0; reg[492:,:]=0
    if k=='E':
        a,b=HP[ids[0]],HP[ids[1]]; T=np.where(np.sign(a)==np.sign(b),np.sign(a)*np.minimum(np.abs(a),np.abs(b)),0)
        keep=(np.abs(T)>8)&reg; keep=cv2.dilate(keep.astype(np.uint8),np.ones((3,3),np.uint8))
    else:
        A=np.sort(np.array([HP[i] for i in ids]),axis=0); n_=len(ids); lo_i=int(n_*.35); hi_i=int(n_*.65); T=A[lo_i:hi_i].mean(0)
        Tc=np.clip(T,-8,8)
        R=np.maximum(sato(Tc,sigmas=[1.5,2.0],black_ridges=False),sato(Tc,sigmas=[1.5,2.0],black_ridges=True))
        lo,hi=np.percentile(R[reg],[78,95])
        M=apply_hysteresis_threshold(R*reg,lo,hi).astype(np.uint8)
        n,lab,st,_=cv2.connectedComponentsWithStats(M,connectivity=8); keep=np.zeros_like(M)
        for j in range(1,n):
            if st[j,4]>=150 and max(st[j,2],st[j,3])>=45: keep[lab==j]=1
        keep=cv2.dilate(keep,np.ones((3,3),np.uint8))
    keep=keep*reg
    cv2.imwrite(f'corr_{k}.png',keep.astype(np.uint8)*255); print(k,keep.mean().round(3),flush=True)
    Mf=cv2.GaussianBlur(keep.astype(np.float32),(0,0),1.0)[...,None]
    for i in ids:
        f=IM[i]
        cl=cv2.morphologyEx(f,cv2.MORPH_CLOSE,ker); op=cv2.morphologyEx(cl,cv2.MORPH_OPEN,ker)
        sm=cv2.GaussianBlur(op,(0,0),0.8)
        dmax=np.abs(f.astype(np.float32)-sm.astype(np.float32)).max(axis=2)
        faint=cv2.GaussianBlur((dmax<150).astype(np.float32),(0,0),0.7)[...,None]
        W_=Mf*faint
        out=f.astype(np.float32)*(1-W_)+sm.astype(np.float32)*W_
        cv2.imwrite(f'src2/{i:02d}.png',np.clip(out,0,255).astype(np.uint8))
