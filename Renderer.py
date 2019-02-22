import bpy
from mathutils import Vector


lod = bpy.context.collection.all_objects["LOD"]
cam = bpy.data.objects["cam"]
depsgraph = bpy.context.depsgraph
coordinates = [lod.matrix_world @ Vector(corner) for corner in lod.bound_box]
co_list = []
for v in coordinates:
    for f in v:
        co_list.append(f)

r = cam.camera_fit_coords(depsgraph, co_list)

cam.data.ortho_scale = r[1]
