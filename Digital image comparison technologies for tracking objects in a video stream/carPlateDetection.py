import cv2
import threading


def process_frames():
    global plates_cascade
    global cap
    global processed_frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        plates = plates_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 50),
                                                 maxSize=(300, 250))
        for (x, y, w, h) in plates:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        processed_frame = frame.copy()


# Завантаження каскадного класифікатора для номерних знаків
plates_cascade = cv2.CascadeClassifier('cascade/haarcascade_plate_number.xml')

# Відкриття відео
cap = cv2.VideoCapture('video/car_flow.mp4')

# Глобальна змінна для зберігання обробленого кадру
processed_frame = None

# Створення та запуск потоку для обробки кадрів
processing_thread = threading.Thread(target=process_frames)
processing_thread.start()

while True:
    if processed_frame is not None:
        cv2.imshow('License Plate Recognition', processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Чекаємо, доки обробка кадрів не завершиться
processing_thread.join()

# Закриття відеопотоку та вікна OpenCV
cap.release()
cv2.destroyAllWindows()
