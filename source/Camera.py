import bpy
from enum import Enum
from math import radians, sin, cos

CAM_NAME = "cam"
camera_range = 190
angle_zoom = [radians(60), radians(55), radians(50), radians(45)]
angle_rotation = [radians(-67.5), radians(22.5), radians(112.5), radians(202.5)]


#
# class View(Enum):
#     NORTH = 0
#     WEST = 1
#     SOUTH = 2
#     EAST = 3
#
#
# class Zoom(Enum):
#     ONE = 0
#     TWO = 1
#     THREE = 2
#     FOUR = 3
#     FIVE = 4
#     SIX = 5


def get_location_and_rotation(rotation, zoom):
    level = zoom.value
    if level > 3:  # zoom 4, 5 & 6 all use the same camera angle
        level = 3

    x = camera_range * sin(angle_zoom[level]) * cos(angle_rotation[rotation.value])
    y = camera_range * sin(angle_zoom[level]) * sin(angle_rotation[rotation.value])
    z = camera_range * cos(angle_zoom[level])
    loc = (x, y, z)
    rot = (angle_zoom[level], 0,
           angle_rotation[rotation.value] + radians(90))  # need to add 90 for proper camera location in scene. .
    return [loc, rot]


def set_camera(location, angles):
    cam = bpy.data.cameras.new(CAM_NAME)
    cam_ob = bpy.data.objects.new(CAM_NAME, cam)
    cam_ob.data.type = "ORTHO"
    cam_ob.data.clip_end = 10000  # in meters, i.e. 10 km seems sufficient
    cam_ob.rotation_mode = "XYZ"
    cam_ob.location = location
    cam_ob.rotation_euler = angles
    bpy.context.scene.objects.link(cam_ob)


def default_render_dimension():
    # need this otherwise camera view is not square to begin with
    # also probably need to pass in zoom level. .?
    bpy.context.scene.render.resolution_x = 256
    bpy.context.scene.render.resolution_y = 256


def gui_ops_camera(rotation, zoom):
    for ob in bpy.data.objects:
        if ob.type == 'CAMERA' and ob.name == CAM_NAME:
            bpy.data.cameras.remove(ob.data, do_unlink=True)
    (location, rotation) = get_location_and_rotation(rotation, zoom)
    set_camera(location, rotation)
    default_render_dimension()

# debug
# gui_ops_camera(View.SOUTH, Zoom.TWO)
