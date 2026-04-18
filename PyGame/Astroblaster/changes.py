# The following changes need to be made to physics_objects.py

# Add the following function to the class PhysicsObject:
def set(self, pos=None, angle=None):
    if pos is not None:
        self.pos = Vector2(pos)
    if angle is not None:
        self.angle = angle

# Add the following function to the class Polygon:
def set(self, pos=None, angle=None):
    super().set(pos=pos, angle=angle)
    self.update(0)


# The following changes need to be made to contact.py:

# Modify the lines of the resolve function where you resolve overlap.
# Instead of a changing position directly, use the set function:
        # RESOLVE OVERLAP
m = 1/(1/self.a.mass + 1/self.b.mass) # reduced mass
self.a.set(pos=self.a.pos + m/self.a.mass*self.overlap*self.normal)
self.b.set(pos=self.b.pos - m/self.b.mass*self.overlap*self.normal)

# You will need to add classes for Polygon_Wall and Polygon_Polygon.
# They can be empty at first, with just pass inside, 
# but you will fill them in as you follow along in class.  


# There are also numerous little changes to the test files.
# Please download the updated versions from Canvas.
