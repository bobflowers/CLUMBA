# This Operators for Internal CLUMBA used
import bpy
from ..utils.log import Log
OPERATORS_INTERNAL = []

class CLMBChengeCurentAddonLayout(bpy.types.Operator):
    bl_idname = "clmb.swith_curent_addon"
    bl_label = bl_idname
    bl_option = {"INTERNAL"}

    number: bpy.props.IntProperty()

    def execute(self, context):
        context.scene.CLMBSceneConteiner.settings.addon_preference = self.number
        return {'FINISHED'}

OPERATORS_INTERNAL.append(CLMBChengeCurentAddonLayout)