import cv2

# Відео файл
video_path = 'video.mp4'
cap = cv2.VideoCapture(video_path)

# Створюємо фоновий субтракційний об'єкт
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Застосовуємо фонове віднімання
    fgmask = fgbg.apply(frame)

    # Розмиття для зменшення шуму
    blurred = cv2.GaussianBlur(fgmask, (5, 5), 0)

    # Виконуємо порогову обробку для виділення основних об'єктів
    _, thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)

    # Використовуємо морфологічні операції для видалення дрібних шумів і з'єднання близьких об'єктів
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Знаходимо контури на зображенні
    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Ігноруємо маленькі контури
        if cv2.contourArea(contour) < 2000:
            continue

        # Обчислюємо обмежувальний прямокутник для кожного контуру
        x, y, w, h = cv2.boundingRect(contour)

        # Фільтруємо контури, які не відповідають розмірам транспортних засобів
        if w < 50 or h < 50 or h > 400 or w > 400:
            continue

        # Класифікація на основі розмірів
        if w < 150 and h < 150:
            vehicle_type = "Car"
        else:
            vehicle_type = "Truck"

        # Малюємо прямокутник та підписуємо тип авто
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, vehicle_type, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Показуємо кадр
    cv2.imshow('Vehicle Detection', frame)

    # Вихід при натисканні клавіші 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
