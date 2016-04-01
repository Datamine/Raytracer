# John Loeber | March 2016 | Python 2.7.10 | contact@johnloeber.com

from cube_specific_helpers import *

CAMERA_Z = -5
IMG_W = 180
IMG_H = 180

BGCOLOR = Rgb(0.3, 0.6, 1.0)
AMBIENT_LIGHT_COLOR = Rgb(0.2, 0.2, 0.2)

SCENE_LIGHT = Light(Vector(-1,1,-1).to_unit(), Rgb(1,1,1))

CUBE = Cube(Vector(0,0,3), 0, 0, 1, Rgb(0.8, 0.8, 0.8))

def intersect(ray):
    """
    rotating a cube and handling the raytracing geometry can get tricky.
    it's easier to equivalently rotate the camera and light source around 
    the cube, such that the cube becomes an axis-aligned bounding box,
    which it is easy to compute intersections for.
    """
    # note that this is not actually the correct rotation
    # ray.origin is the position of the camera 
    # should I make rotate a method of CUBE? Instead of a standalone function?
    new_camera_loc = rotate(ray.origin, CUBE.rot_x, CUBE.rot_y)
    global SCENE_LIGHT
    new_light_dir = rotate(SCENE_LIGHT.direction, CUBE.rot_x, CUBE.rot_y)
    # change the global lighting. not passing lighting as an arg was a bad
    # decision on my part -- need to fix
    SCENE_LIGHT = Light(new_light_dir, SCENE_LIGHT.color)

    vertices = CUBE.vertices()
    # coordinates of vertices nearest to and furthest from the camera
    near = min(vertices, key = lambda x: vector_sub(x, new_camera_loc).l2_norm())
    far = min(vertices, key = lambda x: vector_sub(x, new_camera_loc).l2_norm())

    a = 1.0 / ray.direction.x
    if a >= 0:
        tx_min = (near.x - ray.origin.x) * a
        tx_max = (far.x  - ray.origin.x) * a
    else:
        tx_min = (far.x  - ray.origin.x) * a
        tx_max = (near.x - ray.origin.x) * a


    b = 1.0 / ray.direction.y
    if b >= 0:
        ty_min = (near.y - ray.origin.y) * b
        ty_max = (far.y  - ray.origin.y) * b
    else:
        ty_min = (far.y  - ray.origin.y) * b
        ty_max = (near.y - ray.origin.y) * b

    c = 1.0 / ray.direction.z
    if c >= 0:
        tz_min = (near.z - ray.origin.z) * c
        tz_max = (far.z  - ray.origin.z) * c
    else:
        tz_min = (far.z  - ray.origin.z) * c
        tz_max = (near.z - ray.origin.z) * c

    t0 = max(tx_min, ty_min, tz_min)
    t1 = min(tx_max, ty_max, tz_max)

    if t0 < t1 and t1 > 0.00001:
        normal = Vector(1,1,1)
        return Hit(t, CUBE.color, normal)
    else:
        return None

def shadowed(shape_surface_vector):
    nudge = vector_add(shape_surface_vector, SCENE_LIGHT.direction.scale(0.0001))
    to_the_light = Ray(nudge, SCENE_LIGHT.direction)
    return intersect(to_the_light) != None

def lighting_cube(ray, hit):
    return hit.color

im = Image.new("RGB", (IMG_W, IMG_H), BGCOLOR.to_color())

for x in range(IMG_W):
    for y in range(IMG_H):
        position = Posn(x,y)
        logical_position = logical_loc(position, IMG_W, IMG_H)

        ray_origin = Vector(0,0,CAMERA_Z)
        ray_vector = vector_sub(logical_position, ray_origin).to_unit()
        cast_ray = Ray(ray_origin, ray_vector)
        
        hit = intersect(cast_ray)
        if hit != None:
            color = lighting(cast_ray, hit)
            truecolor = color.to_color()
            im.putpixel((x,y),truecolor)

im.save("cube" + str(int(time())) + ".png", "PNG")
