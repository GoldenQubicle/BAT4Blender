import bpy
from .Enums import View
from math import radians
# from enum import Enum

SUN_NAME = 'sun'
sun_loc = (0, 0, 1000)  # sun position doesn't matter, just put it somewhere up high and out of the way
s_x = radians(180)
s_y = radians(135.0)
s_z = radians(22.5)  # default to north

#
# class View(Enum):
#     NORTH = 0
#     WEST = 1
#     SOUTH = 2
#     EAST = 3


def get_sun_rotation(rotation):
    if rotation == View.NORTH:
        sr = [s_x, s_y, s_z]
    if rotation == View.EAST:
        sr = [s_x, s_y, s_z - radians(90)]
    if rotation == View.SOUTH:
        sr = [s_x, s_y, s_z + radians(180)]
    if rotation == View.WEST:
        sr = [s_x, s_y, s_z - radians(270)]
    return sr


def set_sun(rotation):
    sun = bpy.data.lamps.new(SUN_NAME, "SUN")  # name, type
    sun_ob = bpy.data.objects.new(SUN_NAME, sun)
    sun_ob.rotation_mode = "XYZ"
    sun_ob.location = sun_loc
    sun_ob.rotation_euler = rotation
    bpy.context.scene.objects.link(sun_ob)


def gui_ops_sun(rotation):
    for ob in bpy.data.objects:
        if ob.type == 'LAMP' and ob.name == SUN_NAME:
            bpy.data.lamps.remove(ob.data, do_unlink=True)

    sun_rot = get_sun_rotation(rotation)
    set_sun(sun_rot)


# gui_ops_sun(View.NORTH)
