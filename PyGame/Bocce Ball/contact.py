from pygame.math import Vector2
from physics_objects import PhysicsObject,Circle, Wall

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

    def resolve(self, restitution=None, update=True):
        if update:
            self.update()
        restitution = restitution if restitution is not None else self.kwargs.get("restitution", 1) 
        # ^ priority for restitution is: 1 argument in resolve, 2 argument in generate, 3 default value = 1 (elastic)
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
            relative_velocity = a.vel - b.vel
            # make sure they are moving towards each other
            if relative_velocity.dot(self.normal) < 0:
                # calculate J and impulse as a vector
                J = -(1 + restitution) * m * relative_velocity.dot(self.normal)
                impulse = J * self.normal
                # apply impulses to objects a and b
                a.impulse( impulse)
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
        self.normal = r.normalize()

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

# Empty class for Wall - Wall collisions
# The intersection of two infinite walls is not interesting, so skip them
class Wall_Wall(Contact):
    pass

