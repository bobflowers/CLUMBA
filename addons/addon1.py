#CLUMBA

import bpy

class main:
    name = "addon1"
    CLMBDisable = False
    CLMBVersion = "0.1.0"
    CLMBClassesForRegistration = [] 

    # Test Class ====================================================
    class testCl1(bpy.types.Operator):
        bl_idname = "object.test_cl1"
        bl_label = bl_idname

        def execute(self, context):
            self.report({'INFO'}, self.bl_idname)
            return {'FINISHED'}

    CLMBClassesForRegistration.append(testCl1)
    #====================================================================

    # Addon Settings ====================================================
    def addonPreferencesDraw(layout):
        layout.operator("object.test_cl1")
    #====================================================================
