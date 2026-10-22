import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
        pg=await b.new_page(viewport={'width':1280,'height':720})
        errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
        await pg.goto('file:///tmp/claude-0/-home-claude/84f3faec-af92-5d88-b151-bbf1e79ccb25/scratchpad/demo/game.html')
        await pg.wait_for_timeout(800)
        await pg.screenshot(path='s_menu.png')
        # engine sim bot vs bot
        r=await pg.evaluate('''()=>{const T=window.__T;let res=[];for(let g=0;g<200;g++){T.newGame(g%2?'goku':'vegeta',g%2?'vegeta':'goku');let G=T.G,guard=0;
          while(!G.over&&guard<4000){guard++;const s=G.turn;const a=T.aiNext(s);
            if(a.type==='end'){T.endTurn(s)}else if(a.type==='play')T.play(s,a.idx);else if(a.type==='attack'){if(!T.attack(s,a.uid,a.target)){return 'attack fail '+JSON.stringify(a)}}
            else if(a.type==='ability'){if(!T.useAbility(s,a.target))return 'ab fail'}else if(a.type==='transform')T.transform(s);else if(a.type==='atingir')T.atingir(s,a.uid);
            G.scenes.length=0;G.ev.length=0}
          res.push(G.over?G.over.win+':'+G.n:'stuck')}
          return res.join(' ')}''')
        print(r[:900])
        await pg.click('#go');await pg.wait_for_timeout(2500)
        await pg.screenshot(path='s_game1.png')
        print(errs[:10])
        await b.close()
asyncio.run(main())
