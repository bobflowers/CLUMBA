
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
import importlib.util
from . moduls.operators.registrator import OPERATORS_FOR_REGISTRATION
from . moduls.globalParametrs import ADDONS_FOLDER, DEBUG
from . moduls.utils.internal import CLMBInternal
from . moduls.utils.log import Log
from . moduls.utils.fs import fs

CLASSES = OPERATORS_FOR_REGISTRATION
ADDONS = []

#Settings Conteiner========================================================================
class CLMBSceneConteiner(bpy.types.PropertyGroup):
    addon_preference: bpy.props.IntProperty(options={'HIDDEN'})
CLASSES.append(CLMBSceneConteiner)
#==========================================================================================

# Loading addon from curent addons folder ==================================================
for file in CLMBInternal.scanAddonsFolder():
    fileFull = ADDONS_FOLDER + file
    file = file[:-3]

    spec = importlib.util.spec_from_file_location(file, fileFull)
    if not spec:
        continue
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    if CLMBInternal.isCLUMBAddon(foo):
        ADDONS.append(foo.main)
#==========================================================================================

# Register Data from addons ===============================================================
for addon in ADDONS:
    CLASSES += addon.CLMBClassesForRegistration
#==========================================================================================

# Addon Preferences Drawer ================================================================
class CLMBAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    def draw(self, context):
        layout = self.layout
        layout.label(text="Addons in CLUMBA:")
        lr = layout.row(align = True)

        # Draw Addons Button List
        for i,addon in enumerate(ADDONS):
            op = lr.operator(".cmb_swith_curent_addon", text = addon.name, depress = (i == context.scene.CLMBSceneConteiner.addon_preference) )
            op.number = i
        
        # Draw Addon Preferences
        ## Addon Part
        if len(ADDONS) != 0:
            ADDONS[context.scene.CLMBSceneConteiner.addon_preference].addonPreferencesDraw(layout)

CLASSES.append(CLMBAddonPreferences)
#==========================================================================================

if DEBUG:
    Log.print(__package__,f'This classes requred for registration:\n{CLASSES}')
    Log.print(__package__,f'Addons has been registered:\n{ADDONS}')

def register():
    for clss in CLASSES:
        bpy.utils.register_class(clss)
    bpy.types.Scene.CLMBSceneConteiner = bpy.props.PointerProperty(type=CLMBSceneConteiner)

def unregister():
    for clss in CLASSES:
        bpy.utils.unregister_class(clss)
    del bpy.types.Scene.CLMBSceneConteiner

