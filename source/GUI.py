from .Enums import *
from .Rig import *
from .LOD import *


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


class B4BRender(bpy.types.Operator):
    bl_idname = Operators.RENDER.value[0]
    bl_label = "Render all views & rotations"

    def execute(self, context):
        if context.scene.group_id != "default":
            group = context.scene.group_id
        for v in View:
            for z in Zoom:
                Rig.setup(v, z)
                Renderer.generate_output(v, z, group)

        return {"FINISHED"}


class B4BPreview(bpy.types.Operator):
    bl_idname = Operators.PREVIEW.value[0]
    bl_label = "Preview"

    def execute(self, context):
        v = View[context.window_manager.interface_vars.rotation]
        z = Zoom[context.window_manager.interface_vars.zoom]
        Rig.setup(v, z)
        # q: pass the context to the renderer? or just grab it from internals..
        Renderer.generate_preview(z)
        return {'FINISHED'}


class B4BLODExport(bpy.types.Operator):
    bl_idname = Operators.LOD_EXPORT.value[0]
    bl_label = "LODExport"

    def execute(self, context):
        LOD.export()
        return {'FINISHED'}


class B4BLODAdd(bpy.types.Operator):
    bl_idname = Operators.LOD_FIT.value[0]
    bl_label = "LOD fit"

    def execute(self, context):
        Rig.lod_fit()
        return {'FINISHED'}


class B4BLODDelete(bpy.types.Operator):
    bl_idname = Operators.LOD_DELETE.value[0]
    bl_label = "LODDelete"

    def execute(self, context):
        Rig.lod_delete()
        return {'FINISHED'}


class B4BSunDelete(bpy.types.Operator):
    bl_idname = Operators.SUN_DELETE.value[0]
    bl_label = "SunDelete"

    def execute(self, context):
        Sun.delete_from_scene()
        return {'FINISHED'}


class B4BSunAdd(bpy.types.Operator):
    bl_idname = Operators.SUN_ADD.value[0]
    bl_label = "SunAdd"

    def execute(self, context):
        Sun.add_to_scene()
        return {'FINISHED'}


class B4BCamAdd(bpy.types.Operator):
    bl_idname = Operators.CAM_ADD.value[0]
    bl_label = "CamAdd"

    def execute(self, context):
        Camera.add_to_scene()
        return {'FINISHED'}


class B4BCamDelete(bpy.types.Operator):
    bl_idname = Operators.CAM_DELETE.value[0]
    bl_label = "CamDelete"

    def execute(self, context):
        Camera.delete_from_scene()
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
        # Create a simple row.
        layout.label(text="Rotation:")
        rot = layout.row()
        rot.prop(context.window_manager.interface_vars, 'rotation', expand=True)
        layout.label(text="Zoom:")
        zoom = layout.row()
        zoom.prop(context.window_manager.interface_vars, 'zoom', expand=True)

        self.layout.operator(Operators.PREVIEW.value[0], text="Preview")

        layout.label(text="LOD")
        lod = layout.row(align=True)
        lod.operator(Operators.LOD_FIT.value[0], text="Fit")
        lod.operator(Operators.LOD_DELETE.value[0], text="Delete")
        lod.operator(Operators.LOD_EXPORT.value[0], text="Export .3DS")

        layout.label(text="Camera")
        cam = layout.row(align=True)
        cam.operator(Operators.CAM_ADD.value[0], text="Add")
        cam.operator(Operators.CAM_DELETE.value[0], text="Delete")

        layout.label(text="Sun")
        sun = layout.row(align=True)
        sun.operator(Operators.SUN_ADD.value[0], text="Add")
        sun.operator(Operators.SUN_DELETE.value[0], text="Delete")

        layout.label(text="Render")
        render = layout.row()
        render.prop(context.scene, "group_id")
        self.layout.operator(Operators.RENDER.value[0], text="Render all zooms & rotations")
