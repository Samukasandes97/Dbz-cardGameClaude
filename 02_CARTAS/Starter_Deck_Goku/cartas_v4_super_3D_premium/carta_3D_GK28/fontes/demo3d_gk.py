import re,json,sys,os
sys.path.insert(0,'../cartas')
import frame
B=os.path.dirname(os.path.abspath(__file__))+'/d3'
A=os.path.dirname(os.path.abspath(__file__))
c=json.load(open(A+'/deck_goku_v4.json'))[27]; c['estagio']='comum'
def parts(est):
    h=frame.card_html(dict(c,estagio=est))
    svg=re.search(r'<svg width.*?</svg>',h,re.S).group(0)
    css=re.search(r'<style>(.*?)</style>',h,re.S).group(1)
    return None,svg,css
w0,s0,css=parts('comum')
svgs={e:parts(e)[1] for e in ['comum','rara','super','lendaria']}
# ids duplicados entre svgs: prefixa por estagio
def pref(e,s):
    s=re.sub(r'id="([^"]+)"',lambda m:f'id="{e}_{m.group(1)}"',s)
    s=re.sub(r'url\(#([^)]+)\)',lambda m:f'url(#{e}_{m.group(1)})',s); return s
svgs={e:pref(e,s) for e,s in svgs.items()}
win_css=re.search(r'\.win\{.*?\}',css).group(0)+re.search(r'\.bd\{.*?\}',css).group(0)+re.search(r'\.art\{.*?\}',css).group(0)
art=c['arte']
ax=re.search(r'left:([\d.]+)px;top:([\d.]+)px;width:([\d.]+)px;height:([\d.]+)px;-webkit',css).groups()
html=f'''<!doctype html><html><head><meta charset="utf-8"><style>
#persp{{filter:brightness(1.1) saturate(1.2)}}
html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:#05060a;font-family:Inter}}
#bgl{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 55%,var(--bg1,#2a2f4a) 0,#0a0c16 55%,#030407 100%)}}
#persp{{position:absolute;left:0;top:0;width:1920px;height:1080px;perspective:1050px;perspective-origin:50% 45%}}
#rig{{position:absolute;left:455px;top:-312px;width:1190px;height:1705px;transform-origin:595px 852px;transform:scale(.58);}}
#tilt{{position:absolute;left:0;top:0;width:1190px;height:1705px;transform-style:preserve-3d;transform-origin:595px 852px}}
.L{{position:absolute;left:0;top:0;width:1190px;height:1705px}}
{win_css}
.win{{left:62px;top:62px}}
.cut{{position:absolute;left:{62+float(ax[0])}px;top:{62+float(ax[1])}px;width:{ax[2]}px;height:{ax[3]}px;transform-origin:50% 40%;filter:drop-shadow(0 50px 40px rgba(0,0,0,.8))}}
.cut img{{width:100%;height:100%;display:block}}
.tp,.bt{{filter:drop-shadow(0 22px 20px rgba(0,0,0,.75))}}
.back{{position:absolute;left:0;top:0;width:1190px;height:1705px;border-radius:38px;background:#0a0b10;box-shadow:0 60px 140px rgba(0,0,0,.8)}}
.fr{{position:absolute;left:0;top:0}}
#sheen{{position:absolute;left:0;top:0;width:1190px;height:1705px;border-radius:38px;mix-blend-mode:color-dodge;pointer-events:none}}
#lab{{position:absolute;left:80px;top:150px;color:#fff}}
#lab .k{{font-size:26px;letter-spacing:6px;color:#9fb0c8;font-weight:700}}
#lab .t{{font-size:70px;font-weight:900;line-height:1;margin-top:10px}}
#lab .s{{font-size:30px;margin-top:16px;color:#cfd8e6;font-weight:500;max-width:470px;line-height:1.35}}
#pips{{position:absolute;left:80px;bottom:110px;display:flex;gap:14px}}
.pip{{width:100px;height:10px;border-radius:5px;background:#2a3044}}
#flash{{position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none}}
#ring{{position:absolute;left:660px;top:240px;width:600px;height:600px;border-radius:50%;border:12px solid #fff;opacity:0;pointer-events:none}}
#spk{{position:absolute;inset:0;pointer-events:none}}
</style></head><body>
<div id="bgl"></div>
<div id="lab"><div class="k" id="lk"></div><div class="t" id="lt"></div><div class="s" id="ls"></div></div>
<div id="pips"><div class="pip"></div><div class="pip"></div><div class="pip"></div><div class="pip"></div></div>
<div id="persp"><div id="rig"><div id="tilt">
 <div class="back" style="transform:translateZ(-70px)"></div>
 <div class="L win" style="transform:translateZ(-40px)"><div class="bd"></div><img class="art" src="{art}"></div>
 <div class="L fr" id="f_comum" style="transform:translateZ(55px)">{svgs['comum']}</div>
 <div class="L fr" id="f_rara" style="transform:translateZ(55px);opacity:0">{svgs['rara']}</div>
 <div class="L fr" id="f_super" style="transform:translateZ(55px);opacity:0">{svgs['super']}</div>
 <div class="L fr" id="f_lendaria" style="transform:translateZ(55px);opacity:0">{svgs['lendaria']}</div>
 <div class="L fr tp" id="t_comum" style="opacity:0;clip-path:inset(0 0 1440px 0)">{svgs['comum']}</div><div class="L fr tp" id="t_rara" style="opacity:0;clip-path:inset(0 0 1440px 0)">{svgs['rara']}</div><div class="L fr tp" id="t_super" style="opacity:0;clip-path:inset(0 0 1440px 0)">{svgs['super']}</div><div class="L fr tp" id="t_lendaria" style="opacity:0;clip-path:inset(0 0 1440px 0)">{svgs['lendaria']}</div>
 <div class="L fr bt" id="b_comum" style="opacity:0;clip-path:inset(1530px 0 0 0)">{svgs['comum']}</div><div class="L fr bt" id="b_rara" style="opacity:0;clip-path:inset(1530px 0 0 0)">{svgs['rara']}</div><div class="L fr bt" id="b_super" style="opacity:0;clip-path:inset(1530px 0 0 0)">{svgs['super']}</div><div class="L fr bt" id="b_lendaria" style="opacity:0;clip-path:inset(1530px 0 0 0)">{svgs['lendaria']}</div>
 <div class="cut" id="cut" style="opacity:0"><img src="cut_gk28.png"></div>
 <div id="sheen" style="transform:translateZ(30px)"></div>
</div></div></div>
<div id="ring"></div><canvas id="spk" width="1920" height="1080"></canvas><div id="flash"></div>
<script>
const ST=[
 {{id:'comum',k:'3 CÓPIAS IGUAIS',t:'COMUM',s:'Moldura base do tipo. A cor segue o tipo da carta (Saiyajin = dourado/laranja).',bg:'#2a2f4a'}},
 {{id:'rara',k:'EVOLUÇÃO DA MOLDURA',t:'RARA',s:'A moldura evolui: borda de prata, gemas nos cantos e reflexo metálico.',bg:'#2a4a5a'}},
 {{id:'super',k:'EVOLUÇÃO DA MOLDURA',t:'CARTA 3D',s:'Moldura holográfica com brilho que acompanha a inclinação da carta.',bg:'#4a2a5a'}},
 {{id:'super',k:'EVOLUÇÃO FINAL',t:'SON GOKU',s:'O Goku salta para fora da moldura e a carta ganha profundidade (estilo Snap).',bg:'#4a2a5a',pop:1}},
 {{id:'lendaria',k:'CARTA LENDÁRIA',t:'LENDÁRIA',s:'Carta única: moldura DOURADA com asas, selo e fita de lendária, palavra-chave ATINGIR. Não é evolução, é outra categoria.',bg:'#5a4310',pop:1}}
];
const DUR=[3.4,3.4,4.2,5.2,8.4], TS=[0,3.4,6.8,11.0,16.2], TOTAL=24.6;
function ease(x){{return x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2}}
const sp=document.getElementById('spk').getContext('2d');
function rnd(n){{let x=Math.sin(n*127.1)*43758.5453;return x-Math.floor(x)}}
function setT(t){{
 let i=0;for(let j=0;j<TS.length;j++) if(t>=TS[j]) i=j;
 const S=ST[i], lt=t-TS[i];
 for(const e of ['comum','rara','super','lendaria']){{const fe=document.getElementById('f_'+e);fe.style.opacity=(e===S.id)?1:0;fe.style.clipPath=(S.pop&&e===S.id)?'inset(264px 0 175px 0)':'none'}}
 document.getElementById('lk').textContent=S.k;document.getElementById('lt').textContent=S.t;document.getElementById('ls').textContent=S.s;
 document.getElementById('bgl').style.setProperty('--bg1',S.bg);
 document.querySelectorAll('.pip').forEach((p,n)=>{{const act=(i===0?0:i===1?1:i===2?2:i===3?2:3);p.style.background=n<=act?(n===3?'#ffd54a':'#7fb4ff'):'#2a3044'}});
 // pop (transicao suave)
 let pop=0; if(S.pop){{pop=ease(Math.min(1,lt/1.2))}}
 const cut=document.getElementById('cut');
 cut.style.opacity=pop;
 cut.style.transform=`translateZ(${{70+pop*300}}px) scale(${{1+pop*0.22}}) translate(${{pop*-10}}px,${{-pop*90}}px)`;
 for(const e of ['comum','rara','super','lendaria']){{const on=(e===S.id)?pop:0;for(const p of ['t_','b_']){{const el=document.getElementById(p+e);el.style.opacity=on;el.style.transform=`translateZ(${{55+on*120}}px)`}}}}
 // inclinacao
 const amp=(i<3?1.25:2.1), ry=Math.sin(t*1.25)*15*amp, rx=Math.cos(t*0.95)*9*amp;
 document.getElementById('tilt').style.transform=`rotateY(${{ry}}deg) rotateX(${{rx}}deg)`;
 // reflexo (sheen)
 const sh=document.getElementById('sheen'); const px=50+ry*2.6, py=50-rx*3;
 let col=i===0?'rgba(255,255,255,.0)':i===1?'rgba(210,230,255,.32)':i===4?'rgba(255,220,110,.40)':'rgba(255,255,255,.16)';
 const rb=(i===2||i===3)?`linear-gradient(${{110+ry*4}}deg,rgba(255,80,120,.0) ${{px-40}}%,rgba(255,200,60,.16) ${{px-25}}%,rgba(80,255,150,.14) ${{px-10}}%,rgba(60,220,255,.18) ${{px+5}}%,rgba(160,100,255,.16) ${{px+20}}%,rgba(255,80,160,.0) ${{px+40}}%)`:'';
 sh.style.background=(rb?rb+',':'')+`radial-gradient(ellipse at ${{px}}% ${{py}}%,${{col}} 0,rgba(0,0,0,0) 55%)`;
 // flash/anel na troca
 const fl=document.getElementById('flash'),rg=document.getElementById('ring');
 let f=0,r=0;
 if(i>0&&lt<0.9){{f=(1-lt/0.9)*(S.id==='lendaria'?0.95:0.7); r=lt/0.9}}
 fl.style.opacity=f; fl.style.background=S.id==='lendaria'?'#ffe9a0':S.id==='super'?'#f0d8ff':'#e6f2ff';
 rg.style.opacity=r>0?(1-r)*.9:0; rg.style.transform=`scale(${{0.3+r*2.4}})`; rg.style.borderColor=S.id==='lendaria'?'#ffd54a':'#bfe0ff';
 // faiscas
 sp.clearRect(0,0,1920,1080);
 if(i>=2){{const n=i===4?46:26;for(let k=0;k<n;k++){{const sd=k*7.31,ph=(t*0.35*(0.6+rnd(sd)*0.9)+rnd(sd+1))%1;const x=960+(rnd(sd+2)-.5)*760+Math.sin(t+k)*18,y=980-ph*900;const a=Math.sin(ph*Math.PI);sp.globalAlpha=a*.85;sp.fillStyle=i===4?'#ffe27a':(k%3?'#a8d8ff':'#ffb3f0');sp.beginPath();sp.arc(x,y,2+rnd(sd+3)*4,0,7);sp.fill()}}}}
}}
window.setT=setT;window.TOTAL=TOTAL;setT(0);
</script></body></html>'''
html=html.replace('</script></body>',open(A+'/../cartas/fx.js').read()+'</script></body>')
open(B+'/demo3d.html','w').write(html)
