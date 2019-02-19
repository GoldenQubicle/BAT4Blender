import bpy

CAM_NAME = "cam_654"
loc_z456 = (51.41363, -124.123474, 134.35028)
angle_z456 = (0.7853982, 0, 0.3926991)


# pass an orientation & zoom flag here. . ? and set camera specific for each view -> would need lot of config values
# better grab the camera object and translate & rotate according to flags..?

# q: how to figure out the correct scale . .
# - figure out by lod dimension. .?
# - figure out by checking of lod is in camera view. .?
# probably will need to do both

def rotate_camera(name, rotation):
    if bpy.data.objects.get(name) is not None:
        print("camera exist")
        # do stuff. .
    else:
        print("camera has not been added yet")


def set_camera(location, angles):
    cam = bpy.data.cameras.new(CAM_NAME)
    cam_ob = bpy.data.objects.new(CAM_NAME, cam)
    cam_ob.data.type = "ORTHO"
    cam_ob.rotation_mode = "XYZ"
    cam_ob.location = location
    cam_ob.rotation_euler = angles
    bpy.context.scene.collection.objects.link(cam_ob)


rotate_camera(CAM_NAME)

for ob in bpy.data.objects:
    if ob.name == CAM_NAME:
        bpy.data.objects.remove(ob, do_unlink=True)

set_camera(loc_z456, angle_z456)

rotate_camera(CAM_NAME)
