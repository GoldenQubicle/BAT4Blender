import bpy
import bpy_extras
from math import tan, atan
from mathutils import Vector


def translate(value, left_min, left_max, right_min, right_max):
    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - left_min) / float(left_span)

    # Convert the 0-1 range into a value in the right range.
    return right_min + (value_scaled * right_span)


lod = bpy.data.objects["LOD"]
cam = bpy.data.objects["cam"]
depsgraph = bpy.context.depsgraph
render_dimension = 256
# get the orthographic scale for the LOD object
coordinates = [lod.matrix_world @ Vector(corner) for corner in lod.bound_box]
co_list = []
for v in coordinates:
    for f in v:
        co_list.append(f)

os_lod = cam.camera_fit_coords(depsgraph, co_list)[1]

# calculate the orthographic scale according to gmax
# NOTE the ortho scale actually remains the same until the LOD no longer fits into view
# if true, the os is doubled and the output dimensions adjusted accordingly
unit = 16
targetWidth2 = unit + 8  # unit cube with render slop applied as specified in gmax script
renderFov = 2 * (atan(targetWidth2 / 190.0))
os_gmax = (cam.location[2] + unit / 2) * tan(
    renderFov)  # assuming the gmax camera focus in on lod center height which seems correct

print("actual ortho scale")
print(os_lod)
print("gmax ortho scale")
print(os_gmax)

# if the orthographic scale for the LOD is bigger than gmax derived value (which only uses LOD width)
# we know the object does not fit into camera view, either depth or height wise
#
# not sure yet if the derived os should increased, or if some kind of 'true' os should be used. .
# in addition the render dimensions should be adjusted accordingly in this step* as well
while os_lod > os_gmax:
    os_gmax *= 2
    render_dimension *= 2

# set the os for the camera, and reset the offsets
cam.data.ortho_scale = os_gmax
cam.data.shift_x = 0.0
cam.data.shift_y = 0.0

# get the 2d camera view coordinates for the LOD
coords_2d = [bpy_extras.object_utils.world_to_camera_view(bpy.context.scene, cam, coord) for coord in coordinates]

# given its boxy nature we know the outer left and top vertex in the camera view
# grab these two, which are in 0..1 range, and convert to render dimensions output (see step* above)
# now we know in pixels how far the LOD is from the left and top edges
x_left = coords_2d[0][0] * render_dimension
y_top = coords_2d[2][1] * render_dimension

slop = 2  # keep a 2 pixel distance from edge, can be made variable later for different levels
# finally map the pixel values back to a 0..1 range to use as offset
x_d = translate(x_left - slop, 0, render_dimension, 0.0, 1.0)
y_d = translate(y_top - (render_dimension - slop), 0, render_dimension, 0.0, 1.0)

cam.data.shift_x = x_d
cam.data.shift_y = y_d
bpy.context.scene.render.resolution_x = render_dimension
bpy.context.scene.render.resolution_y = render_dimension

# get the coordinates again with the shift applied to check whether or not the render needs to be square or rectangle
coords_2d = [bpy_extras.object_utils.world_to_camera_view(bpy.context.scene, cam, coord) for coord in coordinates]

x_width = coords_2d[7][0] * render_dimension - coords_2d[0][0] * render_dimension
# if x_width < render_dimension / 2:
#     bpy.context.scene.render.resolution_x = render_dimension / 2
#
# coords_2d = [bpy_extras.object_utils.world_to_camera_view(bpy.context.scene, cam, coord) for coord in coordinates]
# for co in coords_2d:
#     print(co)
