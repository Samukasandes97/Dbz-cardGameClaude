import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1280,'height':720})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/game3.html');await pg.wait_for_timeout(500)
        await pg.click('#go')
        await pg.wait_for_function("window.__T.UIx.mode==='game' && document.querySelector('#coin').style.display==='flex'",timeout=15000)
        await pg.wait_for_function("window.__T.G && !window.__T.UIx.busy && window.__T.G.turn===0",timeout=30000)
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path='../vfx/F_low.png',clip={'x':0,'y':0,'width':420,'height':720})
        await pg.evaluate("(()=>{const p=__T.G.p[0];p.turns=5;p.energyMax=5;p.energy=5;__T.sync()})()");await pg.wait_for_timeout(1600)
        await pg.screenshot(path='../vfx/F_mid.png',clip={'x':0,'y':0,'width':420,'height':720})
        await pg.evaluate("(()=>{const p=__T.G.p[0];p.turns=10;p.energyMax=10;p.energy=10;__T.sync()})()");await pg.wait_for_timeout(1600)
        await pg.screenshot(path='../vfx/F_high.png',clip={'x':0,'y':0,'width':420,'height':720})
        print(errs);await b.close()
asyncio.run(main())
