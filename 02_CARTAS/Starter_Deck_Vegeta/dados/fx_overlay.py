import cv2,numpy as np,random,sys
def bolts(art,region,color,seed,n=14):
    random.seed(seed); h,w=art.shape[:2]; x0,y0,x1,y1=region
    L=np.zeros((h,w,3),np.float32)
    for _ in range(n):
        x=random.randint(x0,x1); y=random.randint(y0,y1); pts=[(x,y)]
        ang=random.uniform(-2.6,-0.5)
        for k in range(random.randint(6,10)):
            ang+=random.uniform(-1.1,1.1); st=random.randint(18,42)
            x=int(np.clip(x+st*np.cos(ang),0,w-1)); y=int(np.clip(y+st*np.sin(ang),0,h-1)); pts.append((x,y))
        cv2.polylines(L,[np.array(pts)],False,color,6,cv2.LINE_AA)
        cv2.polylines(L,[np.array(pts)],False,(1,1,1),1,cv2.LINE_AA)
    g=cv2.GaussianBlur(L,(0,0),9)*1.6+cv2.GaussianBlur(L,(0,0),3)
    S=np.zeros((h,w),np.float32)
    for _ in range(14):
        cv2.circle(S,(random.randint(x0,x1),random.randint(y0,y1)),random.randint(1,3),1,-1)
    g+=cv2.GaussianBlur(S,(0,0),2)[...,None]*np.array(color,np.float32)*2.5
    yy,xx=np.mgrid[0:h,0:w]; cx=(x0+x1)/2; cy=(y0+y1)/2; r=max(x1-x0,y1-y0)*.75
    P=np.exp(-(((xx-cx)**2+(yy-cy)**2)/(2*(r*.55)**2)))[...,None]*np.array(color,np.float32)*.85
    g=g+P
    a=art.astype(np.float32)/255
    out=1-(1-a)*(1-np.clip(L+g,0,1))
    return (out*255).astype(np.uint8)
if __name__=='__main__':
    for i,reg,col,seed in ((25,(0,420,190,650),(1.0,.85,.45),3),(19,(0,430,130,660),(1.0,.9,.5),5)):
        p=f'clean/{i:02d}_art.png'; a=cv2.imread(p)
        if i==25: a=cv2.imread('clean/25_art.png')
        cv2.imwrite(f'clean/{i:02d}_art_fx.png',bolts(a,reg,col[::-1] if False else col,seed))
