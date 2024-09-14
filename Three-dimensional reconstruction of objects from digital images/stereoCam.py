import cv2

# Функція для отримання відеопотоку з камери
def get_video_capture(source):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"Cannot open video source {source}")
        return None
    return cap

# Відкрийте відеопотоки
macbook_camera = get_video_capture(0)  # Вбудована камера ноутбука
iphone_camera_1 = get_video_capture(1)  # Трансляція відео з першого телефону
iphone_camera_2 = get_video_capture(0)  # Трансляціїя відео з другого телефону

# Перевірка, чи всі камери відкриті
if not macbook_camera or not iphone_camera_1 or not iphone_camera_2:
    print("One or more video sources could not be opened.")
    exit()

while True:
    # Читання кадрів з камер
    ret1, frame1 = macbook_camera.read()
    ret2, frame2 = iphone_camera_1.read()
    ret3, frame3 = iphone_camera_2.read()

    if not ret1 or not ret2 or not ret3:
        print("Failed to grab frames from one or more video sources.")
        break

    # Відображення кадрів
    cv2.imshow('MacBook Camera', frame1)
    cv2.imshow('iPhone Camera 1', frame2)
    cv2.imshow('iPhone Camera 2', frame3)

    # Вихід при натисканні клавіші 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Звільнення ресурсів
macbook_camera.release()
iphone_camera_1.release()
iphone_camera_2.release()
cv2.destroyAllWindows()
