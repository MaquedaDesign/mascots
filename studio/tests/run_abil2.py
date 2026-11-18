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
        # dragón colgado de un panel
        await pg.evaluate(M('naranja')+".goHang(MAS.panels[0])"); await pg.wait_for_timeout(1800)
        print('drag mode',await pg.evaluate(M('naranja')+".mode"), await pg.evaluate(M('naranja')+".useAbility('fire')"))
        await pg.wait_for_timeout(1100)
        r=await pg.evaluate("(()=>{const p=MAS.panels[0];return [p.x,p.y,p.w,p.h]})()")
        await pg.screenshot(path=str(SHOTS/'c1.png'), clip={'x':max(0,r[0]-150),'y':max(0,r[1]-60),'width':r[2]+300,'height':r[3]+260})
        await pg.wait_for_timeout(1500)
        # pez sobre un panel
        await pg.evaluate(M('azul')+".goStand(MAS.panels[1])"); await pg.wait_for_timeout(1800)
        print('fish', await pg.evaluate("(()=>{const m="+M('azul')+";return [m.mode,m.onGround,!!m.plat]})()"), await pg.evaluate(M('azul')+".useAbility('shark')"))
        await pg.wait_for_timeout(1300)
        r=await pg.evaluate("(()=>{const p=MAS.panels[1];return [p.x,p.y,p.w,p.h]})()")
        await pg.screenshot(path=str(SHOTS/'c2.png'), clip={'x':max(0,r[0]-40),'y':max(0,r[1]-90),'width':r[2]+80,'height':160})
        for i in range(40):
            st=await pg.evaluate("(()=>{const m="+M('azul')+";return [m.ab?m.ab.phase:null,m.mode,!!m.plat,m.onGround]})()")
            if st[0] is None and st[3]: break
            await pg.wait_for_timeout(250)
        print('fish after',st)
        # camaleón camuflado
        print('camo',await pg.evaluate(M('verde')+".useAbility('camo',{kind:'hide'})")); await pg.wait_for_timeout(1600)
        x=await pg.evaluate("Math.round("+M('verde')+".x)")
        await pg.screenshot(path=str(SHOTS/'c3.png'), clip={'x':max(0,x-200),'y':640,'width':400,'height':260})
        await pg.evaluate(M('verde')+".endAbility()")
        print('mimic',await pg.evaluate(M('verde')+".useAbility('camo',{kind:'mimic'})")); await pg.wait_for_timeout(1600)
        await pg.screenshot(path=str(SHOTS/'c4.png'), clip={'x':max(0,x-200),'y':640,'width':400,'height':260})
        await pg.evaluate(M('verde')+".endAbility()")
        # ajolote pierde el brazo
        print('regen',await pg.evaluate(M('morado')+".useAbility('regen')")); await pg.wait_for_timeout(700)
        x=await pg.evaluate("Math.round("+M('morado')+".x)")
        await pg.screenshot(path=str(SHOTS/'c5.png'), clip={'x':max(0,x-250),'y':620,'width':500,'height':280})
        await pg.wait_for_timeout(1300)
        await pg.screenshot(path=str(SHOTS/'c6.png'), clip={'x':max(0,x-250),'y':620,'width':500,'height':280})
        await pg.wait_for_timeout(2500)
        print('regen done', await pg.evaluate("(()=>{const m="+M('morado')+";return [!!m.ab,m.el.armF.style.visibility,document.querySelectorAll('.limb').length]})()"))
        print('errors',errs); await b.close()
asyncio.run(main())
