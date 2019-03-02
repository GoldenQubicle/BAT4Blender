import bpy

from .Enums import Rotation
from .Camera import gui_ops_camera


class InterfaceVars(bpy.types.PropertyGroup):
    # (unique identifier, property name, property description, icon identifier, number)
    angles = bpy.props.EnumProperty(
        items=[
            (Rotation.NORTH.name, Rotation.NORTH.name, 'North view', '', Rotation.NORTH.value),
            ('30', '30', '30', '', 1),
            ('60', '60', '60', '', 2),
            ('90', '90', '90', '', 3),
        ],
        default=Rotation.NORTH.name
    )


class Rotations(bpy.types.Operator):
    bl_idname = "object.rotation"
    bl_label = "Rotate"

    def execute(self, context):
        # rotationvalue = int(context.window_manager.interface_vars.angles)
        gui_ops_camera(1)
        print("this does work right?!")


class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Layout Demo"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # Create a simple row.
        layout.label(text=" Simple Row:")
        row = layout.row()
        row.prop(context.window_manager.interface_vars, 'angles', expand=True)
        self.layout.operator("object.rotation", text="Rotate")
        # the self layout needs to be 'preview', with a single operator defined!

        # row = layout.row()
        # row.prop(scene, "frame_start")
        # row.prop(scene, "frame_end")
        #
        # # Create an row where the buttons are aligned to each other.
        # layout.label(text=" Aligned Row:")
        #
        # row = layout.row(align=True)
        # row.prop(scene, "frame_start")
        # row.prop(scene, "frame_end")
        #
        # # Create two columns, by using a split layout.
        # split = layout.split()
        #
        # # First column
        # col = split.column()
        # col.label(text="Column One:")
        # col.prop(scene, "frame_end")
        # col.prop(scene, "frame_start")
        #
        # # Second column, aligned
        # col = split.column(align=True)
        # col.label(text="Column Two:")
        # col.prop(scene, "frame_start")
        # col.prop(scene, "frame_end")
        #
        # # Big render button
        # layout.label(text="Big Button:")
        # row = layout.row()
        # row.scale_y = 3.0
        # row.operator("render.render")
        #
        # # Different sizes in a row
        # layout.label(text="Different button sizes:")
        # row = layout.row(align=True)
        # row.operator("render.render")
        #
        # sub = row.row()
        # sub.scale_x = 2.0
        # sub.operator("render.render")
        #
        # row.operator("render.render")

# debug
# def register():
#     bpy.utils.register_class(LayoutDemoPanel)
#     bpy.utils.register_class(Rotations)
#     bpy.utils.register_class(InterfaceVars)
#     bpy.utils.register_class(Zoom)
#     bpy.utils.register_class(Rotation)
#     bpy.types.WindowManager.interface_vars = bpy.props.PointerProperty(type=InterfaceVars)
#
#
# if __name__ == "__main__":
#     register()
