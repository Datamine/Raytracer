class Vector():
    """
    for handling vectors of length three.
    """
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def l2_norm(self):
        """
        return the l2 norm of the vector.
        """
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    def to_unit(self):
        """
        return the unit vector corresponding to the vector.
        """
        magnitude = self.l2_norm()
        return Vector(self.x/magnitude, self.y/magnitude, self.z/magnitude)
    def scalar_mult(self,s):
        """
        multiply the vector by a scalar.
        """
        return Vector(self.x * s, self.y * s, self.z * s)
    def print_v(self):
        """
        print the vector. for debugging.
        """
        print (self.x, self.y, self.z)

class Color():
    """
    for handling RGB colors. Should I use a color library instead?
    """
    def __init__(self,r,g,b):
        """
        where r,g,b are integers in [0,255]
        """
        self.r = r
        self.g = g
        self.b = b
    def to_tuple(self):
        """
        return a tuple so it can be parsed by the Image library.
        """
        return (self.r, self.g, self.b)
    def scale(self, x):
        """
        scale a color by some scalar, within [0,255] bounds.
        """
        r = max(0, min(255, self.r * x))
        g = max(0, min(255, self.g * x))
        b = max(0, min(255, self.b * x))
        return Color(r,g,b)

class Ray():
    """
    A camera or shadow ray is characterized by
    its origin and direction vectors.
    """
    def __init__(self, origin, direction):
        # where o,d are vectors
        self.origin = origin
        self.direction = direction

class Light():
    """
    direction and color of ambient light.
    """
    def __init__(self, direction, color):
        self.direction = direction
        self.color = color

class Sphere():
    """
    defines a sphere in the image.
    """
    def __init__(self, center, radius, color):
        """
        center is a Vector, radius is a float, color is a Color
        """
        self.center = center
        self.radius = radius
        self.color = color

class Hit():
    """
    A hit object is created if a ray strikes the camera,
    otherwise Null. Note: surface_normal is a ray.
    """
    def __init__(self, surface_color, surface_normal):
        self.color = surface_color
        self.normal = surface_normal

def vector_add(v1,v2):
    """
    add two vectors.
    """
    return Vector(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)
 
def vector_sub(v1,v2):
    """
    subtract the second vector from the first vector.
    """
    return Vector(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)
        
def vector_dot(v1,v2):
    """
    take the dot product of two vectors.
    """
    return (v1.x * v2.x) + (v1.y * v2.y) + (v1.z * v2.z)

def color_modulate(c1, c2):
    """
    pointwise multiplication of two colors.
    """
    r_component = int(c1.r * c2.r / 255.0)
    g_component = int(c1.g * c2.g / 255.0)
    b_component = int(c1.b * c2.b / 255.0)
    return Color(r_component, g_component, b_component)

def color_add(c1,c2):
    r = c1.r + c2.r
    r = max(0, min(255, r))

    g = c1.g + c2.g
    g = max(0, min(255, g))
    
    b = c1.b + c2.b
    b = max(0, min(255, b))
    return Color(r,g,b)