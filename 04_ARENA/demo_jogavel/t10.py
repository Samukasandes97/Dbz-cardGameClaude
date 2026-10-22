import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1280,'height':720})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append('C:'+m.text) if m.type=='error' else None)
        await pg.goto('http://localhost:8765/game3.html');await pg.wait_for_timeout(600)
        await pg.screenshot(path='../vfx/g3_menu.png')
        await pg.click('#go');await pg.wait_for_timeout(1500)
        await pg.screenshot(path='../vfx/g3_versus.png')
        await pg.wait_for_function("window.__T.UIx.mode==='game' && document.querySelector('#coin').style.display==='flex'",timeout=15000)
        await pg.wait_for_function("window.__T.G && !window.__T.UIx.busy && window.__T.G.turn===0",timeout=30000)
        await pg.wait_for_timeout(500)
        # dar energia e cartas
        await pg.evaluate("(()=>{const p=__T.G.p[0];p.turns=6;p.energyMax=6;p.energy=6;__T.sync()})()")
        for i in range(4):
            if await pg.evaluate("document.querySelectorAll('.hc.ok').length"):
                await pg.click('.hc.ok >> nth=0',force=True);await pg.wait_for_timeout(1300)
                if await pg.evaluate("!!__T.G.pending"):
                    await pg.click('#board .u.tgt >> nth=0',force=True);await pg.wait_for_timeout(900)
        await pg.wait_for_timeout(600)
        await pg.screenshot(path='../vfx/g3_board.png')
        print(errs)
        await b.close()
asyncio.run(main())
