import pygame
from pygame.math import Vector2
import itertools
import math
import random
from physics_objects import PhysicsObject, Circle

class SingleForce:
    def __init__(self, objects:list[PhysicsObject]=[]):
        self.objects = objects

    def apply(self):
        # Apply the force to all objects in the objects list
        for obj in self.objects:
            force = self.force(obj)
            obj.add_force(force)

    def force(self, obj):
        return Vector2(0,0)
    
class PairForce:
    def __init__(self, objects:list[PhysicsObject]=[]):
        self.objects = objects

    def apply(self):
        # Loop over *all* pairs of objects and apply the calculated force
        # to each object, respecting Newton's 3rd Law.  
        # Use either two nested for loops (taking care to do each pair once)
        # or use the itertools library (specifically, the function combinations).
        # for a in self.objects:
        #     for b in self.objects:
        #         if id(a) < id(b):

        # for i in range(len(self.objects)):
        #     a = self.objects[i]
        #     for j in range(i):
        #         b = self.objects[j]

        for a, b in itertools.combinations(self.objects, 2):
            force = self.force(a,b)
            a.add_force(force)
            b.add_force(-force)

    def force(self, a, b):
        return Vector2(0,0)


class BondForce:
    def __init__(self, pairs:list[list[PhysicsObject]]=[]):
        # pairs has the format 
        # [[obj1, obj2], [obj3, obj4], ... ] 
        # ^ each pair representing a bond between two objects
        if any(len(p) != 2 for p in pairs):
            raise("pairs needs to be a list of pairs")
        self.pairs = pairs

    def apply(self):
        # Loop over all *pairs* from the pairs list.  
        # Apply the force to each member of the pair respecting Newton's 3rd Law.
        for a, b in self.pairs:
            force = self.force(a,b)
            a.add_force(force)
            b.add_force(-force)

    def force(self, a, b):
        return Vector2(0,0)
        
# Add Gravity, SpringForce, SpringRepulsion, AirDrag
class Gravity(SingleForce):
    def __init__(self, acc=(0,0), **kwargs):
        super().__init__(**kwargs)
        self.acc = Vector2(acc)

    def force(self, obj:PhysicsObject):
        # This will mess up for objects with infinite mass
        if obj.mass == math.inf:
            return Vector2(0,0)
        return obj.mass * self.acc
        

class Container(SingleForce):
    def __init__(self, stiffness=0, rect=(0,0,0,0), **kwargs):
        super().__init__(**kwargs)
        self.stiffness = stiffness
        self.rect = pygame.Rect(rect)

    def force(self, obj:Circle):
        force = Vector2(0, 0)
        # Left wall
        overlap = obj.radius - (obj.pos.x - self.rect.x)
        if overlap > 0:
            force +=self.stiffness * overlap * Vector2(1, 0)

        # Right wall
        overlap = obj.radius - (self.rect.x + self.rect.w - obj.pos.x)
        if overlap > 0:
            force +=self.stiffness * overlap * Vector2(-1, 0)

        # Top wall
        overlap = obj.radius - (obj.pos.y - self.rect.y)
        if overlap > 0:
            force +=self.stiffness * overlap * Vector2(0, 1)

        # Bottom wall
        overlap = obj.radius - (self.rect.y + self.rect.h - obj.pos.y)
        if overlap > 0:
            force +=self.stiffness * overlap * Vector2(0, -1)
        
        return force
    
    def draw(self, window, color=(255,255,255), width=1):
        pygame.draw.rect(window, color, self.rect, width)
    

class LennardJones(PairForce):
    def __init__(self, sigma=1, epsilon=1, n=3, **kwargs):
        super().__init__(**kwargs)
        self.sigma = sigma
        self.epsilon = epsilon
        self.n = n

    def force(self, a:PhysicsObject, b:PhysicsObject):
        rvec = a.pos - b.pos
        r = rvec.magnitude()
        Q = (self.sigma / r) ** self.n
        
        return self.n * self.epsilon * Q * (2*Q - 1) * rvec / r**2
    
    
class HarmonicBonds(BondForce):
    def __init__(self, stiffness=0, length=0, **kwargs):
        super().__init__(**kwargs)
        self.stiffness = stiffness
        self.length = length # bond length

    def force(self, a:PhysicsObject, b:PhysicsObject):
        rvec = a.pos - b.pos
        r = rvec.magnitude()
        return -self.stiffness * (r - self.length) * rvec.normalize()
    
    def draw(self, window, color=(255,255,255), width=1):
        for a, b in self.pairs:
            pygame.draw.line(window, color, a.pos, b.pos, width)

class SpringForce(BondForce):
    def __init__(self, stiffness=0, length=0, damping=0, **kwargs):
        super().__init__(**kwargs)
        self.stiffness = stiffness
        self.length = length
        self.damping = damping

    def force(self, a:Circle, b:Circle):
        k = self.stiffness
        l = self.length
        rvec = a.pos - b.pos
        r = rvec.magnitude()
        if r == 0:
            return Vector2(0, 0)
        
        rhat = rvec.normalize()
        v = a.vel - b.vel
        spring_mag = -self.stiffness * (r - self.length)         # -k(|r|-l)
        damping_mag = -self.damping * (v.dot(rhat))              # -b (v_rel · rhat)
        total_mag = spring_mag + damping_mag
        return total_mag * rhat
    
    
    def draw(self, window, color=(255,255,255), width=1):
        for a, b in self.pairs:
            pygame.draw.line(window, color, a.pos, b.pos, width)

class Drag(SingleForce):
    def __init__(self, p=1.2, c_d=0.47, area=0.01, wind=0, **kwargs):
        """
        p: fluid density
        c_d: drag coefficient
        area: cross-sectional area
        wind: wind velocity
        kwargs: keywod arguments (other arguments for SingleForce)
        """
        super().__init__(**kwargs)
        self.p = p
        self.c_d = c_d
        self.area = area
        self.wind = Vector2(wind)

    def force(self, obj: PhysicsObject):
        v = obj.vel

        # Relitive to wind velocity
        v_rel = v - self.wind

        if v_rel.magnitude() == 0:
            return Vector2(0, 0)

        if v.magnitude() == 0:
            return Vector2(0, 0)

        # F = -0.5 * c_d * rho * A * |v| * v
        # return -0.5 * self.c_d * self.p * self.area * v.magnitude() * v
        return -0.5 * self.c_d * self.p * self.area * v_rel.magnitude() * v_rel
    
class SpringRepulsion(PairForce):
    def __init__(self, stiffness=1000, **kwargs):
        super().__init__(**kwargs)
        self.stiffness = stiffness

    def force(self, a:Circle, b:Circle):
        rvec = a.pos - b.pos
        r = rvec.magnitude()
        overlap = (a.radius + b.radius) - r
        if overlap > 0:
            # guard against zero distance
            if r == 0:
                rhat = Vector2(random.random() - 0.5, random.random() - 0.5)
                if rhat.length() == 0:
                    rhat = Vector2(1, 0)
                rhat = rhat.normalize()
            else:
                rhat = rvec.normalize()

            return self.stiffness * overlap * rhat
        return Vector2(0, 0)
    
class RollingFriction(SingleForce):
    """
    Rolling friction force:
    F_friction = -v_hat * min( mu * m * g, m * v / dt + F * v_hat )
    """
    def __init__(self, mu=0.3, g=9.81, pixels_per_meter=1.0, dt=1/60.0, **kwargs):
        super().__init__(**kwargs)
        self.mu = mu
        self.g = g
        self.pixels_per_meter = pixels_per_meter
        self.dt = dt

    def force(self, obj):
        if getattr(obj, 'mass', 0) == math.inf:
            return Vector2(0, 0)

        v = obj.vel
        v_len = v.length()
        if v_len == 0:
            return Vector2(0, 0)

        v_hat = v.normalize()

        # first term - mu * m * g
        first_N = self.mu * obj.mass * self.g

        v_m_s = v_len / self.pixels_per_meter
        # second term
        second_term = obj.mass * (v_m_s / self.dt)
        proj_force_N = (obj.force.dot(v_hat)) / self.pixels_per_meter
        second_term += proj_force_N
        second_N = max(0.0, second_term)

        mag_N = min(first_N, second_N)

        # pixels_per_meter
        mag_px = mag_N * self.pixels_per_meter

        return -v_hat * mag_px
    