from playwright.sync_api import sync_playwright
import os
FPS=24; D='/tmp/claude-0/-home-claude/84f3faec-af92-5d88-b151-bbf1e79ccb25/scratchpad/cartas/fr3d'; os.makedirs(D,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080})
    pg.goto('file:///tmp/claude-0/-home-claude/84f3faec-af92-5d88-b151-bbf1e79ccb25/scratchpad/cartas/demo3d.html'); pg.wait_for_timeout(600)
    T=pg.evaluate('TOTAL'); n=int(T*FPS)
    for i in range(n):
        pg.evaluate(f'setT({i/FPS})'); pg.screenshot(path=f'{D}/f{i:04d}.jpg',type='jpeg',quality=93)
    b.close()
print('ok',n)
