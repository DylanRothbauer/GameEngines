from pygame.math import Vector2
from physics_objects import PhysicsObject,Circle,Wall,Polygon
import math

# Returns a new contact object of the correct subtype
# This function has been done for you.
def generate(a, b, **kwargs):
    # Check if a's type comes later than b's alphabetically.
    # We will label our collision types in alphabetical order, 
    # so the lower one needs to go first.
    if b.contact_type < a.contact_type:
        a, b = b, a
    # This calls the class of the appropriate name based on the two contact types.
    return globals()[f"{a.contact_type}_{b.contact_type}"](a, b, **kwargs)
    
# Generic contact class, to be overridden by specific scenarios
class Contact():
    def __init__(self, a, b, resolve=False, **kwargs):
        self.a = a
        self.b = b
        self.kwargs = kwargs
        self.update()
        self.bool = self.overlap > 0
        if resolve:
            self.bool = self.resolve(update=False)

    def __bool__(self):
        return self.bool

    def update(self):  # virtual function
        self.overlap = 0
        self.normal = Vector2(0, 0)

    def resolve(self, restitution=None, rebound=None, update=True):
        if update:
            self.update()
        restitution = restitution if restitution is not None else self.kwargs.get("restitution", 1)
        rebound = rebound if rebound is not None else self.kwargs.get("rebound", 0)
        # resolve overlap
        if self.overlap > 0:
            a:PhysicsObject = self.a
            b:PhysicsObject = self.b

            # calculate reduced mass
            m = 1/((1/a.mass) + (1/b.mass))
            # change the position of a and b
            a.pos += (self.normal * self.overlap * (m/a.mass))
            b.pos -= (self.normal * self.overlap * (m/b.mass))
            
            # resolve velocity
            # calculate relative velocity
            point = self.point()
            sa = point - a.pos
            vaprime = a.vel + a.avel * sa.rotate(90)
            sb = point - b.pos
            vbprime = b.vel + b.avel * sb.rotate(90)
            relative_velocity = vaprime - vbprime

            #   J = -(1+epsilon) * m * (v · n) + m * v_rebound
            v_rel_dot = relative_velocity.dot(self.normal)
            if v_rel_dot < 0 or rebound != 0:
                J = -(1 + restitution) * m * v_rel_dot + m * rebound
                impulse = J * self.normal
                # apply impulses to objects a and b
                a.impulse(impulse)
                b.impulse(-impulse)
                return True
        return False
        # return True if impulses need to be applied, return False otherwise

# Contact class for two circles
class Circle_Circle(Contact):
    def update(self):  # compute the appropriate values
        a:Circle = self.a
        b:Circle = self.b
        r = a.pos - b.pos
        self.overlap = a.radius + b.radius - r.magnitude()
        # r could be a zero vector if circles share the same center; avoid normalizing zero-length
        if r.magnitude() == 0:
            self.normal = Vector2(0, 0)
        else:
            self.normal = r.normalize()

    def point(self):
        circle:Circle = self.a
        return circle.pos - circle.radius * self.normal

# Contact class for Circle and a Wall 
# Circle is before Wall because it comes before it in the alphabet
class Circle_Wall(Contact):
    # def __init__(self, a, b):
    #     super().__init__(a, b)
    #     self.circle = a
    #     self.wall = b

    def update(self):  # compute the appropriate values
        circle:Circle = self.a
        wall:Wall = self.b

        r = circle.pos - wall.pos
        r_c = r.dot(wall.normal)
        self.overlap = circle.radius - r_c
        self.normal = wall.normal

    def point(self):
        circle:Circle = self.a
        return circle.pos - circle.radius * self.normal

# Empty class for Wall - Wall collisions
# The intersection of two infinite walls is not interesting, so skip them
class Wall_Wall(Contact):
    pass

class Circle_Polygon(Contact):
    def update(self):
        # set overlap & normal
        circle:Circle = self.a
        polygon:Polygon = self.b

        # Part 1
        self.overlap = math.inf
        for i, (point, normal) in enumerate(zip(polygon.points, polygon.normals)):
            overlap = circle.radius - (circle.pos - point).dot(normal)
            # least overlap
            if overlap < self.overlap:
                self.overlap = overlap
                self.normal = normal
                self.i=i

        # Part 2
        if 0 < self.overlap < circle.radius:
            point1 = polygon.points[self.i]
            point2 = polygon.points[self.i - 1]
            r1 = circle.pos - point1
            s1 = point2 - point1
            if (r1.dot(s1) < 0): # point1 contact
                self.overlap = circle.radius - r1.magnitude()
                # r1 may be zero
                if r1.magnitude() == 0:
                    self.normal = Vector2(0, 0)
                else:
                    self.normal = r1.normalize()
            else:
                r2 = circle.pos - point2
                s2 = point1 - point2
                if (r2.dot(s2) < 0): # point2 contact
                    self.overlap = circle.radius - r2.magnitude()
                    # r2 may be zero
                    if r2.magnitude() == 0:
                        self.normal = Vector2(0, 0)
                    else:
                        self.normal = r2.normalize()

    def point(self):
        circle:Circle = self.a
        return circle.pos - circle.radius * self.normal

