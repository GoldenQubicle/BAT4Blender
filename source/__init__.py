import bpy

from .GUI import LayoutDemoPanel
from .Sun import test

bl_info = {
    "name": "BAT4Blender",
    "category": "Render",
    "blender": (2, 79, 0),
    "author": "vrtxt",
    "version": (0, 0, 2),
}


def register():
    bpy.utils.register_class(LayoutDemoPanel)
    test()


def unregister():
    bpy.utils.unregister_class(LayoutDemoPanel)
