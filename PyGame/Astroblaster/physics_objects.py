from pygame.math import Vector2
import pygame
import math

class PhysicsObject:
    def __init__(self, mass=1, pos=(0,0), vel=(0,0), fixed=False,
                 momi=math.inf, angle=0, avel=0, ): # Constructor
        self.mass = mass
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        self.fixed = fixed
        self.clear_force()      # OR PhysicsObject.clear_force(self)
        self.momi = momi        # moment of inertia
        self.avel = avel        # angular velocity
        self.angle = angle      # rotational movement angle

    def set(self, pos=None, angle=None):
        if pos is not None:
            self.pos = Vector2(pos)
        if angle is not None:
            self.angle = angle

    def clear_force(self):
        self.force = Vector2(0,0)
        self.torque = 0

    def add_force(self, force):
        self.force += force

    def add_torque(self, torque):
        self.torque += torque

    def impulse(self, impulse, point=None):
        if point is not None:
            # s = point - center of mass
            s = point - self.pos
            # update avel
            torque = s.cross(impulse)
            self.avel += torque * 1/self.momi

        self.vel += impulse / self.mass

    def update(self, dt):
        if self.fixed:
            # ensure it doesn't move or accumulate forces
            self.force = Vector2(0,0)
            self.vel = Vector2(0,0)
            return
        # update velocity using the current force
        self.vel += (self.force / self.mass) * dt
        self.avel += self.torque / self.momi * dt
        # update position using the newly updated velocity
        self.pos += self.vel * dt
        self.angle += self.avel * dt


class Circle(PhysicsObject): # Inheritance
    def __init__(self, radius=100, color=(255,255,255), width=0, fixed=False, stripes=[], stripe_color=None, stripe_width=None, **kwargs): # kwargs = keyword arguments
        self.radius = radius
        self.color = color
        self.width = width
        self.original_color = color
        self.contact_type = "Circle"

        self.stripes = stripes
        self.stripe_color = self.color if stripe_color is None else stripe_color
        self.stripe_width = self.width if stripe_width is None else stripe_width

        super().__init__(**kwargs) # Call the parent class constructor

        self.fixed_color = (100, 100, 100) # dark gray

    def draw(self, window):
        draw_color = self.fixed_color if self.fixed else self.color
        pygame.draw.circle(window, draw_color, self.pos, self.radius, self.width)

        for angle in self.stripes:
            pygame.draw.line(window, self.stripe_color, self.pos, self.pos + self.radius*Vector2(1,0).rotate_rad(self.angle + angle))


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

class Polygon(PhysicsObject):
    def __init__(self, local_points=[], color=(255,0,0), width=0, normals_length=0,**kwargs):
        self.local_points = [Vector2(x) for x in local_points]
        self.local_normals:list[Vector2] = []
        for i in range(len(self.local_points)):
            point1 = self.local_points[i]
            point2 = self.local_points[i-1]
            self.local_normals.append((point2 - point1).normalize().rotate(90))
        self.check_convex()
        self.color = color
        self.width = width
        self.normals_length = normals_length
        super().__init__(**kwargs)
        self.contact_type = "Polygon"
        self.update(0) # Needed to create points and normals for the first time

    def check_convex(self):
        # Check if the shap is convex
        # And make sure normals are pointing outwards
        if len(self.local_points) > 2:
            convex = True
            epsilon = 1e-12
            for i, point in enumerate(self.local_points):
                d = [(p - point).dot(self.local_normals[i]) for p in self.local_points]
                if max(d) <= epsilon: # all points lie behind normal
                    pass
                elif min(d) >= -epsilon: # all points lie in front of normal (flip it)
                    self.local_normals[i] *= -1
                else: # points lie on both sides of normal, non-convex
                    convex = False
                if not convex:
                    print("WARNING! Non-convex polygon defined. Collisions will be incorrect.")

    def set(self, pos=None, angle=None):
        super().set(pos=pos, angle=angle)
        self.update(0)

    def update(self, dt):
        super().update(dt)
        self.points = [self.pos + local_point.rotate_rad(self.angle) for local_point in self.local_points]
        self.normals = [local_normal.rotate_rad(self.angle) for local_normal in self.local_normals]
    
    def draw(self, window):
        if len(self.points) > 2:
            pygame.draw.polygon(window, self.color, self.points, self.width)
        elif len(self.points) == 2:
            pygame.draw.line(window, self.color, self.points[0], self.points[1], self.width)
        else:
            pygame.draw.circle(window, self.color, self.points[0], self.width)
            
        if self.normals_length > 0:
            for i in range(len(self.normals)):
                point = (self.points[i] + self.points[i-1]) / 2
                normal = self.normals[i]
                pygame.draw.line(window, self.color, point, point + self.normals_length * normal)

class UniformCircle(Circle):
    def __init__(self, density=1, **kwargs):
        # Calculate mass and moment of inertia from density and radius if radius provided
        radius = kwargs.get("radius", None)
        if radius is not None:
            mass = density * math.pi * (radius ** 2)
            momi = 0.5 * mass * (radius ** 2)
        else:
            mass = kwargs.get("mass", 1)
            momi = kwargs.get("momi", math.inf)
        super().__init__(mass=mass, momi=momi, **kwargs)


class UniformPolygon(Polygon):
    def __init__(self, density=None, local_points=[], pos=[0,0], angle=0, shift=True, mass=None, **kwargs):
        if mass is not None and density is not None:
            raise("Cannot specify both mass and density.")
        if mass is None and density is None:
            mass = 1 # if nothing specified, default to mass = 1
        if density is None:
            density = 1
        
        # Calculate mass, moment of inertia, and center of mass
        # by looping over all "triangles" of the polygon
        # preset total_mass, total_momi, center_of_mass_numerator
        total_mass = 0
        total_momi = 0
        center_of_mass_numerator = Vector2(0,0)

        for i in range(len(local_points)):
            s0 = local_points[i]
            s1 = local_points[i-1]

            # Ensure we have Vector2 objects
            s0_2d = Vector2(s0)
            s1_2d = Vector2(s1)
            cross = s0_2d.cross(s1_2d)

            # triangle area (use absolute to ensure positive area regardless of winding)
            area = 0.5 * abs(cross)
            triangle_mass = density * area

            # triangle moment of inertia about origin (approx for the triangle)
            c_I = (triangle_mass/6) * (s0_2d.dot(s0_2d) + s1_2d.dot(s1_2d) + s0_2d.dot(s1_2d))

            # triangle center of mass contribution
            numerator = triangle_mass * ((s0_2d + s1_2d) / 3)

            # add to totals
            total_mass += triangle_mass
            total_momi += c_I
            center_of_mass_numerator += numerator
        
        # calculate total center of mass by dividing numerator by denominator (total mass)
        # center of mass
        if total_mass != 0:
            r = center_of_mass_numerator / total_mass
        else:
            r = Vector2(0,0)

        # if mass is specified, then scale mass and momi
        if mass is not None:
            total_momi *= mass/total_mass
            total_mass = mass

        # Usually we shift local_points origin to center of mass
        if shift:
            # 1. Shift all local_points by com
            # make a new list, for loop or list comprehension
            # 2. Shift pos
            # 3. Use parallel axis theorem to correct the moment of inertia
            shifted_points = []
            for p in local_points:
                shifted_points.append(Vector2(p) - r)

            # Parallel-axis theorem: I_cm = I_origin - M * |r_cm|^2
            I_cm = total_momi - total_mass * r.length_squared()
            I = abs(I_cm)

            local_points = shifted_points
            # shift the position by the center of mass (r)
            pos = Vector2(pos) + r
        else:
            I_cm = c_I
            I = abs(I_cm)

        # Then call super().__init__() with those correct values
        super().__init__(mass=abs(total_mass), momi=I, local_points=local_points, pos=pos, angle=angle, **kwargs) 

# Test UniformPolygon
shape = UniformPolygon(density=0.01, local_points=[[0,0],[20,0],[20,10],[0,10]])
print(f"Check mass: {shape.mass} = {0.01*10*20}")  # check mass
print(f"Check momi: {shape.momi} = {(shape.mass)/12*(10**2+20**2)}")  # check moment of inertia
print(shape.local_points) # check if rectangle is centered (checks center of mass)
print([[-10,-5],[10,-5],[10,5],[-10,5]])
                