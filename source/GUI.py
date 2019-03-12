import bpy

from .Enums import View, Zoom, Operators
from .Camera import gui_ops_camera
from .Sun import gui_ops_sun
from .LOD import gui_ops_lod, gui_ops_lod_export
from .Renderer import gui_ops_render
from .Rig import *


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
        for z in Zoom:
            for v in View:
                print((z, v))
                gui_ops_camera(v, z)
                gui_ops_sun(v)
                gui_ops_lod()
                gui_ops_render(z, v, True)
        return {"FINISHED"}


class B4BPreview(bpy.types.Operator):
    bl_idname = Operators.PREVIEW.value[0]
    bl_label = "Preview"

    def execute(self, context):
        v = View[context.window_manager.interface_vars.rotation]
        z = Zoom[context.window_manager.interface_vars.zoom]
        # gui_ops_camera(v, z)
        # gui_ops_sun(v)
        # gui_ops_lod()
        # gui_ops_render(z, v, False)
        Rig.preview()

        # call gui_ops_LOD ? or just check if present and add if not
        # call gui_ops_render -- will this cause ui freezing . . may want to register a callback of sorts?
        # print("sending")
        # print((v,z))
        return {'FINISHED'}


class B4BLODExport(bpy.types.Operator):
    bl_idname = Operators.LOD_EXPORT.value[0]
    bl_label = "LODExport"

    def execute(self, context):
        gui_ops_lod_export()
        return {'FINISHED'}


class B4BLODAdd(bpy.types.Operator):
    bl_idname = Operators.LOD_ADD.value[0]
    bl_label = "LOD Add"

    def execute(self, context):
        return {'FINISHED'}


class B4BLODDelete(bpy.types.Operator):
    bl_idname = Operators.LOD_DELETE.value[0]
    bl_label = "LODDelete"

    def execute(self, context):
        return {'FINISHED'}


class B4BSunDelete(bpy.types.Operator):
    bl_idname = Operators.SUN_DELETE.value[0]
    bl_label = "SunDelete"

    def execute(self, context):
        return {'FINISHED'}


class B4BSunAdd(bpy.types.Operator):
    bl_idname = Operators.SUN_ADD.value[0]
    bl_label = "SunAdd"

    def execute(self, context):
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
        lod.operator(Operators.LOD_ADD.value[0], text="Add")
        lod.operator(Operators.LOD_DELETE.value[0], text="Delete")
        lod.operator(Operators.LOD_EXPORT.value[0], text="Export .3DS")

        layout.label(text="Sun")
        sun = layout.row(align=True)
        sun.operator(Operators.SUN_ADD.value[0], text="Add Sun")
        sun.operator(Operators.SUN_DELETE.value[0], text="Delete Sun")

        layout.label(text="Render")
        self.layout.operator(Operators.RENDER.value[0], text="Render all zooms & rotations")
