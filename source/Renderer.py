import bpy
import bpy_extras
from math import tan, atan
from mathutils import Vector
# from .LOD import LOD_NAME
# from .Camera import CAM_NAME
from enum import Enum

# render dimensions need to take view into account
# sd default
render_dimension = [16, 32, 64, 128, 256]

LOD_NAME = "LOD"
CAM_NAME = "cam"


class Zoom(Enum):
    ONE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4


def gui_ops_render(zoom):
    lod = bpy.data.objects[LOD_NAME]
    cam = bpy.data.objects[CAM_NAME]
    depsgraph = bpy.context.scene.depsgraph

    os_lod = get_orthographic_scale(depsgraph, cam, lod)
    os_gmax = get_orthographic_scale_gmax(cam.location[2])
    s_f = get_scale_factor(os_lod, os_gmax)

    os_cam = os_gmax * s_f
    dim = render_dimension[zoom.value] * s_f
    cam.data.ortho_scale = os_cam

    offset_camera(cam, lod, dim)
    # lod.hide_render = True
    bpy.ops.render.render('INVOKE_DEFAULT', write_still=False)
    # print("actual ortho scale")
    # print(os_lod)
    # print("gmax ortho scale")
    # print(os_gmax)
    # print("the scale factor")
    # print(s_f)
    # print("camera os")
    # print(os_cam)
    print("output dim")
    print(dim)


def offset_camera(cam, lod, dim):
    # since the renders can be rectangular assing to x, y
    dim_x = dim
    dim_y = dim
    # get the 2d camera view coordinates for the LOD... is this a correct assumption?
    coordinates = [lod.matrix_world * Vector(corner) for corner in lod.bound_box]
    coords_2d = [bpy_extras.object_utils.world_to_camera_view(bpy.context.scene, cam, coord) for coord in coordinates]

    # grab outer left and top vertex in the camera view
    # map their 0..1 range to pixels to determine how far theLOD is from the left and top edges
    c_x = []
    c_y = []
    for c in coords_2d:
        c_x.append(c[0])
        c_y.append(c[1])

    min_x = min(c_x)
    max_y = max(c_y)

    x_left = min_x * dim_x
    y_top = max_y * dim_y
    # print("left x")
    # print(x_left)
    # print("top y")
    # print(y_top)

    # map the pixel values back to a 0..1 range to use as offset
    slop = 2  # keep a 2 pixel distance from edge, can be made variable later for different levels
    x_d = translate(x_left - slop, 0, dim_x, 0.0, 1.0)
    y_d = translate(y_top - (dim_y - slop), 0, dim_y, 0.0, 1.0)
    cam.data.shift_x = x_d
    cam.data.shift_y = y_d

    # TODO check if either right or bottom half render square is empty
    # i.e. does the LOD extend into half of that
    # if so the corresponding render dimension needs to be halved, and then reposition camera again
    bpy.context.scene.render.resolution_x = dim_x
    bpy.context.scene.render.resolution_y = dim_y



def get_scale_factor(os_lod, os_gmax):
    factor = 1
    while os_lod > os_gmax:
        factor *= 2
        os_gmax *= 2
    return factor


def get_orthographic_scale(dg, cam, lod):
    coordinates = [lod.matrix_world * Vector(corner) for corner in lod.bound_box]
    co_list = []
    for v in coordinates:
        for f in v:
            co_list.append(f)

    return cam.camera_fit_coords(dg, co_list)[1]


# NOTE currently passing in camera height depending on zoom
# not sure if that's correct, i.e. perhaps the OS for z5 should be used throughout
def get_orthographic_scale_gmax(cam_z):
    unit = 16
    targetWidth2 = unit + 8  # unit cube with render slop applied as specified in gmax script
    renderFov = 2 * (atan(targetWidth2 / 190.0))
    return (cam_z + unit / 2) * tan(
        renderFov)  # assuming the gmax camera focus in on lod center height which seems correct


def translate(value, left_min, left_max, right_min, right_max):
    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - left_min) / float(left_span)

    # Convert the 0-1 range into a value in the right range.
    return right_min + (value_scaled * right_span)

bpy.data.objects[CAM_NAME].data.shift_x = 0.0
bpy.data.objects[CAM_NAME].data.shift_y = 0.0
gui_ops_render(Zoom.THREE)

# # if the orthographic scale for the LOD is bigger than gmax derived value (which only uses LOD width)
# # we know the object does not fit into camera view, either depth or height wise
# #
# # not sure yet if the derived os should increased, or if some kind of 'true' os should be used. .
# # in addition the render dimensions should be adjusted accordingly in this step* as well

#
# # set the os for the camera, and reset the offsets
# cam.data.ortho_scale = os_gmax
# cam.data.shift_x = 0.0
# cam.data.shift_y = 0.0
#

#

#

#
# # get the coordinates again with the shift applied to check whether or not the render needs to be square or rectangle
# coords_2d = [bpy_extras.object_utils.world_to_camera_view(bpy.context.scene, cam, coord) for coord in coordinates]
#
# x_width = coords_2d[7][0] * render_dimension - coords_2d[0][0] * render_dimension
# # if x_width < render_dimension / 2:
# #     bpy.context.scene.render.resolution_x = render_dimension / 2
# #
# # coords_2d = [bpy_extras.object_utils.world_to_camera_view(bpy.context.scene, cam, coord) for coord in coordinates]
# # for co in coords_2d:
# #     print(co)
