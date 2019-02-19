import bpy
from enum import Enum
from math import radians, sin, cos

CAM_NAME = "cam_654"

range = 190
angle_zoom = [radians(60), radians(55), radians(50), radians(45)]
angle_rotation = radians(67.5)


class Rotation(Enum):
    NORTH = 1,
    EAST = 2,
    SOUTH = 3,
    WEST = 4


class Zoom(Enum):
    ONE = 1,
    TWO = 2,
    THREE = 3,
    FOUR = 4,
    FIVE = 5,
    SIX = 6

# pass an orientation & zoom flag here. . ? and set camera specific for each view -> would need lot of config values
# better grab the camera object and translate & rotate according to flags..?

# q: how to figure out the correct scale . .
# - figure out by lod dimension. .?
# - figure out by checking of lod is in camera view. .?
# probably will need to do both

def get_location_and_angle(rotation, zoom):
    if zoom == Zoom.FOUR or Zoom.FIVE or Zoom.SIX:
        setup = 3
    if zoom == Zoom.THREE:
        setup = 2
    if zoom == Zoom.TWO:
        setup = 1
    if zoom == Zoom.ONE:
        setup = 0

    x = range * sin(angle_zoom[setup]) * sin(angle_rotation)
    y = range * sin(angle_zoom[setup]) * cos(angle_rotation)
    z = range * cos(angle_zoom[setup])
    
    loc = (x, y, z)
    rot = ()
    print(loc)




def set_camera(location, angles):
    cam = bpy.data.cameras.new(CAM_NAME)
    cam_ob = bpy.data.objects.new(CAM_NAME, cam)
    cam_ob.data.type = "ORTHO"
    cam_ob.rotation_mode = "XYZ"
    cam_ob.location = location
    cam_ob.rotation_euler = angles
    bpy.context.scene.collection.objects.link(cam_ob)


def default_render_dimension():
    # need this otherwise camera view is not square to begin with
    bpy.context.scene.render.resolution_x = 256
    bpy.context.scene.render.resolution_y = 256


for ob in bpy.data.objects:
    if ob.name == CAM_NAME:
        bpy.data.objects.remove(ob, do_unlink=True)

config = get_location_and_angle(Rotation.NORTH, Zoom.SIX)

# set_camera(config[0], config[1])
# default_render_dimension()
