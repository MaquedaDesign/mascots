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
        errs=[]
        for vw,name in [((1440,900),'b1'),((390,780),'b2')]:
            pg=await b.new_page(viewport={'width':vw[0],'height':vw[1]}, device_scale_factor=2)
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(DIST+'?fresh&noai')
            await pg.evaluate("localStorage.clear()"); await pg.reload(); await pg.wait_for_timeout(500)
            await pg.evaluate("""(()=>{const n=Date.now(),W=7500;localStorage.setItem('mascotas-uso',JSON.stringify({weekStart:(()=>{const d=new Date(n);const k=(d.getDay()+6)%7;d.setHours(0,0,0,0);d.setDate(d.getDate()-k);return d.getTime()})(),
              log:[{t:n-26*3600e3,c:W*.25},{t:n-2*3600e3,c:W*.08},{t:n-60e3,c:W*.02}],packs:2000,dayOk:0,avg:{cr:1.8,tok:1500,n:12}}))})()""")
            await pg.reload(); await pg.wait_for_timeout(500)
            await pg.evaluate("MAS.openChat(MAS.mascots[0])"); await pg.wait_for_timeout(900)
            await pg.click('.cen'); await pg.wait_for_timeout(300)
            if name=='b1': await pg.screenshot(path=f'out/{name}.png', clip={'x':700,'y':300,'width':520,'height':580})
            else: await pg.screenshot(path=f'out/{name}.png')
            await pg.close()
        print('errors',errs); await b.close()
asyncio.run(main())
