import pygame
from pygame.math import Vector2
from pygame.locals import *
import random
from physics_objects import Circle, Wall
import contact
import math

# Initialize pygame and open window
pygame.init()
window = pygame.display.set_mode(flags=FULLSCREEN)
size = min(window.get_width()/16, window.get_height()/9)
scale = size/120

# Constants
nbullets = 20
ball_radius = 100*scale
ball_density = 1/4
bullet_radius = 20*scale
line_width = int(round(5*scale))
max_radius = 200*scale
speed = 500*scale
X = window.get_width()-1
Y = window.get_height()-1

# Colors
left_color   = (0,200,255)
right_color  = (255,50,0)
ball_color   = (255,255,255)
font_color   = (150,150,150)
bg_color     = (0,0,0)

# Classes
class Bullet(Circle):
    def __init__(self, pos=(0,0), vel=(0,0), color=(0,0,0)):
        self.can_collide = True
        super().__init__(pos=pos, vel=vel, color=color, radius=bullet_radius, mass=bullet_radius**2)

class Gun:
    def __init__(self, type:str):
        if type == "left":
            self.xdirection = 1
            self.pos = Vector2(line_width//2, Y/2)
            self.color = left_color
        elif type == "right":
            self.xdirection = -1
            self.pos = Vector2(X - line_width//2, Y/2)
            self.color = right_color
        else:
            raise(ValueError("Invalid type"))
        self.angle = 0
        self.nbullets = nbullets/2

    def direction(self):
        pass
        # clamp angle to -90, 90
        self.angle = min(max(-90, self.angle), 90)
        
        # return a unit vector in the direction of the angle (positive angle up)
        return Vector2(self.xdirection, 0).rotate(-self.angle * self.xdirection)
        
        
    def draw(self, window):
        pass
        # draw the circle, radius proportional to nbullets
        pygame.draw.circle(window, self.color, self.pos, max_radius*self.nbullets/nbullets, line_width)

        # draw aim line, length = max_radius
        pygame.draw.line(window, self.color, self.pos, self.pos + max_radius*self.direction(), line_width)
        
    def shoot(self):
        global bullets
        # if bullets left, create a new bullet and subtract from nbullets
        if self.nbullets >= 1:
            self.nbullets -= 1
            bullets.append(Bullet(self.pos, speed * self.direction(), self.color))
        
# Timing stuff
fps = 60
dt = 1/fps
clock = pygame.time.Clock()

# Key lists
left_shoot      = [K_1, K_2, K_3, K_4] # 1 2 3 4      shoot
left_up         = [K_q, K_w, K_e, K_r] #  q w e r     up
left_down       = [K_a, K_s, K_d, K_f] #   a s d f    down
left_shoot.extend([K_z, K_x, K_c, K_v]) #    z x c v  shoot
right_shoot     = [K_9, K_0, K_MINUS, K_EQUALS, K_BACKSPACE]     #     9 0 - = ←  shoot
right_up        = [K_i, K_o, K_p, K_LEFTBRACKET, K_RIGHTBRACKET] #    i o p [ ]   up
right_down      = [K_j, K_k, K_l, K_SEMICOLON, K_QUOTE]          #   j k l ; '    down
right_shoot.extend([K_n, K_m, K_COMMA, K_PERIOD, K_SLASH])       #  n m , . /     shoot

# Fonts
font = pygame.font.SysFont("magneto", int(window.get_width()*0.07))

state = "setup"
while state != "quit":
    # Initialize guns
    left_gun = Gun("left")
    right_gun = Gun("right")

    # Set objects
    # ball
    ball = Circle(radius=ball_radius, mass=ball_density*ball_radius**2, color=ball_color, 
                  pos=(window.get_width()/2, window.get_height()/2), 
                  vel=(0,200*scale*random.uniform(-1,1)))
    # walls
    walls = []
    # top
    walls.append(Wall((0, window.get_height()/2 - Y/2), (X, window.get_height()/2 - Y/2), ball_color, line_width))
    # bottom
    walls.append(Wall((X, window.get_height()/2 + Y/2), (0, window.get_height()/2 + Y/2), ball_color, line_width))
    
    # empty list for bullets
    bullets : list[Bullet] = []

    # game state set to "ready"
    state = "ready"
    text = temp = font.render("Ready...", True, font_color)
    # set USEREVENT timer delay for 2 seconds
    pygame.time.set_timer(USEREVENT, 2000, True)

    
    # game loop
    while state not in ("quit", "setup"):
        # update and timing
        pygame.display.update()
        dt = clock.tick(fps) / 1000
        window.fill(bg_color)
        
        # EVENT loop
        while event := pygame.event.poll():
            # Quitting game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                state = "quit"
            # Shooting
            if event.type == KEYDOWN:
                if state == "play":
                    if event.key in left_shoot:
                        left_gun.shoot()
                    if event.key in right_shoot:
                        right_gun.shoot()


            # USEREVENT for transition from "ready" to "play"
            # and to delete "Start!" text after showing for 1 second
            if event.type == USEREVENT:
                if state == "ready":
                    text = font.render("Start!", True, font_color)
                    state = "play"
                    pygame.time.set_timer(USEREVENT, 1000, 1)
                else:
                    text = None
            # Pressing SPACE to start a new game after game over

            
        # Key state to rotate both guns
        key = pygame.key.get_pressed()
        avel = 60 # angular velocity in degrees per second
        if any(key[k] for k in left_up):
            left_gun.angle += avel * dt
        if any(key[k] for k in left_down):
            left_gun.angle -= avel * dt
        if any(key[k] for k in right_up):
            right_gun.angle += avel * dt
        if any(key[k] for k in right_down):
            right_gun.angle -= avel * dt
        
        
        # PHYSICS
        # update bullets and ball
        for obj in bullets + [ball]:
            obj.update(dt)
        
        # Collisions
        # ball with walls
        for w in walls:
            contact.generate(ball, w, restitution=1, resolve=True)
        
        # ball with bullets, set can_collide = False
        for b in bullets:
            if contact.generate(ball, b, restitution=1, resolve=True):
                b.can_collide = False
        
        # bullets with walls, only if can_collide is True, then set can_collide = False
        for b in bullets:
            if b.can_collide:
                for w in walls:
                    if contact.generate(b, w, restitution=1, resolve=True):
                        b.can_collide = False 
        
        # remove bullets that go off screen and credit which side's bullet count based on b.vel.x
        for b in reversed(bullets):
            pass
            # check if bullet went off screen
            if b.pos.x < 0 or b.pos.x > X or b.pos.y < 0 or b.pos.y > Y:
                # remove bullet
                bullets.remove(b)
                # credit appropriate side's nbullets
                # based on x component of velocity
                if b.vel.x < 0 or b.vel.x == 0 and b.color == left_gun.color:
                    left_gun.nbullets += 1
                else:
                    right_gun.nbullets += 1

        # DRAW
        # draw objects
        for obj in bullets + walls + [ball]:
            obj.draw(window)
        
        # draw guns
        left_gun.draw(window)
        right_gun.draw(window)
        
        # If ball went off screen, set text to win messages, set state = "game over"
        if state != "quit":
            if ball.pos.x + ball.radius < 0:
                text = font.render("Right player won!", True, right_color)
                state = "game over"
            if ball.pos.x - ball.radius > X:
                text = font.render("Left player won!", True, left_color)
                state = "game over"  
        
        # Display text in the center of the screen
        if text is not None:
            window.blit(text, ((window.get_width() - text.get_width())/2, (window.get_height() - text.get_height())/2))

        