import cv2
import mediapipe as mp
import numpy as np
import sys
import time
import threading
import pygame

# Ініціалізація MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5,
                                  min_tracking_confidence=0.5)

# Ініціалізація Pygame для відтворення звуку
pygame.mixer.init()


# Функція для обчислення EYE Aspect Ratio (EAR)
def calculate_ear(eye_landmarks):
    A = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
    B = np.linalg.norm(eye_landmarks[2] - eye_landmarks[4])
    C = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])
    ear = (A + B) / (2.0 * C)
    return ear


# Поріг EAR для визначення закритих очей
EAR_THRESHOLD = 0.23
# Максимальний час закритих очей, щоб викликати звук (у секундах)
MAX_CLOSED_EYE_TIME = 3
# Шлях до аудіофайлу
AUDIO_FILE_PATH = 'alarm.wav'


# Функція відтворення звуку
def play_alarm():
    pygame.mixer.music.load(AUDIO_FILE_PATH)
    pygame.mixer.music.play(-1)  # Повторювати звук поки не буде зупинено


# Функція зупинки звуку
def stop_alarm():
    pygame.mixer.music.stop()


# Меню вибору режиму
print("Select mode:")
print("1: Process video file")
print("2: Use webcam to track gaze direction")
mode = input("Enter 1 or 2: ")

if mode == '1':
    cap = cv2.VideoCapture('video.mov')
elif mode == '2':
    cap = cv2.VideoCapture(0)
else:
    print("Invalid selection")
    sys.exit()

start_time = None
alarm_thread = None
alarm_triggered = False

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Перетворення кольорів для MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark
            # Отримання координат очей
            left_eye_landmarks = np.array([(landmarks[i].x, landmarks[i].y) for i in [362, 385, 387, 263, 373, 380]])
            right_eye_landmarks = np.array([(landmarks[i].x, landmarks[i].y) for i in [33, 160, 158, 133, 153, 144]])

            # Масштабування координат до розмірів зображення
            h, w, _ = image.shape
            left_eye_landmarks = np.array([(int(x * w), int(y * h)) for x, y in left_eye_landmarks])
            right_eye_landmarks = np.array([(int(x * w), int(y * h)) for x, y in right_eye_landmarks])

            # Обчислення EAR для обох очей
            left_ear = calculate_ear(left_eye_landmarks)
            right_ear = calculate_ear(right_eye_landmarks)

            # Середнє значення EAR
            ear = (left_ear + right_ear) / 2.0

            # Визначення стану очей і вибір кольору для контурів
            if ear < EAR_THRESHOLD:
                eye_color = (0, 0, 255)  # Червоний
                cv2.putText(image, 'Eyes Closed', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                if start_time is None:
                    start_time = time.time()
                else:
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= MAX_CLOSED_EYE_TIME and not alarm_triggered:
                        alarm_thread = threading.Thread(target=play_alarm)
                        alarm_thread.start()
                        alarm_triggered = True
            else:
                eye_color = (0, 255, 0)  # Зелений
                cv2.putText(image, 'Eyes Open', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                start_time = None
                if alarm_triggered:
                    stop_alarm()
                    alarm_triggered = False

            # Малювання контурів очей
            cv2.polylines(image, [left_eye_landmarks], isClosed=True, color=eye_color, thickness=2)
            cv2.polylines(image, [right_eye_landmarks], isClosed=True, color=eye_color, thickness=2)

    # Відображення результату
    cv2.imshow('Frame', image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
