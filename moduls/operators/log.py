import bpy

OPERATORS_LOG = []

class CLMBChengeCurentAddonLayout(bpy.types.Operator):
    bl_idname = "info.log_to_info"
    bl_label = bl_idname
    #bl_option = {"INTERNAL"}

    text: bpy.props.StringProperty()
    messegeType: bpy.props.StringProperty(default = "")

    def execute(self, context):
        if self.messegeType == "ERROR":
            self.report({'ERROR'}, self.text)
        elif self.messegeType == "WARNING":
            self.report({'WARNING'}, self.text)
        else:
            self.report({'INFO'}, self.text)

        return {'FINISHED'}

OPERATORS_LOG.append(CLMBChengeCurentAddonLayout)