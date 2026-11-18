# Arquitectura

## Tres piezas separadas

1. **Motor de mascotas**: dibuja, anima y mueve. No sabe nada de IA.
2. **Chat con IA**: interfaz del chat y servidor (normas, memoria, energía). Funcionaría sin mascota. La parte de servidor es de cada app; en CardIt va en Supabase.
3. **Puente**: traduce cada respuesta de la IA en acciones de la mascota (emoción → cara, hablar, sticker, señalar, habilidades). Además pasa a la IA la personalidad que viene en el pack.

En el estudio las tres están juntas en `template.html`. Al pasarlas a la app hay que separarlas.

## Motor

- **Esqueleto 2D de 7 piezas**: cabeza, cuerpo, 2 brazos, 2 patas y cola, más ojos y boca vectoriales aparte. Usa jerarquía: patas y cuerpo cuelgan de la raíz; cabeza, brazos y cola del cuerpo. Cada pieza tiene su pivote. Las poses (`stand`, `hang`, `sleep`, `peek`) se definen en espacio raíz.
- **Animación procedural**: sin fotogramas. Respiración, andar, aire, arrastre, colgar, dormir y asomarse, con estirar y encoger.
- **Giro 2.5D**: espejo más estrechamiento; los rasgos de la cara se mueven sobre una esfera; de espaldas se oculta la cara.
- **Caras**: expresiones normal, alegre, triste, asustada, enfadada, sorprendida, dormida y enamorada; parpadeo, mirada y boca que habla.
- **Capas**: delante y detrás de los paneles, con recorte al panel y orden de pintado por pose. Las patas van siempre detrás; al colgar, las manos van detrás de la cabeza.
- **Personalidades** (`PERSONAS`): velocidad, salto, pesos de cada decisión, reacción al cursor y expresión al arrastrar.
- **Frases sueltas** (`LINES`): guionizadas, sin coste de tokens.

## Formato del personaje (pack)

`rig.json` lleva, por personaje: pivotes (`pv`), colocación por pose, cara (ojos, boca, estilo de ojo, rubor), personalidad, historia, voz y `abilities`. Las imágenes son PNG por pieza; la cabeza va con y sin cara (`head_clean`).

## Habilidades (extensiones)

Fuera del núcleo. Cada app registra las que necesita y cada personaje declara las suyas.

```js
registerAbility('fire', {
  label, variants?, scare?,      // scare: probabilidad de lanzarse al asustarse
  can(m, opts),                  // ¿se puede ahora?
  start(m, ab), update(m, dt, ab) /* false = terminar */, animate(m, A, ab), end(m, ab)
});
mascota.useAbility('fire'); mascota.endAbility();
```

Ganchos que ofrece el núcleo:
- `mode = 'ability'`: la habilidad toma el control del movimiento.
- `ab.free`: deja actuar la IA de movimiento a la vez.
- `ab.clip`: recorte.
- `mouthForce`: forzar una forma de boca.
- `fadeK`: sombra.
- `fxDot`: partículas.
- Filtros de color por mascota (`setTint`).

Habilidades actuales:
- `camo` (camaleón): camuflarse con el fondo o copiar el color de otra mascota.
- `fire` (dragón): escupir fuego.
- `shark` (pez): nadar con solo la aleta fuera, en el suelo o en un panel.
- `regen` (ajolote): pierde una pieza visible según la pose y le vuelve a crecer; 30 % al asustarse.

## Señalar y tutoriales

- `pointCard(m, id)`: la mascota salta encima del elemento y lo resalta; luego vuelve.
- `startTutorial(pasos, mascota)`: oscurece todo menos el objetivo y bloquea los clics fuera de él. La mascota se coloca al lado con un bocadillo; el bocadillo busca un sitio que no tape el objetivo. Los pasos son datos:

```js
{ target: '#selector' | () => elemento, text: '…', next: 'click' | 'button', pad?: 8 }
```

## Mapa de la interfaz (para el final)

Sirve para que la IA pueda explicar y señalar cualquier cosa:
- **Objetivos**: cada elemento importante tiene un id fijo y una etiqueta corta (`mazo.barajar` → «Barajar»). En React Native puede ser un envoltorio `<Target>`, o el `testID` y la etiqueta de accesibilidad.
- **Anclajes**: dónde puede ponerse la mascota en cada objetivo.
- **Pantallas**: id, descripción y cómo se llega.
- **La IA** recibe solo los objetivos de la pantalla actual y devuelve acciones: señalar, ir a una pantalla o una secuencia de pasos. La app valida los ids. La IA nunca pulsa por el usuario.

Desde ya conviene ir poniendo ids estables a los elementos clave.

## Paso a React Native

El motor es DOM y CSS. Hay dos caminos:
- **React Native Skia + Reanimated** (recomendado): el esqueleto son matrices y se dibuja igual. Las caras pasan de SVG a trazos de Skia y las partículas a Skia.
- **WebView encima de la app**: más rápido de montar, pero peor integrado (toques, rendimiento, capas con la interfaz nativa).

Se porta tal cual: matrices, poses, IA de movimiento, personalidades, habilidades (cambiando el DOM por el lienzo) y el formato del pack.
