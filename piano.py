import warnings
# Suprimir advertencia protobuf temprano
warnings.filterwarnings("ignore", message=".*SymbolDatabase.GetPrototype.*")

import cv2
import mediapipe as mp
import numpy as np
import pygame
import os
import time
import tempfile
import atexit
import shutil

# Intentaremos usar pydub solo si está disponible para convertir mp3->wav
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except Exception:
    PYDUB_AVAILABLE = False

# --------------------------
# CONFIGURACIÓN DE NOTAS
# --------------------------
mano_derecha = ['C4', 'D4', 'E4', 'F4', 'G4']
mano_izquierda = ['A4', 'B4', 'C5', 'D5', 'E5']
# Orden: meñique izq -> ... -> pulgar izq -> pulgar der -> ... -> meñique der
nota_por_dedo = mano_izquierda[::-1] + mano_derecha  # 10 notas
ruta_sonidos = "sonidos"

# --------------------------
# PYGAME / CARGA SAMPLES
# --------------------------

# --------------------------
# MEDIAPIPE (solo puntas de dedo)
# --------------------------

# --------------------------
# BUCLE PRINCIPAL
# --------------------------
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se puede abrir la cámara.")
    exit(1)

print("\n🎹 Piano activado — usando SOLO puntas y landmarks de ambas manos correctamente emparejados")
print("Mueve las puntas de tus dedos hacia abajo para tocar.\n")

# Nota sobre flip horizontal:
# - En este script flippeamos el frame antes de procesar, por lo que la handedness
#   devuelta por MediaPipe corresponde a la imagen que ves en pantalla.
# - Si prefieres procesar sin flip y sólo voltear para mostrar, mueve el cv2.flip
#   después del procesamiento. Ambas opciones son válidas, solo cambia la referencia visual.

while True:

pygame.mixer.quit()
