import bpy
from math import radians
from .Config import *
from .Enums import View

sun_loc = (0, 0, 1000)  # sun position doesn't matter, just put it somewhere up high and out of the way
s_x = radians(180)
s_y = radians(135.0)
s_z = radians(22.5)  # default to north


class Sun:
    @staticmethod
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

    @staticmethod
    def set_sun(rotation):
        sun = bpy.data.lamps.new(SUN_NAME, "SUN")  # name, type
        sun_ob = bpy.data.objects.new(SUN_NAME, sun)
        sun_ob.rotation_mode = "XYZ"
        sun_ob.location = sun_loc
        sun_ob.rotation_euler = rotation
        bpy.context.scene.objects.link(sun_ob)
        bpy.context.scene.update()


    @staticmethod
    def update(rotation):
        sun_rot = Sun.get_sun_rotation(rotation)
        bpy.data.objects[SUN_NAME].rotation_euler = sun_rot

    @staticmethod
    def add_to_scene():
        if SUN_NAME not in bpy.data.objects:
            sun_rot = Sun.get_sun_rotation(View.NORTH)
            Sun.set_sun(sun_rot)

    @staticmethod
    def delete_from_scene():
        if SUN_NAME in bpy.data.objects:
            ob = bpy.data.objects[SUN_NAME]
            bpy.data.lamps.remove(ob.data, do_unlink=True)

    @staticmethod
    def gui_ops_sun(rotation):
        for ob in bpy.data.objects:
            if ob.type == 'LAMP' and ob.name == SUN_NAME:
                bpy.data.lamps.remove(ob.data, do_unlink=True)

        sun_rot = Sun.get_sun_rotation(rotation)
        Sun.set_sun(sun_rot)


# gui_ops_sun(View.NORTH)
