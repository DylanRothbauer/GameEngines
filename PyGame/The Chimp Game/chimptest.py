import pygame
from pygame.locals import *
from pygame.math import Vector2, Vector3
import random
import math

# CONSTANTS
BG_COLOR = (0,0,0)
MEGENTA = (255,0,255)
ROSE_RED = (255,3,62)
CHERRY_RED = (255,20,147)
CRIMSON_RED = (220,20,60)
MAROON_RED = (128,0,0)

# PYGAME INITIALIZATION
pygame.init()
pygame.font.init()
pygame.mixer.init()

# GAME VARIABLES
labels = [chr(x) for x in range(ord('A'), ord('Z')+1)]
max_lives = 5
state = "intro"
level = 3
lives = max_lives
circles = []
progressIndex = 0
colors = [MAROON_RED, CRIMSON_RED, ROSE_RED, CHERRY_RED, MEGENTA]
correctClickSound = pygame.mixer.Sound("pop.mp3")
clearClickSound = pygame.mixer.Sound("bubbles.mp3")
errorClickSound = pygame.mixer.Sound("error.mp3")

# TIMING
clock = pygame.time.Clock()
FPS = 60
dt = 1/FPS

# CREATE WINDOW
window = pygame.display.set_mode(flags=FULLSCREEN)

# FONTS
font = pygame.font.SysFont('impact', 80, False, False)

# FUNCTIONS
# drawing functions (helpful, but optional)

# function to set up a new game
def setup_game():
    global lives, level
    set_lives(max_lives)
    level = 3

    # At the end
    setup_round()
    pass

# function to set up a new round at the current level
def setup_round():
    global state, circles, progressIndex
    state = "intro"
    circles = []

    # Screen size
    W = window.get_width()
    H = window.get_height()
    screen_area = W * H

    # Circle sizing: total circle area = 20% of screen
    circle_area = 0.2 * screen_area / level
    radius = int(math.sqrt(circle_area / math.pi))

    # Font scaling
    circle_font = pygame.font.SysFont('impact', int(radius * 1.2), False, False)

    # Place circles
    positions = []
    for i in range(level):
        placed = False
        while not placed:
            x = random.randint(radius, W - radius)
            y = random.randint(radius, H - radius)
            pos = Vector2(x, y)

            # check overlap with others
            overlap = False
            for other in positions:
                if pos.distance_to(other) <= 2 * radius:
                    overlap = True
                    break

            if not overlap:
                positions.append(pos)
                placed = True

    random.shuffle(positions)

    # Assign labels and build circle list
    index = 0
    for pos in positions:
        label = labels[index]
        circle = {
            "pos": pos,
            "radius": radius,
            "label": label,
            "font": circle_font
        }
        circles.append(circle)
        index += 1
    
    progressIndex = 0
            
# function to set the lives remaining and the circle color
def set_lives(x):
    global lives
    lives = x
    pass

def level_in_background():
    # Draw giant letter for what level it is
    font_large = pygame.font.Font(None, 1200)
    text_surface_large = font_large.render(labels[level - 1], True, (100, 100, 100))
    text_rect_large = text_surface_large.get_rect(center=(window.get_width()/2, window.get_height()/2))
    window.blit(text_surface_large, text_rect_large)
    # text_surface = font.render(labels[level - 1], True, (100, 100, 100))
    # text_rect = text_surface.get_rect(center=(window.get_width()/2, window.get_height()/2))
    # window.blit(text_surface, text_rect)
    pass
        
# START GAME
setup_game()
while state != "quit":
    # INTRO
    if state == "intro":
        # GRAPHICS
        window.fill(BG_COLOR)
        level_in_background()

        # Draw all circles
        for c in circles:
            pos = c["pos"]
            radius = c["radius"]
            label = c["label"]
            font = c["font"]

            pygame.draw.circle(window, colors[lives - 1], pos, radius)

            text_surface = font.render(label, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=pos)
            window.blit(text_surface, text_rect)

        # DISPLAY AND TIMING
        pygame.display.update()
        dt = clock.tick(FPS)/1000

        # EVENTS
        while True:
            event = pygame.event.poll()
            if not event:  # no more events
                break

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                state = "quit"
            
            # KEYUP: if a letter key is pressed, jump to that level and set up a new round
            elif event.type == KEYUP:
                if event.unicode.isalpha():
                    letter = event.unicode.upper()
                    if letter in labels:
                        level = labels.index(letter) + 1
                        setup_round()
            # MOUSEDOWN: if the circle with label "A" is clicked, go to "play" state
            elif event.type == MOUSEBUTTONDOWN:
                pos = Vector2(event.pos)
                for c in circles:
                    if c["label"] == "A":
                        if pos.distance_to(c["pos"]) <= c["radius"]:
                            progressIndex = 1
                            correctClickSound.play()
                            state = "play"
                            break
            
            
    # PLAY
    elif state == "play":
        # GRAPHICS
        # background graphics
        window.fill(BG_COLOR)
        level_in_background()

        # draw circles without labels
        for c in circles:
            pos = c["pos"]
            radius = c["radius"]
            pygame.draw.circle(window, colors[lives - 1], pos, radius)
        
        # draw label for only the last successfully clicked circle
        if progressIndex > 0:
            lastCircle = circles[progressIndex - 1]
            pos = lastCircle["pos"]
            label = lastCircle["label"]
            font = lastCircle["font"]
            text_surface = font.render(label, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=pos)
            window.blit(text_surface, text_rect)
        
        # DISPLAY AND TIMING
        pygame.display.update()
        dt = clock.tick(FPS)/1000

        # EVENTS
        # DO I NEED A WHILE TRUE HERE?
        while event := pygame.event.poll():
            # ESCAPE TO QUIT
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                state = "quit"
            # MOUSEDOWN
            # if the correct circle is clicked, advance the label
            elif event.type == MOUSEBUTTONDOWN:
                pos = Vector2(event.pos)
                if progressIndex < len(circles):
                    currentCircle = circles[progressIndex]
                    if pos.distance_to(currentCircle["pos"]) <= currentCircle["radius"]:
                        # Play sound effect for correct click
                        correctClickSound.play()
                        progressIndex += 1
                        if progressIndex == len(circles):
                            # If that was the last circle, set a timer to go to win state
                            pygame.time.set_timer(USEREVENT, 1000, 1)
                            # Play a sound effect for winning the round
                            clearClickSound.play()
                            state = "win"
                            lives = max_lives
                            print("PASS: Lives reset to", lives)
                    else:
                        # Save the circle index that we clicked for loose state
                        for c in circles:
                            if pos.distance_to(c["pos"]) <= c["radius"]:
                                incorrectCircle = c
                                break
                        pygame.time.set_timer(USEREVENT, 1000, 1)
                        errorClickSound.play()
                        state = "lose"
                        set_lives(lives - 1)
            # if that was the last circle, then go to the win state (call USEREVENT on 1 sec delay)
            # if an incorrect circle was clicked that is not the currently labeled circle, go to the lose state
            
            # KEYUP: if space pressed, lose one life and go back to "intro" state
            # (keep the same arrangement of circles)
            elif event.type == KEYUP and event.key == K_SPACE:
                set_lives(lives - 1)
                if lives <= 0:
                    state = "game over"
                else:
                    state = "intro"
            
            
    # WIN
    elif state == "win":
        # GRAPHICS
        # background graphics
        
        # draw circles colored green with all labels white
        for c in circles:
            pos = c["pos"]
            radius = c["radius"]
            label = c["label"]
            font = c["font"]

            pygame.draw.circle(window, (0, 200, 0), pos, radius)

            text_surface = font.render(label, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=pos)
            window.blit(text_surface, text_rect)
        
        # DISPLAY AND TIMING
        pygame.display.update()
        dt = clock.tick(FPS)/1000
        
        # EVENTS
        while event := pygame.event.poll():
            # ESCAPE TO QUIT
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                state = "quit"
            # USEREVENT: set up a new round at the level one higher
            elif event.type == USEREVENT:
                level += 1
                setup_round()
            
    # LOSE ROUND   
    elif state == "lose":
        # GRAPHICS
        # background graphics
        
        # draw circles without labels
        for c in circles:
            pos = c["pos"]
            radius = c["radius"]
            pygame.draw.circle(window, colors[lives - 1], pos, radius)

        # draw a label in black for the incorrectly clicked circle
        if progressIndex < len(circles):
            # incorrectCircle = circles[progressIndex - 1]
            # for c in circles:
            #     if pos.distance_to(c["pos"]) <= c["radius"]:
            #         incorrectCircle = c
            #         break
            pos = incorrectCircle["pos"]
            label = incorrectCircle["label"]
            font = incorrectCircle["font"]
            text_surface = font.render(label, True, (0, 0, 0)) # black
            text_rect = text_surface.get_rect(center=pos)
            window.blit(text_surface, text_rect)

        # draw a label in white for the circle that should have been clicked
        if progressIndex > 0:
            correctCircle = circles[progressIndex]
            pos = correctCircle["pos"]
            label = correctCircle["label"]
            font = correctCircle["font"]
            text_surface = font.render(label, True, (255, 255, 255)) # white
            text_rect = text_surface.get_rect(center=pos)
            window.blit(text_surface, text_rect)

        # DISPLAY AND TIMING
        pygame.display.update()
        dt = clock.tick(FPS)/1000
        
        # EVENTS
        while event := pygame.event.poll():
            # ESCAPE TO QUIT
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                state = "quit"
            # USEREVENT: if out of lives, state = "game over" else decrease lives and set up a new round
            elif event.type == USEREVENT:
                if lives <= 0:
                    state = "game over"
                else:
                    state = "intro"


    # GAME OVER
    elif state == "game over":
        # GRAPHICS
        # draw the same losing state but dimmer (nice touch, but optional)
        window.fill(BG_COLOR)
        # draw a message stating the highest completed level
        text_surface = font.render(f"Game Over!", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(window.get_width()/2, window.get_height()/2))
        window.blit(text_surface, text_rect)
        text_surface = font.render(f"Highest Level: {level - 1}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(window.get_width()/2, window.get_height()/2 + 200))
        window.blit(text_surface, text_rect)
        
        
        # DISPLAY AND TIMING
        pygame.display.update()
        dt = clock.tick(FPS)/1000
        
        # EVENTS
        while event := pygame.event.poll():
            # ESCAPE TO QUIT
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                state = "quit"
            # KEYUP: if space pressed, start a new game
            elif event.type == KEYUP and event.key == K_SPACE:
                setup_game()
            