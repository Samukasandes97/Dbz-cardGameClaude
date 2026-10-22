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
        await pg.evaluate("""(()=>{const p=__T.G.p[0];p.turns=10;p.energyMax=10;p.energy=10;
          const get=id=>({...__T.DECKS.goku.find(c=>c.id===id),hid:900+Math.random()});
          p.hand=[get('GK01'),get('GK16')];
          const o=__T.G.p[1];['VG06','VG10','VG12'].forEach((id,i)=>{const c=__T.DECKS.vegeta.find(c=>c.id===id)||__T.DECKS.vegeta[i];o.board.push({uid:5000+i,id:c.id,name:c.n,cats:c.c,kw:c.kw,cost:c.cost,atk0:c.atk,hp:c.hp,max:c.hp,st:c.st,sick:false,atkd:false,entry:null,entryUsed:false,saved:false,justPlayed:false})});
          __T.sync()})()""")
        await pg.wait_for_timeout(600)
        await pg.click('.hc >> nth=0',force=True)
        for i,t in enumerate([150,200,200,200,250]):
            await pg.wait_for_timeout(t);await pg.screenshot(path=f'../vfx/L{i}.png')
        await pg.wait_for_function("!!__T.G.pending",timeout=5000)
        await pg.click('#board .u.tgt >> nth=0',force=True)
        for i,t in enumerate([250,150,150,150,200,300]):
            await pg.wait_for_timeout(t);await pg.screenshot(path=f'../vfx/A{i}.png')
        print(errs)
        await b.close()
asyncio.run(main())
