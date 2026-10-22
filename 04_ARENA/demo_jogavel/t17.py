import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1280,'height':720})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/game3.html');await pg.wait_for_timeout(500)
        await pg.click('[data-p=vegeta]');await pg.click('#go')
        att=0
        for t in range(40):
            try: await pg.wait_for_function("window.__T.G.over||(window.__T.G.turn===0 && !window.__T.UIx.busy)",timeout=30000)
            except Exception as e: print('timeout',t);break
            if await pg.evaluate("!!window.__T.G.over"):break
            for i in range(6):
                if await pg.evaluate("document.querySelectorAll('.hc.ok').length"):
                    await pg.click('.hc.ok >> nth=0',force=True);await pg.wait_for_timeout(700)
                    if await pg.evaluate("!!window.__T.G.pending"):
                        await pg.click('#board .u.tgt >> nth=0',force=True);await pg.wait_for_timeout(700)
            # attack: each ready unit -> first enemy unit or hero
            for k in range(6):
                u=pg.locator('#board .u.ready, #board .u.entry')
                if await u.count()==0:break
                await u.first.click(force=True);await pg.wait_for_timeout(150)
                tg=pg.locator('#board .u.tgt')
                if await tg.count(): await tg.first.click(force=True)
                elif await pg.evaluate("!!document.querySelector('#pt1.tgt')"): await pg.click('#pt1',force=True)
                else:
                    await pg.mouse.click(640,200);break
                att+=1;await pg.wait_for_timeout(900)
            await pg.click('#endbtn',force=True)
        print('over',await pg.evaluate("window.__T.G.over"),'turn',await pg.evaluate("window.__T.G.n"),'attacks',att,errs)
        await pg.screenshot(path='../vfx/g3_end.png')
        await b.close()
asyncio.run(main())
