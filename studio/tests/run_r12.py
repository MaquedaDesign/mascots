import os, pathlib
HERE = pathlib.Path(__file__).resolve().parent
DIST = (HERE.parent / "dist" / "mascotas.html").as_uri()
SHOTS = HERE / "shots"; SHOTS.mkdir(exist_ok=True)
CHROME = {"executable_path": os.environ["CHROME"]} if os.environ.get("CHROME") else {}
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(**CHROME, args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':1440,'height':900}, device_scale_factor=1)
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(DIST+'?fresh&noai')
        await pg.evaluate("localStorage.clear()"); await pg.reload(); await pg.wait_for_timeout(1000)
        M=lambda id: f"MAS.mascots.find(m=>m.id==='{id}')"
        # pez colgado → tiburón en el panel
        await pg.evaluate(M('azul')+".goHang(MAS.panels[1])"); await pg.wait_for_timeout(1800)
        print('fish', await pg.evaluate(M('azul')+".mode"), await pg.evaluate(M('azul')+".useAbility('shark')"))
        await pg.wait_for_timeout(1400)
        r=await pg.evaluate("(()=>{const p=MAS.panels[1];return [p.x,p.y,p.w,p.h]})()")
        await pg.screenshot(path=str(SHOTS/'d1.png'), clip={'x':max(0,r[0]-40),'y':max(0,r[1]-90),'width':r[2]+80,'height':160})
        # ajolote colgado pierde pieza
        await pg.evaluate(M('morado')+".goHang(MAS.panels[0])"); await pg.wait_for_timeout(1800)
        print('regen', await pg.evaluate(M('morado')+".useAbility('regen')"), await pg.evaluate(M('morado')+".ab&&"+M('morado')+".ab.part"))
        await pg.wait_for_timeout(500)
        r=await pg.evaluate("(()=>{const p=MAS.panels[0];return [p.x,p.y,p.w,p.h]})()")
        await pg.screenshot(path=str(SHOTS/'d2.png'), clip={'x':max(0,r[0]-60),'y':max(0,r[1]-60),'width':r[2]+120,'height':r[3]+300})
        await pg.wait_for_timeout(3500)
        # camaleón camuflado delante del panel de mesa (fondo no plano)
        await pg.evaluate(M('verde')+".goStand(MAS.panels[0],140)"); await pg.wait_for_timeout(1500)
        await pg.evaluate(M('verde')+".useAbility('camo',{kind:'hide'})"); await pg.wait_for_timeout(1800)
        await pg.screenshot(path=str(SHOTS/'d3.png'), clip={'x':max(0,r[0]-60),'y':max(0,r[1]-200),'width':r[2]+120,'height':r[3]+220})
        await pg.evaluate(M('verde')+".endAbility()")
        # tutorial
        await pg.evaluate("MAS.startTutorial(MAS.DEMO_TUT,"+M('naranja')+")"); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=str(SHOTS/'d4.png'))
        await pg.click('.panel .fake-btn.pri'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=str(SHOTS/'d5.png'))
        await pg.click('.tut-next'); await pg.wait_for_timeout(1500); await pg.screenshot(path=str(SHOTS/'d6.png')); await pg.click('.tut-next'); await pg.wait_for_timeout(300)
        print('tut on after', await pg.evaluate("document.querySelectorAll('.tut-ring').length"))
        print('errors',errs); await b.close()
asyncio.run(main())
