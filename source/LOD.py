import bpy
from mathutils import Vector, Matrix
from typing import List, Any
from .Config import LOD_NAME


def get_all_bound_boxes() -> List:
    b_boxes = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            bbox_corners = [obj.matrix_world * Vector(corner) for corner in obj.bound_box]
            b_boxes.append(bbox_corners)
    return b_boxes


def get_min_max_xyz(b_boxes: List[List[Any]]) -> List[Any]:
    v = b_boxes[0][0]
    (min_x, max_x, min_y, max_y, min_z, max_z) = (v[0], v[0], v[1], v[1], v[2], v[2])
    for b in b_boxes:
        for v in b:
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


def get_mesh_cube(name) -> object:
    verts = [(1.0, 1.0, -1.0),
             (1.0, -1.0, -1.0),
             (-1.0, -1.0, -1.0),
             (-1.0, 1.0, -1.0),
             (1.0, 1.0, 1.0),
             (1.0, -1.0, 1.0),
             (-1.0, -1.0, 1.0),
             (-1.0, 1.0, 1.0)]
    faces = [(0, 1, 2, 3),
             (4, 7, 6, 5),
             (0, 4, 5, 1),
             (1, 5, 6, 2),
             (2, 6, 7, 3),
             (4, 0, 3, 7)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    return bpy.data.objects.new(name, mesh)


def create_lod(xyz_mm: List[Any]):
    width = xyz_mm[1] - xyz_mm[0]
    depth = xyz_mm[3] - xyz_mm[2]
    height = xyz_mm[5] - xyz_mm[4]
    loc = (xyz_mm[0] + width / 2, xyz_mm[2] + depth / 2, xyz_mm[4] + height / 2)

    c = get_mesh_cube(LOD_NAME)
    c.matrix_world *= Matrix.Translation(loc)
    c.matrix_world *= Matrix.Scale(width / 2, 4, (1, 0, 0))
    c.matrix_world *= Matrix.Scale(depth / 2, 4, (0, 1, 0))
    c.matrix_world *= Matrix.Scale(height / 2, 4, (0, 0, 1))
    c.hide_render = True
    bpy.context.scene.objects.link(c)
    bpy.context.scene.update()


def gui_ops_lod():
    for ob in bpy.data.objects:
        if ob.name == LOD_NAME:
            bpy.data.meshes.remove(ob.data)
            bpy.data.objects.remove(ob, do_unlink=True)

    bb = get_all_bound_boxes()
    min_max_xyz = get_min_max_xyz(bb)
    create_lod(min_max_xyz)


def gui_ops_lod_export():
    # first want to perform a fitting . ? or this may not be desirable if user has made custom LOD..

    print("export lod")

# gui_ops_lod()
