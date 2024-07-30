import bpy
from math import radians, atan2
from mathutils import Vector
from .Config import SUN_NAME
from .Enums import Rotation
from .Utils import b4b_collection


_sun_loc = (0, 0, 1000)  # sun position doesn't matter, just put it somewhere up high and out of the way


def _bat4max_sun_orientation():
    # note that sun angle of BATs differs from in-game sun
    x, y, z = -474, -352, 575  # South sun location in BAT4Max
    return 0, atan2(Vector([x, y]).length, z), atan2(y, x)  # 0°, 45.757°, 36.598°-180°


class Sun:
    @staticmethod
    def get_sun_rotation(rotation):
        s_x, s_y, s_z = _bat4max_sun_orientation()
        if rotation == Rotation.SOUTH:
            return s_x, s_y, s_z
        if rotation == Rotation.EAST:
            return s_x, s_y, s_z + radians(90)
        if rotation == Rotation.NORTH:
            return s_x, s_y, s_z + radians(180)
        if rotation == Rotation.WEST:
            return s_x, s_y, s_z + radians(270)

    @staticmethod
    def set_sun(rotation):
        sun = bpy.data.lights.new(SUN_NAME, "SUN")  # name, type
        sun_ob = bpy.data.objects.new(SUN_NAME, sun)
        sun_ob.rotation_mode = "XYZ"
        sun_ob.location = _sun_loc
        sun_ob.rotation_euler = rotation
        b4b_collection().objects.link(sun_ob)
        bpy.context.view_layer.update()

    @staticmethod
    def update(rotation):
        sun_rot = Sun.get_sun_rotation(rotation)
        bpy.data.objects[SUN_NAME].rotation_euler = sun_rot

    @staticmethod
    def add_to_scene():
        if SUN_NAME not in bpy.data.objects:
            sun_rot = Sun.get_sun_rotation(Rotation.SOUTH)
            Sun.set_sun(sun_rot)

    @staticmethod
    def delete_from_scene():
        if SUN_NAME in bpy.data.objects:
            ob = bpy.data.objects[SUN_NAME]
            bpy.data.lights.remove(ob.data, do_unlink=True)

    # @staticmethod
    # def gui_ops_sun(rotation):
    #     for ob in bpy.data.objects:
    #         if ob.type == 'LAMP' and ob.name == SUN_NAME:
    #             bpy.data.lights.remove(ob.data, do_unlink=True)
    #     sun_rot = Sun.get_sun_rotation(rotation)
    #     Sun.set_sun(sun_rot)


# gui_ops_sun(View.NORTH)
