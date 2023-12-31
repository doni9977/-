import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption('3D Earth')

gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

x_rotate = 0
y_rotate = 0
rotation_speed = 0.2

scale = 1.0

earth_texture = pygame.image.load('C:\\Users\\User\\Desktop\\8k_earth_daymap.jpg')
earth_data = pygame.image.tostring(earth_texture, 'RGB', 1)

width = earth_texture.get_width()
height = earth_texture.get_height()

glEnable(GL_TEXTURE_2D)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, earth_data)

mouse_pressed = False
start_mouse_x = 0
start_mouse_y = 0

def screen_to_world(mouse_x, mouse_y):
    viewport = glGetIntegerv(GL_VIEWPORT)
    winZ = glReadPixels(mouse_x, viewport[3] - mouse_y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    world_x, world_y, world_z = gluUnProject(mouse_x, viewport[3] - mouse_y, winZ, modelview, projection, viewport)
    return world_x, world_y, world_z

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pressed = True
            start_mouse_x, start_mouse_y = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pressed = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                scale += 0.1
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                scale -= 0.1
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            scale += 0.1
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            scale -= 0.1

    if mouse_pressed:
        current_mouse_x, current_mouse_y = pygame.mouse.get_pos()
        delta_x = current_mouse_x - start_mouse_x
        delta_y = current_mouse_y - start_mouse_y
        x_rotate += delta_y * rotation_speed
        y_rotate += delta_x * rotation_speed
        start_mouse_x, start_mouse_y = current_mouse_x, current_mouse_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glRotatef(x_rotate, 1, 0, 0)
    glRotatef(y_rotate, 0, 1, 0)
    glScalef(scale, scale, scale)

    if scale < 0.5:
        scale = 0.5
    elif scale > 3.0:
        scale = 3.0

    glBegin(GL_LINES)
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(2, 0, 0)

    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 2, 0)

    glEnd()

    glColor3f(1, 1, 1)
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, 1, 32, 32)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    viewport = glGetIntegerv(GL_VIEWPORT)
    winZ = glReadPixels(mouse_x, viewport[3] - mouse_y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    world_x, world_y, world_z = gluUnProject(mouse_x, viewport[3] - mouse_y, winZ, modelview, projection, viewport)

    font = pygame.font.Font(None, 36)
    text = font.render(f'Нажатие на мировой координате: ({world_x:.2f}, {world_y:.2f}, {world_z:.2f})', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.bottomright = (display[0], display[1])
    
    pygame.display.get_surface().blit(text, text_rect)

    glPopMatrix()
    pygame.display.flip()
    pygame.time.wait(10)
