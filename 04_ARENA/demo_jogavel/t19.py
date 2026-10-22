import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1280,'height':720})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/game4.html');await pg.wait_for_timeout(500)
        await pg.click('#go')
        await pg.wait_for_function("window.__T.UIx.mode==='game' && document.querySelector('#coin').style.display==='flex'",timeout=15000)
        await pg.wait_for_function("window.__T.G && !window.__T.UIx.busy && window.__T.G.turn===0",timeout=30000)
        await pg.evaluate("(()=>{const p=__T.G.p[0];p.turns=10;p.energyMax=10;p.energy=10;__T.sync()})()")
        await pg.wait_for_timeout(1500)
        for e,n in [(3,'A3'),(7,'A7'),(10,'A10')]:
            await pg.evaluate(f"(()=>{{const p=__T.G.p[0];p.energyMax={e};p.energy={e};__T.sync()}})()")
            await pg.wait_for_timeout(1500);await pg.screenshot(path=f'../vfx/{n}.png',clip={'x':0,'y':300,'width':320,'height':260})
        await pg.click('#zb0')
        await pg.wait_for_timeout(11000);await pg.screenshot(path='../vfx/A_tf.png',clip={'x':0,'y':300,'width':320,'height':260})
        print(errs);await b.close()
asyncio.run(main())
