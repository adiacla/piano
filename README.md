# piano
# Piano con las manos — Proyecto de examen (Ciencia de Datos)

Resumen
-------
Este proyecto implementa un "piano virtual" controlado por las puntas de los dedos usando la cámara. Utiliza MediaPipe Hands (modelo de IA para detección de manos y 21 landmarks) para detectar las puntas de los dedos (landmarks 4, 8, 12, 16, 20) y pygame para reproducir samples (MP3/WAV). Al mover la punta de un dedo hacia abajo se interpreta como una pulsación y se reproduce la nota mapeada.

Objetivo del examen
-------------------
- Integrar visión por computador (MediaPipe) con audio en tiempo real (pygame).
- Implementar detección robusta basada solo en las puntas de los dedos.
- Entregar código ejecutable, instrucciones, y una breve explicación técnica del método.
- (Opcional) Extensiones como grabado de eventos, visualización, o detección por velocidad.

Contexto técnico
----------------
- MediaPipe Hands es un modelo de IA que detecta 21 landmarks por mano (x,y,z normalizados).  
- Usamos exclusivamente las puntas: 4 (thumb tip), 8 (index tip), 12 (middle tip), 16 (ring tip), 20 (pinky tip).  
- La medición de movimiento usa la coordenada y normalizada (0..1) y un umbral relativo para independizar del tamaño del frame.  
- Se aplica un suavizado (EMA) y un cooldown por dedo para reducir falsos positivos y retriggers.  
- El mapeo de notas está organizado para que la mano física izquierda toque las notas graves y la derecha las agudas. El script muestra la imagen RAW (sin flip) para que la posición en pantalla coincida con la posición física.

Requisitos recomendados
-----------------------
- Python 3.8 - 3.11 (recomendado 3.9 o 3.10 en Windows para compatibilidad con mediapipe en algunos sistemas)
- Dependencias Python (ver `requirements.txt` más abajo)
- Opcional (si usas MP3 y quieres conversión automática): ffmpeg (añadir al PATH)
- Cámara web y altavoces/auriculares

requirements.txt sugerido
-------------------------
```text
opencv-python
mediapipe
numpy
pygame
pydub
protobuf==3.20.3
```

Estructura del proyecto (esperada)
----------------------------------
```
proyecto_piano/
├─ piano_calibrado_raw.py       # script principal (muestra RAW, sin flip)
├─ notas_config.py              # (opcional) mapeo notas / helper
├─ requirements.txt
├─ sonidos/
│  ├─ C4.mp3
│  ├─ D4.mp3
│  ├─ E4.mp3
│  ├─ F4.mp3
│  ├─ G4.mp3
│  ├─ A4.mp3
│  ├─ B4.mp3
│  ├─ C5.mp3
│  ├─ D5.mp3
│  └─ E5.mp3
└─ README.md
```

Instalación paso a paso
-----------------------
1. Clona o descarga el repositorio con los archivos.
2. Crea y activa un entorno virtual:
   - Windows (PowerShell):
     - python -m venv .venv
     - .\.venv\Scripts\Activate.ps1
   - Windows (cmd):
     - python -m venv .venv
     - .\.venv\Scripts\activate.bat
   - macOS / Linux:
     - python3 -m venv .venv
     - source .venv/bin/activate
3. Actualiza pip:
   - python -m pip install --upgrade pip setuptools wheel
4. Instala dependencias:
   - pip install -r requirements.txt
5. (Opcional) Si usarás conversión automática MP3→WAV, instala ffmpeg en el sistema y verifica:
   - ffmpeg -version
   - En Windows con Chocolatey: choco install ffmpeg
   - En macOS con Homebrew: brew install ffmpeg
   - En Ubuntu/Debian: sudo apt install ffmpeg
6. Asegúrate de que la carpeta `sonidos/` contiene los archivos con nombres exactos (ej. `C4.mp3`).

Ejecución
---------
1. Ejecuta:
   - python piano_calibrado_raw.py
2. Ventana del programa:
   - La imagen se muestra RAW (sin flip). La mano física izquierda aparece a la izquierda en pantalla.
3. Teclas útiles:
   - s → swap manual (invierte el mapeo Left↔Right)
   - l → calibrar mano física IZQUIERDA (muestra solo tu mano izquierda y pulsa)
   - r → calibrar mano física DERECHA (muestra solo tu mano derecha y pulsa)
   - ESC → salir

Calibración recomendada
-----------------------
1. Al arrancar, deja la cámara mostrando solo tu mano izquierda (centra y separa de la otra mano) y pulsa `l`. El script mapeará la etiqueta MediaPipe detectada a tu mano física izquierda.
2. Muestra solo tu mano derecha y pulsa `r`.
3. Tras calibrar, prueba mover la punta de un dedo hacia abajo: la mano izquierda debe disparar notas graves, la derecha notas agudas.
4. Si algo queda invertido simplemente pulsa `s` para invertir mapeo.

Pruebas rápidas
---------------
- Mueve el meñique de tu mano física izquierda: debería sonar la nota más baja (C4 si usas la configuración por defecto).
- Mueve el meñique de tu mano física derecha: debería sonar la nota más alta (E5).
- Si el sonido no se reproduce verifica `sonidos/` y la carga de archivos en la consola (mensajes de error).

Explicación breve del algoritmo
-------------------------------
- MediaPipe devuelve landmarks normalizados. Tomamos la coordenada y (vertical) de cada tip.
- Suavizamos la coordenada con EMA: y_smooth = alpha * y_now + (1 - alpha) * y_prev.
- Si la diferencia (y_smooth - y_prev) supera el umbral relativo (ej. 0.03), consideramos una pulsación.
- Aplicamos cooldown por dedo para evitar múltiples triggers rápidos.
- Reproducimos el sample asociado con pygame.mixer.Sound.play (no bloqueante).

Mapeo de notas (configuración recomendada)
------------------------------------------
El arreglo `nota_por_dedo` en el script viene de:
```python
mano_izquierda = ['A4', 'B4', 'C5', 'D5', 'E5']   # se invierte internamente
mano_derecha = ['C4', 'D4', 'E4', 'F4', 'G4']
nota_por_dedo = mano_izquierda[::-1] + mano_derecha
# => ['C4','D4','E4','F4','G4','A4','B4','C5','D5','E5']
```
Asegúrate de que tus archivos en `sonidos/` correspondan a esos nombres (`C4.mp3`, ...).

Resolución de problemas comunes
-------------------------------
- Advertencia protobuf: si ves "SymbolDatabase.GetPrototype() is deprecated", usa `protobuf==3.20.3` en requirements o suprime la advertencia con `warnings.filterwarnings(...)`.
- pygame.mixer.init() falla: intenta `pygame.mixer.init(frequency=44100, size=-16, channels=2)` o cierra otras apps que usen audio.
- pygame no reproduce MP3: en algunas plataformas SDL_mixer no incluye soporte MP3; instala `ffmpeg` y `pydub` para convertir automáticamente a WAV, o convierte manualmente tus MP3 a WAV.
- MediaPipe no detecta: mejora iluminación, aleja/acerca la mano y acerca la cámara, prueba con una sola mano para calibrar.

Criterio de evaluación / rúbrica (sugerida)
-------------------------------------------
- 50% Funcionamiento: detección, mapping Left->graves, Right->agudas, reproducir notas (pruebas con 2 manos).  
- 20% Calidad del código: legibilidad, modularidad, manejo de errores.  
- 10% Documentación: README claro, instrucciones de instalación y uso.  
- 10% Usabilidad: calibración, mensajes en pantalla, controles.  
- 10% Extensiones: registro, visualización extra, detección por velocidad, etc.

Checklist de entrega
--------------------
- [ ] `requirements.txt` incluido y funcional.
- [ ] `sonidos/` contiene los 10 archivos (mp3 o wav) con nombres correctos.
- [ ] `piano_calibrado_raw.py` ejecutable y probado.
- [ ] `README.md` con instrucciones (este documento).
- [ ] (Opcional) pequeño video o GIF mostrando ejecución.

Ideas de extensión (puntaje extra)
---------------------------------
- Detectar fuerza/velocidad del golpe y ajustar volumen.
- Visualizar un teclado en pantalla que se ilumine en cada nota.
- Registrar pulsaciones en CSV para análisis (timestamp, dedo, nota).
- Añadir reconocimiento de acordes/gestos para reproducir secuencias.

Contacto y buena práctica
-------------------------
- Incluye en tu README personal comentarios sobre problemas encontrados y cómo los resolviste (p. ej. conversión MP3, compatibilidad en Windows).
- Si la versión de mediapipe da problemas en tu máquina, prueba con Python 3.9/3.10 y reinstala en un venv limpio.

¿Quieres que además te genere:
- el `requirements.txt` final listo para subir,
- y un `notas_config.py` con el mapping recomendado?
Puedo crear esos archivos y pegarlos aquí listos para copiar. ¡Dime si los quieres!  
