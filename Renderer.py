import bpy, bpy_extras
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

# get the orthographic scale for the LOD object
coordinates = [lod.matrix_world @ Vector(corner) for corner in lod.bound_box]
co_list = []
for v in coordinates:
    for f in v:
        co_list.append(f)

r = cam.camera_fit_coords(depsgraph, co_list)

# calculate the orthographic scale according to gmax
targetWidth2 = lod.dimensions[0] + 8
renderFov = 2 * (atan(targetWidth2 / 190.0))
os = (cam.location[2] + lod.dimensions[2] / 2) * tan(renderFov);
cam.data.ortho_scale = os

print("actual ortho scale")
print(r[1])
print("gmax ortho scale")
print(os)

# if the orthographic scale for the LOD is bigger than gmax derived value (which only uses LOD width)
# we know the object does not fit into camera view, either depth or height wise
# not sure yet if the derived os should increased, or if some kind of 'true' os should be used. .
# in addition the render dimensions should be increased in this step* as well
while r[1] > os:
    os *= 2

# set the os for the camera, and reset the offsets
cam.data.ortho_scale = os
cam.data.shift_x = 0.0
cam.data.shift_y = 0.0

# get the 2d camera coordinates for the LOD
coords_2d = [bpy_extras.object_utils.world_to_camera_view(bpy.context.scene, cam, coord) for coord in coordinates]

# given its boxy nature we know the outer left and top vertex in the camera view
# grab these two, which are in 0..1 range so convert to render dimensions output (see step* above)
x_left = coords_2d[0][0] * 256
y_top = coords_2d[2][1] * 256
# now we know in pixels how far the render is from the left and top edges
slop = 2  # keep a 2 pixel distance from edge, can be made variable later for different levels
# finally map the pixel values back to a 0..1 range to use as offset
x_d = translate(x_left - slop, 0, 256, 0.0, 1.0)
y_d = translate(y_top - (256 - slop), 0, 256, 0.0, 1.0)

cam.data.shift_x = x_d
cam.data.shift_y = y_d

