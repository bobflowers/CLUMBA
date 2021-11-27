
bl_info = {
    'name': 'CLUMBA',
    'author': 'Vladimir Tsvetkov',
    'version': (0, 1, 0),
    'blender': (2, 93, 0),
    #'location': 'View3D > Add > Mesh > New Object',
    'description':'',
    "doc_url": "",
    'category': 'System',
}

import bpy

CLASSES = []

#Settings Conteiner========================================================================

class CMB_SceneConteiner(bpy.types.PropertyGroup):
    #addonPreference: bpy.props.IntProperty(options={'HIDDEN'})
    addon_preference: bpy.props.IntProperty()

CLASSES.append(CMB_SceneConteiner)
#==========================================================================================


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Addon1:
    class testCl1(bpy.types.Operator):
        bl_idname = "object.test_cl1"
        bl_label = bl_idname

        def execute(self, context):
            self.report({'INFO'}, self.bl_idname)
            return {'FINISHED'}
    
    def draw(layout):
        layout.operator("object.test_cl1")

    classes = [testCl1]

class Addon2:
    class testCl2(bpy.types.Operator):
        bl_idname = "object.test_cl2"
        bl_label = bl_idname

        def execute(self, context):
            self.report({'INFO'}, self.bl_idname)
            return {'FINISHED'}
    
    def draw(layout):
        layout.operator("object.test_cl2")

    classes = [testCl2]

class Addon3:
    class testCl3(bpy.types.Operator):
        bl_idname = "object.test_cl3"
        bl_label = bl_idname

        def execute(self, context):
            self.report({'INFO'}, self.bl_idname)
            return {'FINISHED'}
    
    def draw(layout):
        layout.operator("object.test_cl3")

    classes = [testCl3]

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

classesForDraw = [Addon1,Addon2,Addon3]


for addon in classesForDraw:
    CLASSES += addon.classes

class CMB_ChengeCurentAddonLayout(bpy.types.Operator):
    bl_idname = ".cmb_swith_curent_addon"
    bl_label = bl_idname
    bl_option = {"INTERNAL"}

    number: bpy.props.IntProperty()

    def execute(self, context):
        print(self.number)
        context.scene.CMB_SceneConteiner.addon_preference = self.number
        return {'FINISHED'}

class CMB_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    def draw(self, context):
        layout = self.layout
        layout.label(text="Addons in CLUMBA:")

        lr = layout.row(align = True)
        
        for i,addon in enumerate(classesForDraw):
            op = lr.operator(".cmb_swith_curent_addon", text = addon.__name__, depress = (i == context.scene.CMB_SceneConteiner.addon_preference) )
            op.number = i
        
        classesForDraw[context.scene.CMB_SceneConteiner.addon_preference].draw(layout)


CLASSES += [
    CMB_AddonPreferences,
    CMB_ChengeCurentAddonLayout,
]
print(CLASSES)
def register():
    for clss in CLASSES:
        bpy.utils.register_class(clss)
    bpy.types.Scene.CMB_SceneConteiner = bpy.props.PointerProperty(type=CMB_SceneConteiner)
def unregister():
    for clss in CLASSES:
        bpy.utils.unregister_class(clss)
    del bpy.types.Scene.CMB_SceneConteiner

