import bpy
import BAT4Blender

bl_info = {
    "name": "BAT4Blender",
    "category": "Render",
    "blender": (2, 79, 0),
    "author": "vrtxt",
    "version": (0, 0, 1),
}


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
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Create an row where the buttons are aligned to each other.
        layout.label(text=" Aligned Row:")

        row = layout.row(align=True)
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Create two columns, by using a split layout.
        split = layout.split()

        # First column
        col = split.column()
        col.label(text="Column One:")
        col.prop(scene, "frame_end")
        col.prop(scene, "frame_start")

        # Second column, aligned
        col = split.column(align=True)
        col.label(text="Column Two:")
        col.prop(scene, "frame_start")
        col.prop(scene, "frame_end")

        # Big render button
        layout.label(text="Big Button:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("render.render")

        # Different sizes in a row
        layout.label(text="Different button sizes:")
        row = layout.row(align=True)
        row.operator("render.render")

        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("render.render")

        row.operator("render.render")


def register():
    print("ello")
    bpy.utils.register_class(LayoutDemoPanel)
    bpy.utils.register_class(BAT4Blender.Config)
    print(BAT4Blender.Config.class_test_function())
    # bpy.utils.register_class(GUI_Button_Sun)
    # bpy.utils.register_class(GUI_Button_Render)
    # bpy.utils.register_class(GUI_Button_Cameras)


def unregister():
    # for obj in bpy.context.scene.objects:
    #     if obj.type == "LIGHT" or obj.type == "CAMERA":
    #         #  need to check for actual sun lights. . otherwise all scene lighting will be removed
    #         bpy.data.objects.remove(obj)
    print("goodbye")
    bpy.utils.unregister_class(BAT4Blender)
    bpy.utils.unregister_class(LayoutDemoPanel)
    # bpy.utils.unregister_class(GUI_Button_Sun)
    # bpy.utils.unregister_class(GUI_Button_Render)
    # bpy.utils.unregister_class(GUI_Button_Cameras)

#
# if __name__ == "__main__":
#     register()
