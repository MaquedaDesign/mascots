"""Genera dist/mascotas.html: el estudio en un solo archivo, con las piezas del pack incrustadas.
Uso: python3 build.py [ruta/al/pack]   (por defecto ../packs/cardit)"""
import base64, io, json, pathlib, sys
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent
PACK = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT.parent / 'packs' / 'cardit'
CHARS = ['verde', 'azul', 'morado', 'naranja']
KEYS = ['head_clean', 'head', 'body', 'arm_L', 'arm_R', 'leg_L', 'leg_R', 'tail']
assets = {}
for c in CHARS:
    assets[c] = {}
    for k in KEYS:
        im = Image.open(PACK / 'parts' / f'{c}_{k}.png').convert('RGBA')
        b = io.BytesIO(); im.save(b, 'WEBP', quality=92, method=6)
        assets[c][k] = {'w': im.width, 'h': im.height, 'src': 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()}
html = (ROOT / 'template.html').read_text().replace('/*ASSETS*/', 'window.ASSETS=' + json.dumps(assets) + ';')
(ROOT / 'dist').mkdir(exist_ok=True)
(ROOT / 'dist' / 'mascotas.html').write_text(html)
print('dist/mascotas.html', len(html) // 1024, 'KB')
