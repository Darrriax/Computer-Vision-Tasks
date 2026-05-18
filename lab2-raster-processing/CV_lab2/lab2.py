import numpy as np
import cv2
import matplotlib.pyplot as plt


def brightness(image, factor):
    corrected_image = image.astype(np.float64) + factor
    corrected_image = np.clip(corrected_image, 0, 255)
    return corrected_image.astype(np.uint8)


def grayscale(image):
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return grayscale_image


def negative(image):
    negative_image = cv2.bitwise_not(image)
    return negative_image


def gradient(image, direction='diagonal'):
    rows, cols, _ = image.shape
    gradient_image = np.zeros_like(image, dtype=np.float64)

    if direction == 'diagonal_top_left':
        for i in range(rows):
            for j in range(cols):
                gradient = (i + j) / (rows + cols) * 255
                gradient_image[i, j] = image[i, j] * (gradient / 255)
    elif direction == 'diagonal_top_right':
        for i in range(rows):
            for j in range(cols):
                distance = np.sqrt((i) ** 2 + (cols - j) ** 2)
                max_distance = np.sqrt(rows ** 2 + cols ** 2)
                gradient = distance / max_distance * 255
                gradient_image[i, j] = image[i, j] * (gradient / 255)
    elif direction == 'diagonal_bottom_left':
        for i in range(rows):
            for j in range(cols):
                distance = np.sqrt((rows - i) ** 2 + (j) ** 2)
                max_distance = np.sqrt(rows ** 2 + cols ** 2)
                gradient = distance / max_distance * 255
                gradient_image[i, j] = image[i, j] * (gradient / 255)
    elif direction == 'diagonal_bottom_right':
        for i in range(rows):
            for j in range(cols):
                distance = np.sqrt((rows - i) ** 2 + (cols - j) ** 2)
                max_distance = np.sqrt(rows ** 2 + cols ** 2)
                gradient = distance / max_distance * 255
                gradient_image[i, j] = image[i, j] * (gradient / 255)
    elif direction == 'from_center':
        center_x, center_y = rows / 2, cols / 2
        for i in range(rows):
            for j in range(cols):
                distance = np.sqrt((center_x - i) ** 2 + (center_y - j) ** 2)
                max_distance = np.sqrt(center_x ** 2 + center_y ** 2)
                gradient = distance / max_distance * 255
                gradient_image[i, j] = image[i, j] * (gradient / 255)
    elif direction == 'to_center':
        center_x, center_y = rows / 2, cols / 2
        for i in range(rows):
            for j in range(cols):
                distance = np.sqrt((center_x - i) ** 2 + (center_y - j) ** 2)
                max_distance = np.sqrt(center_x ** 2 + center_y ** 2)
                gradient = (1 - distance / max_distance) * 255
                gradient_image[i, j] = image[i, j] * (gradient / 255)

    return np.clip(gradient_image, 0, 255).astype(np.uint8)


image_path = 'img.jpeg'
image = cv2.imread(image_path, cv2.IMREAD_COLOR)

brightened_image = brightness(image, 50)
grayscale_image = grayscale(image)
negative_image = negative(image)
diagonal_gradient_image_tl = gradient(image, direction='diagonal_top_left')
diagonal_gradient_image_tr = gradient(image, direction='diagonal_top_right')
diagonal_gradient_image_bl = gradient(image, direction='diagonal_bottom_left')
diagonal_gradient_image_br = gradient(image, direction='diagonal_bottom_right')
from_center_gradient_image = gradient(image, direction='from_center')
to_center_gradient_image = gradient(image, direction='to_center')

plt.figure(figsize=(15, 15))

plt.subplot(4, 3, (1, 3))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Оригінальне зображення')

plt.subplot(4, 3, 4)
plt.imshow(cv2.cvtColor(brightened_image, cv2.COLOR_BGR2RGB))
plt.title('Збільшена яскравість')

plt.subplot(4, 3, 5)
plt.imshow(grayscale_image, cmap='gray')
plt.title('Відтінки сірого')

plt.subplot(4, 3, 6)
plt.imshow(cv2.cvtColor(negative_image, cv2.COLOR_BGR2RGB))
plt.title('Негатив')

plt.subplot(4, 3, 7)
plt.imshow(cv2.cvtColor(diagonal_gradient_image_tl, cv2.COLOR_BGR2RGB))
plt.title('Градієнт: діагональ (зверху-ліворуч)')

plt.subplot(4, 3, 8)
plt.imshow(cv2.cvtColor(diagonal_gradient_image_tr, cv2.COLOR_BGR2RGB))
plt.title('Градієнт: діагональ (зверху-праворуч)')

plt.subplot(4, 3, 9)
plt.imshow(cv2.cvtColor(diagonal_gradient_image_bl, cv2.COLOR_BGR2RGB))
plt.title('Градієнт: діагональ (знизу-ліворуч)')

plt.subplot(4, 3, 10)
plt.imshow(cv2.cvtColor(diagonal_gradient_image_br, cv2.COLOR_BGR2RGB))
plt.title('Градієнт: діагональ (знизу-праворуч)')

plt.subplot(4, 3, 11)
plt.imshow(cv2.cvtColor(from_center_gradient_image, cv2.COLOR_BGR2RGB))
plt.title('Градієнт: від центру')

plt.subplot(4, 3, 12)
plt.imshow(cv2.cvtColor(to_center_gradient_image, cv2.COLOR_BGR2RGB))
plt.title('Градієнт: до центру')

plt.tight_layout()
plt.show()
