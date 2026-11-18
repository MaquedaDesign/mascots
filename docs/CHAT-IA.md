# Chat con IA

## Servidor

- La app nunca lleva la clave. Pasa por un proxy en el servidor (en CardIt, una Edge Function de Supabase) que comprueba la cuenta, los créditos y los límites.
- Modelo previsto: Claude Haiku 5.5, a 0,10 $/MTok de entrada y 0,50 $ de salida (hasta 100K de contexto), con lectura de caché a 0,01 $/MTok.
- Google Play exige poder reportar respuestas de IA generativa desde la app.
- La Ley de IA de la UE (art. 50) obliga a avisar de que es un chatbot desde el 2-8-2026.

## Prompt

Todo lo que lee la IA va en inglés porque gasta menos: normas, formato, personalidad, historia e información de la app. Las muletillas de cada personaje se quedan en español, que es su voz. La IA responde en el idioma del jugador (por defecto, español de España).

Secciones de las normas: SCOPE, STYLE, LANGUAGE, CREATING DECKS AND MODES y MEMORY.

- **Estilo**: normalmente un mensaje y dos solo si hace falta; contestar corto a mensajes cortos; preguntar solo si aporta; la personalidad se reparte en la conversación, no en cada respuesta.
- **Código**:
  - Junta la respuesta en 2 burbujas como mucho.
  - Quita el sticker si la respuesta trae varios mensajes o si ya hubo otro en las últimas 3 respuestas.
  - Filtra lo sensible antes de guardarlo en memoria.
- **Voz por personaje**:
  - Valiente es seco, casi no pregunta y saca faroles, trampas y cómo pillarlas.
  - Viva es ligera.
  - Tranquila, pausada.
  - Tímida, dudosa.

Formato de salida (JSON):

```json
{"emotion":"neutral|happy|sad|scared|angry|surprised|love","messages":["…"],"sticker":null,
 "memory":[{"op":"add","topic":"mus","en":"Loves mus.","text":"Le encanta el mus."},{"op":"edit","id":"m3","en":"…","text":"…"},{"op":"forget","id":"m3"}],
 "summaries":{"mus":{"title":"Mus","en":"…","text":"…"}},
 "topic":null, "point":null}
```

`topic` solo se pide en chats sin tema y `point` solo cuando va la mesa.

## Memoria por temas

- `profile` guarda lo que vale para todo (cómo llamarle, cómo quiere que le ayuden).
- Cada juego o tema tiene un resumen corto y datos telegráficos de unas 8 palabras.
- Cada dato se guarda en inglés, que es lo que lee la IA y sirve para detectar duplicados aunque cambie el idioma, y traducido, que es lo que ve el jugador. Con el título del tema pasa igual.
- A la IA le llega el índice de temas, `profile`, el tema del chat y los temas que se nombren en el mensaje.
- Si un dato cambia, la IA lo edita por id y el código evita duplicar.
- Borrar un tema borra su chat; borrar un chat no borra la memoria.

## Chats

- **General**: no tiene memoria propia. Tras 3 h sin uso aparece la línea «Conversación nueva» y la IA solo ve desde ahí. Si la conversación se centra en un tema con memoria, lo hablado desde esa línea pasa al chat del tema.
- **+ Chat**: chat nuevo y permanente. Se asocia a un tema cuando aparece algo que recordar, y crea el tema si no existe. Si hay varios chats del mismo tema se numeran.
- El historial se queda en el dispositivo y a la IA solo le llegan los últimos 8 mensajes.
- El menú de cada pestaña permite vaciar el chat, ver su memoria y eliminar el chat (salvo General).
- La marca de color de cada respuesta es la de la mascota que la escribió.

## Energía

- 7.500 créditos por semana, unos 3 € al mes de IA por usuario. 1 crédito = 0,0001 $.
- Ventanas de uso: como mucho el 30 % de la semana cada 5 h y el 5 % cada 5 min. Se configuran en el estudio.
- Lo que no se gasta en la semana no se acumula.
- **Extra**: paquetes que no caducan y solo se usan al agotarse la semana. Se muestran en tokens, con la media del jugador cada 5 min de uso.
- Pantalla: barra de lo gastado con las ventanas de 5 h y 5 min marcadas encima.

## Ahorro de tokens

Por orden de impacto: guardar en caché la parte fija, normas en inglés y recortar normas. Se puede medir con `count_tokens` de la API. Escribir las normas en chino no ahorra.

## Tareas sugeridas

- Crear un juego: guía con una pregunta cada vez.
- ¿Juegas conmigo?: se sienta en la partida y, si no hay árbitro, pregunta a qué se juega.
- Ayúdame con la partida: recibe la mesa, aconseja y señala una carta.

Viabilidad:
- Tutoriales y señalar: viables.
- «Juega conmigo»: lo más complejo (herramientas, turnos, coste por turno). Mejor empezar con juegos con árbitro.
