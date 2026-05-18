import cv2
import numpy as np
from matplotlib import pyplot as plt

def process_image(image_path, lower_bound, upper_bound, message):
    # Завантаження зображення
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Застосування Гаусового розмиття
    img = cv2.GaussianBlur(img, (7, 7), 3)

    # Конвертація в HSV колірний простір
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # Створення маски
    mask = cv2.inRange(hsv_img, lower_bound, upper_bound)

    # Морфологічне закриття для видалення шумів
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Заміна кольору лісових насаджень на жовтий
    img[mask > 0] = (255, 255, 0)

    # Обчислення відсотка лісових насаджень в кадрі
    img_shape = img.shape
    forest_area = np.sum(mask == 255)
    print(f"{message} {(forest_area / (img_shape[0] * img_shape[1]) * 100):.1f}% кадру.")

    # Відображення зображення з позначеними лісовими насадженнями
    plt.imshow(img)
    plt.show()

'''
Обробка зображення з високоякісного джерела ДЗЗ
'''
process_image(
    "high_quality_image.png",
    lower_bound=(20, 60, 30),
    upper_bound=(150, 125, 65),
    message="На високоякісному зображенні лісові насадження займають"
)

'''
Обробка зображення з оперативного джерела ДЗЗ
'''
process_image(
    "operational_image.png",
    lower_bound=(0, 150, 0),
    upper_bound=(255, 255, 255),
    message="На оперативному зображенні лісові насадження займають"
)
