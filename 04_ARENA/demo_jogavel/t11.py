import asyncio,sys
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
          p.hand=[get('GK16'),get('GK01'),get('GK06'),get('GK10')];
          const o=__T.G.p[1];const e=__T.DECKS.vegeta.slice(0,3).map((c,i)=>({...c,hid:800+i}));
          __T.sync()})()""")
        await pg.wait_for_timeout(500)
        await pg.screenshot(path='../vfx/g3_a.png')
        # jogar GK16 (protetor) e GK06
        for idx in [0,0]:
            await pg.click('.hc >> nth=0',force=True);await pg.wait_for_timeout(1500)
        await pg.screenshot(path='../vfx/g3_b.png')
        # bot: força unidades inimigas
        await pg.evaluate("""(()=>{const o=__T.G.p[1];[ 'VG06','VG10','VG12'].forEach(id=>{const c=__T.DECKS.vegeta.find(c=>c.id===id)||__T.DECKS.vegeta[3];o.board.push({uid:5000+o.board.length,id:c.id,name:c.n,cats:c.c,kw:c.kw,cost:c.cost,atk0:c.atk,hp:c.hp,max:c.hp,st:c.st,sick:false,atkd:false,entry:null,entryUsed:false,saved:false,justPlayed:false})});__T.sync()})()""")
        await pg.wait_for_timeout(700)
        # jogar a lendária GK01 (Atingir)
        await pg.click('.hc >> nth=0',force=True);await pg.wait_for_timeout(350)
        await pg.screenshot(path='../vfx/g3_leg1.png')
        await pg.wait_for_timeout(450)
        await pg.screenshot(path='../vfx/g3_leg2.png')
        await pg.wait_for_timeout(500)
        await pg.screenshot(path='../vfx/g3_leg3.png')
        if await pg.evaluate("!!__T.G.pending"):
            await pg.click('#board .u.tgt >> nth=0',force=True);await pg.wait_for_timeout(300)
            await pg.screenshot(path='../vfx/g3_at1.png');await pg.wait_for_timeout(250)
            await pg.screenshot(path='../vfx/g3_at2.png');await pg.wait_for_timeout(250)
            await pg.screenshot(path='../vfx/g3_at3.png');await pg.wait_for_timeout(400)
            await pg.screenshot(path='../vfx/g3_at4.png')
        print(errs)
        await b.close()
asyncio.run(main())
