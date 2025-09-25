import pygame
from pygame.locals import *
from pygame.math import Vector2, Vector3
import random
import math
from physics_objects import Circle

# CONSTANTS

# INITIALIZE PYGAME
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("arialblack", 80)

# CREATE WINDOW
window = pygame.display.set_mode([1000,700])

# TIMING
clock = pygame.time.Clock()
FPS = 60
dt = 1/FPS
clock.tick()

# SETUP
objects:list[Circle] = []

# drone
drone = Circle(radius=50, color=(255,0,0), pos=(100,100), vel=(200,0))
objects.append(drone)

# checkpoints
# Randomly arranged on the screen, not overlapping the edges
checkpoints:list[Circle] = []
for i in range(4):
    radius = 100
    checkpoints.append(Circle(radius=radius, color=(0,255,0), width=5, 
                              pos=(random.randint(radius, window.get_width()-radius-1), 
                                   random.randint(radius, window.get_height()-radius-1))))

# GAME LOOP
state = "play"
while state != "quit":
     # DISPLAY AND TIMING
    pygame.display.update()
    clock.tick(FPS) / 1000
    
    # BACKGROUND GRAPHICS
    window.fill((0,0,0))

    # PHYSICS
    ## Clear force from all objects
    for obj in objects:
        obj.clear_force()

    ## Add forces
    ### Gravity downward
    drone.add_force((0, 300))

    ### Thrust force
    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        drone.add_force((0, -800))
    if keys[K_LEFT]:
        drone.add_force((-300, 0))
    if keys[K_RIGHT]:
        drone.add_force((300, 0))
    # ^ In Orbital.py, we will do it in a slightly different way

    ### Air resistance (if time permits)
    drone.add_force(-drone.vel * drone.vel.magnitude()/100* 0.1)

    ## Update objects
    for obj in objects + checkpoints:
        obj.update(dt)

    # GAME ELEMENTS
    ## Checkpoints
    # check to see if the drone is inside a checkpoint
    for c in checkpoints:
        if c.pos.distance_to(drone.pos) < c.radius - drone.radius:
            c.width = 0 # filled in

    
    # GRAPHICS
    draw_objects = checkpoints + objects
    draw_objects.sort(key=lambda x: x.width)
    for obj in draw_objects:
        obj.draw(window)
    
    if all(x.width == 0 for x in checkpoints):
        text = font.render("YOU WIN!", True, (255,255,255))
        window.blit(text, ((window.get_width()-text.get_width())/2, (window.get_height()-text.get_height())/2))
    
   
    # EVENTS
    while event := pygame.event.poll():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            state = "quit"
        # add more events, such as for pause or restarting from game over
        