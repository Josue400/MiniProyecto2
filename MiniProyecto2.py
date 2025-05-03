import cv2
import mediapipe as mp
import serial
import time

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Inicializar comunicación serial con Arduino
arduino = serial.Serial('COM3', 9600)  # Cambiar COM3 por el puerto correcto
time.sleep(2)  # Esperar a que se establezca la conexión

# Inicializar cámara
cap = cv2.VideoCapture(0)

prev_fingers = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    # Convertir imagen a RGB
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Procesar con MediaPipe
    results = hands.process(img_rgb)
    
    finger_count = 0
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Dibujar landmarks de la mano
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Obtener puntos clave de los dedos
            landmarks = hand_landmarks.landmark
            
            # Lógica para contar dedos (basada en posiciones relativas de landmarks)
            fingers = []
            
            # Pulgar
            if landmarks[mp_hands.HandLandmark.THUMB_TIP].x < landmarks[mp_hands.HandLandmark.THUMB_IP].x:
                fingers.append(1)
            else:
                fingers.append(0)
                
            # Otros dedos
            for tip, pip in [(mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP),
                            (mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP),
                            (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP),
                            (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP)]:
                if landmarks[tip].y < landmarks[pip].y:
                    fingers.append(1)
                else:
                    fingers.append(0)
            
            finger_count = sum(fingers)
    
    # Mostrar conteo en la imagen
    cv2.putText(frame, f'Dedos: {finger_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Enviar a Arduino solo si cambió el conteo
    if finger_count != prev_fingers:
        arduino.write(str(finger_count).encode())
        prev_fingers = finger_count
    
    # Mostrar imagen
    cv2.imshow('Contador de Dedos', frame)
    
    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
hands.close()
arduino.close()


