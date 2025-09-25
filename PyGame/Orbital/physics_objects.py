from pygame.math import Vector2
import pygame

class PhysicsObject:
    def __init__(self, mass=1, pos=(0,0), vel=(0,0)): # Constructor
        self.mass = mass
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        self.clear_force() # OR PhysicsObject.clear_force(self)

    def clear_force(self):
        self.force = Vector2(0,0)

    def add_force(self, force):
        self.force += force

    def update(self, dt):
        # update velocity using the current force
        self.vel += (self.force / self.mass) * dt
        # update position using the newly updated velocity
        self.pos += self.vel * dt


class Circle(PhysicsObject): # Inheritance
    def __init__(self, radius=100, color=(255,255,255), width=0, name="", **kwargs): # kwargs = keyword arguments
        self.radius = radius
        self.color = color
        self.width = width
        self.name = name
        super().__init__(**kwargs) # Call the parent class constructor

    def draw(self, window):
        pygame.draw.circle(window, self.color, self.pos, self.radius, self.width)

