import pygame
from pygame.math import Vector2
from pygame.locals import *
import random
from physics_objects import Circle, Wall
from forces import *
import contact
import math

def distance_from_pallino(x):
    return (x.pos - pallino.pos).magnitude()

def next_round():
    global points_awarded, balls_thrown, scoring_player, scoring_balls, pallino_thrown, state, current_player, balls, objects

    # Reset round variables
    points_awarded = False
    scoring_player = None
    scoring_balls = []
    pallino_thrown = False

    balls_thrown[player1_name] = 0
    balls_thrown[player2_name] = 0

    # Keep only walls, gray_circle, and pallino
    objects = [o for o in objects if isinstance(o, Wall) or o.name in ["gray_circle", "pallino"]]
    balls = [b for b in balls if b.name == "pallino"]

    gray_circle.pos = pallino.pos.copy()
    pallino.pos = gray_circle.pos.copy()

    pallino.vel = Vector2(0, 0)
    pallino.fixed = False
    pallino.color = pallino_color

    # Reset player turn and state
    current_player = player1_name
    state = AIMING_THROW
    rolling_friction.objects = objects
    selected_ball = None

def get_next_thrower(balls, pallino, player1_name, player2_name, balls_thrown):
    # Only consider balls that have been thrown (not pallino)
    thrown_balls = [b for b in balls if b.name in [player1_name, player2_name]]
    if not thrown_balls:
        # If no balls thrown yet, player 1 starts
        return player1_name

    # Sort balls by distance to pallino
    thrown_balls.sort(key=lambda b: (b.pos - pallino.pos).length())
    scoring_player = thrown_balls[0].name  # Closest ball's owner

    # The other player is the next thrower, unless out of balls
    next_player = player2_name if scoring_player == player1_name else player1_name
    if balls_thrown[next_player] < 4:
        return next_player
    elif balls_thrown[scoring_player] < 4:
        return scoring_player
    else:
        return None  # Both are out of balls
    
def get_scoring_balls(balls, pallino):
    # Separate balls by player
    player1_balls = [b for b in balls if b.name == player1_name]
    player2_balls = [b for b in balls if b.name == player2_name]

    # Compute distances from each ball to the pallino
    player1_distances = sorted([(b, (b.pos - pallino.pos).length()) for b in player1_balls], key=lambda x: x[1])
    player2_distances = sorted([(b, (b.pos - pallino.pos).length()) for b in player2_balls], key=lambda x: x[1])

    if not player1_distances:
        return player2_name, [b for b, _ in player2_distances]
    if not player2_distances:
        return player1_name, [b for b, _ in player1_distances]

    # Closest ball for each player
    p1_closest = player1_distances[0][1]
    p2_closest = player2_distances[0][1]

    if p1_closest < p2_closest:
        # Player 1 scores for every ball closer than Player 2’s closest
        player_1_scoring_balls = [b for b, d in player1_distances if d < p2_closest]
        return player1_name, player_1_scoring_balls
    elif p2_closest < p1_closest:
        # Player 2 scores for every ball closer than Player 1’s closest
        player_2_scoring_balls = [b for b, d in player2_distances if d < p1_closest]
        return player2_name, player_2_scoring_balls
    else:
        # Tie — no points
        return None, []

# Initialize pygame and open window
pygame.init()
window = pygame.display.set_mode(flags=FULLSCREEN)
bg_color = (0, 190, 0)
font = pygame.font.SysFont(None, 24)

# Constants
DESIRED_PLAY_WIDTH_M = 6.0 # meters
screen_w, screen_h = window.get_size()
PIXELS_PER_METER = screen_w / DESIRED_PLAY_WIDTH_M

BALL_DIAMETER_M = 0.105
BALL_RADIUS_M = BALL_DIAMETER_M / 2.0
BALL_MASS_KG = 1.2
PALLINO_DIAMETER_M = 0.027
PALLINO_RADIUS_M = PALLINO_DIAMETER_M / 2.0

# Radius in pixels
ball_radius = max(1, int(round(BALL_RADIUS_M * PIXELS_PER_METER)))
pallino_radius = max(1, int(round(PALLINO_RADIUS_M * PIXELS_PER_METER)))

# Compute pallino mass assuming same material density
ball_volume = (4.0/3.0) * math.pi * (BALL_RADIUS_M**3) # volume of a sphere
pallino_volume = (4.0/3.0) * math.pi * (PALLINO_RADIUS_M**3)
pallino_mass = BALL_MASS_KG * (pallino_volume / ball_volume) 

# Colors
player1_color = (255, 215, 0)    # gold/yellow
player2_color = (0, 0, 128)      # dark blue
pallino_color = (255, 255, 255)  # white

# Gray circle where balls are placed (1 m diameter)
gray_circle_radius = int(round(0.5 * PIXELS_PER_METER))
gray_circle_color = (150, 150, 150)

# Timing stuff
fps = 60
dt = 1/fps
clock = pygame.time.Clock()
mouse_down_time = 0
max_hold_time = 3000 # You can hold for 4 secs (ms -> s)
max_velocity = 1.5 * PIXELS_PER_METER

# states
QUIT_GAME = -1
PLACING_BALL = 0
AIMING_THROW = 1
CHARGING_THROW = 2
BALLS_ROLLING = 3
DISPLAY_ROUND_RESULT = 4
state = AIMING_THROW  # begin with aiming the pallino at the center of the gray circle

scoring_player = None
scoring_balls = []
player_1_scoring_balls = []
player_2_scoring_balls = []
player_1_points = 0
player_2_points = 0
points_awarded = False

# Set objects
selected_ball = None

#gray_circle
gray_circle = Circle(pos=(gray_circle_radius, screen_h//2), vel=(0,0), mass=math.inf, radius=gray_circle_radius, color=gray_circle_color, name="gray_circle", fixed=True)

#pallino
pallino = Circle(pos=(gray_circle_radius, screen_h//2), vel=(0,0), mass=pallino_mass, radius=pallino_radius, color=pallino_color, name="pallino", fixed=False)

# player 1 ball (for example)
player_1_ball = Circle(pos=(0, screen_h//2), vel=(0,0), mass=BALL_MASS_KG, radius=ball_radius, color=player1_color, name="player_1_ball", fixed=False)
# player 2 (for example)
player_2_ball = Circle(pos=(0, screen_w//2 + 20), vel=(0,0), mass=BALL_MASS_KG, radius=ball_radius, color=player2_color, name="player_2_ball", fixed=False)

objects = []
balls = []
walls = []

# Player setup
player1_name = "Player 1"
player2_name = "Player 2"
current_player = player1_name

balls_thrown = {
    player1_name: 0,
    player2_name: 0
}

# Track whether pallino has been thrown yet
pallino_thrown = False

score_x = screen_w - 250
score_y = 40

# Visual Testing
objects.append(pallino)
balls.append(pallino)
# Boundary walls: top, right, bottom
top_wall = Wall(point1=(0, 0), point2=(screen_w, 0), color=(120,120,120), width=4)
right_wall = Wall(point1=(screen_w, 0), point2=(screen_w, screen_h), color=(120,120,120), width=4)
bottom_wall = Wall(point1=(screen_w, screen_h), point2=(0, screen_h), color=(120,120,120), width=4)
left_wall = Wall(point2=(0, 0), point1=(0, screen_h), color=(120,120,120), width=4)

walls.append(top_wall)
walls.append(right_wall)
walls.append(bottom_wall)
walls.append(left_wall)
objects.append(top_wall)
objects.append(right_wall)
objects.append(bottom_wall)
objects.append(left_wall)

# Set forces
## Rolling friction
rolling_friction = RollingFriction(mu=0.3, g=.30, pixels_per_meter=PIXELS_PER_METER, dt=dt, objects=objects)

# Fonts
# game loop
while state != QUIT_GAME:

    pygame.display.update()
    dt = clock.tick(fps) / 1000
    window.fill(bg_color)
    
    score_title = font.render("Scoreboard", True, (255,255,255))
    window.blit(score_title, (score_x, score_y))

    p1_text = font.render(f"{player1_name}: {player_1_points}", True, player1_color)
    p2_text = font.render(f"{player2_name}: {player_2_points}", True, player2_color)
    window.blit(p1_text, (score_x, score_y + 30))
    window.blit(p2_text, (score_x, score_y + 60))

    if state == "GAME_OVER":
            winner = player1_name if player_1_points >= 6 else player2_name
            win_text = font.render(f"{winner} wins the game!", True, (255,255,255))
            window.blit(win_text, (screen_w//2 - win_text.get_width()//2, screen_h//2))

            # Wait for any key press or click to quit
            keys = pygame.key.get_pressed()
            if any(keys) or pygame.mouse.get_pressed()[0]:
                state = QUIT_GAME
    
    # EVENT loop
    while event := pygame.event.poll():
        # Quitting game
        if (event.type == QUIT 
            or (event.type == KEYDOWN
                and event.key == K_ESCAPE)):
            state = QUIT_GAME
        # Placing a new ball in the gray area
        if event.type == MOUSEBUTTONDOWN:
            pos = Vector2(event.pos)
            if state == AIMING_THROW:
                    state = CHARGING_THROW
                    mouse_down_time = pygame.time.get_ticks()
            
            if pos.distance_to(gray_circle.pos) < gray_circle_radius:
                if state == PLACING_BALL:
                    if pallino in balls:
                        balls.remove(pallino)
                    # Place ball at mouse position
                    if len(balls) < 8:
                        if current_player == player1_name:
                            color = player1_color
                            name = player1_name
                        else:
                            color = player2_color
                            name = player2_name
                        selected_ball = Circle(pos=event.pos, vel=(0,0), mass=BALL_MASS_KG, radius=ball_radius, color=color, name=name, fixed=False)
                        objects.append(selected_ball)
                        balls.append(selected_ball)
                        state = AIMING_THROW
                    else:
                        state = DISPLAY_ROUND_RESULT
                    pass

                elif state == DISPLAY_ROUND_RESULT:
                    # lets reset round
                    next_round()

        elif event.type == MOUSEBUTTONUP:
            mouse_up_time = pygame.time.get_ticks()
            pos = pygame.mouse.get_pos()
            if state == CHARGING_THROW:
                elapsed_time = mouse_up_time - mouse_down_time
                v = max_velocity * math.sqrt(min(elapsed_time, max_hold_time) / max_hold_time)
                mouse_pos = Vector2(pos)

                if not pallino_thrown:
                    # First throw of the round: pallino
                    r_vec = (mouse_pos - pallino.pos).normalize()
                    pallino.vel = v * r_vec
                    pallino_thrown = True
                    state = BALLS_ROLLING
                elif selected_ball is not None:
                    # Throw player ball
                    r_vec = (mouse_pos - selected_ball.pos).normalize()
                    selected_ball.vel = v * r_vec
                    balls_thrown[current_player] += 1
                    state = BALLS_ROLLING

        elif state == BALLS_ROLLING:
            moving = [b for b in balls if b.vel.length() > 0.5]
            if len(moving) == 0:
                # All balls stopped — update scoring status
                scoring_player, scoring_balls = get_scoring_balls(balls, pallino)
                if balls_thrown[player1_name] > 0 and balls_thrown[player2_name] > 0:
                    scoring_player, scoring_balls = get_scoring_balls(balls, pallino)
                else:
                    scoring_balls = []

                next_thrower = get_next_thrower(balls, pallino, player1_name, player2_name, balls_thrown)
                if next_thrower is None:
                    # Both players out of balls — end round
                    state = DISPLAY_ROUND_RESULT
                else:
                    current_player = next_thrower
                    state = PLACING_BALL

                    next_thrower = get_next_thrower(balls, pallino, player1_name, player2_name, balls_thrown)
                    if next_thrower is None:
                        state = DISPLAY_ROUND_RESULT
                    else:
                        current_player = next_thrower
                        state = PLACING_BALL

        elif state == DISPLAY_ROUND_RESULT:
                    balls.sort(key=distance_from_pallino)
                    # state = PLACING_BALL
                    pass

    # GAME
    # PHYSICS
    # clear all forces
    for obj in objects:
        obj.clear_force()

    # apply all forces
    rolling_friction.apply()

    # update all objects
    for obj in objects:
        obj.update(dt)

    # Collisions
    for j in range(len(objects)):
        for i in range(j):
            c = contact.generate(objects[i], objects[j], restitution=1, resolve=True)

    # DRAW
    # draw objects
    gray_circle.draw(window)
    for obj in objects:
        obj.draw(window)

    # draw aiming line
    if state == AIMING_THROW and not pallino_thrown:
        pygame.draw.line(window, (255,255,255), pallino.pos, pygame.mouse.get_pos())
    # Draw a line from the ball at its launch point to the current location of the mouse
    if state == AIMING_THROW or state == CHARGING_THROW:
        if pallino in balls:
            pygame.draw.line(window, (255,255,255), pallino.pos, pygame.mouse.get_pos())
        # Draw players ball line
        elif selected_ball is not None and selected_ball in objects:
            if selected_ball.name == player1_name:
                color = player1_color
            else:
                color = player2_color
            pygame.draw.line(window, color, selected_ball.pos, pygame.mouse.get_pos())

    # highlight balls
    # Draw scoring highlights
    if scoring_balls:
        for b in scoring_balls:
            pygame.draw.circle(window, (255, 255, 0), (int(b.pos.x), int(b.pos.y)), int(b.radius + 5), 3)

    # Draw a charge velocity bar
    if state == CHARGING_THROW and pygame.mouse.get_pressed()[0]:
        current_time = pygame.time.get_ticks()
        elapsed = max(0, current_time - mouse_down_time)
        frac = min(elapsed, max_hold_time) / max_hold_time
        bar_w, bar_h = 200, 20
        bar_x, bar_y = 20, 60
        # Interpolate color from gray (low) to red (high)
        low_color = (80,80,80)
        high_color = (255,0,0)
        bar_color = (
            int(low_color[0] + (high_color[0] - low_color[0]) * frac),
            int(low_color[1] + (high_color[1] - low_color[1]) * frac),
            int(low_color[2] + (high_color[2] - low_color[2]) * frac)
        )
        # Draw background bar
        pygame.draw.rect(window, low_color, (bar_x, bar_y, bar_w, bar_h))
        # Draw filled portion
        pygame.draw.rect(window, bar_color, (bar_x, bar_y, int(bar_w * frac), bar_h))
        # Draw border
        pygame.draw.rect(window, (255,255,255), (bar_x, bar_y, bar_w, bar_h), 2)
        # Draw percentage text
        power_text = font.render(f"Power: {int(frac*100)}%", True, bar_color)
        window.blit(power_text, (bar_x + bar_w + 10, bar_y))

    # Draw messages on screen
    # For testing
    text = font.render(f"State: {state}", True, (255,255,255))
    window.blit(text, (10,10))

    text = font.render(f"Turn: {current_player}", True, (255,255,255))
    window.blit(text, (10, 30))

    # if state == DISPLAY_ROUND_RESULT:
    #     text = font.render(f"THE WINNDER IS: {balls[0].name}", True, (255,255,255))
    #     window.blit(text, (10,40))
    if state == DISPLAY_ROUND_RESULT:
        if not points_awarded:
            if scoring_player:
                points = len(scoring_balls)
                if scoring_player == player1_name:
                    player_1_points += points
                elif scoring_player == player2_name:
                    player_2_points += points
            points_awarded = True  # prevent double scoring

        if scoring_player:
            text = font.render(f"{scoring_player} scores {len(scoring_balls)}!", True, (255,255,0))
            window.blit(text, (10,60))
        else:
            text = font.render("No points this round (tie)", True, (255,255,255))
            window.blit(text, (10,60))

        # Show current total points
        p1_text = font.render(f"{player1_name}: {player_1_points} pts", True, player1_color)
        p2_text = font.render(f"{player2_name}: {player_2_points} pts", True, player2_color)
        window.blit(p1_text, (10, 100))
        window.blit(p2_text, (10, 120))

        # After scoring, check for win condition
        if player_1_points >= 6 or player_2_points >= 6:
            state = "GAME_OVER"

