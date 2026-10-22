import cv2,numpy as np
im=cv2.imread('clean/00_art.png'); h,w=im.shape[:2]
hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV); H,S,V=[hsv[...,i].astype(int) for i in range(3)]
dark=V<60; org=(H>3)&(H<18)&(S>170)&(V>110); blue=(H>100)&(H<130)&(S>150)&(V>40)
skin=(H>=5)&(H<=20)&(S>35)&(S<150)&(V>190)
seed=(dark|org|blue); seed[int(h*.66):]=False
k=lambda n:np.ones((n,n),np.uint8)
seedc=cv2.morphologyEx(seed.astype(np.uint8),cv2.MORPH_CLOSE,k(15)); near=cv2.dilate(seedc,k(41))>0
m=((seedc>0)|(skin&near)).astype(np.uint8)*255; m[int(h*.66):]=0
m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,k(13)); m=cv2.morphologyEx(m,cv2.MORPH_OPEN,k(5))
n,lab,st,_=cv2.connectedComponentsWithStats(m); i=1+np.argmax(st[1:,4])
keep=((lab==i)*255).astype(np.uint8)
cnt,_=cv2.findContours(keep,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); keep=np.zeros_like(m); cv2.drawContours(keep,cnt,-1,255,-1)
a=cv2.GaussianBlur(keep,(0,0),1.5); yy=np.arange(h)[:,None]; a=(a*np.clip((h*.66-yy)/(h*.08),0,1)).astype(np.uint8)
cv2.imwrite('cut_goku.png',np.dstack([im,a]))
