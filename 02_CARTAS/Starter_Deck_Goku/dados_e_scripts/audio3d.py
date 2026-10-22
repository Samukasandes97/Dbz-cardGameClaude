import numpy as np,subprocess,wave,os
sr=44100; T=24.6; N=int(T*sr)
U='/root/.claude/uploads/84f3faec-af92-5d88-b151-bbf1e79ccb25/'
L=np.zeros(N,np.float32); Rr=np.zeros(N,np.float32)
rng=np.random.default_rng(7)
def put(x,t,g=1.0,pan=0.0):
    i=int(t*sr); 
    if i<0: x=x[-i:]; i=0
    j=min(N,i+len(x)); 
    if j<=i: return
    x=x[:j-i]*g
    L[i:j]+=x*(1-max(pan,0)); Rr[i:j]+=x*(1+min(pan,0))
def env(n,a,r,curve=2.0):
    t=np.arange(n)/sr; e=np.minimum(t/max(a,1e-4),1)*np.exp(-t*r); return e
def bell(f,dur=1.8,g=.5):
    n=int(dur*sr); t=np.arange(n)/sr
    x=(np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*f*2.76*t)*np.exp(-t*3)+.35*np.sin(2*np.pi*f*5.4*t)*np.exp(-t*6)+.25*np.sin(2*np.pi*f*1.5*t)) 
    return (x*env(n,.002,2.6)*g).astype(np.float32)
def noise(dur): return rng.standard_normal(int(dur*sr)).astype(np.float32)
def lp(x,fc):
    a=np.exp(-2*np.pi*fc/sr); y=np.zeros_like(x); s=0
    # vetorizado por blocos simples (filtro 1-polo)
    from scipy.signal import lfilter
    return lfilter([1-a],[1,-a],x).astype(np.float32)
def hp(x,fc): return (x-lp(x,fc)).astype(np.float32)
def riser(dur,f0=300,f1=2400,g=.5):
    n=int(dur*sr); t=np.arange(n)/sr; ph=2*np.pi*np.cumsum(f0*(f1/f0)**(t/dur))/sr
    x=np.sin(ph)*.6+np.sin(ph*1.5)*.25; nz=hp(noise(dur),1500)*(t/dur)**2*.8
    e=(t/dur)**1.8
    return ((x+nz)*e*g).astype(np.float32)
def boom(dur=2.4,f0=90,g=.9):
    n=int(dur*sr); t=np.arange(n)/sr; f=f0*np.exp(-t*2.0)+32
    ph=2*np.pi*np.cumsum(f)/sr; x=np.sin(ph)*np.exp(-t*1.5)+lp(noise(dur),400)*np.exp(-t*4)*.8
    return (x*g).astype(np.float32)
def swell_noise(dur,g=.4):
    n=int(dur*sr); t=np.arange(n)/sr; x=hp(noise(dur),3000)*np.sin(np.pi*np.minimum(t/dur,1)*.5+0)**2*np.exp(-np.maximum(t-dur*.35,0)*1.6)
    return (x*g).astype(np.float32)
def pad(freqs,dur,g=.12):
    n=int(dur*sr); t=np.arange(n)/sr; x=0
    for f in freqs:
        for d in (-3,0,3):
            ff=f*(2**(d/1200)); x=x+np.sin(2*np.pi*ff*t+rng.uniform(0,6))*(.7+.3*np.sin(2*np.pi*(.3+rng.uniform(0,.3))*t))
    e=np.minimum(t/(dur*.35),1)**2*np.exp(-np.maximum(t-dur*.6,0)*1.1)
    return (x/len(freqs)/3*e*g).astype(np.float32)
def sfx(path,start,dur,fade=.1,g=1.0):
    r=subprocess.run(['ffmpeg','-v','error','-ss',str(start),'-t',str(dur),'-i',path,'-f','f32le','-ac','1','-ar',str(sr),'-'],capture_output=True)
    x=np.frombuffer(r.stdout,np.float32).copy(); n=len(x); f=int(fade*sr); 
    if n>2*f: x[:f]*=np.linspace(0,1,f); x[-f:]*=np.linspace(1,0,f)
    return x*g
# --- RARA (3.4)
put(riser(.75,500,3000,.35),3.4-.75)
for k,f in enumerate((1046.5,1318.5,1568,2093)): put(bell(f,1.6,.32),3.4+k*.085,pan=(k-1.5)*.35)
put(swell_noise(1.2,.18),3.4)
# --- SUPER RARA (6.8)
put(riser(.95,400,3800,.45),6.8-.95)
put(boom(1.4,110,.45),6.8)
for k,f in enumerate((784,988,1175,1568,1976,2349,3136)): put(bell(f,2.0,.28),6.8+k*.07,pan=np.sin(k)*.6)
put(swell_noise(1.6,.28),6.8)
# --- 3D POP (11.0)
put(sfx(U+'b32118bf-kame_charge.wav',3.6,2.6,.25,.5),8.4)
put(riser(.9,300,4200,.4),11.0-.9)
put(sfx(U+'f788d751-beamhead.wav',0,3.2,.08,.55),11.0)
put(boom(2.0,100,.8),11.0)
for k,f in enumerate((880,1318,1760,2637)): put(bell(f,1.8,.25),11.1+k*.1,pan=(k-1.5)*.4)
# --- LENDARIA (16.2)
put(sfx(U+'b32118bf-kame_charge.wav',0.6,3.6,.2,.6),12.6)
put(riser(1.6,250,5200,.55),16.2-1.6)
put(boom(3.4,85,1.0),16.2)
put(swell_noise(3.2,.45),16.2)
A=[220,330,440,554.4,659.3]
put(pad(A,6.5,.5),16.2)
put(pad([f*2 for f in A[:3]],6.0,.3),16.4)
for k,f in enumerate((1318.5,1568,1760,2093,2637,3136,3520)): put(bell(f,2.6,.3),16.25+k*.11,pan=np.sin(k*1.7)*.7)
ts=np.sort(rng.uniform(17.0,23.2,34))
for k,t0 in enumerate(ts): put(bell(float(rng.choice([2093,2349,2637,3136,3520,4186])),1.2,.16),float(t0),pan=float(rng.uniform(-.8,.8)))
put(bell(880,4.5,.4),19.2); put(bell(1760,4.5,.3),19.2); put(swell_noise(1.8,.3),19.0)
# --- reverb leve (IR sintetica)
def reverb(x,wet=.28,rt=1.8):
    n=int(rt*sr); t=np.arange(n)/sr; ir=(rng.standard_normal(n)*np.exp(-t*3.4)).astype(np.float32); ir[0]=0
    from scipy.signal import fftconvolve
    y=fftconvolve(x,ir)[:len(x)]; y/=np.abs(y).max()+1e-9; return (x*(1-wet*.5)+y*wet*np.abs(x).max()).astype(np.float32)
L=reverb(L); Rr=reverb(Rr)
st=np.stack([L,Rr],1); st/=np.abs(st).max()+1e-9; st*=0.9
pcm=(st*32767).astype(np.int16)
with wave.open('evolucao_som.wav','wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
print('wav ok')
