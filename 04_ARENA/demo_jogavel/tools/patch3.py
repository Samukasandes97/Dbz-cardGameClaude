import re
R='/tmp/claude-0/-home-claude/84f3faec-af92-5d88-b151-bbf1e79ccb25/scratchpad/'
s=open(R+'demo/game2.src.html').read()
T=lambda f:open(R+'tools/'+f).read()
def rep(old,new,cnt=1):
    global s
    assert old in s,('NAO ACHOU: '+old[:80])
    s=s.replace(old,new,cnt)
# CSS unidades
s,n=re.subn(r'/\* unidades \*/.*?\.u \.zz\{[^\n]*\n',lambda m:T('css_new.txt'),s,count=1,flags=re.S);assert n==1
s,n=re.subn(r'@keyframes surge\{[^\n]*\n','',s,count=1);assert n==1
rep('@media (prefers-reduced-motion',T('kf_new.txt')+'@media (prefers-reduced-motion')
rep('#piso{position:absolute;left:286px;top:114px;width:850px;height:438px;','#piso{position:absolute;left:286px;top:100px;width:866px;height:392px;')
rep('left:306px;top:316px;width:810px;height:18px','left:300px;top:288px;width:846px;height:18px')
rep('left:288px;top:312px;width:16px;height:26px','left:282px;top:284px;width:16px;height:26px')
rep('left:1118px;top:312px;width:16px;height:26px','left:1146px;top:284px;width:16px;height:26px')
rep('<div id="stands"></div><div id="piso"></div>','<div id="stands"></div><div id="flare"></div><div id="piso"></div>')
rep(' <canvas id="fx" width="1280" height="720"></canvas>',' <div id="vfx"></div>\n <canvas id="fx" width="1280" height="720"></canvas>')
rep(' <div id="coin">',' <div id="vs"></div>\n <div id="coin">')
# motor
rep("E('beam',{from:'h'+side,to:'h'+opp(side),col:HERO[p.key].col,big:1});\n dmgHero(opp(side),10);if(p.key==='vegeta')healHero(side,10)}",
    "const be={t:'beam',from:'h'+side,to:'h'+opp(side),col:HERO[p.key].col,big:1,k:'cb',key:p.key};G.ev.push(be);\n dmgHero(opp(side),10);be.kill=!!G.over&&G.over.win===side;if(p.key==='vegeta')healHero(side,10)}")
rep("E('beam',{from:'h'+side,to:'u'+id,col:'#a35cff'})","E('beam',{from:'h'+side,to:'u'+id,col:'#a35cff',k:'oz'})")
rep("if(tgt.hero){E('beam',{from:'h'+side,to:'h'+opp(side),col:HERO[p.key].col});dmgHero(opp(side),d)}",
    "if(tgt.hero){E('beam',{from:'h'+side,to:'h'+opp(side),col:HERO[p.key].col,k:'ab',key:p.key,tf:p.hero.tf});dmgHero(opp(side),d)}")
rep("E('beam',{from:'h'+side,to:'u'+u.uid,col:HERO[p.key].col});dmgUnit","E('beam',{from:'h'+side,to:'u'+u.uid,col:HERO[p.key].col,k:'ab',key:p.key,tf:p.hero.tf});dmgUnit")
rep("E('beam',{from:'u'+u.uid,to:'u'+t.uid,col:'#ffd45a'});","E('beam',{from:'u'+u.uid,to:'u'+t.uid,col:'#ffd45a',k:'at',ac:auraCol(u)});")
rep("u.hp-=n;E('hit',{uid:u.uid,n});","u.hp-=n;E('hit',{uid:u.uid,n,hpb:u.hp+n});")
# VFX engine
rep('/* ================= INTERFACE ================= */',T('vfx_js.txt')+'/* ================= INTERFACE ================= */')
# aura crescente
old=s[s.index("  const au=$('#au'+side);const ak="):]
old=old[:old.index('\n')]
new=r'''  const au=$('#au'+side);const em=p.energyMax,tier=hp.tf?4:em>=10?3:em>=7?2:em>=4?1:0;const AUS=['aura_branca_media','aura_branca_forte','aura_amarela_media','aura_amarela_forte','aura_amarela_maxima'];const ak=tier+'|'+p.key;
  if(au._k!==ak){au._k=ak;au.src='a/ui/'+AUS[tier]+'.webp';au.style.filter=hp.tf?`hue-rotate(${H.auraHue}deg) brightness(1.15)`:'none';au.style.animation=tier>=1?'auraP '+(2.8-tier*.4)+'s ease-in-out infinite':'none'}
  au.style.transformOrigin=side?'50% 45%':'50% 57%';au.style.transition='transform 1.1s cubic-bezier(.2,.8,.3,1),opacity 1.1s';au.style.transform=`scale(${hp.tf?1.45:(.46+.08*Math.min(10,em)).toFixed(3)})`;au.style.opacity=hp.tf?.88:(.3+.045*Math.min(10,em)).toFixed(2);'''
s=s.replace(old,new,1)
# makeUnit
i=s.index('function makeUnit(u){');j=s.index('function updateUnit(')
s=s[:i]+r'''function makeUnit(u){const el=document.createElement('div');el.className='u';el.dataset.k='u:'+u.uid;el.dataset.rk='u'+u.uid;
 el.innerHTML=`<div class="in surge"><div class="glow"></div><div class="glass"></div><img class="cardimg" src="a/cards/${u.id}.webp" alt="" draggable="false"><div class="rdyr"></div><div class="dome" style="display:none"></div><div class="bd a"><svg viewBox="0 0 40 40"><polygon points="20,1 25,13 38,9 30,20 38,31 25,27 20,39 15,27 2,31 10,20 2,9 15,13" fill="#e8481f" stroke="#fff" stroke-width="2.2" stroke-linejoin="round"/></svg><b></b></div><div class="bd h"><svg viewBox="0 0 24 22"><path d="M12 21 C1 13 2 3 7.5 2 C10 1.6 12 3.6 12 5 C12 3.6 14 1.6 16.5 2 C22 3 23 13 12 21 Z" fill="#d9232c" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg><b></b></div><span class="zz" style="display:none">Zz</span></div>`;
 el._q={a:el.querySelector('.bd.a b'),h:el.querySelector('.bd.h b'),bda:el.querySelector('.bd.a'),bdh:el.querySelector('.bd.h'),dome:el.querySelector('.dome'),zz:el.querySelector('.zz'),inn:el.querySelector('.in')};
 setTimeout(()=>el._q.inn.classList.remove('surge'),600);return el}
'''+s[j:]
# updateUnit
i=s.index('function updateUnit(');j=s.index('function syncBoard(')
s=s[:i]+r'''function updateUnit(el,u,p,mine){const q=el._q,sy=synLv(p),ti=tintOf(p,u),fa=finalAtk(p,u);
 el.style.setProperty('--g',ti.c?(ti.c==='Humano'?'#e8f4ff':CAT[ti.c]):'#fff');
 q.a.textContent=fa;q.bda.classList.toggle('up',fa>u.atk0);q.bda.classList.toggle('dn',fa<u.atk0);q.h.textContent=u.hp;q.bdh.classList.toggle('dn',u.hp<u.max);
 q.dome.style.display=u.kw==='Protetor'?'block':'none';q.zz.style.display=(u.sick&&!u.entry&&mine?'block':'none');
 const tg=UI.tg||{};const act=!!ti.c;
 el.classList.toggle('syn',act);
 el.classList.toggle('ready',mine&&G.turn===0&&!G.over&&!G.pending&&canAct(p,u)&&!u.sick&&!UI.busy);
 el.classList.toggle('entry',mine&&G.turn===0&&!G.over&&!G.pending&&canAct(p,u)&&u.sick&&!UI.busy);
 el.classList.toggle('sel',!!(UI.sel&&UI.sel.k==='u:'+u.uid));
 el.classList.toggle('tgt',!mine&&!!(tg.units&&tg.units.includes(u.uid)))}
'''+s[j:]
# syncBoard geometria
rep("const p=G.p[side],row=side?118:342,n=p.board.length,tot=n*108.6+(n-1)*8,x0=296+(830-tot)/2;","const p=G.p[side],row=side?112:310,n=p.board.length,tot=n*118+(n-1)*4,x0=292+(854-tot)/2;")
rep("(x0+i*116.6)+'px');el.style.setProperty('--y',row+'px');void el.offsetWidth}","(x0+i*122)+'px');el.style.setProperty('--y',row+'px');void el.offsetWidth}")
rep("el.style.setProperty('--x',(x0+i*116.6)+'px');el.style.setProperty('--y',row+'px');el.style.pointerEvents","el.style.setProperty('--x',(x0+i*122)+'px');el.style.setProperty('--y',row+'px');el.style.pointerEvents")
# evFx
rep("if(e.t==='beam'){const a=posOf(e.from),b=posOf(e.to);beam(a.cx,a.cy,b.cx,b.cy,e.col,e.big);\n   setTimeout(()=>{burst(b.cx,b.cy,e.col,e.big?70:38,e.big?12:8);ring(b.cx,b.cy,e.col,e.big?200:110);sfx(e.big?'boom':'kiplo',.8);if(e.big)shake(16)},230)}",
 "if(e.t==='beam'){const a=posOf(e.from),b=posOf(e.to);\n   if(e.k==='ab')abilityFx(e,a,b);else if(e.k==='at')atingirFx(e,a,b);\n   else{beam(a.cx,a.cy,b.cx,b.cy,e.col,e.big);\n   setTimeout(()=>{burst(b.cx,b.cy,e.col,e.big?70:38,e.big?12:8);ring(b.cx,b.cy,e.col,e.big?200:110);sfx(e.big?'boom':'kiplo',.8);if(e.big)shake(16)},230);\n   if(e.k==='cb'&&e.kill){UI.killFx=true;setTimeout(()=>raysFx(e.key==='goku'?'blue':'purple'),260)}}}")
rep("else if(e.t==='hit'){const b=posOf('u'+e.uid);float(b.cx,b.y+20,e.n>0?'-'+e.n:'0',e.n>0?'#ff5a4a':'#ccc');",
 "else if(e.t==='hit'){const b=posOf('u'+e.uid);float(b.cx,b.y+20,e.n>0?'-'+e.n:'0',e.n>0?'#ff5a4a':'#ccc');if(e.n>=5&&e.n>=2*(e.hpb||99))bigBolt(b.cx,b.cy);else if(e.n>=3)spr('splat',b.cx,b.cy,b.w*1.6,{speed:1.2,blend:true});")
# doPlay entrada
rep("burst(rr.cx,rr.cy,cc,22,6);ring(rr.cx,rr.cy,cc,80)}","burst(rr.cx,rr.cy,cc,22,6);ring(rr.cx,rr.cy,cc,80);entryFx(u,rr)}")
# doAbility mãos
rep("await sleep(520);\n if(k==='vegeta'&&!G.p[side].hero.tf","handsPanel(k);await sleep(760);\n if(k==='vegeta'&&!G.p[side].hero.tf")
# checkOver atraso kill
rep("function checkOver(){if(!G.over||UI.ended)return;","function checkOver(){if(!G.over||UI.ended)return;if(UI.killFx){UI.killFx=false;setTimeout(checkOver,2100);return}")
# start: versus + flare
rep("const bg=rnd(SCENES);$('#bg').style.backgroundImage=`url(a/scenes/${bg})`;","const bg=rnd(SCENES);$('#bg').style.backgroundImage=`url(a/scenes/${bg})`;dayFlare('a/scenes/'+bg);")
rep("muList(['batalha1','batalha2']);","muList(['batalha1','batalha2']);Object.keys(SH).forEach(k=>{const i=new Image();i.src='a/vfx/'+k+'.webp'});['beam_kame','boom_big'].forEach(n=>{const v=vidEl(n);v.load()});")
rep("await coinToss(first);","await versus(mine,bot);await coinToss(first);")
# sheets json
rep("const VFXL=document.getElementById('vfx');let SH={};","const VFXL=document.getElementById('vfx');let SH={};fetch('a/vfx/sheets.json').then(r=>r.json()).then(j=>{SH=j}).catch(()=>{});")
open(R+'demo/game3.src.html','w').write(s)
print('ok',len(s))
