from playwright.sync_api import sync_playwright
import os
D='/tmp/claude-0/-home-claude/84f3faec-af92-5d88-b151-bbf1e79ccb25/scratchpad/gkdeck/d3/fr'; os.makedirs(D,exist_ok=True)
FPS=24; T0,T1=6.8,16.15
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080})
    pg.goto('file:///tmp/claude-0/-home-claude/84f3faec-af92-5d88-b151-bbf1e79ccb25/scratchpad/gkdeck/d3/demo3d.html'); pg.wait_for_timeout(800)
    n=int((T1-T0)*FPS)
    for i in range(n):
        pg.evaluate(f'setT({T0+i/FPS})'); pg.screenshot(path=f'{D}/f{i:04d}.jpg',type='jpeg',quality=94)
    b.close()
print(n)
