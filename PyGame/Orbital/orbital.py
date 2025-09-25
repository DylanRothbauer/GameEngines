import pygame
from pygame.locals import *
from pygame.math import Vector2, Vector3
import random
import math
from physics_objects import Circle


# INITIALIZE PYGAME
pygame.init()

# CREATE WINDOW
screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
SIZE = 0.4*min(screen_height, screen_width)
window = pygame.display.set_mode([2*SIZE+1, 2*SIZE+1])
center = Vector2(window.get_width(), window.get_height()) / 2

# FONT
pygame.font.init()
font = pygame.font.SysFont("arialblack", 80)

# TIMING
clock = pygame.time.Clock()
FPS = 60
dt = 1/FPS
clock.tick()
start_time = None
elapsed_time = 0
final_time = None
paused = False
collected = 0

# CONSTANTS
GM = SIZE**3 / 15

# SETUP
def init_game():
    global collected
    collected = 0
    objects:list[Circle] = []
    # Sun
    sun = Circle(radius=SIZE/10, color=(255,255,0), pos=center)

    # Ship
    ship = Circle(radius=SIZE/30, color=(135,206,250), pos=(window.get_width()/4, window.get_height()/4), name="ship")

    # Initial velocities
    r_vec = ship.pos - sun.pos
    r = r_vec.length()
    v = math.sqrt(GM * sun.mass / r)
    direction = r_vec.rotate(90).normalize() # perpendicular to r_vec
    ship.vel = direction * v

    objects.append(ship)

    # Dots
    dot_radius = ship.radius / 2
    num_dots = 6
    min_r = SIZE * 0.2
    max_r = SIZE * 0.9

    for i in range(num_dots):
        step = (max_r - min_r) / (num_dots + 1)
        r = min_r + step * (i + 1)
        angle = random.uniform(0, 360) # random angle around the sun
        bad_dot_angle = random.uniform(0, 360)
        bad_dot_r_vec = Vector2(r, 0).rotate(bad_dot_angle)
        r_vec = Vector2(r, 0).rotate(angle)

        dot = Circle(radius=dot_radius, color=(255, 255, 255))
        bad_dot = Circle(radius=dot_radius, color=(255, 0, 0), name="bad_dot")
        bad_dot.pos = sun.pos + bad_dot_r_vec

        while bad_dot.pos == ship.pos: # So it doesnt spawn on ship
            bad_dot_angle = random.uniform(0, 360)
            bad_dot_r_vec = Vector2(r, 0).rotate(bad_dot_angle)
            bad_dot.pos = sun.pos + bad_dot_r_vec
            
        #bad_dot.pos = sun.pos + bad_dot_r_vec
        dot.pos = sun.pos + r_vec

        v = math.sqrt(GM * sun.mass / r)
        direction = r_vec.rotate(90).normalize()
        bad_dot_direction = bad_dot_r_vec.rotate(90).normalize()
        bad_dot.vel = bad_dot_direction * v
        dot.vel = direction * v

        objects.append(dot)
        objects.append(bad_dot)

    # Reset timer and state-related vars
    start_time = pygame.time.get_ticks()
    elapsed_time = 0
    final_time = None
    paused = False
    state = "play"

    return objects, sun, ship, start_time, elapsed_time, final_time, paused, state, num_dots, collected

# GAME LOOP
objects, sun, ship, start_time, elapsed_time, final_time, paused, state, num_dots, collected = init_game()

while state != "quit":
    # DISPLAY AND TIMING
    pygame.display.update()
    clock.tick(FPS) / 1000

    # BACKGROUND GRAPHICS
    window.fill((0,0,0))

    # EVENTS
    while event := pygame.event.poll():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            state = "quit"
        elif event.type == KEYDOWN and event.key == K_p:
            if state == "play":
                paused = not paused
        elif event.type == KEYDOWN and event.key == K_SPACE:
            # Restart: reinitialize game state
            objects, sun, ship, start_time, elapsed_time, final_time, paused, state, num_dots, collected = init_game()
        # add more events, such as for pause or restarting from game over
    if paused:
        # Draw pause message and skip physics
        text = font.render("PAUSED", True, (255, 255, 255))
        window.blit(text, ((window.get_width()-text.get_width())/2, (window.get_height()-text.get_height())/2))
        pygame.display.update()
        # stop the timer
        if start_time is not None:
            start_time += clock.get_time()  # Adjust start_time to account for paused duration
        continue

    if state in ("play", "game over"):
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    elif state == "win" and final_time is None:
        # Freeze the timer once
        final_time = elapsed_time

    # Timer
    display_time = final_time if final_time is not None else elapsed_time
    minutes = display_time // 60
    seconds = display_time % 60
    time_text = font.render(f"{minutes:02}:{seconds:02}", True, (255, 255, 255))
    window.blit(time_text, (20, 20))

    # Collected
    points_text = font.render(f"{collected} / {num_dots}", True, (255,255,255))
    window.blit(points_text, (400,20))

    # Sun
    sun.draw(window)

    # PHYSICS
    ## Clear force from all objects
    for obj in objects:
        obj.clear_force()

    ## Add forces
    ### Gravitational force toward sun
    for obj in objects:
        r_vec = sun.pos - obj.pos
        r = r_vec.length()

        if r != 0:
            r_hat = r_vec.normalize()
            F = (GM * sun.mass * obj.mass / r**2) * r_hat
            obj.add_force(F)

    ### Thrust force
    keys = pygame.key.get_pressed()
    thrust = Vector2(0,0)
    if keys[K_UP]:
        thrust.y -= 1
    if keys[K_DOWN]:
        thrust.y += 1
    if keys[K_LEFT]:
        thrust.x -= 1
    if keys[K_RIGHT]:
        thrust.x += 1

    if thrust.length() > 0:
        thrust = thrust.normalize() * (SIZE/15) * ship.mass # thurst.normalize() makes it length 1 so diagonal isn't stronger
        ship.add_force(thrust)

        # Flame behind ship (small yellow circle)
        flame_pos = ship.pos - thrust.normalize() * ship.radius
        pygame.draw.circle(window, (255,255,0), flame_pos, ship.radius/4)

    ## Update objects
    for obj in objects:
        obj.update(dt)

    # GAME ELEMENTS
    ## Dot collection
    for dot in objects[1:]: # skip the sun which is the first object
        if dot.pos.distance_to(ship.pos) < dot.radius + ship.radius:
            if dot.name == "bad_dot":
                state = "game over"
                continue

            collected += 1
            objects.remove(dot)

    ## Winning
    if len(objects) == 1: # only the ship is left
        state = "win"

    ## Losing
    if ship.pos.distance_to(sun.pos) < sun.radius + ship.radius:
        state = "game over"

    # GRAPHICS
    for obj in objects:
        obj.draw(window)
    
    
    if state == "game over":
        window.fill((0,0,0))
        sun.draw(window)
        text = font.render("YOU LOSE!", True, (255,0,0))
        window.blit(text, ((window.get_width()-text.get_width())/2, (window.get_height()-text.get_height())/2))

        # Dont draw the ship!
        for obj in objects:
            if obj.name == "ship":
                continue
            obj.draw(window)

        display_time = final_time if final_time is not None else elapsed_time
        minutes = display_time // 60
        seconds = display_time % 60
        time_text = font.render(f"{minutes:02}:{seconds:02}", True, (255, 255, 255))
        window.blit(time_text, (20, 20))

        # Collected
        points_text = font.render(f"{collected} / {num_dots}", True, (255,255,255))
        window.blit(points_text, (400,20))

        # pygame.display.update()
        # pygame.time.delay(2000)
    elif state == "win":
        text = font.render("YOU WIN!", True, (0,128,0))
        window.blit(text, ((window.get_width()-text.get_width())/2, (window.get_height()-text.get_height())/2))
        # pygame.display.update()
        # pygame.time.delay(2000)