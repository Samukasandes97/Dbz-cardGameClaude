import numpy as np, json, os, sys
from PIL import Image, ImageSequence
R='/tmp/claude-0/-home-claude/84f3faec-af92-5d88-b151-bbf1e79ccb25/scratchpad/'
S=R+'MESTRE/DBZ_CardGame/01_HEROIS/_COMUM/VFX_referencias_dele/novos_21out/'
O=R+'demo/a/vfx/'; os.makedirs(O,exist_ok=True)
M={}
def frames(fn,step=1,crop=None,size=None):
    im=Image.open(S+fn); out=[]; dur=[]
    n=getattr(im,'n_frames',1)
    for i in range(0,n,step):
        im.seek(i); f=im.convert('RGBA')
        if crop: f=f.crop(crop)
        if size: f=f.resize(size,Image.LANCZOS)
        out.append(f); dur.append(im.info.get('duration',40))
    return out,(sum(dur)/len(dur))*step
def smooth(x,a,b): t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
def luma_key(f,lo,hi,boost=1.0):
    a=np.asarray(f).astype(np.float32); rgb=a[...,:3]; m=rgb.max(axis=2)
    al=smooth(m,lo,hi)*(a[...,3]/255.0)
    # remove bg contribution a little & boost
    out=np.dstack([np.clip(rgb*boost,0,255),al*255]).astype(np.uint8)
    return Image.fromarray(out,'RGBA')
def color_key(f,bg,tol,soft):
    a=np.asarray(f).astype(np.float32); d=np.sqrt(((a[...,:3]-np.array(bg))**2).sum(axis=2))
    al=smooth(d,tol,tol+soft)
    out=np.dstack([a[...,:3],al*255]).astype(np.uint8); return Image.fromarray(out,'RGBA')
def sheet(name,fr,cols,ms,q=82):
    n=len(fr); w,h=fr[0].size; rows=(n+cols-1)//cols
    sh=Image.new('RGBA',(w*cols,h*rows),(0,0,0,0))
    for i,f in enumerate(fr): sh.paste(f,((i%cols)*w,(i//cols)*h))
    sh.save(O+name+'.webp','WEBP',quality=q,method=6,alpha_quality=90)
    M[name]=dict(fw=w,fh=h,n=n,cols=cols,ms=round(ms))
    print(name,sh.size,n,round(os.path.getsize(O+name+'.webp')/1024),'KB')
# 12 lendária (cian, preto): 17 frames
fr,ms=frames('12_image.gif',1,size=(640,576)); fr=[luma_key(f,14,60) for f in fr]; sheet('leg',fr,5,ms)
# 08 raio forte
fr,ms=frames('08_image.gif',3,size=(420,315)); fr=[luma_key(f,55,120) for f in fr]; sheet('bolt',fr,7,ms)
# 14 raios radiais (tela cheia, sem chave)
fr,ms=frames('14_image.gif',1); sheet('rays',fr,6,ms,78)
# 06 estrela azul
fr,ms=frames('06_image.gif',3,size=(320,256)); fr=[luma_key(f,55,120) for f in fr]; sheet('star',fr,6,ms)
# 07 impacto amarelo
fr,ms=frames('07_image.gif',3,size=(256,256)); fr=[luma_key(f,18,70) for f in fr]; sheet('hity',fr,6,ms)
# 02 splat branco
fr,ms=frames('02_image.gif',1,crop=(0,0,460,510),size=(276,306)); fr=[luma_key(f,90,150) for f in fr]; sheet('splat',fr,5,ms)
# 05 swoosh dourado
fr,ms=frames('05_image.gif',1,size=(200,200)); fr=[luma_key(f,60,130) for f in fr]; sheet('swoosh',fr,6,ms)
# 09 faiscas
fr,ms=frames('09_image.gif',1,size=(273,261)); fr=[luma_key(f,10,50) for f in fr]; sheet('spark',fr,5,ms)
# 10 explosão (alfa nativo)
fr,ms=frames('10_image.gif',1,size=(360,298)); sheet('boomc',fr,4,ms)
# 13 poeira com anel (chave de cor do fundo)
fr,ms=frames('13_image.gif',2,size=(480,360)); fr=[color_key(f,(80,77,68),14,22) for f in fr]; sheet('dust',fr,5,ms)
# 04 fumaça
fr,ms=frames('04_image.gif',2,size=(358,354)); fr=[color_key(f,(104,104,105),10,20) for f in fr]; sheet('smoke',fr,6,ms)
# 01 cúpula do protetor (estática -> recorte)
im=Image.open(S+'01_image.webp').convert('RGBA').crop((0,0,500,425)); a=np.asarray(im).astype(np.float32)
m=a[...,:3].max(axis=2); blue=(a[...,2]-np.maximum(a[...,0],a[...,1]))
al=smooth(m,70,140)*smooth(blue,10,50)
al[395:,370:]=0
o=np.dstack([a[...,:3],al*255]).astype(np.uint8); Image.fromarray(o,'RGBA').save(O+'dome.webp','WEBP',quality=88,method=6,alpha_quality=95)
M['dome']=dict(w=500,h=425)
# 15 brilho prismático (flare), 16 versus
im=Image.open(S+'15_image.jpg').convert('RGBA'); a=np.asarray(im).astype(np.float32); m=a[...,:3].max(axis=2)
bgm=np.median(a[...,:3].reshape(-1,3),axis=0); d=np.abs(a[...,:3]-bgm).sum(axis=2)
al=smooth(d,40,140); o=np.dstack([a[...,:3],al*255]).astype(np.uint8); Image.fromarray(o,'RGBA').save(O+'flare.webp','WEBP',quality=85,method=6,alpha_quality=90)
Image.open(S+'16_image.jpg').convert('RGB').save(O+'versus.webp','WEBP',quality=90,method=6)
# 11 mãos (7 painéis)
im=Image.open(S+'11_image.png').convert('RGB')
P={'goku':(0,0,512,394),'vegeta':(512,0,1024,394),'ssj':(1024,0,1536,394),'piccolo':(0,394,512,762),'freeza':(512,394,1024,762),'gohan':(1024,394,1536,762),'cell':(0,768,1536,1024)}
for k,b in P.items(): im.crop(b).save(O+'mao_'+k+'.webp','WEBP',quality=88,method=6)
json.dump(M,open(O+'sheets.json','w'))
