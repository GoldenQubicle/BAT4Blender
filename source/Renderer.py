import bpy_extras
from math import tan, atan
from mathutils import Vector
from .Config import *
from .Utils import *
from .Enums import View, Zoom

# render dimensions need to take view into account
# sd default
render_dimension = [16, 32, 64, 128, 256]


class Renderer:
    @staticmethod
    def generate_output(v, z, gid):

        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.context.scene.render.image_settings.color_mode = 'RGBA'
        # this might be a problem as i suspect the scale factor should be calculated for z5 exclusively
        s_f = Renderer.camera_manouvring(z)

        if s_f > 1:
            # output resolution! not I dont! it's already been handled since I tell blender to crop!
            # HOWEVER this does have an interaction with the dimensions! as images > 256 are split, the rest is fine!
            row = 0
            b = 1 / s_f
            for i in range(0, s_f ** 2):
                col = i % s_f
                min_x = col * b
                max_x = min_x + b
                min_y = row * b
                max_y = min_y + b
                bpy.data.scenes["Scene"].render.use_border = True
                bpy.data.scenes["Scene"].render.use_crop_to_border = True
                bpy.data.scenes["Scene"].render.border_min_x = min_x
                bpy.data.scenes["Scene"].render.border_max_x = max_x
                bpy.data.scenes["Scene"].render.border_min_y = min_y
                bpy.data.scenes["Scene"].render.border_max_y = max_y
                bpy.context.scene.render.filepath = get_relative_path_for("B4B_{}_{}.png".format(col, row))

                bpy.ops.render.render(write_still=True)
                # TODO figure out if the tile is empty
                # if not, write it and increase the no count for the file name!
                # print(col, row)
                # print(min_x, max_x, min_y, max_y)
                if col + 1 == s_f:
                    row += 1
        else:
            filename = tgi(gid, z.value, v.value, 0)
            bpy.context.scene.render.filepath = get_relative_path_for("{}.png".format(filename))
            bpy.ops.render.render(write_still=True)

    @staticmethod
    def generate_preview(zoom):
        Renderer.camera_manouvring(zoom)
        bpy.ops.render.render('INVOKE_DEFAULT', write_still=False)

    @staticmethod
    def camera_manouvring(zoom):
        lod = bpy.data.objects[LOD_NAME]
        cam = bpy.data.objects[CAM_NAME]
        depsgraph = bpy.context.scene.depsgraph
        bpy.context.scene.camera = cam  # apparently invoke default also checks if the scene has a camera..?

        os_lod = Renderer.get_orthographic_scale(depsgraph, cam, lod)
        os_gmax = Renderer.get_orthographic_scale_gmax()  # NOTE using hardcoded defaults! probably not quite correct. .
        s_f = Renderer.get_scale_factor(os_lod, os_gmax)

        os_cam = os_gmax * s_f
        dim = render_dimension[zoom.value] * s_f
        cam.data.ortho_scale = os_cam
        Renderer.offset_camera(cam, lod, dim)
        return s_f

    @staticmethod
    def offset_camera(cam, lod, dim):
        # since the renders can be rectangular assing to x, y
        dim_x = dim
        dim_y = dim
        cam.data.shift_x = 0.0
        cam.data.shift_y = 0.0
        # get the 2d camera view coordinates for the LOD... is this a correct assumption?
        coordinates = [lod.matrix_world * Vector(corner) for corner in lod.bound_box]
        coords_2d = [bpy_extras.object_utils.world_to_camera_view(bpy.context.scene, cam, coord) for coord in
                     coordinates]

        # grab outer left and top vertex in the camera view
        # map their 0..1 range to pixels to determine how far theLOD is from the left and top edges
        c_x = []
        c_y = []

        for c in coords_2d:
            c_x.append(c[0])
            c_y.append(c[1])

        min_x = min(c_x)
        max_y = max(c_y)

        x_left = min_x * dim_x
        y_top = max_y * dim_y
        # print("left x")
        # print(x_left)
        # print("top y")
        # print(y_top)

        # map the pixel values back to a 0..1 range to use as offset
        slop = 2  # keep a 2 pixel distance from edge, can be made variable later for different levels
        x_d = translate(x_left - slop, 0, dim_x, 0.0, 1.0)
        y_d = translate(y_top - (dim_y - slop), 0, dim_y, 0.0, 1.0)
        cam.data.shift_x = x_d
        cam.data.shift_y = y_d

        # TODO check if either right or bottom half render square is empty
        # i.e. does the LOD extend into half of that
        # if so the corresponding render dimension needs to be halved, and then reposition camera again
        # so yeah lets not do this, instead just make sure to write all sections with a correct file name
        # because that way, on convert / import as fsh the 'blank' tiles will just not be applied to the LOD
        # however, this is a bit wasteful as it does limit the render size (i.e. 0..F is simply taken up earlier)
        # also, related, I have no way of checking of part of the model is in the lower right quadrant as the
        # positional check is performed on a vertex basis
        bpy.context.scene.render.resolution_x = dim_x
        bpy.context.scene.render.resolution_y = dim_y

    @staticmethod
    def get_scale_factor(os_lod, os_gmax):
        factor = 1
        while os_lod > os_gmax:
            factor *= 2
            os_gmax *= 2
        return factor

    @staticmethod
    def get_orthographic_scale(dg, cam, lod):
        coordinates = [lod.matrix_world * Vector(corner) for corner in lod.bound_box]
        co_list = []
        for v in coordinates:
            for f in v:
                co_list.append(f)

        return cam.camera_fit_coords(dg, co_list)[1]

    # NOTE currently passing in camera height depending on zoom
    # not sure if that's correct, i.e. perhaps the OS for z5 should be used throughout
    @staticmethod
    def get_orthographic_scale_gmax():
        cam_z = 134.35028  # default location for zoom 5. .
        unit = 16
        targetWidth2 = unit + 8  # unit cube with render slop applied as specified in gmax script
        renderFov = 2 * (atan(targetWidth2 / 190.0))
        return (cam_z + unit / 2) * tan(
            renderFov)  # assuming the gmax camera focus in on lod center height which seems correct
