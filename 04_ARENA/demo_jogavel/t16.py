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
        await pg.evaluate("""(()=>{const p=__T.G.p[0];p.turns=10;p.energyMax=10;p.energy=10;p.board.length=0;
          const get=id=>({...__T.DECKS.goku.find(c=>c.id===id),hid:900+Math.random()});p.hand=[get('GK01')];
          const o=__T.G.p[1];o.board.length=0;[5,6,7].forEach((k,i)=>{const c=__T.DECKS.vegeta[k];o.board.push({uid:5000+i,id:c.id,name:c.n,cats:c.c,kw:c.kw,cost:c.cost,atk0:c.atk,hp:c.hp,max:c.hp,st:c.st,sick:false,atkd:false,entry:null,entryUsed:false,saved:false,justPlayed:false})});__T.sync()})()""")
        await pg.wait_for_timeout(700)
        await pg.click('.hc >> nth=0',force=True)
        for i in range(4):
            await pg.screenshot(path=f'../vfx/G{i}.png',clip={'x':280,'y':90,'width':880,'height':420})
        print(errs);await b.close()
asyncio.run(main())
