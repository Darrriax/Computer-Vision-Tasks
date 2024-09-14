import pygame
import numpy as np

# _______________________________________________Налаштування___________________________________________________________
# Розміри вікна
window_width = 900
window_height = 600

# Розміри паралелепіпеда
print("Фігура: паралелепіпед")
height = int(input("Введіть висоту: "))
width = int(input("Введіть ширину: "))
depth = int(input("Введіть глибину: "))

# Задання початкових координат паралелепіпеда
initial_coordinates = np.array([[0, 0, 0, 1],
                                [height, 0, 0, 1],
                                [height, width, 0, 1],
                                [0, width, 0, 1],
                                [0, 0, depth, 1],
                                [height, 0, depth, 1],
                                [height, width, depth, 1],
                                [0, width, depth, 1]])

pygame.init()

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Лабораторна робота №1")

# Щоб паралелепіпед при запуску програми був розташований в центрі вікна
shift_vector = np.array([window_width / 2 - height / 2, window_height / 2 - width / 2, 0, 0])
initial_coordinates += shift_vector.astype(int)
parallelepiped_coordinates = initial_coordinates.copy()


# ___________________________Функція для матричних перетворень в центрі початку координат, _____________________________
# ________________________а потім зміщення центру обʼєкта у точку, де він знаходився перед цим__________________________
def transform_and_center(coordinates, transformation_matrix):
    center = np.mean(coordinates, axis=0)
    translated_coordinates = coordinates - center
    transformed_coordinates = np.dot(translated_coordinates, transformation_matrix)
    final_coordinates = transformed_coordinates + center

    return final_coordinates


# ______________________________________________Малювання та оновлення вікна____________________________________________
def draw_and_update():
    screen.fill((255, 255, 255))
    pygame.draw.polygon(screen, (0, 0, 0), parallelepiped_coordinates[:4, :2], 2)
    pygame.draw.polygon(screen, (0, 0, 0), parallelepiped_coordinates[4:, :2], 2)
    for i in range(4):
        pygame.draw.line(screen, (0, 0, 0), parallelepiped_coordinates[i, :2],
                         parallelepiped_coordinates[i + 4, :2], 2)
    pygame.display.flip()


# _______________________________________Функції для обертання навколо осей X, Y, Z_____________________________________
def rotate_x(angle):
    rotation_matrix = np.array([[1, 0, 0, 0],
                                [0, np.cos(angle), np.sin(angle), 0],
                                [0, -np.sin(angle), np.cos(angle), 0],
                                [0, 0, 0, 1]])
    return rotation_matrix


def rotate_y(angle):
    rotation_matrix = np.array([[np.cos(angle), 0, -np.sin(angle), 0],
                                [0, 1, 0, 0],
                                [np.sin(angle), 0, np.cos(angle), 0],
                                [0, 0, 0, 1]])
    return rotation_matrix


def rotate_z(angle):
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle), 0, 0],
                                [np.sin(angle), np.cos(angle), 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])
    return rotation_matrix


# _____________________________________________Функція для масштабування_______________________________________________
def scale(sx, sy, sz):
    scaling_matrix = np.array([[sx, 0, 0, 0],
                               [0, sy, 0, 0],
                               [0, 0, sz, 0],
                               [0, 0, 0, 1]])
    return scaling_matrix


# ___________________________________________________Початок програми___________________________________________________
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                parallelepiped_coordinates[:, 1] -= 10  # Зміщення вгору
            elif event.key == pygame.K_DOWN:
                parallelepiped_coordinates[:, 1] += 10  # Зміщення вниз
            elif event.key == pygame.K_LEFT:
                parallelepiped_coordinates[:, 0] -= 10  # Зміщення вліво
            elif event.key == pygame.K_RIGHT:
                parallelepiped_coordinates[:, 0] += 10  # Зміщення вправо
            elif event.key == pygame.K_s:
                parallelepiped_coordinates = transform_and_center(parallelepiped_coordinates, rotate_x(np.radians(30)))
            elif event.key == pygame.K_w:
                parallelepiped_coordinates = transform_and_center(parallelepiped_coordinates, rotate_x(-np.radians(30)))
            elif event.key == pygame.K_a:
                parallelepiped_coordinates = transform_and_center(parallelepiped_coordinates, rotate_y(np.radians(30)))
            elif event.key == pygame.K_d:
                parallelepiped_coordinates = transform_and_center(parallelepiped_coordinates, rotate_y(-np.radians(30)))
            elif event.key == pygame.K_q:
                parallelepiped_coordinates = transform_and_center(parallelepiped_coordinates, rotate_z(np.radians(30)))
            elif event.key == pygame.K_e:
                parallelepiped_coordinates = transform_and_center(parallelepiped_coordinates, rotate_z(-np.radians(30)))
            elif event.key == pygame.K_x:
                parallelepiped_coordinates = transform_and_center(parallelepiped_coordinates,
                                                                  scale(1.1, 1.1, 1.1))  # Збільшення
            elif event.key == pygame.K_z:
                parallelepiped_coordinates = transform_and_center(parallelepiped_coordinates,
                                                                  scale(0.9, 0.9, 0.9))  # Зменшення
            elif event.key == pygame.K_1:
                parallelepiped_coordinates = initial_coordinates.copy()
                for frame in range(16):
                    for i in range(10):
                        # Перевірка парності циклу: якщо парне – то зменшуємо фігуру, якщо ні – збільшуємо
                        if frame % 2 == 0:
                            parallelepiped_coordinates = transform_and_center(parallelepiped_coordinates,
                                                                              scale(0.95, 0.95, 0.95))
                        else:
                            parallelepiped_coordinates = transform_and_center(parallelepiped_coordinates,
                                                                              scale(1.05, 1.05, 1.05))
                        draw_and_update()
                        pygame.time.delay(50)

                    for i in range(5):
                        # Перевірка циклу, фігура переміщується вверх-вправо-вниз-вліво та одночасно обертається
                        if frame % 4 == 0:
                            parallelepiped_coordinates[:, 1] -= 10
                        elif (frame - 1) % 4 == 0:
                            parallelepiped_coordinates[:, 0] += 10
                        elif (frame - 2) % 4 == 0:
                            parallelepiped_coordinates[:, 1] += 10
                        else:
                            parallelepiped_coordinates[:, 0] -= 10

                        parallelepiped_coordinates = transform_and_center(parallelepiped_coordinates,
                                                                          rotate_z(-np.radians(15)))
                        draw_and_update()
                        pygame.time.delay(50)
                parallelepiped_coordinates = initial_coordinates.copy()
                break
            elif event.key == pygame.K_2:
                for frame in range(16):
                    # Рандомне переміщення фігури
                    random_x = int(np.random.uniform(-300, 300))
                    random_y = int(np.random.uniform(-300, 300))
                    new_coordinates = parallelepiped_coordinates.copy()
                    new_coordinates[:, 1] += random_x
                    new_coordinates[:, 0] += random_y

                    # Перевірка, чи не виходить фігура на межі екрану
                    if (0 <= new_coordinates[:, 0].min() < window_width) and (
                            0 <= new_coordinates[:, 1].min() < window_height):
                        parallelepiped_coordinates = new_coordinates

                        # Рандомне обертання
                        random_rot_x = np.radians(np.random.uniform(0, 360))
                        random_rot_y = np.radians(np.random.uniform(0, 360))
                        random_rot_z = np.radians(np.random.uniform(0, 360))
                        rotation_matrix = rotate_x(random_rot_x) @ rotate_y(random_rot_y) @ rotate_z(random_rot_z)
                        parallelepiped_coordinates = transform_and_center(parallelepiped_coordinates, rotation_matrix)

                        # Рандомне масштабування фігури
                        scaling = np.random.uniform(0.5, 1.5)
                        parallelepiped_coordinates = transform_and_center(parallelepiped_coordinates,
                                                                          scale(scaling, scaling, scaling))

                        draw_and_update()
                        pygame.time.delay(2000)

                        # Очищення екрану
                        screen.fill((255, 255, 255))
                        pygame.display.flip()
                        pygame.time.delay(1000)

    draw_and_update()

pygame.quit()
