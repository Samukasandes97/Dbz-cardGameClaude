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
        await pg.evaluate("""(()=>{const p=__T.G.p[0];p.turns=8;p.energyMax=8;p.energy=8;
          const o=__T.G.p[1];['VG06','VG10'].forEach((id,i)=>{const c=__T.DECKS.vegeta[i+5];o.board.push({uid:5000+i,id:c.id,name:c.n,cats:c.c,kw:c.kw,cost:c.cost,atk0:c.atk,hp:c.hp,max:c.hp,st:c.st,sick:false,atkd:false,entry:null,entryUsed:false,saved:false,justPlayed:false})});
          __T.sync()})()""")
        await pg.wait_for_timeout(600)
        await pg.click('#ab0');await pg.wait_for_timeout(300)
        await pg.click('#pt1')
        for i in range(8):
            await pg.screenshot(path=f'../vfx/B{i}.png')
        await pg.wait_for_timeout(1500)
        # raio forte e comeback rays
        await pg.evaluate("bigBolt(640,200)");await pg.wait_for_timeout(250);await pg.screenshot(path='../vfx/C0.png')
        await pg.wait_for_timeout(1500)
        await pg.evaluate("raysFx('blue')");await pg.wait_for_timeout(350);await pg.screenshot(path='../vfx/C1.png')
        await pg.wait_for_timeout(2000)
        print(errs)
        await b.close()
asyncio.run(main())
