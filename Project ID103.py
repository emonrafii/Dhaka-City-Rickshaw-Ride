from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import sys

sunX = -40
rickshawX = 300
wheelAngle = 0
sceneX = 0
night = False
moving = True
nightTimer = 0

def square(x, y, width, height):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

def triangle(x, y, width, height):
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width / 2, y + height)
    glEnd()

def polygon(points):
    glBegin(GL_POLYGON)
    for x, y in points:
        glVertex2f(x, y)
    glEnd()

def circle(cx, cy, radius):
    x = 0
    y = radius
    d = 1 - radius
    glBegin(GL_POINTS)
    while x <= y:
        glVertex2f(cx + x, cy + y)
        glVertex2f(cx - x, cy + y)
        glVertex2f(cx + x, cy - y)
        glVertex2f(cx - x, cy - y)
        glVertex2f(cx + y, cy + x)
        glVertex2f(cx - y, cy + x)
        glVertex2f(cx + y, cy - x)
        glVertex2f(cx - y, cy - x)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
    glEnd()

# Filled Circle
def filledCircle(cx, cy, radius):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(cx, cy)
    for angle in range(361):
        rad = math.radians(angle)
        x = cx + radius * math.cos(rad)
        y = cy + radius * math.sin(rad)
        glVertex2f(x, y)
    glEnd()

# Glow Effect using Blending
def glow(x, y, radius, color):
    glColor4f(color[0], color[1], color[2], 0.12)
    filledCircle(x, y, radius + 25)
    glColor4f(color[0], color[1], color[2], 0.22)
    filledCircle(x, y, radius + 12)
    glColor4f(color[0], color[1], color[2], 1.0)
    filledCircle(x, y, radius)

# Gradient Sky (Shading)
def drawSky():
    glBegin(GL_QUADS)
    if night:
        glColor3f(0.12, 0.15, 0.30)
        glVertex2f(0, 200)
        glVertex2f(800, 200)
        glColor3f(0.02, 0.03, 0.12)
        glVertex2f(800, 600)
        glVertex2f(0, 600)
    else:
        glColor3f(0.65, 0.85, 1.0)
        glVertex2f(0, 200)
        glVertex2f(800, 200)
        glColor3f(0.20, 0.55, 0.95)
        glVertex2f(800, 600)
        glVertex2f(0, 600)
    glEnd()

# Fog Effect using Alpha Blending
def drawFog():
    glBegin(GL_QUADS)
    if night:
        glColor4f(0.65, 0.70, 0.90, 0.12)
    else:
        glColor4f(0.90, 0.95, 1.0, 0.20)
    glVertex2f(0, 200)
    glVertex2f(800, 200)
    glColor4f(0.90, 0.95, 1.0, 0.0)
    glVertex2f(800, 285)
    glVertex2f(0, 285)
    glEnd()


# Building Function
def building(x, y, width, height, color):
    # Building Body
    glColor3f(*color)
    square(x, y, width, height)
    # Roof
    glColor3f(0.25, 0.25, 0.30)
    square(x - 5, y + height, width + 10, 10)
    # Windows
    windowWidth = 20
    windowHeight = 25
    for row in range(3):
        for col in range(3):
            wx = x + 15 + col * 35
            wy = y + 25 + row * 55
            if night and (row + col) % 2 == 0:
                glColor3f(1.0, 0.78, 0.30)
            else:
                glColor3f(0.55, 0.80, 0.95)
            square(wx, wy, windowWidth, windowHeight)
            # Window Frame
            glColor3f(0.25, 0.25, 0.30)
            glBegin(GL_LINE_LOOP)
            glVertex2f(wx, wy)
            glVertex2f(wx + windowWidth, wy)
            glVertex2f(wx + windowWidth, wy + windowHeight)
            glVertex2f(wx, wy + windowHeight)
            glEnd()

    # Balcony
    glColor3f(0.35, 0.35, 0.40)
    square(x + 10, y + 10, width - 20, 5)
    glBegin(GL_LINES)
    for i in range(5):
        bx = x + 15 + i * 25
        glVertex2f(bx, y + 10)
        glVertex2f(bx, y + 25)
    glEnd()

# Tree Function
def tree(x, y, size):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(size, size, 1)
    # Trunk
    glColor3f(0.40, 0.20, 0.08)
    square(-8, 0, 16, 60)
    # Leaves
    glColor3f(0.05, 0.40, 0.12)
    filledCircle(0, 85, 30)
    filledCircle(-20, 70, 25)
    filledCircle(20, 70, 25)
    glPopMatrix()

# Road Function
def road():
    global sceneX
    # Green Ground
    glColor3f(0.20, 0.55, 0.20)
    square(0, 100, 800, 100)
    # Road
    glColor3f(0.20, 0.20, 0.23)
    square(0, 0, 800, 100)
    # Moving Road Lines
    glColor3f(1.0, 1.0, 1.0)
    for i in range(-100, 900, 100):
        x = i - (sceneX % 100)
        square(x, 48, 50, 5)

# Sun and Moon
def sun():
    if not night:
        # Sun Glow
        glow(sunX, 470, 30, (1.0, 0.80, 0.10))
    else:
        # Moon Glow
        glow(700, 470, 25, (0.75, 0.85, 1.0))
        # Moon
        glColor3f(0.90, 0.92, 1.0)
        filledCircle(700, 470, 25)
        # Moon Shadow
        glColor3f(0.12, 0.15, 0.30)
        filledCircle(710, 480, 22)

# Street Light
def streetLight():
    # Pole
    glColor3f(0.25, 0.25, 0.30)
    square(390, 200, 6, 100)
    # Top Bar
    square(375, 295, 35, 6)
    if night:
        # Light Glow
        glow(392, 290, 8, (1.0, 0.85, 0.35))
    else:
        glColor3f(0.85, 0.85, 0.70)
        filledCircle(392, 290, 6)

# Wheel Function
def wheel(x, y):

    glPushMatrix()

    glTranslatef(x, y, 0)
    glRotatef(wheelAngle, 0, 0, 1)

    # Wheel
    glPointSize(3)
    glColor3f(0.05, 0.05, 0.05)
    circle(0, 0, 20)
    # Spokes
    glBegin(GL_LINES)
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        glVertex2f(0, 0)
        glVertex2f(20 * math.cos(rad), 20 * math.sin(rad))
    glEnd()
    # Center
    glColor3f(0.75, 0.75, 0.75)
    filledCircle(0, 0, 5)
    glPopMatrix()

# Rickshaw Function
def rickshaw():
    glPushMatrix()
    glTranslatef(rickshawX, 0, 0)
    # Main Body
    glColor3f(0.05, 0.55, 0.25)
    polygon([
        (0, 40),
        (120, 40),
        (110, 90),
        (15, 90)
    ])
    # Seat
    glColor3f(0.85, 0.15, 0.10)
    square(25, 90, 65, 10)
    # Hood
    glColor3f(0.95, 0.10, 0.15)
    polygon([
        (10, 95),
        (25, 150),
        (90, 150),
        (115, 95)
    ])

    # Hood Decoration
    glColor3f(1.0, 0.85, 0.10)
    triangle(40, 110, 35, 25)
    # Driver Head
    glColor3f(0.85, 0.65, 0.45)
    filledCircle(65, 155, 12)
    # Driver Body
    glColor3f(0.05, 0.20, 0.55)
    square(55, 125, 20, 25)
    # Wheels
    wheel(25, 35)
    wheel(100, 35)
    glPopMatrix()

# Moving City Background
def cityPart(offset):
    glPushMatrix()
    glTranslatef(offset, 0, 0)
    # Buildings
    building(50, 200, 110, 200, (0.85, 0.65, 0.50))
    building(230, 200, 140, 260, (0.65, 0.70, 0.80))
    building(450, 200, 120, 220, (0.85, 0.75, 0.60))
    building(650, 200, 110, 180, (0.75, 0.65, 0.75))
    # Trees
    tree(180, 200, 0.5)
    tree(600, 200, 1.0)
    # Street Light
    streetLight()
    glPopMatrix()

# Display Function
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT)
    # Sky
    drawSky()
    # Sun / Moon
    sun()
    # Road and Ground
    road()
    # Moving City Background
    cityPart(-sceneX)
    cityPart(800 - sceneX)
    # Fog
    drawFog()
    # Rickshaw
    rickshaw()
    glutSwapBuffers()

# Animation Function
def update(value):
    global sunX, wheelAngle, sceneX
    global night, nightTimer
    if moving:
        # Sun moves from Left to Right
        if not night:
            sunX += 1
            # Sun disappears on Right
            if sunX > 850:
                night = True
                nightTimer = 0
        else:
            # Night stays for 3 seconds
            nightTimer += 1
            if nightTimer >= 100:
                night = False
                sunX = -40
                nightTimer = 0
        # Background Movement
        sceneX += 1
        if sceneX >= 800:
            sceneX = 0
        # Wheel Rotation
        wheelAngle -= 8
    glutPostRedisplay()
    glutTimerFunc(30, update, 0)

# Keyboard Function
def keyboard(key, x, y):
    global moving, night, sunX
    if key == b'n':
        night = not night
        if not night:
            sunX = -40
    elif key == b' ':
        moving = not moving
    elif key == b'\x1b':
        sys.exit(0)
    glutPostRedisplay()


# Arrow Key Event
def arrowKey(key, x, y):
    global rickshawX
    if key == GLUT_KEY_RIGHT:
        rickshawX += 10
    elif key == GLUT_KEY_LEFT:
        rickshawX -= 10
    glutPostRedisplay()

# Mouse Event
def mouseClick(button, state, x, y):
    global night, sunX
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        night = not night
        if not night:
            sunX = -40
    glutPostRedisplay()

# Coordinate System
def iterate():
    glViewport(0, 0, 800, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 600)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Dhaka City Rickshaw Ride")
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glClearColor(0.5, 0.7, 1.0, 1.0)
glutDisplayFunc(showScreen)
glutReshapeFunc(lambda w, h: iterate())
glutKeyboardFunc(keyboard)
glutSpecialFunc(arrowKey)
glutMouseFunc(mouseClick)
glutTimerFunc(30, update, 0)
iterate()
glutMainLoop()