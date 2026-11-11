# Nota sobre el uso de inteligencia artificial

En el desarrollo de *Las Crónicas de Eldoria: El Cristal del Alba* usamos herramientas de IA en dos momentos distintos.

## Versión original (1.0.0): Claude

Un asistente de IA (Claude, de Anthropic) funcionó como herramienta de orquestación. Generó la primera versión del proyecto en GDevelop: los efectos de sonido y la música, el diseño de los niveles y la lógica de eventos (diálogos e interacciones). También realizó pruebas técnicas iniciales.

Nuestro equipo, formado por Mauricio Campos y Kliment García, definió la consigna y los requisitos del juego, dirigió el trabajo indicando qué se necesitaba en cada etapa, probó el juego en GDevelop y ajustó lo que encontró: agregó el salto con la flecha arriba, afinó el movimiento del personaje principal y de los NPCs, y usó la portada como pantalla de título.

## Versión modificada (1.4.1): trabajo local e IA Gemini

La ampliación del juego se hizo **de forma local, directamente en el editor de GDevelop**, por el equipo. Incluye:

- Nuevas pantallas y escenas (`Secreto` y `Nivel2b`) y niveles más largos.
- Máximo de vidas ampliado a 10.
- Plataformas dispuestas en vertical para trepar.
- Música cambiada por pistas propias de la biblioteca de GDevelop.
- Textos modificados (diálogos, carteles y mensajes).
- Jefe final, el Rey Goblin, con 4 vidas, rápido y que persigue a Lyra.

La **única parte generada con IA** en esta versión son las **imágenes nuevas** (fondo de la cinemática, imágenes de transición, pantalla final y fondos de apoyo). Se crearon con **Gemini** (Google): el equipo redactó las especificaciones de cada imagen (escena, estilo pixel art, paleta y composición) y Gemini devolvió el resultado. Después revisamos las imágenes y las incorporamos al proyecto.

| Elemento | Origen |
|---|---|
| Imágenes nuevas (cinemática, transición, pantalla final, fondos `F*.png`) | Gemini, a partir de especificaciones del equipo |
| Lógica, eventos, diseño de niveles, jefe final y textos de la versión 1.4.1 | Trabajo local del equipo en GDevelop |
| Música de menú, niveles, final y Game Over | Biblioteca de GDevelop (uso público) |
| Gráficos, efectos y música de la versión original | Generados con Claude (ver arriba) |

Todas las decisiones finales sobre qué incluir en la entrega las tomó el equipo.
