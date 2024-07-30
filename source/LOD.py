import bpy
import bmesh
from mathutils import Vector, Matrix
from typing import List, Any
from .Config import LOD_NAME
from .Utils import b4b_collection, translate, clip
from .Enums import Rotation


class LOD:
    @staticmethod
    def fit_new():
        bb = LOD.get_all_bound_boxes()
        min_max_xyz = LOD.get_min_max_xyz(bb)
        LOD.create_and_update(min_max_xyz)

    @staticmethod
    def get_all_bound_boxes() -> List:
        b_boxes = []
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH' and not obj.hide_render:
                bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
                b_boxes.append(bbox_corners)
        return b_boxes

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def create_and_update(xyz_mm: List[Any]):
        width = xyz_mm[1] - xyz_mm[0]
        depth = xyz_mm[3] - xyz_mm[2]
        height = xyz_mm[5] - xyz_mm[4]
        loc = (xyz_mm[0] + width / 2, xyz_mm[2] + depth / 2, xyz_mm[4] + height / 2)

        c = LOD.get_mesh_cube(LOD_NAME)
        c.matrix_world @= Matrix.Translation(loc)
        c.matrix_world @= Matrix.Scale(width / 2, 4, (1, 0, 0))
        c.matrix_world @= Matrix.Scale(depth / 2, 4, (0, 1, 0))
        c.matrix_world @= Matrix.Scale(height / 2, 4, (0, 0, 1))
        c.hide_render = True
        c.display_type = 'WIRE'
        b4b_collection().objects.link(c)
        bpy.context.view_layer.update()

    @staticmethod
    def assign_material_name(lod_slice, name: str):
        mat = bpy.data.materials.get(name)
        if mat is None:
            mat = bpy.data.materials.new(name=name)
        if lod_slice.data.materials:
            lod_slice.data.materials[0] = mat
        else:
            lod_slice.data.materials.append(mat)
        return mat

    @staticmethod
    def export(lod_objects, filepath: str, rotation: Rotation):
        r"""Export a list of sliced LOD objects as a single .obj file"""
        # if LOD_NAME in bpy.data.objects:
        with bpy.context.temp_override(selected_objects=lod_objects):
            # In Blender 4+, bpy.ops.wm.obj_export can be used instead, but arguments differ
            bpy.ops.export_scene.obj(
                filepath=filepath,  # "{}.obj".format(get_relative_path_for(LOD_NAME)),
                check_existing=False,
                axis_up='Y',
                axis_forward=(
                    '-Z' if rotation == Rotation.SOUTH else
                    'X' if rotation == Rotation.EAST else
                    'Z' if rotation == Rotation.NORTH else
                    '-X'),  # WEST
                use_selection=True,
                use_materials=True,  # only needed for preserving the material name
                use_triangles=True,
            )
        # else:
        #     print("there is no LOD to export!")

    @staticmethod
    def _copy_bmesh_with_face_filter(mesh: bmesh.types.BMesh, name: str, face_filter) -> bpy.types.Mesh:
        mesh.verts.index_update()  # important if vertices have been added that still have index -1

        faces = [f for f in mesh.faces if face_filter(f)]
        vertices = list(set(v for f in faces for v in f.verts))
        vmap = {vert.index: i for i, vert in enumerate(vertices)}  # maps vertex indices of old mesh to new mesh (with fewer vertices)
        coords = [v.co for v in vertices]
        polys = [tuple(vmap[v.index] for v in f.verts) for f in faces]

        mesh2 = bpy.data.meshes.new(name=name)
        mesh2.from_pydata(coords, [], polys)
        mesh2.update(calc_edges=True)
        return mesh2

    def copy_visible_faces(lod, cam) -> bpy.types.Object:
        r"""Create a copy of the LOD containing only faces whose normals point towards the camera.
        """
        cam_view_direction = cam.matrix_world @ Vector([0, 0, -1]) - cam.location
        bm = bmesh.new()
        bm.from_mesh(lod.data)
        name = 'b4b_lod_visible'
        mesh = LOD._copy_bmesh_with_face_filter(bm, name, lambda f: f.normal.dot(cam_view_direction) < 0)
        obj = bpy.data.objects.new(name, mesh)
        obj.location = lod.location
        obj.scale = lod.scale
        obj.rotation_euler = lod.rotation_euler
        obj.hide_render = True
        b4b_collection().objects.link(obj)
        return obj

    def sliced(lod, cam, canvas):
        r"""Slice up the visible part of the LOD along the canvas tile grid and
        return a dictionary of the tile positions and the sliced LOD objects.
        """
        from .Canvas import Canvas
        canvas_grid = canvas.grid(cam)

        bpy.context.view_layer.update()  # this is important to get up-to-date local coordinates, as tiles were just created/cam was just positioned
        lod_visible = LOD.copy_visible_faces(lod, cam)  # as the knife_project modifies this object, we create it anew for each tile
        lod_visible.parent = cam  # for local coordinates (to find vertices inside tile boundary)
        lod_visible.matrix_parent_inverse = cam.matrix_world.inverted()  # TODO or .matrix_local?

        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = lod_visible

        # apply bisect operator along grid (multiple times)
        bpy.ops.object.mode_set(mode='EDIT')
        for no, coords in [(Vector([1, 0, 0]), canvas_grid.column_coords),
                           (Vector([0, 1, 0]), canvas_grid.row_coords)]:
            for co in coords[1:-1]:
                bpy.ops.mesh.select_all(action='SELECT')
                plane_co = cam.matrix_world @ co - cam.location
                plane_no = cam.matrix_world @ no - cam.location
                bpy.ops.mesh.bisect(plane_co=plane_co, plane_no=plane_no)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')

        bm = bmesh.new()
        bm.from_mesh(lod_visible.data)

        def create_slice_obj(row: int, col: int):
            name = 'b4b_lod_slice'
            # As some or all vertices of a face could lie on the grid, to avoid
            # numerical issues, we check whether the center of the polygon is
            # inside the canvas tile.
            slice_mesh = LOD._copy_bmesh_with_face_filter(
                    bm, name,
                    lambda f: canvas_grid.is_point_in_tile(Canvas._mean([lod_visible.matrix_local @ v.co for v in f.verts]), row=row, col=col))

            slice_obj = bpy.data.objects.new(name, slice_mesh)
            slice_obj.location = lod_visible.location
            slice_obj.scale = lod_visible.scale
            slice_obj.rotation_euler = lod_visible.rotation_euler
            slice_obj.hide_render = True
            slice_obj.parent = cam
            slice_obj.matrix_parent_inverse = cam.matrix_world.inverted()  # TODO or .matrix_local?
            b4b_collection().objects.link(slice_obj)
            bpy.context.view_layer.update()  # important so that computation of uv-map sees current coordinates

            # set uv coordinates
            uv_map = LOD._compute_uv_of_lod_slice(slice_obj, *canvas_grid.frame.tile_border_absolute_LRTB(canvas, row=row, col=col))
            uv_layer = slice_obj.data.uv_layers.new(name='UVmap')
            for polygon in slice_obj.data.polygons:
                for loopindex in polygon.loop_indices:  # loopindex corresponds to a "face vertex"
                    meshloop = slice_obj.data.loops[loopindex]
                    meshuvloop = uv_layer.data[loopindex]
                    meshuvloop.uv.xy = uv_map[meshloop.vertex_index]

            return slice_obj

        slice_objs = {pos: create_slice_obj(*pos) for pos in canvas.tiles()}
        bm.free()
        bpy.data.meshes.remove(lod_visible.data, do_unlink=True)
        return slice_objs

    def _compute_uv_of_lod_slice(lod_slice, x_min: float, x_max: float, y_max: float, y_min: float):

        def vert2uv(vert):
            # the local coordinates are relative to the parent (canvas_tile),
            # so first two coordinates correspond to u,v (up to stretching)
            c = lod_slice.matrix_local @ vert.co
            return (clip(translate(c[0], x_min, x_max, 0.0, 1.0), 0, 1),
                    clip(translate(c[1], y_min, y_max, 0.0, 1.0), 0, 1))

        uv_map = {v.index: vert2uv(v) for v in lod_slice.data.vertices}
        return uv_map
