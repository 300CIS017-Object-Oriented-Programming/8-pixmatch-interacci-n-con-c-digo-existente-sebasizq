## Requisitos Funcionales y Criterios de Aceptación

### 1. Configuración de Nivel de Dificultad

**Requisito:** El sistema debe permitir a los jugadores seleccionar el nivel de dificultad antes de comenzar el juego.

**Criterios de Aceptación:**
- Opciones de dificultad fácil, medio y difícil disponibles para selección.
- La configuración de dificultad debe influir en la mecánica del juego, como la frecuencia de regeneración de imágenes y la puntuación.
- Tiempos de regeneración específicos:
  - Fácil: cada 8 segundos.
  - Medio: cada 6 segundos.
  - Difícil: cada 5 segundos.

### 2. Configuración de Nombre y País del Jugador

**Requisito:** El sistema debe permitir que los jugadores ingresen su nombre y país antes de comenzar un nuevo juego.

**Criterios de Aceptación:**
- Los jugadores pueden ingresar su nombre y país en un campo de texto antes de iniciar el juego.
- La información del nombre y el país se utilizará opcionalmente para mostrar en el ranking de puntuaciones.

### 3. Inicio de Nuevo Juego

**Requisito:** Los jugadores deben poder iniciar un nuevo juego después de seleccionar la dificultad y configurar su nombre y país.

**Criterios de Aceptación:**
- Después de seleccionar la dificultad y completar los campos de nombre y país, el jugador puede hacer clic en un botón para comenzar un nuevo juego.
- Al iniciar un nuevo juego, se restablece el tablero y se generan nuevos emojis y casillas.

### 4. Mecánica del Juego

**Requisito:** El juego debe presentar una mecánica donde los jugadores deben seleccionar las casillas correctas para ganar puntos.

**Criterios de Aceptación:**
- Los jugadores ganan puntos al seleccionar la casilla con el emoji que coincide con el emoji mostrado en la barra lateral.
- Se resta un punto por cada casilla incorrecta seleccionada.
- El juego finaliza cuando todas las casillas han sido seleccionadas.
- Se muestra un mensaje de victoria si el jugador tiene una puntuación positiva al final del juego, y un mensaje de derrota si la puntuación es negativa o igual a cero.

### 5. Ranking de Puntuaciones

**Requisito:** El sistema debe llevar un registro de las puntuaciones más altas y mostrar un ranking de los jugadores.

**Criterios de Aceptación:**
- Después de cada juego, se actualiza el ranking con la puntuación del jugador.
- El ranking muestra el nombre, país y puntuación de los jugadores.

