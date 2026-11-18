import os, pathlib
HERE = pathlib.Path(__file__).resolve().parent
DIST = (HERE.parent / "dist" / "mascotas.html").as_uri()
SHOTS = HERE / "shots"; SHOTS.mkdir(exist_ok=True)
CHROME = {"executable_path": os.environ["CHROME"]} if os.environ.get("CHROME") else {}
import asyncio
from playwright.async_api import async_playwright
FAKE = """
window.claude={use:async(n)=>{ if(n!=='sample') return null;
  const f=async()=>({text:'x',truncated:false});
  f.json=async(input,opts)=>{ window.__in=input; await new Promise(r=>setTimeout(r,300));
    const u=input[input.length-1].content.toLowerCase();
    if(u.includes('encanta el mus')) return {emocion:'alegre',mensajes:['¡El mus mola! ¿En pareja?'],sticker:null,memoria:[{accion:'añadir',tema:'mus',titulo:'Mus',texto:'Le encanta el mus.'}],resumen_tema:{mus:'Le encanta el mus.'},tema:'mus'};
    if(u.includes('domingos')) return {emotion:'happy',messages:['¡Qué equipazo!'],sticker:null,memory:[{op:'add',topic:'mus',en:'Plays in a pair with his brother on Sundays.',text:'Juega en pareja con su hermano los domingos.'},{op:'add',topic:'profile',en:'Prefers short replies.',text:'Prefiere respuestas cortas.'}],summaries:{mus:{en:'Loves mus; plays with his brother on Sundays.',text:'Le encanta el mus; juega con su hermano los domingos.'}}};
    return {emocion:'normal',mensajes:['¡Hola! ¿Qué tal?'],sticker:null,memoria:[],resumen_tema:{},tema:null};
  };
  return f; }};
"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(**CHROME, args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':1440,'height':900}, device_scale_factor=2)
        await pg.add_init_script(FAKE); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(DIST+'?fresh&noai')
        await pg.evaluate("localStorage.clear()"); await pg.reload(); await pg.wait_for_timeout(600)
        clip={'x':700,'y':300,'width':520,'height':580}
        async def send(t,w=2000):
            await pg.fill('.cform input',t); await pg.press('.cform input','Enter'); await pg.wait_for_timeout(w)
        await pg.evaluate("MAS.openChat(MAS.mascots[3])"); await pg.wait_for_timeout(900)
        await send('hola')
        await pg.evaluate("MAS.closeChat()"); await pg.evaluate("MAS.openChat(MAS.mascots[1])"); await pg.wait_for_timeout(900)
        await send('¿qué tal?')
        # General caducado: separador y la IA no ve lo anterior
        await pg.evaluate("(()=>{const h=JSON.parse(localStorage.getItem('mascotas-hilos'));h.find(t=>t.id==='general').last=Date.now()-4*3600e3;localStorage.setItem('mascotas-hilos',JSON.stringify(h))})()")
        await pg.reload(); await pg.wait_for_timeout(600)
        await pg.evaluate("MAS.openChat(MAS.mascots[0])"); await pg.wait_for_timeout(900)
        await pg.screenshot(path=str(SHOTS/'v1.png'), clip=clip)
        # + Chat abre uno nuevo
        await pg.click('.tbar .tnew'); await pg.wait_for_timeout(300)
        await send('me encanta el mus')
        await pg.screenshot(path=str(SHOTS/'v2.png'), clip=clip)
        print('tabs',await pg.evaluate("[...document.querySelectorAll('.tbar button')].map(b=>b.textContent+(b.classList.contains('on')?'*':''))"))
        await pg.click('.tbar .tnew'); await pg.wait_for_timeout(300)
        print('tabs',await pg.evaluate("[...document.querySelectorAll('.tbar button')].map(b=>b.textContent+(b.classList.contains('on')?'*':''))"))
        await pg.click('.cen'); await pg.wait_for_timeout(300); await pg.screenshot(path=str(SHOTS/'v3.png'), clip=clip)
        print('errors',errs); await b.close()
asyncio.run(main())
