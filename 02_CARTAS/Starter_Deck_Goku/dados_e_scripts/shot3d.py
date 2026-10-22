import sys
from playwright.sync_api import sync_playwright
ts=[float(x) for x in sys.argv[1:]]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080})
    pg.goto('file:///tmp/claude-0/-home-claude/84f3faec-af92-5d88-b151-bbf1e79ccb25/scratchpad/cartas/demo3d.html'); pg.wait_for_timeout(600)
    for t in ts:
        pg.evaluate(f'setT({t})'); pg.wait_for_timeout(120); pg.screenshot(path=f'd3_{t}.png')
    b.close()
