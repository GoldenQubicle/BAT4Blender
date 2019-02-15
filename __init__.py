import bpy
from BAT4Blender import Config

bl_info = {
    "name": "BAT4Blender",
    "category": "Render",
    "blender": (2, 80, 0),
    "author": "vrtxt",
    "version": (0, 0, 1),
}


def register():
    bpy.utils.register_class(GUIPanel)
    bpy.utils.register_class(GUI_Button_Sun)
    bpy.utils.register_class(GUI_Button_Render)
    bpy.utils.register_class(GUI_Button_Cameras)
    bpy.utils.register_class(Config)


def unregister():
    for obj in bpy.context.scene.objects:
        if obj.type == "LIGHT" or obj.type == "CAMERA":
            #  need to check for actual sun lights. . otherwise all scene lighting will be removed
            bpy.data.objects.remove(obj)

    bpy.utils.unregister_class(GUIPanel)
    bpy.utils.unregister_class(GUI_Button_Sun)
    bpy.utils.unregister_class(GUI_Button_Render)
    bpy.utils.unregister_class(GUI_Button_Cameras)
    bpy.utils.unregister_class(Config)


class GUIPanel(bpy.types.Panel):
    bl_idname = "uipanel"
    bl_label = "BAT4Blender"
    bl_space_type = "PROPERTIES"
    bl_screen = "BAT"
    bl_region_type = "WINDOW"
    bl_context = "output"

    def draw(self, context):
        self.layout.operator("object.light", icon='LIGHT_SUN', text="Add Sun")
        self.layout.operator("object.camrig", icon='VIEW_CAMERA', text="Add Camera Rig")
        self.layout.operator("object.render", icon='RENDER_RESULT', text='Render Cameras (not zooms!) ')


class GUI_Button_Render(bpy.types.Operator):
    bl_label = "output"
    bl_idname = "object.render"
    bl_description = "Render camera 5 view"

    def invoke(self, context, event):
        # add check if camera exists beforehand..
        for i in range(0, 4):
            cam_name = '{0}{1}'.format('cam_z', i + 1)

            context.scene.camera = bpy.data.objects[cam_name]
            context.scene.render.engine = "BLENDER_EEVEE"  # CYCLES
            context.scene.render.alpha_mode = 'TRANSPARENT'
            context.scene.render.resolution_x = 256
            context.scene.render.resolution_y = 256
            context.scene.render.image_settings.file_format = "PNG"
            context.scene.render.image_settings.color_mode = "RGBA"
            context.scene.render.image_settings.color_depth = "16"
            context.scene.render.filepath = '{0}{1}{2}'.format("C:\\Users\\Erik\\Documents\\Blender\\", cam_name, ".png" )
            # bpy.ops.render.render('INVOKE_DEFAULT',
            #                       write_still=True)  # invoke brings up render window, write_still toggles output
            bpy.ops.render.render(write_still=True)

        return {"FINISHED"}


class GUI_Button_Sun(bpy.types.Operator):
    bl_label = "sun"
    bl_idname = "object.light"
    bl_description = "Add sun to scene"

    def invoke(self, context, event):
        sun = bpy.data.lights.new("Sun", "SUN")  # name, type
        sun_ob = bpy.data.objects.new("Sun", sun)
        sun_ob.rotation_mode = "XYZ"
        sun_ob.location = Config.sun_loc
        sun_ob.rotation_euler = Config.sun_rot
        context.scene.collection.objects.link(sun_ob)
        return {"FINISHED"}


class GUI_Button_Cameras(bpy.types.Operator):
    bl_label = "Camera Rig"
    bl_idname = "object.camrig"
    bl_description = "Add Camera Rig"

    def invoke(self, context, event):
        for i in range(0, 4):
            cam_name = '{0}{1}'.format('cam_z', i+1)
            cam = bpy.data.cameras.new(cam_name)
            cam_ob = bpy.data.objects.new(cam_name, cam)
            cam_ob.data.type = "ORTHO"
            cam_ob.rotation_mode = "XYZ"
            cam_ob.location = Config.cam_location[i]
            cam_ob.rotation_euler = Config.cam_rotation[i]
            context.scene.collection.objects.link(cam_ob)
        return {"FINISHED"}


# class GUI_Button_Camera5(bpy.types.Operator):
#     bl_label = "Camera5"
#     bl_idname = "object.cam5"
#     bl_description = "Add camera for zoom 5"
#
#     def invoke(self, context, event):
#         print(Cam.loc_z456)
#         camz5 = bpy.data.cameras.new("camz5")
#         camz5_ob = bpy.data.objects.new("camz5", camz5)
#         camz5_ob.data.type = "ORTHO"
#         camz5_ob.rotation_mode = "XYZ"
#         camz5_ob.location = Cam.loc_z456
#         camz5_ob.rotation_euler[0] = radians(Cam.angles[0])
#         camz5_ob.rotation_euler[1] = 0.0
#         camz5_ob.rotation_euler[2] = radians(Cam.angles[4])
#         # camz5_ob.location[0] = 51.41363
#         # camz5_ob.location[1] = -124.123474
#         # camz5_ob.location[2] = 134.35028
#
#         # camz5_ob.rotation_euler[0] = 0.785398
#         # camz5_ob.rotation_euler[1] = 0.0
#         # camz5_ob.rotation_euler[2] = 0.392699
#         camz5_ob.data.ortho_scale = 37.0
#         camz5_ob.data.shift_x = 0.0
#         camz5_ob.data.shift_y = 0.0
#         context.scene.collection.objects.link(camz5_ob)
#         return {"FINISHED"}
