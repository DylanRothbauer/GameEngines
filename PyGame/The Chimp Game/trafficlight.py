import pygame
from pygame.locals import * # Constants like QUIT, K_ESCAPE
from pygame.math import Vector2

# Constants
BG_COLOR = (0,0,0)

# Timing
FPS = 60
dt = 1/FPS  # timestep
clock = pygame.time.Clock()

# Initialize
pygame.init()
pygame.font.init()
#print(pygame.font.get_fonts())
'''
For Font:
- step 1 is to create a font
- step 2 is to render text with that font
'''

font = pygame.font.SysFont('impact', 80, False, False)

# Create window
window = pygame.display.set_mode([1000,700]) # params - size of window

# MAIN LOOP
state = "off"
while state != "quit":  # this runs once per frame
    # GRAPHICS
    # Clear the graphics window
    window.fill(BG_COLOR)
    # Draw everything

    # Draw grey rectangle
    height = window.get_height()
    width = height / 3
    y = 0 # top of the screen
    centerx = window.get_width() / 2
    x = centerx - width / 2
    pygame.draw.rect(window, (80, 80, 80), (x, y, width, height))
    
    # Draw circles
    radius = width / 2 * .9
    red = (255, 0, 0) if state == "red" else (80, 0, 0)
    yellow = (255, 255, 0) if state == "yellow" else (80, 80, 0)
    green = (0, 255, 0) if state == "green" else (0, 80, 0)

    red_center = Vector2(centerx, (0 + .5) * width)
    yellow_center = Vector2(centerx, (1 + .5) * width)
    green_center = Vector2(centerx, (2 + .5) * width)
    pygame.draw.circle(window, red, red_center, radius)
    pygame.draw.circle(window, yellow, yellow_center, radius)
    pygame.draw.circle(window, green, green_center, radius)

    # Draw text
    text = font.render("STOP", True, (0,0,0))
    window.blit(text, red_center - Vector2(text.get_width(), text.get_height())/2)
    
    text = font.render("GO", True, (0,0,0))
    window.blit(text, green_center - Vector2(text.get_width(), text.get_height())/2) # blit means to copy pixels from one surface to another

    # Update the display
    pygame.display.update()
    # Delay to limit frame rate
    clock.tick(FPS)/1000
    
    # EVENTS
    while event := pygame.event.poll():
        # quit event
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            state = "quit"
        # more events
        elif event.type == MOUSEBUTTONDOWN:
            # Is the mouse click inside the rectangle?
            if red_center.distance_to(event.pos) <= radius:
                if state == "green":
                    state = "yellow"
                    pygame.time.set_timer(USEREVENT, 2000, 1) # 2 seconds
                else:
                    state = "red"
            elif yellow_center.distance_to(event.pos) <= radius:
                state = "yellow"
                pygame.time.set_timer(USEREVENT, 2000, 1) # cancels the USEREVENT timer
            elif green_center.distance_to(event.pos) <= radius:
                state = "green"
            elif abs(Vector2(event.pos).x - centerx) > width /2:
                state = "off"
        elif event.type == USEREVENT and state == "yellow":
            state = "red"
