import bpy
import os

tid_fsh = "7ab50e44"
tid_s3d = "5ad0e817"


def instance_id(z, v, count):
    t = 0  # default to day render
    # This mapping should allow for more than 16 anim groups (for slicing of large BAT models).
    # Available bits for sliced tile IDs:
    # digit 8: 4 bits
    # digit 7: 2 bits (2 bits rotation)
    # digit 6: 1 bit (3 bits zoom)
    # digit 5: (1 bit nightlight) 3 bits
    assert count >= 0 and count < (1 << (4 + 2 + 1 + 3)), "This building is huge! It's just not going to work!"
    offset = ((count & 0x0380) << (3 + 2)) | ((count & 0x0040) << (3 + 2)) | ((count & 0x0030) << 2) | (count & 0x000f)
    iid = 0x30000 + t * 0x10000 + z * 0x100 + v * 0x10 + offset
    return iid


def tgi_formatter(gid, z, v, count, is_model=False):
    iid = instance_id(z, v, count)
    return f"{tid_s3d if is_model else tid_fsh}_{gid}_{iid:08x}"


def get_relative_path_for(fn):
    fp = bpy.data.filepath
    folder = os.path.dirname(fp)
    path = os.path.join(folder, fn)
    return path


def translate(value, left_min, left_max, right_min, right_max):
    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - left_min) / float(left_span)

    # Convert the 0-1 range into a value in the right range.
    return right_min + (value_scaled * right_span)


def clip(value: float, min: float, max: float) -> float:
    return min if value < min else max if value > max else value


def b4b_collection():
    from .Config import COLLECTION_NAME
    if COLLECTION_NAME in bpy.data.collections:
        return bpy.data.collections[COLLECTION_NAME]
    else:
        c = bpy.data.collections.new(COLLECTION_NAME)
        bpy.context.scene.collection.children.link(c)
        return c


def blend_file_name():
    return bpy.path.display_name_from_filepath(bpy.context.blend_data.filepath)
