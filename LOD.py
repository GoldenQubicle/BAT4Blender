from typing import List, Any
from bpy_extras.io_utils import unpack_list, unpack_face_list

import bpy

from mathutils import Vector
from mathutils import Matrix


def get_all_bound_boxes() -> List:
    bboxes: List[List[Any]] = []
    for ob in bpy.context.collection.all_objects:
        if ob.type == 'MESH':
            bbox_corners = [ob.matrix_world @ Vector(corner) for corner in ob.bound_box]
            bboxes.append(bbox_corners)
    return bboxes


def get_min_max_xyz(bboxes: List[List[Any]]) -> List[Any]:
    (min_x, max_x, min_y, max_y, min_z, max_z) = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    for bb in bboxes:
        for v in bb:
            if v[0] < min_x:
                min_x = v[0]
            if v[0] > max_x:
                max_x = v[0]
            if v[1] < min_y:
                min_y = v[1]
            if v[1] > max_y:
                max_y = v[1]
            if v[2] < min_z:
                min_z = v[2]
            if v[2] > max_z:
                max_z = v[2]
    return [min_x, max_x, min_y, max_y, min_z, max_z]


bb = get_all_bound_boxes()
min_max_xyz = get_min_max_xyz(bb)
print(min_max_xyz)

# (min_x, max_x, min_y, max_y, min_z, max_z) = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
# for b in bb:
#     print("bound box")
#     for v in b:
#         if v[0] < min_x:
#             min_x = v[0]
#         if v[0] > max_x:
#             max_x = v[0]
#         if v[1] < min_y:
#             min_y = v[1]
#         if v[1] > max_y:
#             max_y = v[1]
#         if v[2] < min_z:
#             min_z = v[2]
#         if v[2] > max_z:
#             max_z = v[2]


# start with min / max x,y,z variables at 0 (i.e. world origin)
# go over all vertices and get the min / max values for x,y,z
# from this set of 6 values; calculate dimensions and center location
