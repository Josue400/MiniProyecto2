Este código utiliza visión por computadora y machine learning para detectar la cantidad de dedos levantados en una mano y enviar esa información a un Arduino mediante comunicación serial

1. **Componentes Principales**
   
    OpenCV (cv2): Procesa el video de la cámara en tiempo real.

    MediaPipe (mediapipe): Modelo de IA preentrenado para detectar manos y sus puntos clave (landmarks).
    PySerial (serial): Envía datos desde Python al Arduino mediante USB (COM3 en este caso).

    Arduino: Recibe el conteo de dedos y puede controlar LEDs, motores, displays, etc.


   **COMO ES QUE FUNCIONA**

**Captura de imagen:**

  ret, frame = cap.read() obtiene un fotograma de la cámara.

**Detección de Manos:**

  Convierte la imagen a RGB (MediaPipe requiere este formato).
  hands.process(img_rgb) devuelve los landmarks (21 puntos por mano).

**Conteo de Dedos:**
  Lógica basada en landmarks:
  Pulgar: Compara la posición horizontal (x) de la punta (THUMB_TIP) con la articulación (THUMB_IP).

**Otros dedos:** 
  Compara la posición vertical (y) de la punta (TIP) con la articulación (PIP).
  Si TIP.y < PIP.y, el dedo está levantado.
  finger_count = sum(fingers) suma los dedos detectados (0-5).

**Visualización:**
  Muestra el conteo en pantalla con cv2.putText().
  Dibuja los landmarks y conexiones con mp_draw.draw_landmarks().




  https://drive.google.com/file/d/1UABNFrejHKWzpHJ-56AoUVqfOfwrSZJe/view?usp=sharing
