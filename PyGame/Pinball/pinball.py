import pygame
from pygame.constants import *
from pygame.math import Vector2
from physics_objects import Circle, Polygon, Wall
from tiled_helper_json import Circle, Wall, Polygon, load_tmj_to_objects
import contact
from forces import *
import math

# Flipper helper functions
def press_flipper(flipper, dt):
    if flipper is None:
        return
    if flipper.name == "left":
        flipper.angle -= flipper_speed * dt  # negative to go up
        if flipper.angle <= -flipper_angle_limit:
            flipper.angle = -flipper_angle_limit
            flipper.avel = 0.0
        else:
            flipper.avel = -flipper_speed
    else:  # right flipper
        # Right flipper rotates counterclockwise from pi
        flipper.angle += flipper_speed * dt
        if flipper.angle >= math.pi + flipper_angle_limit:
            flipper.angle = math.pi + flipper_angle_limit
            flipper.avel = 0.0
        else:
            flipper.avel = flipper_speed

def release_flipper(flipper, dt):
    if flipper is None:
        return
    if flipper.name == "left":
        flipper.angle += flipper_speed * dt
        if flipper.angle >= 0:
            flipper.angle = 0
            flipper.avel = 0.0
        else:
            flipper.avel = flipper_speed
    else:
        flipper.angle -= flipper_speed * dt
        if flipper.angle <= math.pi:
            flipper.angle = math.pi
            flipper.avel = 0.0
        else:
            flipper.avel = -flipper_speed

# Plunger helper functions
def press_plunger():
    global plunger_vel, plunger_acc, plunger_state
    plunger_state = "retracting"
    plunger_acc = 0.0
    plunger_vel = abs(plunger_retract_speed)

def release_plunger():
    global plunger_acc, plunger_state
    plunger_state = "releasing"
    plunger_acc = plunger_release_accel

def update_plunger(dt):
    global plunger_vel, plunger_acc, plunger_state
    if plunger is None:
        return
    if plunger_state == "retracting":
        plunger.vel.y = abs(plunger_retract_speed)
    elif plunger_state == "releasing":
        plunger.vel.y += plunger_acc * dt
    elif plunger_state == "idle":
        plunger.vel.y = 0.0
        plunger_acc = 0.0

    # move plunger vertically
    plunger.pos.y += plunger.vel.y * dt

    # limits
    if plunger.pos.y >= plunger_min_y:
        plunger.pos.y = plunger_min_y
        plunger.vel.y = 0.0
        plunger_acc = 0.0
        plunger_state = "idle"
    # If plunger reaches the top while releasing, transfer impulse to ball
    if plunger.pos.y <= plunger_max_y:
        # if plunger_state == "releasing" and ball is not None:
        #     ball.vel.y = min(-plunger_vel * 1.2, -400)
        plunger.pos.y = plunger_max_y
        plunger.vel.y = 0.0
        plunger_acc = 0.0
        plunger_state = "idle"


pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load("game-music-loop-6.mp3")
objects, (width, height) = load_tmj_to_objects("pinball.tmj")
window = pygame.display.set_mode([width, height])


PIXELS_PER_METER = 100
GRAVITY = 9.81 * math.sin(math.radians(6.5)) * PIXELS_PER_METER
game_state = ""
bumper_sound = pygame.mixer.Sound("pop.mp3")
bonus_zone_sound = pygame.mixer.Sound("bonus.mp3")

# Plunge variables
plunger_retract_speed = 300.00
plunger_release_accel = -1200.00
plunger_vel = 0.0
plunger_acc = 0.0
plunger_state = "idle"
plunger_max_y = None
plunger_min_y = None

# Flipper variables
flipper_speed = 5.0  # radians per second
flipper_angle_limit = math.radians(30)  # maximum angle from rest position

# Ball reset variables
ball_reset_y = -100  # y position to reset ball to
ball_reset_x = width // 2  # x position to reset ball to

# Fonts
plunger_state_font = pygame.font.SysFont('Arial', 24)

# Colors
original_bumper_color = None

# Variables
score = 0
balls_left = 3
bumper_color_change_duration = 1.0  # seconds

# Clock object for timing
clock = pygame.time.Clock()
fps = 60
dt = 1/fps

# OBJECTS
ball:Circle = None
walls:list[Wall] = []
plunger:Polygon = None
flippers:list[Polygon] = []
bonus_circles:list[Circle] = []
bumpers:list[Polygon] = []
exit_zone:Polygon = None

for x in objects:
    if x.type == "ball": # ball
        ball = x
        ball.color = (0,255,0)
        ball.mass = 1
        ball_reset_x, ball_reset_y = ball.pos.x, ball.pos.y
    elif x.type == "wall": # walls
        x.color = (255,255,255)
        walls.append(x)
    elif x.type == "flipper": # paddles/flippers
        x.color = (0,0,255)
        if x.name == "right":
            x.angle = math.pi # pointing left
        flippers.append(x)
    elif x.type == "plunger": # plunger
        x.color = (255,0,0)
        plunger = x
        plunger_max_y = plunger.pos.y
        plunger_min_y = 700 # hardcoded for now
    elif x.type == "bonus_circle":
        bonus_circles.append(x)
    elif x.type == "bumper":
        x.rebound = 200
        # store the original color per-bumper and a timer for color changes
        original_bumper_color = x.color
        bumper_color_change_duration = 0.0
        bumpers.append(x)
    elif x.type == "exit_zone":
        exit_zone = x

# bumpers
# bonus zones

objects:list = []
objects.append(ball)
objects.append(plunger)
objects.extend(walls)
objects.extend(flippers)
objects.extend(bumpers)

gravity = Gravity(objects=objects, acc=(0,GRAVITY))

# Game loop
running = True
pygame.mixer.music.play(-1)
while running:
    pygame.display.update()
    clock.tick(fps)
    window.fill((0,0,0))

    # EVENTS
    while event := pygame.event.poll():
        if event.type == QUIT:
            running = False

    # KEY STATE
    # Plunger control
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                print("Plunger key pressed")
                press_plunger()
        elif event.type == KEYUP:
            if event.key == K_DOWN:
                print("Plunger key released")
                release_plunger()
    
    # Paddle controls
    # Update flippers
    keys = pygame.key.get_pressed()
    for flipper in flippers:
        if flipper.name == "left" and keys[K_LEFT]:
            press_flipper(flipper, dt)
        elif flipper.name == "right" and keys[K_RIGHT]:
            press_flipper(flipper, dt)
        else:
            release_flipper(flipper, dt)
    
    # PHYSICS
    # Add forces
    
    # Update plunger
    update_plunger(dt)

    # Apply forces
    gravity.apply()

    # Update particles
    for o in objects:
        o.update(dt)
    
    # Clear force from all particles
    for o in objects:
        o.clear_force()

    # Checking if pinball has fallen out of the game
        
    # CONTACTS
    for obj in objects:
        contact.generate(ball, obj, restitution=obj.restitution, rebound=obj.rebound, resolve=obj.resolve)
    
    # GRAPHICS
    ## Clear window
    window.fill((0,0,0))


    # Add to score if ball overlaps with bonus circle
    for c in bonus_circles:
        c.draw(window)
        contact_instance = contact.generate(ball, c)
        if contact_instance.overlap > 0:
            bonus_zone_sound.play()
            score += 1

    for b in bumpers:
        if bumper_color_change_duration <= 0.0:
            b.color = original_bumper_color
        c = contact.generate(ball, b)
        if c.overlap > 0:
            bumper_sound.play()
            b.color = (255,255,0)
            if bumper_color_change_duration >= 0.0:
                bumper_color_change_duration -= dt
            

    # Check if ball is in exit zone
    if exit_zone is not None:
        exit_zone.draw(window)
        contact_instance = contact.generate(ball, exit_zone)
        if contact_instance.overlap > 0:
            if balls_left > 0:
                balls_left -= 1
                # Reset ball position
                ball.pos = Vector2(ball_reset_x, ball_reset_y)
                ball.vel = Vector2(0,0)
            else:
                game_state = "game_over"

    ## Draw objects
    for o in objects:
        o.draw(window)
    
    # Draw score
    score_text = plunger_state_font.render(f'Score: {score}', True, (255, 255, 255))
    window.blit(score_text, (200, 60))
    if game_state != "game_over":
        # Draw balls left
        balls_left_text = plunger_state_font.render(f'Balls Left: {balls_left}', True, (255, 255, 255))
        window.blit(balls_left_text, (400, 60))
    else:
        game_over_text = plunger_state_font.render('Game Over', True, (255, 0, 0))
        window.blit(game_over_text, (width//2 - 50, height//2 - 20))

    
