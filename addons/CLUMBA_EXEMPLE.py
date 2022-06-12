#CLUMBA <-- It's teg for mark this file like addon init file 

import bpy

from CLUMBA.moduls.utils.internal  import CLMBAttribute, CLMBAddon, CLMBHandler, CLMBTimer
from CLUMBA.moduls.globalParams import CLMBGlobalParams
from CLUMBA.moduls.utils.scene     import Scene
from CLUMBA.moduls.utils.keys      import Key
from CLUMBA.moduls.utils.utils     import Log



# Initiate an Addon ============================================
ADDON = CLMBAddon( name =  "Exemple Addon", version = "0.1.0" )   # <-- Create an Instance of addon
#===============================================================  # !!!WARNING!!! The instance should name "ADDON". Because Dynamic Loader using it to load addon

# Initiate an Addon ============================================
ADDON.disable = not CLMBGlobalParams.DEBUG
#===============================================================

# Test Operator ================================================
class ExempleAddon(bpy.types.Operator):
    bl_idname = "object.exemple_addon"
    bl_label = "TEST"

    def execute(self, context):
        Log.print(self,"Exemple Adon",Log.LogType.INFO)
        self.report({'INFO'}, "Exemple Adon")
        return {'FINISHED'}

ADDON.appendClass(ExempleAddon) # <-- Add operator to queue for registration 
#===============================================================

# Key Registrator ==============================================
key = Key(ExempleAddon,"F", ctrl=True) # <-- Create a Key Map 
#===============================================================

# Addon Attributes =============================================
class ExemplePropertyGroup(bpy.types.PropertyGroup):
    exempleInt:        bpy.props.IntProperty()
    exempleString:     bpy.props.StringProperty(default="Exemple Text")
    savedCount:        bpy.props.IntProperty()

ADDON.appendClass(ExemplePropertyGroup)

ADDON.appendAtributes( CLMBAttribute( bpy.types, "Scene", "CLMBA_Exemple", bpy.props.BoolProperty(name="Exemple", default = True) ) )
ADDON.appendAtributes( CLMBAttribute( bpy.types, "Scene", "CLMBA_ExemplePropertyGroup", bpy.props.PointerProperty( type = ExemplePropertyGroup) ) )
#===============================================================

# Handler Registrator ==========================================
def handlerFunction(scene):
    scene.CLMBA_ExemplePropertyGroup.exempleInt += 1

def handlerFunction2(scene):  
    scene = Scene.getSceneByNumber()
    scene.CLMBA_ExemplePropertyGroup.exempleString = "Exemple Text Was Saved |"
        
    scene.CLMBA_ExemplePropertyGroup.savedCount += 1
    scene.CLMBA_ExemplePropertyGroup.exempleString = f'{scene.CLMBA_ExemplePropertyGroup.exempleString[:24]} {scene.CLMBA_ExemplePropertyGroup.savedCount} | times'

ADDON.appendHandlers( CLMBHandler.Handler( CLMBHandler.HandlersTypes.FrameChanges.frameChangePost, handlerFunction) )
ADDON.appendHandlers( CLMBHandler.Handler( CLMBHandler.HandlersTypes.Save.savePost, handlerFunction2) )
#===============================================================

# Timers Registrator ===========================================
def in_5_seconds():
    scene = Scene.getSceneByNumber()
    scene.CLMBA_ExemplePropertyGroup.exempleInt += 1
    
    print(f"Hello World {scene.CLMBA_ExemplePropertyGroup.exempleInt}")
    return 5.0

ADDON.appendTimer(CLMBTimer( in_5_seconds ))
#===============================================================

# Addon Settings UI ============================================
def CLMBAPreferencesDraw(layout):
    BL = layout.box()
    BLR = BL.row(align = True)
    BLR.label(text="", icon = "QUESTION")
    BLR.label(text="Test Button in Preference UI")
    BL.operator("object.exemple_addon")
    
    BL = layout.box()
    BLR = BL.row(align = True)
    BLR.label(text="", icon = "QUESTION")
    BLR.label(text="Setup of keys")
    key.getBlenderUInterface(BL)  # <-- Dtaw KeyMap Settings

    BL = layout.box()
    BLR = BL.row(align = True)
    BLR.label(text="", icon = "QUESTION")
    BLR.label(text="Attributes")
    BL.prop(Scene.getSceneByNumber(), "CLMBA_Exemple")
    BL.prop(Scene.getSceneByNumber().CLMBA_ExemplePropertyGroup, "exempleInt")
    BL.prop(Scene.getSceneByNumber().CLMBA_ExemplePropertyGroup, "exempleString")


ADDON.CLMBAPreferencesDraw = CLMBAPreferencesDraw # <-- Set method to addon 
#===============================================================

# Addon RightHand Menu UI ======================================
def CLMBARightHandDraw(layout):
    BL = layout.box()
    BLR = BL.row(align = True)
    BLR.label(text="", icon = "QUESTION")
    BLR.label(text="Test Button in RightHand Menu")
    BL.operator("object.exemple_addon")

ADDON.CLMBARightHandUI = CLMBARightHandDraw # <-- Set method to addon
#===============================================================