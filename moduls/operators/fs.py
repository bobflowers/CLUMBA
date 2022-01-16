# This Operators for File System CLUMBA used
import re
import bpy
import os
import subprocess
from ..utils.log import Log
from ..globalParametrs import SYSTEM_NAME


OPERATORS_FS = []

class CLMBOpenFolder(bpy.types.Operator):
    bl_label = "Open Folder"
    bl_idname = "clmb.open_folder"
    bl_option = {"INTERNAL"}

    folderPath: bpy.props.StringProperty(subtype='DIR_PATH')

    def execute(self, context):
        if not os.path.isdir(self.folderPath):
            self.report({"ERROR"}, f"Folder {self.folderPath} doesn't exists")
            return {"CANCELLED"}

        # Diferent way to open folder in other OS
        if SYSTEM_NAME == "Windows":
            os.startfile(self.folderPath)
        else:
            subprocess.Popen(["open", self.folderPath])
        return {'FINISHED'}

OPERATORS_FS.append(CLMBOpenFolder)