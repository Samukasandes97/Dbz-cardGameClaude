import sys,json,numpy as np
sys.path.insert(0,'anal')
from feat import load
from scipy.signal import stft
from PIL import Image,ImageDraw,ImageFont
import matplotlib; matplotlib.use('Agg'); import matplotlib.cm as cm
F=json.load(open('anal/feats.json'))
era=sys.argv[1]; out=sys.argv[4]
L=[int(v) for v in sys.argv[2].split(',')] if ',' in sys.argv[2] else None
a,b=(0,0) if L else (int(sys.argv[2]),int(sys.argv[3]))
dr={'E':'aud_in','M':'aud_mid','T':'aud_teen','N':'aud_end'}[era]
name={'E':'Goku (Z - Early)','M':'Goku (Z - Mid)','T':'Goku (Teen)','N':'Goku (Z - End)'}[era]
ids=L if L else [n for n in range(a,b+1) if f'{era}{n}' in F]
TW,TH=320,172; cols=6; rows=(len(ids)+cols-1)//cols
S=Image.new('RGB',(cols*TW,rows*TH),(12,12,18)); dr_=ImageDraw.Draw(S); ft=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf',13)
for i,n in enumerate(ids):
    x=load(f'{dr}/{name}_{n}.ogg'); f,t,Z=stft(x,16000,nperseg=512,noverlap=448); m=np.abs(Z)[:160]
    m=np.log1p(m*60); m/=m.max(); img=(cm.magma(m[::-1])[...,:3]*255).astype(np.uint8)
    w=max(10,int((TW-8)*min(1,len(x)/16000/3.0))); im=Image.fromarray(img).resize((w,TH-34))
    X=(i%cols)*TW+4; Y=(i//cols)*TH
    S.paste(im,(X,Y+30)); q=F[f'{era}{n}']
    dr_.text((X,Y+2),f"{n}  {q['dur']}s syl{q['syl']} f0 {int(q['f0'])}→{int(q['f0max'])} v{q['voiced']}",font=ft,fill=(255,220,90))
S.save(out)
