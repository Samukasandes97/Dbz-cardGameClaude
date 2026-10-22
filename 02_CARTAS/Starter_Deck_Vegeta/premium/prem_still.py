import sys,json,os
sys.path.insert(0,'../cartas')
import frame
from playwright.sync_api import sync_playwright
c=dict(id='VG28',nome='Vegeta',tema='saiyajin',tipo_carta='unidade',tipo='Saiyajin',tipo2='Vilão',tema2='vilao',custo=4,codigo='DB-VG28',palavra='Atacar',arte='',arte_wh=[1066,908],fonte='GIF',atk=4,pv=4,estagio='premium',hole=True)
B=os.path.abspath('prem')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1190,'height':1705},device_scale_factor=1)
    for name,mode,css in (('frame_full',None,None),('frame_noirid','noirid',None),('irid_mask',None,'svg>*:not(.irid){display:none!important} .irid *{stroke:#fff!important} .irid [fill]:not([fill=none]){fill:#fff!important}')):
        frame.PREM_MODE=mode
        open(f'{B}/{name}.html','w').write(frame.card_html(c)); pg.goto(f'file://{B}/{name}.html'); pg.wait_for_timeout(400)
        if css: pg.add_style_tag(content=css); pg.wait_for_timeout(200)
        pg.locator('#card').screenshot(path=f'{B}/{name}.png',omit_background=True)
    b.close()
