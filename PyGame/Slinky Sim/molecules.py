import pygame
from pygame.constants import *
from pygame.math import Vector2, Vector3
import math
from physics_objects import Circle  # copy in physics_objects.py from your previous project
from forces import *
import random
import colorsys


# INITIALIZE PYGAME AND OPEN WINDOW
pygame.init()
window = pygame.display.set_mode([700, 700])

# SETUP TIMING
fps = 60*3
dt = 1/fps
clock = pygame.time.Clock()

# SETUP OBJECTS
objects = [] 
spacing = 100
vel = 100
radius = 20
bond_length = 3*radius
pairs =[]
for i in range(6):
    x = spacing*(i + 1)
    for j in range(6):
        y = spacing*(j + 1)
        color = 255*Vector3(colorsys.hsv_to_rgb(random.random(), 1, 1))  # random bright, fully saturated color
        objects.append(a:=Circle(radius=radius, color=color, pos=Vector2(x, y) + Vector2(bond_length/2, 0).rotate(45), vel=Vector2(vel,0).rotate(random.uniform(0,360))))
        objects.append(b:=Circle(radius=radius, color=color, pos=Vector2(x, y) - Vector2(bond_length/2, 0).rotate(45), vel=Vector2(vel,0).rotate(random.uniform(0,360))))
        pairs.append((a,b))
        
# SETUP FORCES
box = Container(stiffness=100, rect=(radius,radius, window.get_width()-2*radius, window.get_height()-2*radius), objects=objects)
pairwise = LennardJones(sigma=2*radius, epsilon=10000, n=3, objects=objects)
bonds = HarmonicBonds(stiffness=100, length=bond_length, pairs=pairs)

# game loop
state = "running"
clock.tick()
while state != "quit":
    # DISPLAY
    pygame.display.update()
    # TIMING
    clock.tick(fps)
    # BACKGROUND GRAPHICS
    window.fill([0,0,0])

    # PHYSICS
    ## clear all forces from each object
    for o in objects:
        o.clear_force()

    ## apply each force
    box.apply()
    pairwise.apply()
    bonds.apply()
    
    ## update all objects
    for o in objects:
        o.update(dt)
    
    # GRAPHICS
    ## draw all objects
    for o in objects:
        o.draw(window)
     
    box.draw(window)
    bonds.draw(window)
    # EVENTS
    while event := pygame.event.poll():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            state = "quit"
        elif event.type == KEYDOWN:
            if event.unicode in ("+", "="):
                for o in objects:
                    o.vel *= 1.1
            elif event.unicode in ("-", "_"):
                for o in objects:
                    o.vel /= 1.1
            elif event.unicode == " " or event.key == K_BACKSPACE:
                for o in objects:
                    o.vel *= 0
     