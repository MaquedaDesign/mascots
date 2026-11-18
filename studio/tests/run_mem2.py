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
        await pg.add_init_script(FAKE)
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append('c:'+m.text) if m.type=='error' else None)
        await pg.goto(DIST+'?fresh&noai')
        await pg.evaluate("localStorage.clear()"); await pg.reload(); await pg.wait_for_timeout(600)
        await pg.evaluate("MAS.openChat(MAS.mascots[2])"); await pg.wait_for_timeout(1000)
        clip={'x':700,'y':300,'width':520,'height':580}
        async def send(t,w=2200):
            await pg.fill('.cform input',t); await pg.press('.cform input','Enter'); await pg.wait_for_timeout(w)
        await send('hola')
        await send('me encanta el mus')
        await pg.screenshot(path=str(SHOTS/'t1.png'), clip=clip)
        print('tabs',await pg.evaluate("[...document.querySelectorAll('.tbar button')].map(b=>b.textContent+(b.classList.contains('on')?'*':''))"))
        txt=await pg.evaluate("window.__in[0].content"); i=txt.index('WHAT YOU KNOW'); print(txt[i:i+200])
        await send('juego con mi hermano los domingos')
        txt=await pg.evaluate("window.__in[0].content"); print('typed fmt has topic:', '"topic": null' in txt); open(SHOTS/'prompt.txt','w').write(txt)
        await pg.click('.tbar [data-th=general]'); await pg.wait_for_timeout(300)
        await send('hola')
        await pg.click('.tbar .tnew'); await pg.wait_for_timeout(300)
        print('tabs',await pg.evaluate("[...document.querySelectorAll('.tbar button')].map(b=>b.textContent+(b.classList.contains('on')?'*':''))"))
        # sticker gg overflow
        await pg.evaluate("document.querySelector('.stkbtn').click()"); await pg.wait_for_timeout(200)
        await pg.click('.stkpick [data-stk=gg]'); await pg.wait_for_timeout(1500)
        for k in range(6):
            ov=await pg.evaluate("(()=>{const m=document.querySelector('.msgs');return [m.scrollWidth,m.clientWidth]})()"); 
            if ov[0]>ov[1]: print('OVERFLOW',ov)
            await pg.wait_for_timeout(250)
        await pg.screenshot(path=str(SHOTS/'t2.png'), clip=clip)
        # menú de la pestaña activa (Chat nuevo) y eliminarla
        await pg.click('.tbar .on'); await pg.wait_for_timeout(200); await pg.screenshot(path=str(SHOTS/'t8.png'), clip=clip)
        await pg.click('.tmenu [data-m=del]'); await pg.click('.tmenu [data-m=del]'); await pg.wait_for_timeout(200)
        print('tabs',await pg.evaluate("[...document.querySelectorAll('.tbar button')].map(b=>b.textContent+(b.classList.contains('on')?'*':''))"))
        # memoria
        await pg.click('.cmem'); await pg.wait_for_timeout(300)
        await pg.evaluate("document.querySelectorAll('.memview details').forEach(d=>d.open=true)")
        await pg.click('.memview li .mforget'); await pg.wait_for_timeout(150); await pg.screenshot(path=str(SHOTS/'t3.png'), clip=clip)
        await pg.click('.memview li .mforget.sure'); await pg.wait_for_timeout(150)
        await pg.click('.memview [data-deltopic=mus]'); await pg.click('.memview [data-deltopic=mus]'); await pg.wait_for_timeout(150)
        print('after delete mus', await pg.evaluate("Object.keys(JSON.parse(localStorage.getItem('mascotas-memoria-temas')))"))
        # volver pulsando la cabecera a la izquierda
        await pg.mouse.click(1000, 400); await pg.wait_for_timeout(150)
        print('view', await pg.evaluate("MAS.chat?MAS.chat.view:'?'"))
        await pg.click('.cen'); await pg.wait_for_timeout(300); await pg.click('.ev-avg'); await pg.wait_for_timeout(150); await pg.screenshot(path=str(SHOTS/'t4.png'), clip=clip)
        hb=await pg.evaluate("(()=>{const r=document.querySelector('.chatp header').getBoundingClientRect();return [r.left+40,r.top+r.height/2]})()")
        await pg.mouse.click(hb[0],hb[1]); await pg.wait_for_timeout(150)
        print('view after header click', await pg.evaluate("document.querySelector('.enview').hidden"))
        await pg.screenshot(path=str(SHOTS/'t9.png'), clip=clip)
        print('errors',errs); await b.close()
asyncio.run(main())
