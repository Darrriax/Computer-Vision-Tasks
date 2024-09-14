from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Car body dimensions
car_length = 4.0
car_width = 2.0
car_height = 1

# Wheel dimensions
wheel_radius = 0.3
wheel_width = 0.3

main_color = (1, 0.2, 0.5)
second_color = (1, 0.1, 0.4)

# Camera angles
angle_y = 0
angle_x = 0


def draw_trapezoidal_cabin(red, green, blue):
    glPushMatrix()
    glColor3f(red, green, blue)

    # Define vertices for the trapezoidal cabin
    cabin_vertices = [
        # Front face
        [-car_length / 1.5 / 4, 0, car_width / 2],
        [car_length / 1.5 / 3.5, 0, car_width / 2],
        [car_length / 1.5 / 6, car_height / 1.1, car_width / 2],
        [-car_length / 6, car_height / 1.1, car_width / 2],

        # Back face
        [-car_length / 1.5 / 4, 0, -car_width / 2],
        [car_length / 1.5 / 3.5, 0, -car_width / 2],
        [car_length / 1.5 / 6, car_height / 1.1, -car_width / 2],
        [-car_length / 6, car_height / 1.1, -car_width / 2],

        # Left face
        [-car_length / 1.5 / 4, 0, car_width / 2],
        [-car_length / 1.5 / 4, 0, -car_width / 2],
        [-car_length / 1.5 / 6, car_height / 1.1, -car_width / 2],
        [-car_length / 1.5 / 6, car_height / 1.1, car_width / 2],

        # Right face
        [car_length / 1.5 / 4, 0, car_width / 2],
        [car_length / 1.5 / 4, 0, -car_width / 2],
        [car_length / 1.5 / 6, car_height / 1.1, -car_width / 2],
        [car_length / 1.5 / 6, car_height / 1.1, car_width / 2],

        # Top face
        [-car_length / 1.5 / 6, car_height / 1.1, car_width / 2],
        [car_length / 1.5 / 6, car_height / 1.1, car_width / 2],
        [car_length / 1.5 / 6, car_height / 1.1, -car_width / 2],
        [-car_length / 1.5 / 6, car_height / 1.1, -car_width / 2],

        # Bottom face
        [-car_length / 1.5 / 4, 0, car_width / 2],
        [car_length / 1.5 / 4, 0, car_width / 2],
        [car_length / 1.5 / 4, 0, -car_width / 2],
        [-car_length / 1.5 / 4, 0, -car_width / 2],
    ]

    glTranslatef(0, car_height, 0)

    glBegin(GL_QUADS)
    for i in range(0, len(cabin_vertices), 4):
        for j in range(4):
            glVertex3fv(cabin_vertices[i + j])
    glEnd()

    glPopMatrix()


def draw_wheel_arch():
    glPushMatrix()
    glColor3f(second_color[0], second_color[1], second_color[2])
    glTranslatef(0, wheel_radius, 0)
    glRotatef(90, 1, 0, 0)
    gluDisk(gluNewQuadric(), 0, wheel_radius * 1.5, 30, 1)
    glPopMatrix()


def draw_car_body():
    glPushMatrix()

    # Main body
    glColor3f(main_color[0], main_color[1], main_color[2])
    glScalef(car_length, car_height, car_width)
    glutSolidCube(1.0)
    glPopMatrix()

    # Second body
    glPushMatrix()
    glColor3f(second_color[0], second_color[1], second_color[2])
    glScalef(car_length - 0.1, car_height / 1.9, car_width + 0.09)
    glTranslatef(0, -car_height / 2, 0)
    glutSolidCube(1.0)
    glPopMatrix()

    # Roof
    glPushMatrix()
    glColor3f(second_color[0], second_color[1], second_color[2])
    glScalef(car_length / 3.4, 0.2, car_width - 0.1)
    glTranslatef(0.25, car_height * 7, 0)
    glutSolidCube(1.0)
    glPopMatrix()

    # Hood
    glPushMatrix()
    glColor3f(second_color[0], second_color[1], second_color[2])
    glScalef(car_length / 3, 0.2, car_width - 0.2)
    glTranslatef(0.99, car_height * 2.4, 0)
    glutSolidCube(1.0)
    glPopMatrix()

    # Rear hood
    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)
    glScalef(car_length / 2.6, 0.2, car_width - 0.2)
    glTranslatef(-0.76, car_height * 2.4, 0)
    glutSolidCube(1.0)
    glPopMatrix()

    # Front bumper
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)  # Gray color
    glScalef(car_length / 4, 0.3, car_width + 0.1)
    glTranslatef(car_length / 3 + 0.22, -car_height * 1.5, 0)
    glutSolidCube(1.0)
    glPopMatrix()

    # Rear bumper
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)  # Gray color
    glScalef(car_length / 4, 0.3, car_width + 0.1)
    glTranslatef(-car_length / 3 - 0.22, -car_height * 1.5, 0)
    glutSolidCube(1.0)
    glPopMatrix()

    # Rear light left
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)
    glScalef(car_length / 22, car_height / 2.5, car_width / 8)
    glTranslatef(-car_length - 7, car_height / 2, -car_width - 1.55)
    glutSolidCube(1.0)
    glPopMatrix()

    # Rear light right
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)
    glScalef(car_length / 22, car_height / 2.5, car_width / 8)
    glTranslatef(-car_length - 7, car_height / 2, car_width + 1.55)
    glutSolidCube(1.0)
    glPopMatrix()

    # Rear number plate
    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)
    glScalef(car_length / 4.83, car_height / 4, car_width / 4)
    glTranslatef(-car_length / 2, -car_height / 1, 0)
    glutSolidCube(1.0)
    glPopMatrix()

    # Front light left
    glPushMatrix()
    glColor3f(0.8, 0.8, 0.0)
    glTranslatef(car_length / 1.99, car_height / 4, -car_width / 2.8)
    glRotatef(90, 0, 1, 0)
    gluDisk(gluNewQuadric(), 0, 0.15, 30, 1)
    glPopMatrix()

    # Front right left
    glPushMatrix()
    glColor3f(0.8, 0.8, 0.0)
    glTranslatef(car_length / 1.99, car_height / 4, car_width / 2.8)
    glRotatef(90, 0, 1, 0)
    gluDisk(gluNewQuadric(), 0, 0.15, 30, 1)
    glPopMatrix()

    # Orange lights
    glPushMatrix()
    glColor3f(0.9, 0.5, 0.0)
    glScalef(car_length / 30, car_height / 4, car_width / 20)
    glTranslatef(car_length * 3.7, car_height, car_width * 5)
    glutSolidCube(1.0)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.9, 0.5, 0.0)
    glScalef(car_length / 30, car_height / 4, car_width / 20)
    glTranslatef(car_length * 3.7, car_height, -car_width * 5)
    glutSolidCube(1.0)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.9, 0.5, 0.0)
    glScalef(car_length / 30, car_height / 4, car_width / 20)
    glTranslatef(-car_length * 3.8, car_height / 0.9, car_width * 5)
    glutSolidCube(1.0)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.9, 0.5, 0.0)
    glScalef(car_length / 30, car_height / 4, car_width / 20)
    glTranslatef(-car_length * 3.8, car_height / 0.9, -car_width * 5)
    glutSolidCube(1.0)
    glPopMatrix()

    # Front number plate
    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)
    glScalef(car_length / 4.83, car_height / 4, car_width / 4)
    glTranslatef(car_length / 2, -car_height, 0)
    glutSolidCube(1.0)
    glPopMatrix()

    # Radiator grill
    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)
    glScalef(car_length / 4.84, car_height / 2, car_width / 5)
    glTranslatef(car_length / 2, car_height - 0.7, -0.6)
    glutSolidCube(1.0)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)
    glScalef(car_length / 4.84, car_height / 2, car_width / 5)
    glTranslatef(car_length / 2, car_height - 0.7, 0.6)
    glutSolidCube(1.0)
    glPopMatrix()


def draw_wheel():
    glPushMatrix()

    # Wheel
    glColor3f(0.2, 0.2, 0.2)  # Dark gray color
    glutSolidTorus(wheel_width, wheel_radius, 9, 9)

    glPopMatrix()


def draw_car():
    # Draw car body
    glPushMatrix()
    glTranslatef(0, wheel_radius + car_height / 2, 0)
    draw_car_body()
    glPopMatrix()

    # Draw trapezoidal cabin
    glPushMatrix()
    glTranslatef(0.4, wheel_radius, 0)
    draw_trapezoidal_cabin(second_color[0], second_color[1], second_color[2])
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.4, wheel_radius, 0)
    glScalef(car_length / 3.8, car_height / 1.04, car_width / 2.3)
    draw_trapezoidal_cabin(0, 0, 0)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.4, wheel_radius, 0)
    glScalef(car_length / 4.4, car_height / 1.05, car_width / 1.99)
    draw_trapezoidal_cabin(0, 0, 0)
    glPopMatrix()

    # Draw wheels and wheel arches
    for dx in [-car_length / 2.5 + wheel_radius, car_length / 2.5 - wheel_radius]:
        for dz in [-car_width / 1.8 + wheel_radius, car_width / 1.8 - wheel_radius]:
            glPushMatrix()
            glColor3f(0.8, 0.8, 0.8)
            glTranslatef(dx, wheel_radius, dz * 1.33)
            gluDisk(gluNewQuadric(), 0, wheel_radius, 30, 1)
            glPopMatrix()

            glPushMatrix()
            glTranslatef(dx, wheel_radius, dz)
            draw_wheel()
            glTranslatef(0, wheel_radius, 0)
            glPopMatrix()


def display():
    global angle_x, angle_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(10.0, 5.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # Apply rotations
    glRotatef(angle_y, 0, 1, 0)
    glRotatef(angle_x, 1, 0, 0)

    # Draw car
    draw_car()

    glutSwapBuffers()


def keyboard(key, x, y):
    global angle_x, angle_y

    if key == b'\x1b':  # Escape key
        sys.exit()
    elif key == GLUT_KEY_UP:
        angle_x += 5
    elif key == GLUT_KEY_DOWN:
        angle_x -= 5
    elif key == GLUT_KEY_LEFT:
        angle_y -= 5
    elif key == GLUT_KEY_RIGHT:
        angle_y += 5

    glutPostRedisplay()


def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"3D Car Animation")
    init()
    glutDisplayFunc(display)
    glutSpecialFunc(keyboard)
    glutMainLoop()


if __name__ == "__main__":
    main()
