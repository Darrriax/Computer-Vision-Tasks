import numpy as np
import matplotlib.pyplot as plt

# Точки паралелепіпеда
points = np.array([
    [-50, -50, -50],
    [150, -50, -50],
    [100, 50, -50],
    [-100, 50, -50],
    [-50, -50, 50],
    [150, -50, 50],
    [100, 50, 50],
    [-100, 50, 50]
])
# Ребра паралелепіпеда
edges = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]]


fig = plt.figure()
manager = plt.get_current_fig_manager()
manager.set_window_title('Паралелепіпед')
ax = fig.add_subplot(111, projection='3d')

# Малювання кожного ребра
for edge in edges: ax.plot3D(*zip(*points[edge]), color='r')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()

# Функція обчислення кривої Безьє
def bezier_curve(P, t):
    T = np.tile(t, (3, 1)).T
    return (1 - T) ** 2 * P[0] + 2 * (1 - T) * T * P[1] + T ** 2 * P[2]


fig = plt.figure()
manager = plt.get_current_fig_manager()
manager.set_window_title('Паралелепіпед. Метод інтерполяції: кривими Безьє')
ax = fig.add_subplot(111, projection='3d')

# Побудова ребер
for edge in edges:
    p1 = points[edge[0]]
    p2 = points[edge[1]]
    P = np.array([p1, (p1 + p2) / 2, p2])  # Контрольні точки для кривої

    # Інтерполяція кривими Безьє
    t = np.linspace(0, 1, 100)
    B = bezier_curve(P, t)
    ax.plot(B[:, 0], B[:, 1], B[:, 2], 'b')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
