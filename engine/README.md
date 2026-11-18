# engine (por hacer)

Aquí irá el motor separado del estudio. Es lo único que instalan las apps.

API prevista:

```js
const stage = createStage({ pack, container })        // pack: rig.json + imágenes
const m = stage.add('verde')                           // una mascota del pack
m.setExpression('alegre', segundos); m.say('texto')
m.goTo({ panel, pose: 'stand' | 'hang' | 'sleep' | 'peek' })
m.useAbility('camo', { kind: 'hide' })
stage.registerAbility(nombre, def)                     // extensiones propias de cada app
stage.point(objetivo); stage.tutorial(pasos)
stage.on('tap', m => abrirChat(m))
```

Hoy todo esto está en `studio/template.html`. Para separarlo:
- Del motor: clase `Mascot`, matrices, `PERSONAS`, caras (`eyeSVG`, `mouthSVG`), habilidades, `pointCard` y tutoriales.
- Del estudio: el panel lateral (Probar y Taller) y las herramientas de recorte.
- Del chat (en cada app): `chatPanel`, memoria, energía y prompt.
