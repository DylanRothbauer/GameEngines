from pygame.math import Vector2
import pygame
import math

class PhysicsObject:
    def __init__(self, mass=1, pos=(0,0), vel=(0,0), fixed=False): # Constructor
        self.mass = mass
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        self.fixed = fixed
        self.clear_force() # OR PhysicsObject.clear_force(self)

    def clear_force(self):
        self.force = Vector2(0,0)

    def add_force(self, force):
        self.force += force

    def impulse(self, impulse):
        self.vel += impulse / self.mass

    def update(self, dt):
        if self.fixed:
            # ensure it doesn't move or accumulate forces
            self.force = Vector2(0,0)
            self.vel = Vector2(0,0)
            return
        # update velocity using the current force
        self.vel += (self.force / self.mass) * dt
        # update position using the newly updated velocity
        self.pos += self.vel * dt


class Circle(PhysicsObject): # Inheritance
    def __init__(self, radius=100, color=(255,255,255), width=0, name="", fixed=False,**kwargs): # kwargs = keyword arguments
        self.radius = radius
        self.color = color
        self.width = width
        self.name = name
        self.original_color = color
        self.contact_type = "Circle"

        super().__init__(**kwargs) # Call the parent class constructor

        self.fixed_color = (100, 100, 100) # dark gray

    def draw(self, window):
        draw_color = self.fixed_color if self.fixed else self.color
        pygame.draw.circle(window, draw_color, self.pos, self.radius, self.width)


class Wall(PhysicsObject):
    def __init__(self, point1=(0,0), point2=(0,0), color=(255,255,255), width=1):
        super().__init__(mass=math.inf)
        self.color = color
        self.width = width
        self.set_points(point1, point2)  # this also sets self.pos and self.normal
        self.contact_type = "Wall"

    def draw(self, window):
        pygame.draw.line(window, self.color, self.point1, self.point2, self.width)
        #pygame.draw.line(window, self.color, self.pos, self.pos + 100*self.normal) # normal

    def update(self, dt):
        super().update(dt)
        self.point1 += self.vel * dt
        self.point2 += self.vel * dt

    def set_points(self, point1=None, point2=None):
        if point1 is not None:
            self.point1 = Vector2(point1)
        if point2 is not None:
            self.point2 = Vector2(point2)
        self.pos = (self.point1 + self.point2)/2
        self.update_normal()

    def update_normal(self):
        self.normal = (self.point2 - self.point1).normalize().rotate(90)
