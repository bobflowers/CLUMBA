#CLUMBA

import bpy

class main:
    name = "test2"
    CLMBDisable = False
    CLMBVersion = "0.1.0"
    CLMBClassesForRegistration = []

    # Test Class ====================================================
    class ExempleAddon2(bpy.types.Operator):
        bl_idname = "object.exemple_addon2"
        bl_label = bl_idname

        def execute(self, context):
            #CLMBPrint(self.bl_idname, "LOL", showInBlender=True)
            return {'FINISHED'}

    CLMBClassesForRegistration.append(ExempleAddon2)
    #====================================================================

    # Addon Settings ====================================================
    def addonPreferencesDraw(layout):
        layout.operator("object.exemple_addon2")
    #====================================================================
