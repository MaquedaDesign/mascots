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

Hecho en CardIt (fase M1, 18-11-2026, `app/src/mascotas/`): **vistas + Reanimated + react-native-svg, sin Skia** (CardIt
no usa Skia: con muchas piezas iba peor que las vistas).
- Cada pieza es una vista con su imagen; su matriz se pasa a `translate`, `rotate`, `skewX` y `scale` alrededor de su
  centro (`aTransformacion`), sin `matrix` ni `transformOrigin`.
- Todo se calcula en el hilo de la interfaz (`useFrameCallback`) con funciones puras con `'worklet'`, que también se
  prueban con Node: esqueleto, cerebro (qué hace), vida (lo que se mueven las piezas) y un «cuadro» por fotograma (una
  lista de números que leen todas las vistas).
- Delante y detrás: cada pieza está dos veces y se enciende la que toca; lo de detrás va en una caja con `overflow:
  hidden` que recorta por el borde de la superficie. El orden de pintado solo cambia con la pose (sin `zIndex` animado).
- La cara, con react-native-svg dentro de la vista de la cabeza (se mueve con ella); el parpadeo, una escala de vista.
- Las superficies se apuntan desde las vistas de la app (`useSuperficie`) y se miden en la ventana.
- Sin botes (regla de CardIt): saltos por curvas suaves, sin rebotar ni aplastarse.

Falta pasarlo de CardIt a `engine/` (y copiarlo a las apps como el kit), y las habilidades.
