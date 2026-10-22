import cv2,numpy as np
im=cv2.imread('../cartas/clean/27_art.png'); h,w=im.shape[:2]
hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV); H,S,V=[hsv[...,i].astype(int) for i in range(3)]
k=lambda n:np.ones((n,n),np.uint8)
mask=np.full((h,w),cv2.GC_PR_BGD,np.uint8)
org=(H>=3)&(H<=17)&(S>150)&(V>120); hair=(V<45); skin=(H>=5)&(H<=20)&(S>30)&(S<150)&(V>170)
fgc=cv2.morphologyEx((org|hair|skin).astype(np.uint8),cv2.MORPH_OPEN,k(3))
roi=np.zeros((h,w),np.uint8); cv2.rectangle(roi,(105,8),(430,h-1),1,-1)
mask[roi==0]=cv2.GC_BGD; mask[(fgc>0)&(roi>0)]=cv2.GC_PR_FGD
core=cv2.erode(cv2.morphologyEx(fgc,cv2.MORPH_CLOSE,k(15)),k(9))*roi; mask[core>0]=cv2.GC_FGD
yel=(H>=18)&(H<=35)&(S>120)&(V>180); mask[yel&(core==0)]=cv2.GC_BGD
cv2.grabCut(im,mask,None,np.zeros((1,65)),np.zeros((1,65)),6,cv2.GC_INIT_WITH_MASK)
m=((mask==cv2.GC_FGD)|(mask==cv2.GC_PR_FGD)).astype(np.uint8)
legs=((H>=3)&(H<=17)&(S>150)&(V>110)).astype(np.uint8); legs[:395]=0
legs=cv2.morphologyEx(legs,cv2.MORPH_CLOSE,k(21)); legs=cv2.morphologyEx(legs,cv2.MORPH_OPEN,k(5))
n,lab,st,_=cv2.connectedComponentsWithStats(legs); legs=(lab==1+np.argmax(st[1:,4])).astype(np.uint8)
poly=lambda pts: cv2.fillPoly(np.zeros((h,w),np.uint8),[np.array(pts,np.int32)],1)
m=np.maximum.reduce([m,legs,poly([(188,372),(348,368),(356,432),(184,430)]),poly([(325,280),(422,288),(426,340),(340,350)])])
m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,k(9))
n,lab,st,_=cv2.connectedComponentsWithStats(m); m=(lab==1+np.argmax(st[1:,4])).astype(np.uint8)
cnt,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); m2=np.zeros_like(m); cv2.drawContours(m2,cnt,-1,1,-1)
inner=cv2.erode(m2,k(9))
band=(m2>0)&(inner==0)
bad=(((H>=18)&(H<=35)&(S>110)&(V>170))|((H>=85)&(H<=110)&(V>140)))&band
m2[cv2.dilate(bad.astype(np.uint8),k(3))>0]=0
m2=cv2.morphologyEx(m2,cv2.MORPH_OPEN,k(3))
n,lab,st,_=cv2.connectedComponentsWithStats(m2); m2=(lab==1+np.argmax(st[1:,4])).astype(np.uint8)
a=cv2.GaussianBlur(m2.astype(np.float32)*255,(0,0),1.0)
yy=np.arange(h)[:,None]; a=a*np.clip((0.82*h-yy)/(0.10*h),0,1)
cv2.imwrite('d3/cut_gk28.png',np.dstack([im,np.clip(a,0,255).astype(np.uint8)]))
prev=im.copy(); prev[a<128]=(40,200,40); cv2.imwrite('d3/cut_prev.jpg',prev)
