import bpy
from .Enums import View, Zoom
from .Camera import gui_ops_camera
from .Sun import gui_ops_sun
from .LOD import gui_ops_lod
from .Renderer import gui_ops_render


class InterfaceVars(bpy.types.PropertyGroup):
    # (unique identifier, property name, property description, icon identifier, number)
    rotation = bpy.props.EnumProperty(
        items=[
            (View.NORTH.name, 'N', 'North view', '', View.NORTH.value),
            (View.EAST.name, 'E', 'East view', '', View.EAST.value),
            (View.SOUTH.name, 'S', 'South view', '', View.SOUTH.value),
            (View.WEST.name, 'W', 'West view', '', View.WEST.value)
        ],
        default=View.NORTH.name
    )

    zoom = bpy.props.EnumProperty(
        items=[
            (Zoom.ONE.name, '1', 'zoom 1', '', Zoom.ONE.value),
            (Zoom.TWO.name, '2', 'zoom 2', '', Zoom.TWO.value),
            (Zoom.THREE.name, '3', 'zoom 3', '', Zoom.THREE.value),
            (Zoom.FOUR.name, '4', 'zoom 4', '', Zoom.FOUR.value),
            (Zoom.FIVE.name, '5', 'zoom 5', '', Zoom.FIVE.value),
        ],
        default=Zoom.FIVE.name
    )


class PreviewOp(bpy.types.Operator):
    bl_idname = "object.preview"
    bl_label = "Preview"

    def execute(self, context):
        v = View[context.window_manager.interface_vars.rotation]
        z = Zoom[context.window_manager.interface_vars.zoom]
        gui_ops_camera(v, z)
        gui_ops_sun(v)
        gui_ops_lod()
        gui_ops_render(z)

        # call gui_ops_LOD ? or just check if present and add if not
        # call gui_ops_render -- will this cause ui freezing . . may want to register a callback of sorts?
        # print("sending")
        # print((v,z))
        return {'FINISHED'}


class MainPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "BAT4Blender"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # Create a simple row.
        layout.label(text="Rotation:")
        rot = layout.row()
        rot.prop(context.window_manager.interface_vars, 'rotation', expand=True)
        layout.label(text="Zoom:")
        zoom = layout.row()
        zoom.prop(context.window_manager.interface_vars, 'zoom', expand=True)

        self.layout.operator("object.preview", text="Preview")
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
