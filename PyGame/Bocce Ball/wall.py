# copy this into your physics_objects.py file

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