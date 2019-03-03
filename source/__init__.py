import bpy

from .GUI import MainPanel, InterfaceVars, PreviewOp
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
    bpy.utils.register_class(MainPanel)
    bpy.utils.register_class(PreviewOp)
    test()


def unregister():
    bpy.utils.unregister_class(InterfaceVars)
    del bpy.types.WindowManager.interface_vars
    bpy.utils.unregister_class(MainPanel)
    bpy.utils.unregister_class(PreviewOp)
