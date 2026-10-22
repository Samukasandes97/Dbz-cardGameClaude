def deco(t,W,H,wx,wy,ww,wh,mode=None):
    irid=(lambda s:'' ) if mode=='noirid' else (lambda s:f'<g class="irid">{s}</g>')
    d='''<defs>
<linearGradient id="chrome" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".12" stop-color="#8793a3"/><stop offset=".26" stop-color="#f3f7fc"/><stop offset=".4" stop-color="#5b6676"/><stop offset=".55" stop-color="#e2e9f2"/><stop offset=".7" stop-color="#7a8696"/><stop offset=".85" stop-color="#fbfdff"/><stop offset="1" stop-color="#8f9bab"/></linearGradient>
<linearGradient id="chromeV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="#8b97a7"/><stop offset=".5" stop-color="#3b4552"/><stop offset=".55" stop-color="#a8b4c4"/><stop offset="1" stop-color="#f4f8fd"/></linearGradient>
<linearGradient id="irid" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4df2ff"/><stop offset=".25" stop-color="#8a6bff"/><stop offset=".5" stop-color="#ff55e0"/><stop offset=".75" stop-color="#3dffc4"/><stop offset="1" stop-color="#4df2ff"/></linearGradient>
<filter id="brush" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.0012 0.85" numOctaves="2" seed="7" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1.5 -0.62"/></filter>
<filter id="cglow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="7" result="b"/><feColorMatrix in="b" type="matrix" values="0.3 0 0 0 0.25  0 0.8 0 0 0.45  0 0 1 0 0.6  0 0 0 1.1 0"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="bandclip"><path clip-rule="evenodd" d="M30 34H@A V@B H30Z M@C @D H@E V@F H@C Z"/></clipPath>
</defs>'''
    for k,v in zip('ABCDEF',(W-30,H-34,wx-6,wy-6,wx+ww+6,wy+wh+6)): d=d.replace('@'+k,str(v))
    # textura metal escovado nas faixas da moldura
    d+=f'<g clip-path="url(#bandclip)"><rect x="30" y="34" width="{W-60}" height="{H-68}" fill="#fff" filter="url(#brush)" opacity=".34" style="mix-blend-mode:screen"/></g>'
    # borda externa cromada + luz interna
    d+=f'<rect x="7" y="9" width="{W-14}" height="{H-18}" rx="36" fill="none" stroke="url(#chrome)" stroke-width="18" filter="url(#cglow)"/>'
    d+=f'<rect x="22" y="25" width="{W-44}" height="{H-50}" rx="28" fill="none" stroke="#fff" stroke-width="3" opacity=".85"/>'
    d+=irid(f'<rect x="31" y="34" width="{W-62}" height="{H-68}" rx="24" fill="none" stroke="url(#irid)" stroke-width="5" filter="url(#glow)"/>')
    # janela
    d+=f'<rect x="{wx-13}" y="{wy-13}" width="{ww+26}" height="{wh+26}" rx="32" fill="none" stroke="url(#chrome)" stroke-width="12" filter="url(#cglow)"/>'
    d+=f'<rect x="{wx-3}" y="{wy-3}" width="{ww+6}" height="{wh+6}" rx="25" fill="none" stroke="#fff" stroke-width="2.5" opacity=".9"/>'
    d+=irid(f'<rect x="{wx-8}" y="{wy-8}" width="{ww+16}" height="{wh+16}" rx="29" fill="none" stroke="url(#irid)" stroke-width="5" filter="url(#glow)"/>')
    d+=f'<path fill-rule="evenodd" d="M30 34H{W-30}V{H-34}H30Z M{wx-6} {wy-6}H{wx+ww+6}V{wy+wh+6}H{wx-6}Z" fill="url(#chrome)" opacity=".16" style="mix-blend-mode:screen"/>'
    # cantos: gemas octogonais cromadas com nucleo iridescente
    def gem(x,y,r):
        pts=' '.join(f'{x+r*__import__("math").cos(a*3.14159/4+0.3927):.1f},{y+r*__import__("math").sin(a*3.14159/4+0.3927):.1f}' for a in range(8))
        return f'<polygon points="{pts}" fill="url(#chrome)" stroke="#1b2028" stroke-width="3"/>'+irid(f'<circle cx="{x}" cy="{y}" r="{r*.5:.0f}" fill="url(#irid)" stroke="#fff" stroke-width="2"/>')
    for x,y in ((wx-6,wy-6),(wx+ww+6,wy-6),(wx-6,wy+wh+6),(wx+ww+6,wy+wh+6)): d+=gem(x,y,26)
    # laminas anguladas dos dois lados da placa do nome
    for sx in (1,-1):
        x0=205 if sx==1 else 985
        for k,(dy,ln) in enumerate(((0,170),(30,142),(60,114),(90,86))):
            d+=f'<path d="M{x0} {92+dy} L{x0-sx*ln} {58+dy*0.85} L{x0-sx*(ln-34)} {104+dy*0.85} L{x0-sx*6} {122+dy*0.4}Z" fill="url(#chrome)" stroke="#1b2028" stroke-width="2.5" opacity="{0.98-k*.05}"/>'
    # rebites nas laterais
    for yy in (360,620,880,1140,1400):
        for xx in (wx-34,wx+ww+34):
            d+=f'<circle cx="{xx}" cy="{yy}" r="9" fill="url(#chrome)" stroke="#1b2028" stroke-width="2"/>'+irid(f'<circle cx="{xx}" cy="{yy}" r="3.5" fill="url(#irid)"/>')
    # fita PREMIUM + emblema
    cx=W//2; cy=H-100; sy=cy-68
    d+=f'<path d="M{cx-250} {cy+18} L{cx-165} {cy-28} H{cx+165} L{cx+250} {cy+18} L{cx+165} {cy+46} H{cx-165}Z" fill="url(#chromeV)" stroke="#1b2028" stroke-width="3"/>'
    d+=f'<text x="{cx}" y="{cy+17}" text-anchor="middle" font-family="Inter" font-weight="900" font-size="29" letter-spacing="9" fill="#141a22">PREMIUM</text>'
    d+=f'<g filter="url(#cglow)"><polygon points="{cx},{sy-44} {cx+36},{sy} {cx},{sy+44} {cx-36},{sy}" fill="url(#chrome)" stroke="#fff" stroke-width="4"/></g>'
    d+=irid(f'<polygon points="{cx},{sy-26} {cx+20},{sy} {cx},{sy+26} {cx-20},{sy}" fill="url(#irid)" stroke="#fff" stroke-width="2"/>')
    return d
