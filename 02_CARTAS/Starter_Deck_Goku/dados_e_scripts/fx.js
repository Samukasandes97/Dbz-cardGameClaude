(function(){
const bg=document.getElementById('bgl');
const mk=(css)=>{const d=document.createElement('div');d.style.cssText='position:absolute;pointer-events:none;'+css;return d};
const halo=mk('left:0;top:0;width:1920px;height:1080px;mix-blend-mode:screen');bg.after(halo);
const rays=mk('left:1050px;top:540px;width:2600px;height:2600px;margin:-1300px 0 0 -1300px;mix-blend-mode:screen;-webkit-mask-image:radial-gradient(circle,#000 0,rgba(0,0,0,.6) 30%,transparent 62%)');bg.after(rays);
const rays2=mk('left:1050px;top:540px;width:2600px;height:2600px;margin:-1300px 0 0 -1300px;mix-blend-mode:screen;-webkit-mask-image:radial-gradient(circle,#000 0,rgba(0,0,0,.5) 35%,transparent 64%)');bg.after(rays2);
const tilt=document.getElementById('tilt');
const sweep=mk('left:0;top:0;width:1190px;height:1705px;border-radius:38px;overflow:hidden;mix-blend-mode:screen;transform:translateZ(62px)');
const sw=mk('top:-300px;left:0;width:300px;height:2400px;background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.85),rgba(255,255,255,0))');sweep.appendChild(sw);tilt.appendChild(sweep);
const cv=document.createElement('canvas');cv.width=1920;cv.height=1080;cv.style.cssText='position:absolute;left:0;top:0;pointer-events:none;mix-blend-mode:screen';document.body.appendChild(cv);const cx=cv.getContext('2d');
const back=document.querySelector('.back'),cut=document.getElementById('cut');
function R(n){let x=Math.sin(n*91.7)*43758.5453;return x-Math.floor(x)}
function hsl2rgb(h){const f=n=>{const k=(n+h/30)%12;return Math.round(255*(.5-.5*Math.max(-1,Math.min(k-3,9-k,1))))};return [f(0),f(8),f(4)]}
function col(id,t){return id==='comum'?[255,160,50]:id==='rara'?[170,215,255]:id==='super'?hsl2rgb((t*80)%360):[255,205,60]}
const C=(c,a)=>`rgba(${c[0]},${c[1]},${c[2]},${a})`;
window.fx=function(t){
 let i=0;for(let j=0;j<TS.length;j++) if(t>=TS[j]) i=j; const S=ST[i], lt=t-TS[i]; const c=col(S.id,t); const pul=Math.sin(t*4.2);
 const boost=(i===0?0.55:i===1?0.8:1.0)*(S.pop?1.25:1);
 halo.style.background=`radial-gradient(ellipse 760px 900px at 1050px 540px,${C(c,.55*boost)} 0,${C(c,.18*boost)} 40%,rgba(0,0,0,0) 70%)`;halo.style.opacity=.7+.3*pul;
 rays.style.background=`repeating-conic-gradient(from ${t*10}deg at 50% 50%,${C(c,0)} 0deg,${C(c,.22)} 5deg,${C(c,0)} 10deg)`;rays.style.opacity=i===0?.25:i===1?.45:.8;
 const g1=14+9*pul,g2=44+14*pul;
 for(const e of ['comum','rara','super','lendaria']){const on=e===S.id;
  for(const p of ['f_','t_','b_']){const el=document.getElementById(p+e);
   el.style.filter=(p==='f_'?'':'drop-shadow(0 22px 20px rgba(0,0,0,.75)) ')+`drop-shadow(0 0 ${g1}px ${C(c,.95)}) drop-shadow(0 0 ${g2}px ${C(c,.6)})`}}
 back.style.boxShadow=`0 0 ${110+50*pul}px ${C(c,.75*boost)},0 0 ${240}px ${C(c,.35*boost)},0 60px 140px rgba(0,0,0,.8)`;
 const popOn=S.pop?1:0; cut.style.filter=`drop-shadow(0 50px 40px rgba(0,0,0,.8)) drop-shadow(0 0 ${popOn*(18+8*pul)}px ${C(c,.95)}) drop-shadow(0 0 ${popOn*46}px ${C(c,.55)})`;
 const x=(((t*0.42)%1)*2300)-500; sw.style.transform=`translateX(${x}px) rotate(18deg)`; sweep.style.opacity=i===0?.35:.9;
 // canvas: brilhos, anel de choque, raios e relampagos
 cx.clearRect(0,0,1920,1080);
 const n=i===0?18:i===1?34:60;
 for(let k=0;k<n;k++){const sd=k*5.17,ph=(t*0.28*(0.5+R(sd)*1.0)+R(sd+1))%1;const px=1050+(R(sd+2)-.5)*980+Math.sin(t*1.3+k)*22,py=1010-ph*960;const a=Math.sin(ph*Math.PI);const r=2.5+R(sd+3)*5;
  const cc=(k%4===0)?[255,255,255]:c;cx.globalAlpha=a*.95;cx.shadowColor=C(cc,1);cx.shadowBlur=22;cx.fillStyle=C(cc,1);cx.beginPath();cx.arc(px,py,r,0,7);cx.fill();
  if(k%5===0){cx.shadowBlur=0;cx.globalAlpha=a*.8;cx.strokeStyle=C([255,255,255],1);cx.lineWidth=1.6;cx.beginPath();cx.moveTo(px-r*3,py);cx.lineTo(px+r*3,py);cx.moveTo(px,py-r*3);cx.lineTo(px,py+r*3);cx.stroke()}}
 cx.shadowBlur=0;cx.globalAlpha=1;
 if(i>0&&lt<1.1){const u=lt/1.1;
  cx.strokeStyle=C([255,255,255],1-u);cx.lineWidth=10*(1-u)+2;cx.shadowColor=C(c,1);cx.shadowBlur=30;cx.beginPath();cx.arc(1050,540,80+u*980,0,7);cx.stroke();
  cx.lineWidth=4;for(let k=0;k<36;k++){const a=k/36*6.2832+R(k)*.2;const r0=120+u*380,r1=r0+90+R(k+9)*320*(1-u);cx.globalAlpha=1-u;cx.beginPath();cx.moveTo(1050+Math.cos(a)*r0,540+Math.sin(a)*r0);cx.lineTo(1050+Math.cos(a)*r1,540+Math.sin(a)*r1);cx.stroke()}
  cx.globalAlpha=1}
 if((S.id==='super'||S.id==='lendaria')&&lt<0.9&&i>1&&S.pop!==1){const fl=Math.floor(lt*24);
  for(let b=0;b<6;b++){let x0=1050,y0=540;const a=R(b*3.1+fl)*6.28;cx.strokeStyle=C([255,255,255],.95);cx.shadowColor=C(c,1);cx.shadowBlur=26;cx.lineWidth=3.5;cx.beginPath();cx.moveTo(x0,y0);
   for(let s=1;s<=9;s++){const d=s*95;x0=1050+Math.cos(a)*d+(R(b*7+s+fl*3)-.5)*70;y0=540+Math.sin(a)*d+(R(b*5+s+fl*2)-.5)*70;cx.lineTo(x0,y0)}cx.stroke()}
  cx.shadowBlur=0}

 const rig=document.getElementById('rig');
 if(S.id==='lendaria'){
  const z=Math.min(1,lt/3.0); const ez=z*z*(3-2*z);
  rig.style.transform=`scale(${.58*(1+.09*ez)})`;
  rays2.style.background=`repeating-conic-gradient(from ${-t*16}deg at 50% 50%,rgba(255,235,150,0) 0deg,rgba(255,235,150,.28) 3.5deg,rgba(255,235,150,0) 7deg)`;rays2.style.opacity=.9;
  rays.style.opacity=1; sw.style.transform=`translateX(${(((t*0.9)%1)*2300)-500}px) rotate(18deg)`;
  // chuva de ouro
  for(let k=0;k<90;k++){const sd=k*3.3,ph=(t*0.22*(0.6+R(sd)*0.9)+R(sd+1))%1;const px=R(sd+2)*1920,py=-40+ph*1160;cx.save();cx.translate(px,py);cx.rotate(t*3*(R(sd+4)-.5)*4+k);cx.globalAlpha=.9;cx.shadowColor='rgba(255,215,80,1)';cx.shadowBlur=14;cx.fillStyle=k%3?'#ffd54a':'#fff4b0';cx.fillRect(-4,-7,8,14*(.5+R(sd+5)));cx.restore()}
  // lens flare no revelar
  if(lt<2.4){const u=lt/2.4,a=Math.sin(Math.min(1,u*1.4)*Math.PI);
   const gr=cx.createLinearGradient(0,540,1920,540);gr.addColorStop(0,'rgba(255,220,120,0)');gr.addColorStop(.5,`rgba(255,248,210,${.95*a})`);gr.addColorStop(1,'rgba(255,220,120,0)');cx.fillStyle=gr;cx.fillRect(0,540-5-14*a,1920,10+28*a);
   for(let k=0;k<5;k++){const fx_=1050+(k-2)*210*(1+u*.6),r=26+k*16;const rg=cx.createRadialGradient(fx_,540,0,fx_,540,r);rg.addColorStop(0,`rgba(255,240,170,${.55*a})`);rg.addColorStop(1,'rgba(255,200,80,0)');cx.fillStyle=rg;cx.beginPath();cx.arc(fx_,540,r,0,7);cx.fill()}}
  // pulso dourado cheio na entrada
  if(lt<0.6){cx.fillStyle=`rgba(255,230,150,${.55*(1-lt/.6)})`;cx.fillRect(0,0,1920,1080)}
 } else { rig.style.transform='scale(.58)'; rays2.style.opacity=0 }
};
const _s=window.setT; window.setT=function(t){_s(t);window.fx(t)};
})();
