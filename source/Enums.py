from enum import Enum


class Operators(Enum):
    PREVIEW = "object.b4b_preview",
    RENDER = "object.b4b_render",
    LOD_ADD = "object.b4b_lod_add",
    LOD_EXPORT = "object.b4b_lod_export",
    LOD_FIT = "object.b4b_lod_fit",
    LOD_CUSTOM = "object.b4b_lod_custom",
    LOD_DELETE = "object.b4b_lod_delete",
    SUN_ADD = "object.b4b_sun_add",
    SUN_DELETE = "object.b4b_sun_delete",


class View(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3


class Zoom(Enum):
    ONE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
