import bpy
from .Config import *
from .LOD import *
from .FileManager import *


class Rig:
    @staticmethod
    def preview():
        # print("debug script check")
        if CAM_NAME not in bpy.data.objects \
                or SUN_NAME not in bpy.data.objects \
                or LOD_NAME not in bpy.data.objects:
            print("yooo")

    @staticmethod
    def lod_fit():
        Rig.lod_delete()
        LOD.fit_new()

    @staticmethod
    def lod_export():
        if LOD_NAME in bpy.data.objects:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[LOD_NAME].select = True
            bpy.ops.export_scene.autodesk_3ds(
                filepath="{}.3ds".format(FileManager.get_relative_path_for(LOD_NAME)),
                check_existing=False,
                axis_forward='Y',
                axis_up='Z',
                use_selection=True
            )
            bpy.data.objects[LOD_NAME].select = False

        else:
            print("there is no LOD to export!")

    @staticmethod
    def lod_delete():
        if LOD_NAME in bpy.data.objects:
            ob = bpy.data.objects[LOD_NAME]
            bpy.data.meshes.remove(ob.data)
            bpy.data.objects.remove(ob, do_unlink=True, do_ui_user=True)
        bpy.context.scene.update()
