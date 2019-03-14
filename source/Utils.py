import bpy
import os


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