#CLUMBA

import bpy
#from ..moduls.utils.log import *


class main:
    name = "ExempleAddon"
    CLMBDisable = False
    CLMBVersion = "0.1.0"
    CLMBClassesForRegistration = []

    # Test Class ====================================================
    class ExempleAddon(bpy.types.Operator):
        bl_idname = "object.exemple_addon"
        bl_label = bl_idname

        def execute(self, context):
            #CLMBPrint(self.bl_idname, "LOL", showInBlender=True)
            return {'FINISHED'}

    CLMBClassesForRegistration.append(ExempleAddon)
    #====================================================================

    # Addon Settings ====================================================
    def addonPreferencesDraw(layout):
        layout.operator("object.exemple_addon")
    #====================================================================
