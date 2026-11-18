import pathlib
P = pathlib.Path(__file__).resolve().parents[2] / "packs" / "cardit" / "parts"
import numpy as np, cv2, sys
from PIL import Image
def ell(m,cx,cy,rx,ry,ang=0):
    cv2.ellipse(m,(int(cx),int(cy)),(int(rx),int(ry)),ang,0,360,255,-1)
masks={
 'verde':[('e',119,129,39,46),('e',38,161,26,11)],
 'azul':[('e',122,145,36,45),('e',41,167,23,10)],
 'morado':[('e',75,145,20,31),('e',193,148,23,33),('e',130,172,27,10)],
 'naranja':[('p',[(86,142),(90,137),(150,101),(163,108),(167,150),(162,182),(140,190),(108,188),(92,172)]),('p',[(80,147),(87,158),(158,118),(152,102)]),('split',[(37,189),(106,189),(106,214),(37,214)])],
}
for c,ms in masks.items():
    im=np.array(Image.open(f'{P}/{c}_head.png'))
    rgb=im[...,:3].copy(); a=im[...,3]
    m=np.zeros(a.shape,np.uint8); split=None
    for t in ms:
        if t[0]=='e': ell(m,*t[1:])
        elif t[0]=='p': cv2.fillPoly(m,[np.array(t[1])],255)
        else: cv2.fillPoly(m,[np.array(t[1])],255); split=t[1]
    m[a<250]=0
    out=cv2.inpaint(rgb,m,6,cv2.INPAINT_TELEA).astype(np.float32)
    keep=np.zeros(m.shape,bool)
    if split is not None:
        orange=rgb[185,70].astype(np.float32); cream=rgb[212,120].astype(np.float32)
        for y in range(189,215):
            for x in range(37,107):
                if m[y,x]==0: continue
                seam=204-(x-37)*(9/69)
                t=np.clip((y-seam)/2.0+0.5,0,1)
                out[y,x]=orange*(1-t)+cream*t
        keep[189:215,37:107]=True
    mk=m>0; upd=mk&~keep
    for _ in range(800):
        avg=(np.roll(out,1,0)+np.roll(out,-1,0)+np.roll(out,1,1)+np.roll(out,-1,1))/4
        out[upd]=avg[upd]
    rng=np.random.default_rng(1)
    noise=cv2.GaussianBlur(rng.normal(0,3.0,out.shape[:2]).astype(np.float32),(0,0),1.2)
    out[mk]+=noise[mk][:,None]
    res=np.dstack([out.clip(0,255).astype(np.uint8),a])
    Image.fromarray(res).save(f'{P}/{c}_head_clean.png')
ims=[]
for c in masks:
    r=Image.open(f'{P}/{c}_head_clean.png'); bg=Image.new('RGBA',r.size,(60,60,60,255)); bg.alpha_composite(r); ims.append(bg)
W=sum(i.width for i in ims)+30; H=max(i.height for i in ims)
p=Image.new('RGBA',(W,H),(60,60,60,255)); x=0
for i in ims: p.paste(i,(x,0)); x+=i.width+10
p.save('clean_all.png')
