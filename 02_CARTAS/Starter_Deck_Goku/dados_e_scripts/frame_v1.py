import json,os,sys,html
from playwright.sync_api import sync_playwright
B=os.path.dirname(os.path.abspath(__file__))
THEMES={
 'saiyajin':dict(main='#ffc83a',mid='#f08a1c',deep='#5a2806',dark='#2a1305',glow='#ffd978',acc='#ff7a2b',orb1='#ffb347',orb2='#c2540a',orb3='#5e2204',name='SAIYAJIN'),
 'humano':dict(main='#59b6ff',mid='#2a78d8',deep='#0d2f6b',dark='#081a3a',glow='#9fd6ff',acc='#ff9a2e',orb1='#5aa8ff',orb2='#1c56b8',orb3='#0a2a66',name='HUMANO'),
 'namek':dict(main='#7be36a',mid='#2fa040',deep='#0c4a1c',dark='#07250f',glow='#b8ffa8',acc='#ffd23a',orb1='#7ae070',orb2='#1f8a36',orb3='#0a3d18',name='NAMEKUSEIJIN'),
 'vilao':dict(main='#c77bff',mid='#8a3fd8',deep='#3a0f6b',dark='#1d0838',glow='#e3b8ff',acc='#ff4fa0',orb1='#c07bff',orb2='#6a2cb8',orb3='#2a0a5e',name='VILÃO'),
 'androide':dict(main='#ff6a5a',mid='#d8262a',deep='#6b0d10',dark='#3a0709',glow='#ffb0a8',acc='#ffd23a',orb1='#ff6a5a',orb2='#b8181c',orb3='#5e0a0c',name='ANDROIDE'),
}
def card_html(c):
    t=THEMES[c.get('tema','saiyajin')]
    item=c.get('tipo_carta','unidade')=='item'
    W,H=1190,1705
    # arte
    art=c['arte']; aw,ah=c['arte_wh']
    win_x,win_y,win_w,win_h=62,62,1066,1581
    top=215; bh=win_y+win_h-top; bw=bh*aw/ah
    if bw>win_w: bw=win_w; bh=bw*ah/aw; top=win_y+win_h-bh
    ax=(win_w-bw)/2; ay=top-win_y
    kw=c.get('palavra','')
    kwrow=''
    if kw:
        kwrow=f'''<g transform="translate(595,236)">
 <rect x="-262" y="-27" width="262" height="54" rx="27" fill="#14110c" stroke="{t['main']}" stroke-width="3"/>
 <text x="-131" y="9" text-anchor="middle" font-family="Inter" font-weight="800" font-size="25" fill="{t['glow']}" letter-spacing="1">PALAVRA-CHAVE</text>
 <rect x="14" y="-27" width="{max(150,len(kw)*24+60)}" height="54" rx="27" fill="url(#pill)" stroke="{t['glow']}" stroke-width="2"/>
 <text x="{14+max(150,len(kw)*24+60)/2}" y="10" text-anchor="middle" font-family="Inter" font-weight="900" font-size="30" fill="#2a1200">{html.escape(kw.upper())}</text></g>'''
        # centraliza o par
        pw=262+14+max(150,len(kw)*24+60)
        kwrow=kwrow.replace('translate(595,236)',f'translate({595-pw/2+262},236)')
    stats=''
    if not item:
        stats=f'''
<g transform="translate(108,1596)"><rect x="0" y="0" width="296" height="84" rx="24" fill="#120f0a" stroke="url(#gold)" stroke-width="5"/><rect x="6" y="6" width="284" height="72" rx="19" fill="url(#chip)"/>
 <g transform="translate(24,16) scale(1.0)">{FIST}</g>
 <text x="104" y="58" font-family="Inter" font-weight="900" font-size="38" fill="#fff6dc" letter-spacing="1">ATK</text>
 <text x="262" y="60" text-anchor="end" font-family="Inter" font-weight="900" font-size="62" fill="#ffffff" stroke="#2a1305" stroke-width="2" paint-order="stroke">{c['atk']}</text></g>
<g transform="translate(786,1596)"><rect x="0" y="0" width="296" height="84" rx="24" fill="#120f0a" stroke="url(#gold)" stroke-width="5"/><rect x="6" y="6" width="284" height="72" rx="19" fill="url(#chip)"/>
 <g transform="translate(26,18)">{HEART}</g>
 <text x="108" y="58" font-family="Inter" font-weight="900" font-size="38" fill="#fff6dc" letter-spacing="1">PV</text>
 <text x="262" y="60" text-anchor="end" font-family="Inter" font-weight="900" font-size="62" fill="#ffffff" stroke="#2a1305" stroke-width="2" paint-order="stroke">{c['pv']}</text></g>'''
    ns=min(88,int(540/(0.68*max(len(c['nome']),6))))
    tipo=c.get('tipo','Saiyajin')
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:transparent}}
#card{{position:relative;width:{W}px;height:{H}px;overflow:hidden;border-radius:38px;background:#0a0b10}}
.win{{position:absolute;left:{win_x}px;top:{win_y}px;width:{win_w}px;height:{win_h}px;border-radius:22px;overflow:hidden;background:#000}}
.bd{{position:absolute;inset:-60px;background:url('{art}') center/cover;filter:blur(38px) brightness(.78) saturate(1.25)}}
.art{{position:absolute;left:{ax}px;top:{ay}px;width:{bw}px;height:{bh}px;-webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 80px),linear-gradient(to right,transparent 0,#000 26px,#000 calc(100% - 26px),transparent 100%);-webkit-mask-composite:source-in;mask-composite:intersect}}
svg{{position:absolute;left:0;top:0}}
</style></head><body><div id="card">
<div class="win"><div class="bd"></div><img class="art" src="{art}"></div>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs>
 <pattern id="carbon" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="14" height="14" fill="#101218"/><rect width="7" height="7" fill="#171a21"/><rect x="7" y="7" width="7" height="7" fill="#171a21"/></pattern>
 <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['glow']}"/><stop offset=".45" stop-color="{t['main']}"/><stop offset="1" stop-color="{t['mid']}"/></linearGradient>
 <linearGradient id="band" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t['deep']}"/><stop offset=".5" stop-color="{t['dark']}"/><stop offset="1" stop-color="{t['deep']}"/></linearGradient>
 <linearGradient id="pill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t['glow']}"/><stop offset="1" stop-color="{t['mid']}"/></linearGradient>
 <linearGradient id="chip" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t['mid']}"/><stop offset="1" stop-color="{t['deep']}"/></linearGradient>
 <linearGradient id="nameg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2c2"/><stop offset=".45" stop-color="{t['main']}"/><stop offset="1" stop-color="{t['mid']}"/></linearGradient>
 <radialGradient id="orb" cx=".38" cy=".3" r=".8"><stop offset="0" stop-color="{t['orb1']}"/><stop offset=".6" stop-color="{t['orb2']}"/><stop offset="1" stop-color="{t['orb3']}"/></radialGradient>
 <filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<!-- moldura (carbono + banda do tema) -->
<path fill-rule="evenodd" d="M38 0H{W-38}Q{W} 0 {W} 38V{H-38}Q{W} {H} {W-38} {H}H38Q0 {H} 0 {H-38}V38Q0 0 38 0Z M{win_x+22} {win_y}H{win_x+win_w-22}Q{win_x+win_w} {win_y} {win_x+win_w} {win_y+22}V{win_y+win_h-22}Q{win_x+win_w} {win_y+win_h} {win_x+win_w-22} {win_y+win_h}H{win_x+22}Q{win_x} {win_y+win_h} {win_x} {win_y+win_h-22}V{win_y+22}Q{win_x} {win_y} {win_x+22} {win_y}Z" fill="url(#carbon)"/>
<path fill-rule="evenodd" d="M30 34H{W-30}V{H-34}H30Z M{win_x-6} {win_y-6}H{win_x+win_w+6}V{win_y+win_h+6}H{win_x-6}Z" fill="url(#band)" opacity=".92"/>
<rect x="{win_x-5}" y="{win_y-5}" width="{win_w+10}" height="{win_h+10}" rx="27" fill="none" stroke="url(#gold)" stroke-width="6"/>
<rect x="{win_x-14}" y="{win_y-14}" width="{win_w+28}" height="{win_h+28}" rx="34" fill="none" stroke="{t['mid']}" stroke-width="2" opacity=".8"/>
<rect x="22" y="26" width="{W-44}" height="{H-52}" rx="30" fill="none" stroke="{t['acc']}" stroke-width="3" opacity=".9"/>
<!-- cantos tecnologicos -->
<path d="M{W-34} 150V96L{W-96} 34H{W-250}" fill="none" stroke="{t['acc']}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)"/>
<path d="M{W-62} 200V120" fill="none" stroke="{t['main']}" stroke-width="5" stroke-linecap="round"/>
<path d="M34 {H-220}V{H-120}L100 {H-54}" fill="none" stroke="{t['acc']}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" opacity=".95"/>
<path d="M{W-34} {H-220}V{H-120}L{W-100} {H-54}" fill="none" stroke="{t['acc']}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" opacity=".95"/>
<!-- placa do nome -->
<path d="M250 30H940L985 78V166L925 214H265L205 166V78Z" fill="url(#carbon)" stroke="url(#gold)" stroke-width="5"/>
<path d="M262 40H928L968 82V160L918 202H272L222 160V82Z" fill="none" stroke="{t['mid']}" stroke-width="2" opacity=".9"/>
<text x="615" y="118" text-anchor="middle" font-family="Inter" font-weight="900" font-size="{ns}" fill="url(#nameg)" stroke="#1b0d03" stroke-width="5" paint-order="stroke" letter-spacing="3" filter="url(#glow)">{html.escape(c['nome'].upper())}</text>
<text x="615" y="176" text-anchor="middle" font-family="Inter" font-weight="600" font-size="31" fill="#dfe6ef" letter-spacing="2">TIPO <tspan fill="{t['main']}">—</tspan> {html.escape(tipo)}</text>
{kwrow}
<!-- orbe de custo -->
<g filter="url(#glow)"><circle cx="164" cy="164" r="116" fill="#0d0e13" stroke="url(#gold)" stroke-width="8"/>
<circle cx="164" cy="164" r="104" fill="none" stroke="{t['acc']}" stroke-width="5"/>
<circle cx="164" cy="164" r="92" fill="url(#orb)" stroke="#fff3" stroke-width="2"/>
<ellipse cx="140" cy="116" rx="52" ry="24" fill="#fff" opacity=".22"/></g>
<text x="164" y="108" text-anchor="middle" font-family="Inter" font-weight="800" font-size="25" fill="#fff6dc" letter-spacing="2">ESFERA</text>
<text x="164" y="206" text-anchor="middle" font-family="Inter" font-weight="900" font-size="104" fill="#ffffff" stroke="#2a1305" stroke-width="4" paint-order="stroke">{c['custo']}</text>
{stats}
<text x="595" y="1672" text-anchor="middle" font-family="Inter" font-weight="700" font-size="22" fill="#cdd3dc" letter-spacing="3">{html.escape(c['codigo'])}</text>
</svg></div></body></html>'''
FIST='''<g fill="#fff6dc" stroke="#2a1305" stroke-width="3" stroke-linejoin="round"><rect x="6" y="22" width="52" height="32" rx="9"/><rect x="6" y="8" width="13" height="22" rx="6"/><rect x="19" y="4" width="13" height="26" rx="6"/><rect x="32" y="4" width="13" height="26" rx="6"/><rect x="45" y="8" width="13" height="22" rx="6"/><path d="M6 42Q-6 36 0 28L10 32Z"/></g>'''
HEART='''<path d="M32 58C8 40 2 28 2 18C2 8 10 2 19 2C25 2 29 5 32 10C35 5 39 2 45 2C54 2 62 8 62 18C62 28 56 40 32 58Z" fill="#ff7a3a" stroke="#2a1305" stroke-width="4" stroke-linejoin="round"/><path d="M14 14Q18 8 25 9" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" opacity=".7"/>'''
def render(cards,outdir):
    os.makedirs(outdir,exist_ok=True)
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':1190,'height':1705},device_scale_factor=1)
        for c in cards:
            hp=os.path.join(B,'render',c['id']+'.html'); open(hp,'w').write(card_html(c))
            pg.goto('file://'+hp); pg.wait_for_timeout(400)
            pg.locator('#card').screenshot(path=os.path.join(outdir,c['id']+'.png'),omit_background=True)
        b.close()
if __name__=='__main__':
    cards=json.load(open(sys.argv[1])); render(cards,sys.argv[2])
