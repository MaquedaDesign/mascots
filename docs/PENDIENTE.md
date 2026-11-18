# Pendiente

## Nombres de los personajes

Por ahora siguen Viva, Tranquila, Tímida y Valiente (que son también los nombres de las personalidades). Se busca nombres propios internacionales. Propuestas:

| Personaje | Propuestas |
|---|---|
| Camaleón lima (alegre) | Ivy, Kiki, Zoe |
| Pez cian (tranquilo) | Marina, Nami, Maya |
| Ajolote lila (tímido) | Momo, Lily, Yumi |
| Dragón coral (rebelde) | Ash, Rex, Kai, Drake |

Al decidirlos, cambiarlos también en las historias (`STORIES` y `STORIES_EN`), porque se nombran entre ellos.

## Próximos pasos

1. Separar el motor del estudio en `engine/`: esqueleto, poses, caras, comportamiento, habilidades, señalar y tutoriales.
2. ~~Pasarlo a React Native~~: hecho en CardIt con vistas, Reanimated y react-native-svg, sin Skia (ver `ARQUITECTURA.md`);
   falta traerlo aquí a `engine/`.
3. Puente con el chat de CardIt (Edge Function con los límites de `CHAT-IA.md`).
4. Probar con la IA real: si elige bien el tema, si edita en vez de duplicar y si el tono sale natural.
5. Al final, con la interfaz asentada: mapa de la interfaz para que la IA señale cualquier cosa.
6. Repo del chatbot solo cuando otra app lo necesite.

## Ideas sueltas

- Ajolote: meterse en una burbuja y flotar; branquias que brillan.
- Tutoriales en la app: un registro de objetivos (`useTutorialTarget('id')`) y medir su posición con `measureInWindow`.
