import os, pathlib
HERE = pathlib.Path(__file__).resolve().parent
DIST = (HERE.parent / "dist" / "mascotas.html").as_uri()
SHOTS = HERE / "shots"; SHOTS.mkdir(exist_ok=True)
CHROME = {"executable_path": os.environ["CHROME"]} if os.environ.get("CHROME") else {}
import asyncio
from playwright.async_api import async_playwright
FAKE="""window.claude={use:async(n)=>{if(n!=='sample')return null;const f=async()=>({text:'x'});
 f.json=async(input)=>{window.__in=input;await new Promise(r=>setTimeout(r,300));const u=input[input.length-1].content;
  if(/Ayúdame/.test(u))return {emotion:'happy',messages:['Yo jugaría el 3 de espadas.'],sticker:null,memory:[],point:'c3'};
  return {emotion:'neutral',messages:['Vale.'],sticker:null,memory:[]}};return f}};"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(**CHROME, args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':1440,'height':900}, device_scale_factor=1)
        await pg.add_init_script(FAKE); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(DIST+'?fresh&noai')
        await pg.evaluate("localStorage.clear()"); await pg.reload(); await pg.wait_for_timeout(700)
        await pg.evaluate("MAS.openChat(MAS.mascots[3])"); await pg.wait_for_timeout(1000)
        print('sugs',await pg.evaluate("[...document.querySelectorAll('.sugs button')].map(b=>b.textContent+'|'+(b.dataset.mode||''))"))
        await pg.click('.sugs [data-mode=help]'); await pg.wait_for_timeout(2600)
        await pg.screenshot(path=str(SHOTS/'e1.png'))
        txt=await pg.evaluate("window.__in[0].content"); print('TASK' in txt, 'TABLE' in txt, '"point": null' in txt)
        await pg.wait_for_timeout(5000)
        print('back to chat', await pg.evaluate("[MAS.mascots[3].mode,MAS.mascots[3].attach&&MAS.mascots[3].attach.kind]"))
        await pg.click('.tbar .on'); await pg.wait_for_timeout(200)
        print('align', await pg.evaluate("(()=>{const a=document.querySelector('.tbar .on').getBoundingClientRect(),b=document.querySelector('.tmenu').getBoundingClientRect();return [a.left,b.left,a.bottom,b.top]})()"))
        print('errors',errs); await b.close()
asyncio.run(main())
