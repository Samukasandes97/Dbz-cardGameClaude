import numpy as np, json
from PIL import Image
from scipy import ndimage as ndi
N=222
def load(i):return np.array(Image.open(f'fr/f_{i+1:03d}.png').convert('RGB'))
stack=np.stack([load(i) for i in range(0,N,2)])
plate=np.percentile(stack,8,axis=0).astype('float32');del stack
def keyed(i):
    a=load(i).astype('float32');e=np.clip(a-plate-6,0,255)
    e[...,1]=np.minimum(e[...,1],e[...,0]*.97);e[...,2]=np.minimum(e[...,2],e[...,1]*.75)
    sat=(e[...,0]-e[...,2])/np.maximum(e[...,0],1);white=(e[...,0]>235)&(e[...,1]>185)
    ok=np.clip((sat-.08)/.2,0,1);white=(e[...,0]>205)&(e[...,1]>150);ok=np.where(white,1,ok)
    ok[205:295,758:818]=np.clip((sat[205:295,758:818]-.3)/.2,0,1)*0.35   # alvo
    ok[190:300,165:235]=np.clip((sat[190:300,165:235]-.38)/.2,0,1)
    e=e*ok[...,None]
    m=e.max(axis=2);m=ndi.gaussian_filter(m,.6)
    al=np.clip((m-26)/110,0,1)**.85
    al=np.maximum(al,np.minimum(ndi.grey_closing(al,size=(9,9)),.85)*(ndi.maximum_filter(al,size=3)>.3))
    lab,n=ndi.label(al>.2)
    if n:
        sz=ndi.sum(al>.2,lab,range(1,n+1));keep=np.isin(lab,[q+1 for q,z in enumerate(sz) if z>=25]);al=al*ndi.binary_dilation(keep,iterations=2)
    col=e/np.maximum(m[...,None],1)*255
    col=np.clip(col*1.0,0,255)
    return np.dstack([col,al*255]).astype('uint8')
def crop(img,cx,cy,w,h,ox=.5,oy=.5):
    x0=int(cx-w*ox);y0=int(cy-h*oy);out=np.zeros((h,w,4),'uint8')
    sx0,sy0=max(0,x0),max(0,y0);sx1,sy1=min(img.shape[1],x0+w),min(img.shape[0],y0+h)
    out[sy0-y0:sy1-y0,sx0-x0:sx1-x0]=img[sy0:sy1,sx0:sx1]
    h_,w_=out.shape[:2];r=34
    ry=np.minimum(np.arange(h_),h_-1-np.arange(h_))/r;rx=np.minimum(np.arange(w_),w_-1-np.arange(w_))/r
    ramp=np.clip(np.minimum(ry[:,None],rx[None,:]),0,1)**1.2
    out[...,3]=(out[...,3]*ramp).astype('uint8');return out
def sheet(frames,cols,name):
    n=len(frames);h,w=frames[0].shape[:2];rows=(n+cols-1)//cols
    S=np.zeros((rows*h,cols*w,4),'uint8')
    for i,f in enumerate(frames):S[(i//cols)*h:(i//cols+1)*h,(i%cols)*w:(i%cols+1)*w]=f
    Image.fromarray(S,'RGBA').save(f'../demo/a/vfx/{name}.webp',quality=86,method=6);return w,h,n,cols
J=json.load(open('../demo/a/vfx/sheets.json'))
fr=[crop(keyed(i),201,247,300,310,.5,.62) for i in range(0,72,2)]
w,h,n,cols=sheet(fr,6,'fire');J['fire']={'fw':w,'fh':h,'n':n,'cols':cols,'ms':66}
fr=[];last=(420,247)
for i in range(36,58,2):
    k=keyed(i);m=k[...,3].copy();m[:,:300]=0;m[:,700:]=0
    if (m>80).sum()>1500:
        ys,xs=np.nonzero(m>80);last=(xs.mean(),ys.mean())
    fr.append(crop(k,last[0]-10,last[1],240,200,.62,.5))
w,h,n,cols=sheet(fr,4,'sphere');J['sphere']={'fw':w,'fh':h,'n':n,'cols':cols,'ms':66}
fr=[crop(keyed(i),787,247,260,260) for i in range(52,72,2)]
w,h,n,cols=sheet(fr,4,'hitf');J['hitf']={'fw':w,'fh':h,'n':n,'cols':cols,'ms':66}
json.dump(J,open('../demo/a/vfx/sheets.json','w'))
S=Image.new('RGB',(1600,830),(35,35,60))
for r,(nm,idx,y) in enumerate([('fire',[2,8,16,26],0),('sphere',[2,5,8,10],320),('hitf',[1,3,5,8],530)]):
    d=J[nm];im=Image.open(f'../demo/a/vfx/{nm}.webp').convert('RGBA')
    for k,i in enumerate(idx):
        c,rr=i%d['cols'],i//d['cols'];fr_=im.crop((c*d['fw'],rr*d['fh'],(c+1)*d['fw'],(rr+1)*d['fh']));S.paste(fr_,(k*380,y),fr_)
S.save('../vfx/sprites_new.png')
