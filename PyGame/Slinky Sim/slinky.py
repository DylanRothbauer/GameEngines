import pygame
from pygame.constants import *
from pygame.math import Vector2, Vector3
import math
from physics_objects import Circle  # copy in physics_objects.py from your previous project
from forces import *
from pygame.color import Color
import random
import colorsys

# INITIALIZE PYGAME AND OPEN WINDOW
pygame.init()
screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
window = pygame.display.set_mode([0.8*screen_width, 0.8*screen_height])

# SCALE
HEIGHT_METERS = 2.0
PIXELS_PER_METER = window.get_height() / HEIGHT_METERS

# SETUP TIMING
fps = 60*3
dt = 1/fps
clock = pygame.time.Clock()

# SETUP OBJECTS
objects:list[Circle] = []
pairs = []
num_circles = 15
radius_m = 0.035          # 35 mm
spacing_m = 0.105         # 105 mm
mass = 0.01               # 10 grams 
vel = (0,0)
damping = 0.5             # damping coefficient
stiffness = 50            # spring stiffness

# Input/Input/Interaction variables
grabbed = None
prev_mouse_pos = None
grabbed_offset = None

# Drag parameters
area_m2 = math.pi * (radius_m**2)
p = 1.2
c_d = 0.47

p_px = p / (PIXELS_PER_METER ** 3)   # kg / pixel^3
area_px = area_m2 * (PIXELS_PER_METER ** 2)

# Wind
wind_m_s = 0.0
WIND_STEP_M_S = 0.2
MAX_WIND_M_S = 30.0

radius_px = radius_m * PIXELS_PER_METER
spacing_px = spacing_m * PIXELS_PER_METER

# Gravity Constant
GRAVITY = 9.8 * PIXELS_PER_METER

x_center = window.get_width() / 2
y_start = window.get_height() / 20

def get_random_color():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)

def draw_wind_bar(screen, wind, max_speed=MAX_WIND_M_S, bar_length=500, bar_height=10):
    cx = screen.get_width() // 2
    cy = 30
    wind_m_s = wind.x / PIXELS_PER_METER
    length = int((wind_m_s / max_speed) * bar_length)

    # bar outline
    pygame.draw.rect(screen, (200, 200, 200), (cx - bar_length, cy, 2*bar_length, bar_height), 1)

    # wind bar
    if length > 0: # Right wind
        color = (255, 0, 0)
        pygame.draw.rect(screen, color, (cx, cy, length, bar_height))
    elif length < 0:  # Left wind
        color = (0, 0, 255)
        pygame.draw.rect(screen, color, (cx + length, cy, -length, bar_height))

    # wind text
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Wind: {wind_m_s:.2f} m/s", True, (255, 255, 255))
    screen.blit(text, (20, 60))
        
for i in range(num_circles):
    x = x_center
    y = y_start + i * spacing_px
    if i == 0:
        circle = Circle(mass=mass, pos=Vector2(x, y), radius=radius_px, fixed=True, color=(255,0,0), vel=vel)
    else:
        circle = Circle(mass=mass, pos=Vector2(x, y), radius=radius_px, color=get_random_color(), vel=vel)
        pairs.append((objects[-1], circle))

    #pairs.append((circle, circle2))
    objects.append(circle)

# here is one circle as an example
# circle = Circle(mass=1, pos=(window.get_width()/2, window.get_height()/20), radius=30)  # change mass and radius
# objects.append(circle)

# SETUP FORCES
gravity = Gravity(objects=objects, acc=(0,GRAVITY))
bonds = SpringForce(stiffness=stiffness, length=spacing_px, damping=damping, pairs=pairs)
drag = Drag(p=p_px, c_d=c_d, area=area_px, wind=Vector2(wind_m_s * PIXELS_PER_METER, 0), objects=objects)
replusion = SpringRepulsion(stiffness=stiffness, objects=objects)

# game loop
state = "running"
clock.tick()
while state != "quit":
    # DISPLAY
    pygame.display.update()
    # TIMING
    clock.tick(fps)
    # BACKGROUND GRAPHICS
    window.fill([135,206,235])  # sky blue
 
    # EVENTS
    while event := pygame.event.poll():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            state = "quit"
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = Vector2(event.pos)
            ctrl_held = pygame.key.get_mods() & KMOD_CTRL
            for o in objects:
                if (o.pos - mouse_pos).magnitude() < o.radius:
                    if ctrl_held:
                        # Delete circle
                        objects.remove(o)

                        # Remove bonds
                        pairs = [pair for pair in pairs if o not in pair] # remove any pair involving o
                        bonds.pairs = pairs
                        break
                    else:
                        grabbed = o
                        prev_mouse_pos = mouse_pos
                        grabbed_offset = grabbed.pos - mouse_pos
                        break
        elif event.type == MOUSEBUTTONUP:
            if grabbed is not None:
                if grabbed.fixed:
                    grabbed.vel = Vector2(0, 0)
            grabbed = None
            prev_mouse_pos = None
            grabbed_offset = None
        elif event.type == KEYDOWN and event.key == K_SPACE:
            if grabbed is not None:
                grabbed.fixed = not grabbed.fixed # toggle fixed/free
                if grabbed.fixed:
                    grabbed.color = (100, 100, 100)
                    grabbed.vel = Vector2(0, 0)
                else:
                    grabbed.color = grabbed.original_color

     
    # PHYSICS
    mouse_pos = Vector2(pygame.mouse.get_pos())
    ## clear all forces from each object
    for o in objects:
        o.clear_force()

    ## apply all forces
    gravity.apply()
    bonds.apply()
    drag.apply()
    replusion.apply()
    
    ## update all objects
    mouse_vel = None
    if prev_mouse_pos is not None:
        mouse_vel = (mouse_pos - prev_mouse_pos) / dt

    for o in objects:
        if o is grabbed:
            o.clear_force()
            if mouse_vel is not None:
                o.vel = mouse_vel
            o.update(dt)
        else:
            # normal objects updated from forces
            o.update(dt)

    if grabbed is not None:
        prev_mouse_pos = mouse_pos
    
    # STATE CHECKS
    ## Mouse state check for grabbing objects
    ## Key state check for changing wind velocity
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        wind_m_s = max(wind_m_s - WIND_STEP_M_S, -MAX_WIND_M_S)
        drag.wind = Vector2(wind_m_s * PIXELS_PER_METER, 0)
    if keys[pygame.K_RIGHT]:
        wind_m_s = min(wind_m_s + WIND_STEP_M_S, MAX_WIND_M_S)
        drag.wind = Vector2(wind_m_s * PIXELS_PER_METER, 0)

    # GRAPHICS
    ## draw all objects
    for o in objects:
        o.draw(window)

    bonds.draw(window)
    draw_wind_bar(window, drag.wind)

