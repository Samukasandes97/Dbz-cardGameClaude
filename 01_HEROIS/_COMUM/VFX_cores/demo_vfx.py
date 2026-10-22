import numpy as np, cv2, glob, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
C='/tmp/claude-0/-home-claude/84f3faec-af92-5d88-b151-bbf1e79ccb25/scratchpad/cartas/out_goku_v2/'
W,H=1920,1080
FONT='/usr/share/fonts/opentype/inter/Inter-Black.otf'
import os
if not os.path.exists(FONT):
    FONT=glob.glob('/usr/share/fonts/opentype/inter/Inter-*Bold*.otf')[0]
def arena():
    y,x=np.mgrid[0:H,0:W].astype(np.float32)
    g=np.clip(1-(((x-W/2)/W)**2*1.6+((y-H*.55)/H)**2*1.8),0,1)
    b=np.stack([20+26*g,22+30*g,34+40*g],-1)
    grid=((x%120<2)|(y%120<2)).astype(np.float32)[...,None]*8
    return np.clip(b+grid,0,255)
A=arena()
def card(id,h):
    im=Image.open(C+id+'.png').convert('RGBA'); w=int(h*im.width/im.height)
    return im.resize((w,h),Image.LANCZOS)
def paste(base,im,cx,cy,alpha=1.0,rot=0):
    if rot: im=im.rotate(rot,expand=True,resample=Image.BICUBIC)
    a=np.asarray(im).astype(np.float32); x0=int(cx-a.shape[1]/2); y0=int(cy-a.shape[0]/2)
    xs,ys=max(0,x0),max(0,y0); xe,ye=min(W,x0+a.shape[1]),min(H,y0+a.shape[0])
    if xe<=xs or ye<=ys: return
    s=a[ys-y0:ye-y0,xs-x0:xe-x0]; al=s[...,3:4]/255*alpha
    base[ys:ye,xs:xe]=base[ys:ye,xs:xe]*(1-al)+s[...,:3]*al
def screen(a,b): return 255-(255-a)*(255-np.clip(b,0,255))/255
def hshift(d,target,src=12):
    hsv=cv2.cvtColor(np.clip(d,0,255).astype(np.uint8),cv2.COLOR_RGB2HSV)
    m=hsv[...,1]>40
    hsv[...,0]=np.where(m,(hsv[...,0].astype(int)+target-src)%180,hsv[...,0]).astype(np.uint8)
    return cv2.cvtColor(hsv,cv2.COLOR_HSV2RGB).astype(np.float32)
def rd(f): return cv2.cvtColor(cv2.imread(f),cv2.COLOR_BGR2RGB).astype(np.float32)
def load(d): return sorted(glob.glob(d+'/*.jpg'))
def caption(txt,sub,col):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    f=ImageFont.truetype(FONT,64); f2=ImageFont.truetype(FONT,32)
    d.rectangle([60,60,70,170],fill=col); d.text((92,50),txt,font=f,fill=(255,255,255,255)); d.text((94,128),sub,font=f2,fill=col+(255,))
    return np.asarray(im).astype(np.float32)
def over(frame,cap):
    a=cap[...,3:4]/255; return frame*(1-a)+cap[...,:3]*a
TEST=os.environ.get('TEST')
ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','vfx_demo.mp4'],stdin=subprocess.PIPE)
def out(fr): ff.stdin.write(np.clip(fr,0,255).astype(np.uint8).tobytes())
# ---- 1 lendária entra em campo (dourado)
L=load('f_leg'); bgL=np.min(np.stack([rd(f) for f in L[::12]]),0)
s=2.2; gold=GOLD=None
big=card('GK01',720)
for i in range(240):
    t=i/30; fr=A.copy()
    sc=min(1,0.55+0.45*min(1,max(0,(t-0.7)/0.6))); al=min(1,max(0,(t-0.6)/0.5))
    if al>0:
        im=big.resize((int(big.width*sc),int(big.height*sc)),Image.LANCZOS)
        paste(fr,im,960,500-int(20*np.sin(t*2)),al)
    d=np.clip(rd(L[min(i,len(L)-1)])-bgL,0,255)*1.4
    d=hshift(d,26,12)
    dd=cv2.resize(d,None,fx=s,fy=s,interpolation=cv2.INTER_LINEAR)
    cx,cy=int(dd.shape[1]*0.5),int(dd.shape[0]*0.63); ox,oy=cx-960,cy-770
    crop=dd[oy:oy+H,ox:ox+W]
    fr=screen(fr,crop)
    fl=max(0,1-abs(t-0.75)/0.25)*180   # flash dourado
    fr=screen(fr,np.array([255,200,60],np.float32)*fl/255)
    if t>0.9:
        pass
    fr=over(fr,caption('CARTA LENDÁRIA ENTRA EM CAMPO','Efeito DOURADO — ao entrar na partida',(245,179,1)))
    out(fr)
print('leg ok',flush=True)
# ---- 2 ataque / Atingir por cor
segs=[('f_blue',None,'GOKU BASE — AZUL','Atingir / ataque (cor da forma)',(60,140,255),'GK02'),
('f_fire',27,'GOKU SUPER SAIYAJIN — AMARELO','Atingir / ataque (cor da forma)',(255,214,40),'GK12'),
('f_pur',None,'VEGETA BASE — ROXO','Atingir / ataque (cor da forma)',(176,80,255),'GK24'),
('f_fire',60,'PICCOLO / NAMEK — VERDE (proposta)','Atingir / ataque (cor da forma)',(60,210,90),'GK03'),
('f_fire',0,'ANDROIDE / CELL — VERMELHO (proposta)','Atingir / ataque (cor da forma)',(240,60,60),'GK29'),
('f_fire',165,'MAJIN BUU — ROSA (proposta)','Atingir / ataque (cor da forma)',(255,110,190),'GK22')]
cache={}
for d_,tg,txt,sub,col,cid in segs:
    if d_ not in cache:
        F=load(d_); cache[d_]=(F,np.median(np.stack([rd(f) for f in F[::10]]),0))
    F,bg=cache[d_]
    A1=card(cid,320); T=card('GK19',320); cap=caption(txt,sub,col)
    for i,f in enumerate(F):
        fr=A.copy(); paste(fr,A1,388,500); 
        shake=(6*np.sin(i*1.9) if 118<i<150 else 0)
        paste(fr,T,1572+shake,500)
        d=np.clip(rd(f)-bg,0,255)
        d[300:700,250:530]*=0.30   # fantasma do card de referência
        d[300:700,1470:1680]*=0.3
        a=np.clip(d.max(-1,keepdims=True)/170,0,1)**0.8
        d=d*1.25
        if tg is not None: d=hshift(d,tg,12)
        fr=fr*(1-a)+d+bg*a*0.55
        fr=over(fr,cap); out(fr)
    print(txt,flush=True)
ff.stdin.close(); ff.wait(); print('ok')
