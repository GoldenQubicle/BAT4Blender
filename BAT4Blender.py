import bpy


def test_function():
    print("ello tehre")


class Config(bpy.types.Operator):
    bl_idname = 'empty.class'
    bl_label = 'Empty Class'
    bl_description = "Empty Class"

    sun_loc = (0, 0, 1000)  # sun position doesn't matter, just put it somewhere up high and out of the way
    sun_rot = (3.1415927410125732, 2.356194496154785, 0.39269909262657166)  # in radians

    # x,y,z coordinates
    loc_z456 = (51.41363, -124.123474, 134.35028)
    loc_z3 = (55.698982, - 134.46922, 122.129654)
    loc_z2 = (59.560425, -143.79158, 108.97952)
    loc_z1 = (62.968586, -152.01959, 94.99999)
    cam_location = (loc_z1, loc_z2, loc_z3, loc_z456)

    # angle in radians
    rot_z456 = (0.7853982, 0, 0.3926991)
    rot_z3 = (0.87266463, 0, 0.3926991)
    rot_z2 = (0.9599311, 0, 0.3926991)
    rot_z1 = (1.0471976, 0, 0.3926991)
    cam_rotation = (rot_z1, rot_z2, rot_z3, rot_z456)


