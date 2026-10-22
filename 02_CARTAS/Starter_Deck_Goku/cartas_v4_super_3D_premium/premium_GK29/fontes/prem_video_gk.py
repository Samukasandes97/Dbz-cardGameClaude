import cv2,numpy as np,glob,math,subprocess,sys,random
W,H=1190,1705; WX,WY,WW,WH=62,62,1066,1581
G=sorted(glob.glob('prem/g[0-9][0-9][0-9].png')); N=len(G)
FR=cv2.imread('prem/frame_noirid.png',cv2.IMREAD_UNCHANGED).astype(np.float32)/255
IM=cv2.imread('prem/irid_mask.png',cv2.IMREAD_UNCHANGED).astype(np.float32)/255
fa=FR[...,3:4]; ia=IM[...,3:4]
xx,yy=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32))
CWD=360; SC=WW/CWD
KF=[(0,450),(1.4,450),(1.8,320),(3.4,320),(3.9,300),(11.2,300)]
def cxof(t): return float(np.interp(t,[a for a,b in KF],[b for a,b in KF]))
ART_TOP=190-WY
def hsv2rgb(h,s,v):
    z=np.stack([(h%1)*179,np.full_like(h,s*255),np.full_like(h,v*255)],-1).astype(np.uint8)
    return cv2.cvtColor(z,cv2.COLOR_HSV2RGB).astype(np.float32)/255
def art_layer(k):
    x0=int(np.clip(cxof(k/30.0)-CWD/2,0,640-CWD)); g=cv2.imread(G[min(N-1,int(k*25/30))])[:,x0:x0+CWD]
    big=cv2.resize(g,(WW,int(480*SC)),interpolation=cv2.INTER_LANCZOS4)
    bl=cv2.GaussianBlur(big,(0,0),2.0); big=cv2.addWeighted(big,1.6,bl,-0.6,0)
    win=np.zeros((WH,WW,3),np.float32)
    bd=cv2.GaussianBlur(cv2.resize(big,(WW,WH)),(0,0),40).astype(np.float32)*.8
    win[:]=bd
    h=big.shape[0]; a=big.astype(np.float32)
    m=np.ones((h,1,1),np.float32); f=min(70,h//4)
    m[:f,0,0]=np.linspace(0,1,f)
    fb=170; m[-fb:,0,0]=np.minimum(m[-fb:,0,0],np.linspace(1,0,fb)**1.3)
    y0=ART_TOP; y1=min(WH,y0+h)
    win[y0:y1]=win[y0:y1]*(1-m[:y1-y0])+a[:y1-y0]*m[:y1-y0]
    yy_=np.arange(WH,dtype=np.float32)[:,None,None]
    sh=1-0.92*np.clip((yy_-820)/330,0,1)**0.8
    win*=sh
    return win
def card(k,sheen,t,flat_tilt=0):
    out=np.zeros((H,W,3),np.float32); out[:]=(10,11,16)[::-1]
    out=out/255
    win=art_layer(k)[...,::-1]/255  # BGR->RGB
    # folha holografica suave por cima da arte
    hh=((xx+yy)/1500.0+t*0.15)
    holo=hsv2rgb(hh,0.55,1.0)
    reg=np.zeros((H,W,1),np.float32); reg[WY:WY+WH,WX:WX+WW]=1
    wfull=np.zeros((H,W,3),np.float32); wfull[WY:WY+WH,WX:WX+WW]=win
    band=np.exp(-((((xx*0.62+yy*0.38)/(W*0.62+H*0.38))-sheen)/0.07)**2)[...,None]
    wfull=1-(1-wfull)*(1-0.10*holo*reg)
    wfull=1-(1-wfull)*(1-0.30*band*reg*hsv2rgb(((xx+yy)/900.0)+sheen*2,0.35,1.0))
    out=out*(1-reg)+wfull*reg
    # moldura
    F=FR[...,:3][...,::-1]
    out=out*(1-fa)+F*fa
    # iridescencia animada nos aneis
    ir=hsv2rgb(((xx*0.5+yy*0.35)/900.0)+t*0.18,0.85,1.0)
    out=out*(1-ia*0.9)+ir*ia*0.9
    # brilho que varre o metal
    metal=fa*(1-reg)
    sp=hsv2rgb(((xx+yy)/700.0)+sheen*2.5,0.30,1.0)
    out=1-(1-out)*(1-0.62*band*metal*sp)
    out=1-(1-out)*(1-0.22*np.exp(-((((xx*0.62+yy*0.38)/(W*0.62+H*0.38))-(sheen+0.16))/0.025)**2)[...,None]*metal)
    # faiscas
    rnd=random.Random(4); sp_=np.zeros((H,W),np.float32)
    for i in range(46):
        px=rnd.uniform(40,W-40); py=rnd.uniform(40,H-40); ph=rnd.uniform(0,6.28); sz=rnd.uniform(9,26)
        a=max(0,math.sin(t*3.2+ph))**6
        if a<.05: continue
        cv2.line(sp_,(int(px-sz),int(py)),(int(px+sz),int(py)),a,2,cv2.LINE_AA); cv2.line(sp_,(int(px),int(py-sz)),(int(px),int(py+sz)),a,2,cv2.LINE_AA)
        cv2.circle(sp_,(int(px),int(py)),3,a,-1,cv2.LINE_AA)
    sp_=cv2.GaussianBlur(sp_,(0,0),2.2)*2.2+sp_
    out=1-(1-out)*(1-np.clip(sp_,0,1)[...,None]*np.array([.9,.97,1.0],np.float32))
    rgba=np.dstack([np.clip(out,0,1),fa[...,0]*0+ (FR[...,3]>0)*1.0])
    # alfa da carta = silhueta externa (moldura preenchida) -> usar mascara arredondada
    r=np.zeros((H,W),np.uint8); cv2.rectangle(r,(0,0),(W-1,H-1),255,-1)
    rr=np.zeros((H,W),np.float32)
    cv2.rectangle(rr,(38,0),(W-39,H-1),1,-1); cv2.rectangle(rr,(0,38),(W-1,H-39),1,-1)
    for cx,cy in ((38,38),(W-39,38),(38,H-39),(W-39,H-39)): cv2.circle(rr,(cx,cy),38,1,-1,cv2.LINE_AA)
    rgba[...,3]=cv2.GaussianBlur(rr,(0,0),0.8)
    return rgba
def flat_rgb(k,sheen,t):
    c=card(k,sheen,t); return (c[...,:3]*c[...,3:4]+0*(1-c[...,3:4]))
if __name__=='__main__':
    mode=sys.argv[1]
    FPS=30; TOT=int(N*30/25)
    if mode=='flat':
        p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H-1}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','14','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart','GK29_premium_carta.mp4'],stdin=subprocess.PIPE)
        for f in range(TOT):
            t=f/FPS; sheen=((t/2.4)%1.0)*1.5-0.25
            c=card(f,sheen,t); bg=np.zeros((H,W,3),np.float32)
            out=(c[...,:3]*c[...,3:4]+bg*(1-c[...,3:4]))
            p.stdin.write((np.clip(out[:H-1],0,1)*255).astype(np.uint8).tobytes())
        p.stdin.close(); p.wait()
    else:
        CW,CH=1920,1080; ch=980; s=ch/H
        p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{CW}x{CH}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','15','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart','GK29_premium_showcase_FHD.mp4'],stdin=subprocess.PIPE)
        yy2,xx2=np.mgrid[0:CH,0:CW].astype(np.float32)
        f_=1900.0
        for f in range(TOT):
            t=f/FPS; yaw=math.radians(13*math.sin(2*math.pi*t/4.8)); pit=math.radians(4*math.sin(2*math.pi*t/3.2+1))
            sheen=0.5+0.55*math.sin(2*math.pi*t/4.8)*0.9+ (t/9.7)*0.0
            c=card(f,sheen,t)
            # homografia 3D
            pts=np.array([[-W/2,-H/2,0],[W/2,-H/2,0],[W/2,H/2,0],[-W/2,H/2,0]],np.float32)*s
            Ry=np.array([[math.cos(yaw),0,math.sin(yaw)],[0,1,0],[-math.sin(yaw),0,math.cos(yaw)]]); Rx=np.array([[1,0,0],[0,math.cos(pit),-math.sin(pit)],[0,math.sin(pit),math.cos(pit)]])
            P=pts@(Rx@Ry).T; P[:,2]+=f_
            dst=np.stack([CW/2+P[:,0]*f_/P[:,2],CH/2+P[:,1]*f_/P[:,2]],1).astype(np.float32)
            src=np.array([[0,0],[W,0],[W,H],[0,H]],np.float32)
            M=cv2.getPerspectiveTransform(src,dst)
            card8=np.dstack([c[...,:3],c[...,3:4]]).astype(np.float32)
            wr=cv2.warpPerspective(card8,M,(CW,CH),flags=cv2.INTER_AREA if False else cv2.INTER_LINEAR)
            # fundo: gradiente escuro + halo iridescente pulsante
            d=np.sqrt((xx2-CW/2)**2+((yy2-CH/2)*1.25)**2)
            hue=(t*0.07+d/2600.0)
            halo=np.clip(1-d/900.0,0,1)**2.2*(0.55+0.25*math.sin(t*2.6))
            bg=np.zeros((CH,CW,3),np.float32); bg[:]=np.array([14,16,24],np.float32)/255
            bg=bg*(1-0.5*np.clip(d/1300,0,1)[...,None])+hsv2rgb(hue,0.6,1.0)*halo[...,None]*0.55
            # sombra
            a=wr[...,3:4]; out=wr[...,:3]*a+bg*(1-a)
            p.stdin.write((np.clip(out,0,1)*255).astype(np.uint8).tobytes())
        p.stdin.close(); p.wait()
