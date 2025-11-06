# 🎮 Juego tipo Mario Bros (Python + Pygame)

**Autor:** Richard Jonathan Quinteros Mendoza  

Juego 2D estilo *Mario Bros* desarrollado en **Python** usando la librería **Pygame**.  
El objetivo es saltar entre plataformas, evitar obstáculos y recolectar ítems para obtener ventajas temporales.  
Incluye música, efectos de sonido, plataformas desvanecibles y fondos que cambian según el nivel.

---

## 📂 Estructura del proyecto

> ⚠️ Todas las carpetas deben estar dentro de la carpeta raíz `mario/`.

## 📁 Estructura del proyecto

```text
mario/

│

├── audios/               # Efectos y música de fondo
│   ├── salto.mp3
│   ├── game_over.mp3
│   └── fondo_music.mp3
│

├── fondos/               # Imágenes de fondos (día, noche, espacio...)
│   ├── fondo1.png
│   ├── fondo_2.png
│   ├── fondo_noche.png
│   └── space.png
│

├── imagenes de mario/    # Sprites y animaciones del jugador
│   ├── m2.png
│   ├── cor1.png
│   ├── cor2.png
│   ├── co3.png
│   └── salt.png
│

├── plataformas/          # Imágenes de plataformas y nubes
│   ├── plata.png
│   ├── nube2.png
│   └── fonfo2.png
│

├── objetos/              # Objetos interactivos (hongos, pinchos)
│   ├── hongo.png
│   └── pinchon.png
│

├── juego.py              # Código principal del juego
└── README.md
```

---

## 🕹️ Descripción

Controla a **Mario** saltando entre plataformas para obtener puntos y evitar obstáculos.  
Al recolectar hongos puedes obtener un *súper salto*.  
El fondo cambia dinámicamente según el puntaje (día, noche, espacio).  
El juego termina con **Game Over** si Mario cae o toca un pincho, y se muestra **Winner** al alcanzar 600 puntos.

### ✨ Características principales

- 🎵 Música de fondo en bucle.  
- 🔊 Efectos de sonido (salto, game over).  
- ☁️ Plataformas desvanecibles.  
- 🖥️ Soporte para pantalla completa y modo ventana.  
- ⭐ Sistema de puntaje y niveles visuales.  
- 🎮 Menú de instrucciones, pausa y botones de reinicio/salida.

---

## ⚙️ Requisitos

- **Python:** 3.10.12  
- **Dependencias:**
  
```bash
pip install pygame
```
## Se recomienda usar un entorno virtual:
``` bash
python3 -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
pip install pygame
```
## ▶️ Clonar repositorio
``` bash
git clone https://github.com/Rick2297/Juego-de-Mario-Bros.git
```
## Notas técnicas
- Sistema operativo de desarrollo: Kubuntu Linux / Windows
- Procesador recomendado: Intel i3-1215U 
- Memoria RAM: 8 GB
- IDEs usados: Visual Studio Code 

## 📝 Licencia
Proyecto creado con fines educativos y de aprendizaje en desarrollo de videojuegos 2D con Pygame


