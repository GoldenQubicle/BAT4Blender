from __future__ import annotations

import bpy
from collections.abc import Iterator
from dataclasses import dataclass
from math import ceil
from mathutils import Vector

_MAX_TILE_SIZE_PX = 256
_MIN_TILE_SIZE_PX = 4
_SLOP = 3


class Canvas:
    r"""A 2D rendering canvas, divided into tiles of size at most 256 px.
    """
    width_px: int
    height_px: int
    num_columns: int
    num_rows: int

    def __init__(self, width_px: int, height_px: int):
        assert width_px % _MIN_TILE_SIZE_PX == 0 and height_px % _MIN_TILE_SIZE_PX == 0, "FSH dimensions must be multiple of 4"
        self.width_px = width_px
        self.height_px = height_px
        self.num_columns = ceil(width_px / _MAX_TILE_SIZE_PX)
        self.num_rows = ceil(height_px / _MAX_TILE_SIZE_PX)

    @staticmethod
    def create(cam, lod, dim_lod: float, margin: int) -> Canvas:
        r"""Create a Canvas for the current LOD and camera, and include a slop margin.
        The dim_lod parameter is a factor to map the LOD dimensions from the 0..1 range to the pixel range.
        """
        from .Camera import Camera
        # convert from 3d space to 2d camera space
        u_min, u_max, v_max, v_min = Camera.lod_bounds_LRTB(cam, lod)

        max_res = max(bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y)
        dim_u = (u_max - u_min) * dim_lod * (bpy.context.scene.render.resolution_x / max_res)
        dim_v = (v_max - v_min) * dim_lod * (bpy.context.scene.render.resolution_y / max_res)

        w = Canvas._round_up_to_fsh_chunk(dim_u + 2 * margin)
        h = Canvas._round_up_to_fsh_chunk(dim_v + 2 * margin)
        return Canvas(width_px=w, height_px=h)

    @staticmethod
    def _round_up_to_fsh_chunk(f) -> int:
        cnt, rem = divmod(ceil(f), _MAX_TILE_SIZE_PX)
        result = cnt * _MAX_TILE_SIZE_PX + (0 if rem == 0 else
                                            8 if rem <= 8 else
                                            16 if rem <= 16 else
                                            32 if rem <= 32 else
                                            64 if rem <= 64 else
                                            128 if rem <= 128 else
                                            _MAX_TILE_SIZE_PX)
        return result

    def tile_dimensions_px(self, row: int, col: int) -> (int, int):
        assert 0 <= row and row < self.num_rows
        assert 0 <= col and col < self.num_columns
        w = self.width_px - col * _MAX_TILE_SIZE_PX if col == self.num_columns - 1 else _MAX_TILE_SIZE_PX
        h = self.height_px - row * _MAX_TILE_SIZE_PX if row == self.num_rows - 1 else _MAX_TILE_SIZE_PX
        return w, h

    def tiles(self) -> Iterator[(int, int)]:
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                yield row, col

    def tile_border_px_LRTB(self, row: int, col: int) -> (int, int, int, int):
        l = col * _MAX_TILE_SIZE_PX
        r = min((col + 1) * _MAX_TILE_SIZE_PX, self.width_px)
        t = row * _MAX_TILE_SIZE_PX
        b = min((row + 1) * _MAX_TILE_SIZE_PX, self.height_px)
        return l, r, t, b

    def tile_border_fractional_LRTB(self, row: int, col: int) -> (float, float, float, float):
        l, r, t, b = self.tile_border_px_LRTB(row=row, col=col)
        return l / self.width_px, r / self.width_px, t / self.height_px, b / self.height_px

    @staticmethod
    def find_view3d():
        for area in bpy.context.window.screen.areas:
            if area.type == 'VIEW_3D':
                v3d = area.spaces[0]
                # rv3d = v3d.region_3d
                for region in area.regions:
                    if region.type == 'WINDOW':
                        return {'area': area, 'space': v3d, 'region': region}
        return {}

    @staticmethod
    def _mean(vertices: list) -> Vector:
        assert vertices, "vertices list must not be empty"
        return sum(vertices[1:], vertices[0]) / len(vertices)

    def grid(self, cam) -> CanvasGrid:
        frame = CanvasFrame(cam)
        column_coords = [frame.weighted(self.tile_border_fractional_LRTB(row=0, col=col)[0], 0) for col in range(self.num_columns)] + [frame.top_r]
        row_coords = [frame.weighted(0, self.tile_border_fractional_LRTB(row=row, col=0)[2]) for row in range(self.num_rows)] + [frame.bot_l]
        return CanvasGrid(frame=frame,
                          column_coords=column_coords,
                          row_coords=row_coords)


class CanvasFrame:
    bot_l: Vector
    bot_r: Vector
    top_l: Vector
    top_r: Vector

    def __init__(self, cam):
        cam_verts = cam.data.view_frame(scene=bpy.context.scene)  # with scene keyword, this shrinks shorter dimension to fit resolution
        cam_center = Canvas._mean(cam_verts)
        assert len(cam_verts) == 4
        self.bot_l, = [v for v in cam_verts if v[0] < cam_center[0] and v[1] < cam_center[1]]
        self.bot_r, = [v for v in cam_verts if v[0] > cam_center[0] and v[1] < cam_center[1]]
        self.top_l, = [v for v in cam_verts if v[0] < cam_center[0] and v[1] > cam_center[1]]
        self.top_r, = [v for v in cam_verts if v[0] > cam_center[0] and v[1] > cam_center[1]]

    def weighted(self, sx, sy) -> Vector:
        return ((self.top_l * (1-sy) + self.bot_l * sy) * (1-sx) +
                (self.top_r * (1-sy) + self.bot_r * sy) * sx)

    def tile_border_absolute_LRTB(self, canvas: Canvas, row: int, col: int) -> (float, float, float, float):
        l, r, t, b = canvas.tile_border_fractional_LRTB(row=row, col=col)
        tile_top_l = self.weighted(l, t)
        tile_bot_r = self.weighted(r, b)
        return tile_top_l[0], tile_bot_r[0], tile_top_l[1], tile_bot_r[1]


@dataclass
class CanvasGrid:
    frame: CanvasFrame
    column_coords: list[Vector]  # arbitrary points on the grid lines (num_columns + 1), in cam coordinates
    row_coords: list[Vector]  # arbitrary points on the grid lines (num_rows + 1), in cam coordinates

    def is_point_in_tile(self, v: Vector, row: int, col: int) -> bool:
        # TODO convert v to cam coordinates?
        x0, x1 = [c[0] for c in self.column_coords[col:col+2]]
        y0, y1 = [c[1] for c in self.row_coords[row:row+2]]
        return x0 <= v[0] and v[0] <= x1 and y0 >= v[1] and v[1] >= y1
