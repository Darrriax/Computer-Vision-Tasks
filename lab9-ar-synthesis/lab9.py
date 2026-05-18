from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cars.car1 as car1
import cars.car2 as car2
import cars.car3 as car3
import cars.car4 as car4
import random

# Store car positions and speeds
cars = []


def generate_main_color():
    return (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))


def generate_random_color(main_color):
    r = max(0, min(1, main_color[0] - 0.1))
    g = max(0, min(1, main_color[1] - 0.1))
    b = max(0, min(1, main_color[2] - 0.1))
    return (r, g, b)


def is_position_clear(x_position, lane, min_distance=6):
    for car in cars:
        if car['lane'] == lane and abs(car['x_position'] - x_position) < min_distance:
            return False
    return True


def init_cars(num_cars):
    global cars
    cars = []
    lane_positions = [-4.5, -1.5, 1.5, 4.5]  # Four lanes on the road
    for _ in range(num_cars):
        while True:
            x_position = random.uniform(-20, 20)
            lane = random.choice(lane_positions)
            if is_position_clear(x_position, lane):
                break
        speed = random.uniform(0.05, 0.3)
        direction = 1 if lane > 0 else -1  # Set direction based on lane
        car_module = random.choice([car1, car2, car3, car4])
        main_color = generate_main_color()
        second_color = generate_random_color(main_color)
        car = {
            'module': car_module,
            'x_position': x_position,
            'speed': speed,
            'main_color': main_color,
            'second_color': second_color,
            'wheel_color': (0.5, 0.5, 0.5),
            'lane': lane,
            'target_speed': speed,
            'direction': direction
        }
        cars.append(car)


def draw_scene():
    # Draw road
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(-30, 0, -6)
    glVertex3f(30, 0, -6)
    glVertex3f(30, 0, 6)
    glVertex3f(-30, 0, 6)
    glEnd()

    # Draw solid double line in the middle
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex3f(-20, 0.02, -0.1)
    glVertex3f(20, 0.02, -0.1)
    glVertex3f(-20, 0.02, 0.1)
    glVertex3f(20, 0.02, 0.1)
    glEnd()

    # Draw dashed lines for other lanes
    glLineWidth(1)
    for z in [-3, 3]:
        for i in range(-20, 20, 2):
            glBegin(GL_LINES)
            glVertex3f(i, 0.02, z)
            glVertex3f(i + 1, 0.02, z)
            glEnd()

    # Draw cars with random colors
    for car in cars:
        glPushMatrix()
        glTranslatef(car['x_position'], 0, car['lane'])
        if car['direction'] == -1:  # If car is moving backward, rotate it 180 degrees
            glRotatef(180, 0, 1, 0)
        car['module'].main_color = car['main_color']
        car['module'].second_color = car['second_color']
        car['module'].wheel_color = car['wheel_color']
        car['module'].draw_car()
        glPopMatrix()

    # Draw bushes along the road
    for z in [-7, 7]:
        for i in range(-20, 21, 2):
            draw_bush(i, z)


def draw_bush(x, z):
    glColor3f(0.0, 0.5, 0.0)
    glPushMatrix()
    glTranslatef(x, 0, z)
    glutSolidSphere(1, 16, 16)
    glPopMatrix()


def update_cars():
    for i, car in enumerate(cars):
        # Reset target speed to the current speed
        car['target_speed'] = car['speed']

        # Check for the car in front in the same lane and direction
        for j, other_car in enumerate(cars):
            if i != j and car['lane'] == other_car['lane'] and car['direction'] == other_car['direction']:
                distance = (other_car['x_position'] - car['x_position']) * car['direction']
                if 0 < distance < 6:
                    if distance < 0.5:
                        car['target_speed'] = 0
                    elif car['speed'] > other_car['speed']:
                        car['target_speed'] = other_car['speed']
                    break

        # Smooth acceleration and deceleration
        if car['speed'] < car['target_speed']:
            car['speed'] = min(car['speed'] + 0.005, car['target_speed'])
        elif car['speed'] > car['target_speed']:
            car['speed'] = max(car['speed'] - 0.005, car['target_speed'])

        # Update car position based on direction
        car['x_position'] += car['speed'] * car['direction']
        if car['x_position'] > 20 or car['x_position'] < -20:
            while True:
                new_x_position = -20 if car['direction'] == 1 else 20
                new_lane = random.choice([-4.5, -1.5, 1.5, 4.5])
                if is_position_clear(new_x_position, new_lane):
                    break
            car['x_position'] = new_x_position
            car['speed'] = random.uniform(0.05, 0.15)
            car['target_speed'] = car['speed']
            car['module'] = random.choice([car1, car2, car3, car4])
            car['main_color'] = generate_main_color()
            car['second_color'] = generate_random_color(car['main_color'])
            car['lane'] = new_lane
            car['direction'] = 1 if new_lane > 0 else -1  # Update direction


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(-10.0, 30.0, 30.0,  # Позиція камери
              0.0, 0.0, 0.0,  # Позиція, на яку дивиться камера
              0.0, 1.0, 0.0)  # Вектор, що вказує вертикальну орієнтацію камери
    draw_scene()
    glutSwapBuffers()


def idle():
    update_cars()
    glutPostRedisplay()


def keyboard(key, x, y):
    if key == b'\x1b':
        sys.exit()


def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.7, 0.4, 0.2, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(35, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    # Set up lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [40.0, 25.0, 10.0, 0.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 5.0, 1.0, 1.0])

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glShadeModel(GL_SMOOTH)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"3D Car Animation on Road")
    init()
    init_cars(num_cars=5)
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboard)
    glutMainLoop()


if __name__ == "__main__":
    main()
