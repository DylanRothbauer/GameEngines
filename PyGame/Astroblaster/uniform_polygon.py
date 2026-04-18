''' Copy this into your physics_objects.py file! '''

class UniformCircle(Circle):
    def __init__(self, density=1, **kwargs):
        # calculate mass and moment of inertia
        super().__init__(mass=mass, momi=momi, **kwargs)


class UniformPolygon(Polygon):
    def __init__(self, density=None, local_points=[], pos=[0,0], angle=0, shift=True, mass=None, **kwargs):
        if mass is not None and density is not None:
            raise("Cannot specify both mass and density.")
        if mass is None and density is None:
            mass = 1 # if nothing specified, default to mass = 1
        
        # Calculate mass, moment of inertia, and center of mass
        # by looping over all "triangles" of the polygon
        for i in range(len(local_points)):
            # triangle mass
            # triangle moment of inertia
            # triangle center of mass

            # add to total mass
            # add to total moment of inertia
            # add to center of mass numerator
            pass
        
        # calculate total center of mass by dividing numerator by denominator (total mass)

        # if mass is specified, then scale mass and momi
        if mass is not None:
            total_momi *= mass/total_mass
            total_mass = mass

        # Usually we shift local_points origin to center of mass
        if shift:
            # 1. Shift all local_points by com
            # 2. Shift pos
            # 3. Use parallel axis theorem to correct the moment of inertia
            pass            

        # Then call super().__init__() with those correct values
        super().__init__(mass=total_mass, momi=total_momi, local_points=local_points, pos=pos, angle=angle, **kwargs) 

# Test UniformPolygon
shape = UniformPolygon(density=0.01, local_points=[[0,0],[20,0],[20,10],[0,10]])
print(f"Check mass: {shape.mass} = {0.01*10*20}")  # check mass
print(f"Check momi: {shape.momi} = {shape.mass/12*(10**2+20**2)}")  # check moment of inertia
print(shape.local_points) # check if rectangle is centered (checks center of mass)
print([[-10,-5],[10,-5],[10,5],[-10,5]])  
