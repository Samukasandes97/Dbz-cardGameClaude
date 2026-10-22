import numpy as np,subprocess,os,re,json,sys
from scipy.io import wavfile
from scipy.signal import stft,find_peaks,medfilt
def load(p):
    r=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout
    return np.frombuffer(r,np.int16).astype(np.float32)/32768
def pitch(x,sr=16000,fr=0.032,hop=0.01):
    n=int(fr*sr);h=int(hop*sr);out=[]
    for i in range(0,len(x)-n,h):
        s=x[i:i+n]; s=s-s.mean(); e=np.sum(s*s)
        if e<1e-4*n: out.append(0);continue
        ac=np.correlate(s,s,'full')[n-1:]; ac/=ac[0]+1e-9
        lo,hi=int(sr/450),int(sr/70); k=np.argmax(ac[lo:hi])+lo
        out.append(sr/k if ac[k]>0.45 else 0)
    return np.array(out)
def feats(x):
    sr=16000; d=len(x)/sr
    env=np.sqrt(np.convolve(x*x,np.ones(320)/320,'same')); envs=np.convolve(env,np.ones(480)/480,'same')
    pk,_=find_peaks(envs,height=envs.max()*0.35,distance=int(0.12*sr),prominence=envs.max()*0.15)
    p=pitch(x); v=p[p>0]
    f,t,Z=stft(x,sr,nperseg=512,noverlap=384); S=np.abs(Z)
    cen=(S*f[:,None]).sum(0)/(S.sum(0)+1e-9)
    slope=0
    if len(v)>5: slope=np.polyfit(np.arange(len(v)),v,1)[0]*100/ max(1,len(v))
    return dict(dur=round(d,2),syl=int(len(pk)),peak=round(float(np.abs(x).max()),2),rms=round(float(np.sqrt((x**2).mean())),3),
      voiced=round(float((p>0).mean()) if len(p) else 0,2),f0=round(float(np.median(v)),0) if len(v) else 0,f0max=round(float(np.percentile(v,95)),0) if len(v) else 0,
      f0slope=round(float(slope),1),cent=round(float(np.median(cen)),0),attack=round(float(np.argmax(envs)/sr/d),2))
if __name__=='__main__':
    res={}
    for era,dr in (('E','aud_in'),('M','aud_mid')):
        for f in sorted(os.listdir(dr)):
            n=int(re.search(r'_(\d+)\.ogg',f).group(1)); res[f'{era}{n}']=feats(load(f'{dr}/{f}'))
    json.dump(res,open('anal/feats.json','w'))
    print(len(res))
