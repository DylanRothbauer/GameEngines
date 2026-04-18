import pygame
from pygame.locals import *
from pygame.math import Vector2, Vector3
import random
import math

from physics_objects import Circle, Wall, Polygon, UniformPolygon, UniformCircle
import itertools
import contact

# initialize pygame and open window
pygame.init()
width, height = 800, 600
window = pygame.display.set_mode([width, height])

# set timing stuff
fps = 60
dt = 1/fps
clock = pygame.time.Clock()

# Functions
def respawn_shooter():
    global shooter, shapes, bullets, dead, respawn_timer, ignore_score_until
    shapes.clear()
    bullets.clear()
    bombs.clear()
    shooter = None
    dead = True
    respawn_timer = 2.0
    ignore_score_until = pygame.time.get_ticks()/1000.0 + 2.0

def spawn(): # spawns a new shape
    # choose a random template and spawn just above the top of the screen
    global shape_templates, shapes, shape_density
    template_index = random.randrange(len(shape_templates))
    local_points = [Vector2(p) for p in shape_templates[template_index]]
    # apply a small scale variation
    scale = random.uniform(0.8, 1.2)
    local_points = [p * scale for p in local_points]
    # spawn x between margins
    x = random.uniform(50, width-50)
    y = -max(p.y for p in local_points) - 10
    shape = UniformPolygon(density=shape_density, local_points=local_points, pos=Vector2(x,y), angle=random.uniform(0,math.pi*2), color=[random.randint(80,255) for _ in range(3)])
    # initial velocity: downward with some variation, small sideways, small angular
    shape.vel = Vector2(random.uniform(-30,30), random.uniform(40,120))
    shape.avel = random.uniform(-3,3)
    shape.type_index = template_index
    shapes.append(shape)
    print(f"[spawn] template={template_index} pos=({x:.1f},{y:.1f}) vel={shape.vel}")

def spawn_bomb():
    if random.random() < 0.50:
        x = random.uniform(50, width - 50)
        y = -30
        b = UniformCircle(radius=12, pos=Vector2(x, y), density=.003)
        b.is_bomb = True
        b.vel = Vector2(random.uniform(-30,30), random.uniform(40,120))
        b.color = (255, 0, 0)
        b.explosion_radius = 120
        bombs.append(b)
        print(f"[spawn_bomb] pos=({x:.1f},{y:.1f})")

def explode(bomb):
    global shapes, score

    destroyed = 0
    new_shapes = []

    for s in shapes:
        dist = (s.pos - bomb.pos).length()
        if dist < bomb.explosion_radius:
            destroyed += 1
        else:
            new_shapes.append(s)

    shapes = new_shapes
    score += destroyed * 5

    print("Explosion! destroyed", destroyed)


def spawn_bullet():
    global shooter, bullets, frames_since_shot, shoot_cooldown_frames, bullet_density

    # cooldown
    if shooter is None:
        return
    if frames_since_shot < shoot_cooldown_frames:
        return

    frames_since_shot = 0

    # ---- Compute shooter tip (front point) ----
    local_pts = getattr(shooter, "local_points", shooter.points)
    # find highest (smallest y) local vertex
    top_local = min(local_pts, key=lambda p: p.y)

    # rotate into world-space
    if hasattr(top_local, "rotate_rad"):
        top_world = top_local.rotate_rad(shooter.angle)
    else:
        top_world = top_local.rotate(math.degrees(shooter.angle))

    # final world position
    tip = shooter.pos + top_world

    # ---- Create bullet ----
    bullet_radius = 6
    bullet = UniformCircle(
        density=bullet_density,
        radius=bullet_radius,
        pos=Vector2(tip.x, tip.y),
        color=(255, 230, 0)   # yellow-ish
    )

    # bullet physics
    bullet.vel = Vector2(0, -500)     # straight upward
    bullet.avel = 0
    bullet.fixed = False
    bullet.is_bullet = True

    bullets.append(bullet)

lives = 3
score = 0
game_over = False
running = True
dead = False
paused = False

# gameplay settings
shape_density = 0.0005
bullet_density = shape_density
shape_spawn_interval_frames = 90
frames_since_spawn = 0
shape_templates = []

def make_templates():
    templates = []
    # equilateral triangle (pointing up)
    templates.append([Vector2(0,-24), Vector2(20,12), Vector2(-20,12)])
    # square
    templates.append([Vector2(-18,-18), Vector2(18,-18), Vector2(18,18), Vector2(-18,18)])
    # rhombus (two fused equilateral triangles)
    templates.append([Vector2(0,-30), Vector2(24,0), Vector2(0,30), Vector2(-24,0)])
    # small pentagon
    templates.append([Vector2(0,-22), Vector2(20,-6), Vector2(12,18), Vector2(-12,18), Vector2(-20,-6)])
    # long rectangle
    templates.append([Vector2(-10,-40), Vector2(10,-40), Vector2(10,40), Vector2(-10,40)])
    # big hexagon
    templates.append([Vector2(-28,-12), Vector2(0,-28), Vector2(28,-12), Vector2(28,12), Vector2(0,28), Vector2(-28,12)])
    return templates

shape_templates = make_templates()

# lists of objects
walls = []
shapes = []
bullets = []
bombs = []

# Shooter placeholder
shooter = None

# shooting control
shoot_cooldown_frames = 6
frames_since_shot = shoot_cooldown_frames

# respawn handling
respawn_timer = 0.0
ignore_score_until = 0.0
while running:
    pygame.display.update()
    clock.tick(fps)
    window.fill([0,0,0])
    
    # game loop
    # EVENT loop
    while event := pygame.event.poll():
        # Quitting game
        if (event.type == pygame.QUIT 
            or (event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE)):
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            paused = not paused
        # Use USEREVENT to start a new shooter after a delay of 2 seconds
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            spawn_bullet()

    if not paused:
        # PHYSICS
        # ensure walls exist
        if not walls:
            ground_y = height - 50
            ground = Wall(point1=(0, ground_y), point2=(width, ground_y), color=(0,200,0), width=8)
            left = Wall(point1=(0,0), point2=(0,height), color=(0,0,0), width=1)
            right = Wall(point1=(width,0), point2=(width,height), color=(0,0,0), width=1)
            # top = Wall(point1=(0,0), point2=(width,0), color=(0,0,0), width=1)
            walls.extend([ground, left, right])

        # spawn shooter if missing and not currently in dead timeout
        if shooter is None and not dead:
            # spawn at center near ground
            shooter_local = [Vector2(0,-18), Vector2(14,12), Vector2(-14,12)]
            shooter = UniformPolygon(density=shape_density, local_points=shooter_local, pos=Vector2(width/2, height-100), color=(180,180,255))
            shooter.fixed = False
            shooter.is_shooter = True

        # handle keyboard input for shooter
        keys = pygame.key.get_pressed()
        if shooter is not None:
            if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                shooter.vel.x = -220
            elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                shooter.vel.x = 220
            else:
                shooter.vel.x = 0

            # clamp horizontal position so the central point doesn't go off-screen

        # shooting
        frames_since_shot += 1

        # spawn shapes periodically
        frames_since_spawn += 1
        if frames_since_spawn >= shape_spawn_interval_frames:
            frames_since_spawn = 0
            spawn()
            spawn_bomb()

        # update all objects
        # walls don't need updating
        for s in shapes:
            s.update(dt)
        for b in bullets:
            b.update(dt)
        if shooter is not None:
            shooter.update(dt)
        for bomb in bombs:
            bomb.update(dt)


        # keep shooter on screen (central point)
        if shooter is not None:
            shooter.pos.x = max(0, min(width, shooter.pos.x))
            shooter.update(0)

        # collisions between bullets and polygons and polygons with each other
        # check bullets hitting ground or going off screen
        # check polygons hitting ground or going off screen or hitting shooter
        # check bombs hitting ground or going off screen or hitting shooter

        # Collision with bullet & polygons
        for b in bullets:
            for s in shapes:
                c = contact.generate(b, s)
                if c.overlap > 0:
                    c.resolve()
                    print("Bullet hit polygon!")
        
        # Collision with polygons
        shape_list = shapes[:]
        for i in range(len(shape_list)):
            a = shape_list[i]
            for j in range(i+1, len(shape_list)):
                b = shape_list[j]
                c = contact.generate(a, b)
                if c and c.overlap > 0:
                    c.resolve()

        for bomb in bombs[:]:
            for s in shapes[:]:
                c = contact.generate(bomb, s)
                if c.overlap > 0:
                    c.resolve()
    
            # collisions with shooter
            for s in shapes:
                if shooter is not None:
                    c2 = contact.generate(s, shooter)
                    if c2.overlap > 0:
                        # shooter hit: lose a life
                        lives -= 1
                        # clear shapes and bullets, remove shooter, set dead timer and ignore scoring
                        respawn_shooter()
                        break
            # Bomb hits ground
            for bomb in bombs[:]:
                c = contact.generate(bomb, walls[0])
                if c.overlap > 0:
                    explode(bomb)
                    bombs.remove(bomb)
                    lives -= 1
                    respawn_shooter()
                    break

            # check off-screen scoring/removal
            # --- SHAPE OFF-SCREEN CHECK / SCORING ---
            shape_margin = 50
            for s in shapes[:]:
                out_left   = s.pos.x < -shape_margin
                out_right  = s.pos.x > width + shape_margin
                out_bottom = s.pos.y > height + shape_margin

                if out_left or out_right or out_bottom:
                    # Only score if player is not in the ignore window (like after dying)
                    if pygame.time.get_ticks()/1000.0 > ignore_score_until:
                        score += 1

                    shapes.remove(s)

            for bullet in bullets[:]:
                for bomb in bombs[:]:
                    c = contact.generate(bullet, bomb)
                    if c.overlap > 0:
                        explode(bomb)
                        bombs.remove(bomb)
                        bullets.remove(bullet)
                        break

            for b in bullets:
                for s in shapes:
                    c = contact.generate(b, s)
                    if c.overlap > 0:
                        c.resolve()
                        print("Bullet hit polygon!")

        # check bullets going off screen or beyond margin
        margin = 200
        for b in bullets[:]:
            if b.pos.y > height + margin:
                bullets.remove(b)
            elif b.pos.y < -margin or b.pos.x < -margin or b.pos.x > width + margin:
                bullets.remove(b)

        # respawn timer handling
        if dead:
            respawn_timer -= dt
            if respawn_timer <= 0:
                dead = False
                # shooter will be recreated in next loop iteration

    # DRAW section
    # clear the screen (already filled at top of loop)
    # draw ground and walls
    if walls:
        walls[0].draw(window)  # ground (green)

    # draw shapes
    for s in shapes:
        s.draw(window)

    # draw bullets
    for b in bullets:
    # draw a filled circle at integer pixel coords
        pygame.draw.circle(window, b.color if hasattr(b, "color") else (255,220,0), (int(b.pos.x), int(b.pos.y)), int(getattr(b, "radius", getattr(b, "r", 6))))

    # draw shooter
    if shooter is not None:
        shooter.draw(window)

    for bomb in bombs:
        pygame.draw.circle(window, (255, 0, 0),
        (int(bomb.pos.x), int(bomb.pos.y)), int(bomb.radius))


    # display running score and lives in corners
    try:
        font = pygame.font.SysFont(None, 28)
        score_surf = font.render(f"Score: {score}", True, (255,255,255))
        lives_surf = font.render(f"Lives: {lives}", True, (255,255,255))
        window.blit(score_surf, (10,10))
        window.blit(lives_surf, (width-110,10))
    except Exception:
        pass

    # display game over
    if lives <= 0:
        try:
            big = pygame.font.SysFont(None, 72)
            go = big.render("GAME OVER", True, (255,0,0))
            window.blit(go, (width/2 - go.get_width()/2, height/2 - go.get_height()/2))
        except Exception:
            pass
    # update the display after drawing
    pygame.display.update()
        
