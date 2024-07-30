import bpy
from .GUI import InterfaceVars, MainPanel
from . import GUI_ops

bl_info = {
    "name": "BAT4Blender",
    "category": "Render",
    "blender": (3, 2, 0),  # minimum Blender version
    "author": "vrtxt",
    "version": (0, 0, 3),
}


# note: registering is order dependent! i.e. registering layout before vars will throw errors
def register():
    print("Registering addon BAT4Blender.")
    bpy.utils.register_class(InterfaceVars)
    bpy.types.WindowManager.interface_vars = bpy.props.PointerProperty(type=InterfaceVars)
    bpy.types.Scene.group_id = bpy.props.StringProperty(
            name="Group ID",
            description="the Group ID as provided by gmax",
            default="")
    bpy.types.Scene.b4b_hd = bpy.props.EnumProperty(
        items=[
            ('SD', 'SD', "standard definition", '', 0),
            ('HD', 'HD', "high definition (doubles zoom 5 resolution)", '', 1),
        ],
        default='SD',
    )

    bpy.utils.register_class(MainPanel)
    bpy.utils.register_class(GUI_ops.B4BPreview)
    bpy.utils.register_class(GUI_ops.B4BRender)
    bpy.utils.register_class(GUI_ops.B4BLODExport)
    bpy.utils.register_class(GUI_ops.B4BLODAdd)
    bpy.utils.register_class(GUI_ops.B4BLODDelete)
    bpy.utils.register_class(GUI_ops.B4BSunAdd)
    bpy.utils.register_class(GUI_ops.B4BSunDelete)
    bpy.utils.register_class(GUI_ops.B4BCamAdd)
    bpy.utils.register_class(GUI_ops.B4BCamDelete)
    bpy.utils.register_class(GUI_ops.B4BGidRandomize)
    bpy.utils.register_class(GUI_ops.OkOperator)
    bpy.utils.register_class(GUI_ops.MessageOperator)


def unregister():
    print("Unregistering addon BAT4Blender.")
    del bpy.types.WindowManager.interface_vars
    del bpy.types.Scene.group_id
    del bpy.types.Scene.b4b_hd
    bpy.utils.unregister_class(InterfaceVars)
    bpy.utils.unregister_class(MainPanel)
    bpy.utils.unregister_class(GUI_ops.B4BPreview)
    bpy.utils.unregister_class(GUI_ops.B4BRender)
    bpy.utils.unregister_class(GUI_ops.B4BLODExport)
    bpy.utils.unregister_class(GUI_ops.B4BLODAdd)
    bpy.utils.unregister_class(GUI_ops.B4BLODDelete)
    bpy.utils.unregister_class(GUI_ops.B4BSunAdd)
    bpy.utils.unregister_class(GUI_ops.B4BSunDelete)
    bpy.utils.unregister_class(GUI_ops.B4BCamAdd)
    bpy.utils.unregister_class(GUI_ops.B4BCamDelete)
    bpy.utils.unregister_class(GUI_ops.B4BGidRandomize)
    bpy.utils.unregister_class(GUI_ops.OkOperator)
    bpy.utils.unregister_class(GUI_ops.MessageOperator)
