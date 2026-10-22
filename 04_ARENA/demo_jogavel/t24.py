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
        for key,fr,to in [('goku','h0','h1'),('vegeta','h1','h0')]:
            await pg.evaluate("evFx([{t:'beam',from:'%s',to:'%s',col:'#46b5ff',big:1,k:'cb',key:'%s',kill:true}])"%(fr,to,key))
            for i in range(5):
                await pg.wait_for_timeout(450);await pg.screenshot(path=f'../vfx/C_{key}{i}.png')
            await pg.wait_for_timeout(3000)
        print(errs);await b.close()
asyncio.run(main())
