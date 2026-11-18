import pathlib
import asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--no-sandbox'])
        pg=await b.new_page()
        await pg.goto((pathlib.Path(__file__).resolve().parents[1]/'dist'/'mascotas.html').as_uri()+'?noai')
        data=await pg.evaluate("""(()=>{
          const AK={tail:'tail',legB:'leg_R',legF:'leg_L',armB:'arm_R',armF:'arm_L',head:'head_clean',body:'body'};
          const PARENT={body:null,legF:null,legB:null,head:'body',armF:'body',armB:'body',tail:'body'};
          const out={units:'px de la hoja original (escala 1)',drawOrder:'z mayor = delante; layer f = delante del panel, b = detrás',
            parents:PARENT,characters:{}};
          for(const [id,C] of Object.entries(MAS.CHARS)){
            const parts={};for(const k of Object.keys(AK))parts[k]={file:`${id}_${AK[k]}.png`,w:C.sz[k].w,h:C.sz[k].h,pivot:C.pv[k]};
            const poses={};for(const [n,P] of Object.entries(C.poses)){poses[n]={};for(const [k,v] of Object.entries(P))poses[n][k]={x:+v.ax.toFixed(1),y:+v.ay.toFixed(1),rot:+v.rot.toFixed(1),layer:v.layer,z:v.z}}
            out.characters[id]={name:C.name,species:C.species,color:C.color,parts,headWithFace:`${id}_head.png`,poses,
              face:{artAngle:C.face.phi0,radius:C.face.Rf,features:C.feats.map(f=>({type:f.type,x:+(f.x??NaN).toFixed?.(1)??null,y:f.y,rx:f.rx,ry:f.ry,azimuth:f.a,centerX:+f.hx.toFixed(1),rot:f.rot})),
                eye:C.face.eye,mouth:C.face.mouth,ink:C.eyeInk,skin:C.skin},
              personality:C.pers};
          }
          return out;})()""")
        json.dump(data,open(pathlib.Path(__file__).resolve().parents[2]/'packs'/'cardit'/'rig.json','w'),ensure_ascii=False,indent=1)
        await b.close()
asyncio.run(main())
