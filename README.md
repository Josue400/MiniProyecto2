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



**CODIGO DEL ARDUINO**

// Pines para cada segmento del display (A, B, C, D, E, F, G, DP)
const int segmentPins[] = {2, 3, 4, 5, 6, 7, 8, 9}; // A=2, B=3, ..., G=8, DP=9
// Dígitos del 0 al 9 en representación de 7 segmentos (A-G, sin DP)
const byte digitPatterns[10] = {
  B11111100, // 0 (A,B,C,D,E,F encendidos)
  B01100000, // 1 (B,C encendidos)
  B11011010, // 2 (A,B,G,E,D encendidos)
  B11110010, // 3 (A,B,G,C,D encendidos)
  B01100110, // 4 (F,G,B,C encendidos)
  B10110110, // 5 (A,F,G,C,D encendidos)
  B10111110, // 6 (A,F,G,C,D,E encendidos)
  B11100000, // 7 (A,B,C encendidos)
  B11111110, // 8 (Todos encendidos)
  B11110110  // 9 (A,B,C,D,F,G encendidos)
};

void setup() {
  Serial.begin(9600);
  // Configurar pines de los segmentos como salida
  for (int i = 0; i < 8; i++) {
    pinMode(segmentPins[i], OUTPUT);
  }
  resetDisplay();
}

void loop() {
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();
    if (receivedChar >= '0' && receivedChar <= '9') {
      int digit = receivedChar - '0';
      displayDigit(digit);
    }
  }
}

void displayDigit(int digit) {
  resetDisplay();
  if (digit >= 0 && digit <= 9) {
    byte pattern = digitPatterns[digit];
    // Encender segmentos según el patrón
    for (int i = 0; i < 7; i++) { // Itera de A a G (sin DP)
      bool state = bitRead(pattern, 7 - i); // Lee cada bit del patrón
      digitalWrite(segmentPins[i], state);
    }
  }
}

void resetDisplay() {
  // Apagar todos los segmentos
  for (int i = 0; i < 8; i++) {
    digitalWrite(segmentPins[i], LOW);
  }
}
