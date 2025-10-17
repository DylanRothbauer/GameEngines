import pygame
from pygame.locals import *
from physics_objects import Circle, Wall
import contact
from pygame.math import Vector2

# Create window
window = pygame.display.set_mode([800, 600])

# Clock object for timing
clock = pygame.time.Clock()
fps = 60
dt = 1/fps

# Objects
objects = []
objects.append(Circle(pos=(400,300), vel=(0,0), mass=14, radius=100, color=(0,0,255)))
objects.append(Circle(pos=(100,290), vel=(100,0), mass=10, radius=50, color=(255,0,0)))

objects.append(Wall(point1=(400,0), point2=(800,600), color=(255,255,255), width=1))
objects.append(Wall(point2=(0,600), point1=(800,300), color=(255,255,255), width=1))

# Game loop
running = True
while running:
    pygame.display.update()
    clock.tick(fps)
    window.fill([0,0,0])
    
    # Event handling loop
    while event := pygame.event.poll():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
 
    # Physics
    ## Add forces
    # no forces to add

    ## Update particles
    for obj in objects:
        obj.update(dt)

    ## Clear force from all particles
    for obj in objects:
        obj.clear_force()

    # Collisions
    for j in range(len(objects)):
        for i in range(j):
            c = contact.generate(objects[i], objects[j], restitution=1, resolve=True)
            if c.overlap > 0:
                window.fill([255,255,0]) # color background yellow

    # Graphics
    ## Draw objects
    for obj in objects:
        obj.draw(window)

    # calculate the center of mass an draw it
    com_num = Vector2(0,0)
    com_den = 0
    for obj in objects:
        com_num += obj.mass * obj.pos
        com_den += obj.mass
    com = com_num / com_den
    #com = sum([obj.mass * obj.pos for obj in objects], Vector2(0,0)) / sum([obj.mass for obj in objects])
    pygame.draw.circle(window, (0,255,0), com, 10) # draw center of mass as a small green circle

