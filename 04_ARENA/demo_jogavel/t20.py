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
        n=0
        for step in range(70):
            await pg.wait_for_timeout(450)
            st=await pg.evaluate("({t:__T.G.turn,busy:__T.UIx.busy,over:!!__T.G.over})")
            if st['over']:break
            if st['t']==0 and not st['busy']:
                await pg.evaluate("""(async()=>{const G=__T.G;for(let i=G.p[0].hand.length-1;i>=0;i--){if(!playReason(0,i)){await doPlay(0,i);break}}
 await new Promise(r=>setTimeout(r,900));const p=G.p[0];for(const u of p.board){if(__T.canAct(p,u)){const t=__T.legalTargets(0,u);const k=t&&t.units&&t.units[0];if(k){await doAttack(0,u.uid,{uid:k});break}}}})().catch(e=>console.log('ERR',e))""")
                await pg.wait_for_timeout(1200)
                await pg.evaluate("document.querySelector('#endbtn').click()")
            await pg.screenshot(path=f'../vfx/P{n}.png');n+=1
        print(errs);await b.close()
asyncio.run(main())
