import bpy

from .GUI import LayoutDemoPanel, InterfaceVars, Rotations
from .Sun import test

bl_info = {
    "name": "BAT4Blender",
    "category": "Render",
    "blender": (2, 79, 0),
    "author": "vrtxt",
    "version": (0, 0, 2),
}


# note: registering is order dependent! e.g. registering layout before vars will throw errors
def register():
    bpy.utils.register_class(InterfaceVars)
    bpy.types.WindowManager.interface_vars = bpy.props.PointerProperty(type=InterfaceVars)
    bpy.utils.register_class(LayoutDemoPanel)
    bpy.utils.register_class(Rotations)
    test()


def unregister():
    del bpy.types.WindowManager.interface_vars
    bpy.utils.unregister_class(LayoutDemoPanel)
    bpy.utils.unregister_class(InterfaceVars)
    bpy.utils.unregister_class(Rotations)
