
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
from os import path
from . moduls.operators.registrator import OPERATORS_FOR_REGISTRATION
from . moduls.globalParams import CLMBGlobalParams
from . moduls.utils.internal import CLMBInternal
from . moduls.utils.utils import Log, Utils
from . moduls.utils.fs import fs
from . moduls.utils.internal import CLMBAttribute
from . moduls.utils.keys import Key

CLASSES    = OPERATORS_FOR_REGISTRATION
ADDONS     = []
ATTRIBUTES = []
HANDLERS   = []
TIMERS     = []

rightHandMenusNamesList = []

# Loading addon from curent addons folder ==================================================
for file in CLMBInternal.scanAddonsFolder():
    fileFull = CLMBGlobalParams.ADDONS_FOLDER + file
    file = file[:-3]

    spec = importlib.util.spec_from_file_location(file, fileFull)
    if not spec:
        continue
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    if CLMBInternal.isCLUMBAddon(foo.ADDON):
        foo.ADDON.path =  path.split(fileFull)[0]
        ADDONS.append(foo.ADDON)
#==========================================================================================

# Register Data from addons ===============================================================
for addon in ADDONS:
    if addon.disable:
        continue
    CLASSES    += addon.getClasses()
    ATTRIBUTES += addon.getAtributes()
    HANDLERS   += addon.getHandlers()
    TIMERS     += addon.getTimers()
    if addon.CLMBARightHandUI.__sizeof__() > 48:
        rightHandMenusNamesList.append((addon.name,addon.name,addon.name))
#==========================================================================================

#Settings Conteiner========================================================================
class CLMBSettings(bpy.types.PropertyGroup):
    addon_preference:        bpy.props.IntProperty(options={'HIDDEN'})
    addon_right_hand_select: bpy.props.EnumProperty(items = rightHandMenusNamesList, name = "Addon Setting")
class CLMBSceneConteiner(bpy.types.PropertyGroup):
    settings: bpy.props.PointerProperty( type = CLMBSettings)

CLASSES.append(CLMBSettings)
CLASSES.append(CLMBSceneConteiner)
#==========================================================================================

# Addon Preferences UI ====================================================================
class CLMBAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    def draw(self, context):
        layout = self.layout
        layout.label(text="Addons in CLUMBA:")
        lr = layout.row(align = True)

        # Draw Addons Button List
        for i,addon in enumerate(ADDONS):
            op = lr.operator("clmb.swith_curent_addon", text = addon.name, depress = (i == context.scene.CLMBSceneConteiner.settings.addon_preference) )
            op.number = i
        
        # Draw Addon Preferences
        ## Addon Part
        if len(ADDONS) != 0:
            addonFolder = ADDONS[context.scene.CLMBSceneConteiner.settings.addon_preference].path
            LR = layout.row(align = True)
            LR.label(text=f'Addon path: {addonFolder}')
            openFolder = LR.operator("clmb.open_folder", text = "", icon = "FILEBROWSER")
            openFolder.folderPath = addonFolder
            ADDONS[context.scene.CLMBSceneConteiner.settings.addon_preference].CLMBAPreferencesDraw(layout)

CLASSES.append(CLMBAddonPreferences)
#==========================================================================================

# Addon RightHand menu UI =================================================================
class PANEL_PT_CLMBRightHandUI(bpy.types.Panel):
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_category     = 'CLUMBA'
    bl_label        = 'CLUMBA Addons'

    def draw(self, context):
        layout = self.layout
        if not rightHandMenusNamesList:
            BL = layout.box()
            BLR = BL.row(align = True)
            BLR.label(text="", icon = "QUESTION")
            BLRC = BLR.column(align = True)
            BLRC.label(text="This menu will be available,")
            BLRC.label(text="if at least one addon uses it.")
        else:
            BL = layout.box()
            BL.label(text="Select an addon:", icon = "QUESTION")
            BL.prop(context.scene.CLMBSceneConteiner.settings,"addon_right_hand_select", text = "")
            for addon in ADDONS:
                if addon.name == context.scene.CLMBSceneConteiner.settings.addon_right_hand_select:
                    addon.CLMBARightHandUI(layout)

CLASSES.append(PANEL_PT_CLMBRightHandUI)
#==========================================================================================

if CLMBGlobalParams.DEBUG:
    print(Utils.getSeparatorLine("DEBUG"))
    Log.print(__package__,f'Addons required for registration:')
    for i in ADDONS:
        print(f"\t??? {i}")

    Log.print(__package__,f'This classes required for registration:')
    for i in CLASSES:
        print(f"\t??? {i}")

    Log.print(__package__,f'Attributes required for registration:')
    for i in ATTRIBUTES:
        print(f"\t??? {i}")
        
    Log.print(__package__,f'Handlers required for registration:')
    for i in HANDLERS:
        print(f"\t??? {i}")

    Log.print(__package__,f'Timers required for registration:')
    for i in TIMERS:
        print(f"\t??? {i}")

    Log.print(__package__,f'Keys required for registration:')
    for i in Key.KEY_STORAGE:
        print(f"\t??? {i}")

    print(Utils.getSeparatorLine())


def register():
    for key in Key.KEY_STORAGE.values():
        key.registrate()

    for clss in CLASSES:
        bpy.utils.register_class(clss)
    bpy.types.Scene.CLMBSceneConteiner = bpy.props.PointerProperty(type=CLMBSceneConteiner)
    for atr in ATTRIBUTES:
        atr.registrate()
    for hdlr in HANDLERS:
        hdlr.registrate()
    for hdlr in TIMERS:
        hdlr.registrate()


def unregister():
    
    Key.globalUnregistrate()

    for hdlr in TIMERS:
        hdlr.unRegistrate()
    for clss in CLASSES:
        bpy.utils.unregister_class(clss)
    for atr in ATTRIBUTES:
        atr.unRegistrate()
    for hdlr in HANDLERS:
        hdlr.unRegistrate()

    del bpy.types.Scene.CLMBSceneConteiner