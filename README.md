# Mascotas

Sistema de mascotas animadas para las apps de Quadmoon. Empezó con los cuatro personajes de CardIt.

La idea es un **motor genérico** que cada app usa con sus propios personajes ya configurados. La herramienta para preparar personajes (recortes, anclajes, caras) es el **estudio** y nunca va dentro de una app.

## Estructura

| Carpeta | Qué es |
|---|---|
| `studio/` | Banco de pruebas y herramienta web: probar personajes, poses, caras, habilidades, chat con IA, energía y tutoriales. Hoy contiene también el prototipo del motor y del chat. |
| `packs/cardit/` | Personajes de CardIt: piezas recortadas (`parts/`), configuración (`rig.json`) y la hoja original (`source/sheet.png`). |
| `engine/` | Aquí irá el motor separado del estudio (ver `engine/README.md`). |
| `docs/` | Decisiones y diseño: `ARQUITECTURA.md`, `CHAT-IA.md`, `PENDIENTE.md`. |

## Uso rápido

```bash
cd studio
python3 build.py          # genera dist/mascotas.html con las piezas incrustadas
```

Abre `studio/dist/mascotas.html` en el navegador. Sin la capacidad de IA del artefacto, el chat responde con ejemplos. Parámetros útiles en la URL: `?noai` (sin movimiento automático) y `?fresh`.

Pruebas (Playwright + Chrome): `python3 tests/run_mem2.py`. Las capturas quedan en `tests/shots/`. Se puede indicar Chrome con la variable `CHROME=/ruta/a/chrome`.

## Estado

Es un prototipo web funcional: 4 personajes, poses, caras vectoriales y expresiones, giro 2.5D, personalidades, habilidades, chat con IA (memoria por temas, chats por tema, energía y límites), señalar cartas y tutoriales guiados.

El paso siguiente es separar el motor y pasarlo a React Native (ver `docs/PENDIENTE.md`). Este repo no usa GitHub Actions.
