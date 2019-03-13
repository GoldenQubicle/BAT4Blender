import bpy
import os


class FileManager:

    @staticmethod
    def get_relative_path_for(fn):
        fp = bpy.data.filepath
        folder = os.path.dirname(fp)
        path = os.path.join(folder, fn)
        return path
