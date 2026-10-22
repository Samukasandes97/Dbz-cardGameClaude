import numpy as np,cv2,glob
from PIL import Image,ImageDraw,ImageFont
W,H=1920,1080
def rd(f): return cv2.cvtColor(cv2.imread(f),cv2.COLOR_BGR2RGB).astype(np.float32)
def hs(d,fn):
    hsv=cv2.cvtColor(np.clip(d,0,255).astype(np.uint8),cv2.COLOR_RGB2HSV); h=hsv[...,0].astype(int); m=hsv[...,1]>40
    hsv[...,0]=np.where(m,fn(h)%180,h).astype(np.uint8); return cv2.cvtColor(hsv,cv2.COLOR_HSV2RGB).astype(np.float32)
src={}
for k,d in (('blue','f_blue'),('fire','f_fire'),('pur','f_pur')):
    F=sorted(glob.glob(d+'/*.jpg')); src[k]=(F,np.median(np.stack([rd(f) for f in F[::10]]),0))
P=[('GOKU BASE','azul','blue',lambda h:np.where(h<35,105,h)),
('GOKU SSJ','azul + amarelo','blue',None),
('VEGETA BASE','roxo','pur',None),
('PICCOLO Makankosappo','roxo + amarelo','pur',lambda h:np.where((h>3)&(h<20),25,h)),
('PICCOLO golpe amarelo','amarelo','fire',lambda h:h+15),
('NAMEK genérico','verde','fire',lambda h:h+48),
('ANDROIDE / FREEZA raio','vermelho','fire',lambda h:h-12),
('CELL','por carta (arte)','fire',None)]
f=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Black.otf',44)
tiles=[]
for n,c,s,fn in P:
    F,bg=src[s]; im=rd(F[88]); d=np.clip(im-bg,0,255)
    if fn: d=hs(d,fn)
    t=np.clip(np.array([18,20,32],np.float32)+d*1.3,0,255)[150:760,200:1300]
    pi=Image.fromarray(t.astype(np.uint8)); dr=ImageDraw.Draw(pi); dr.text((16,10),n,font=f,fill=(255,255,255)); dr.text((16,64),c,font=f,fill=(255,205,60))
    tiles.append(pi)
S=Image.new('RGB',(4*1100//2,2*610//2))
for i,t in enumerate(tiles): S.paste(t.resize((550,305)),((i%4)*550,(i//4)*305))
S.save('presets_cores.png')
