import bpy
import rna_keymap_ui

from .utils import Log
from ..globalParams import CLMBGlobalParams


class Key:
    KEY_STORAGE = {}
    __doc__ = 'Blender Reference: https://docs.blender.org/api/current/bpy.types.KeyMapItem.html'

    def __init__(self, operator, key, keyMap = "Window", action = 'PRESS', shift = False, ctrl = False, alt = False):
        ''' Blender Reference: https://docs.blender.org/api/current/bpy.types.KeyMapItem.html'''
            
        self.__guard = True
        
        self.propertyName = operator.bl_idname
        self.name = operator.bl_idname
        if  hasattr(operator,"bl_label"):
            self.name = operator.bl_label
            
        self.keyMap = keyMap
        self.value = action
        self.shift = shift
        self.ctrl  = ctrl
        self.alt   = alt
        self.key = key.upper()

        self.KEY_STORAGE[self.name] = self

    def __repr__(self):
       return f'{self.name}'

    def getBlenderUInterface(self, layout):
        '''Method implement an key kontroller UI into an addon interface'''
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        drawed = 0
        for km in kc.keymaps:
            for kmi in km.keymap_items:
                if kmi.name != self.name:
                    continue
                drawed +=1
                layout.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, layout, 0)

        if not self.__guard or not drawed:
            BL = layout.box()
            BLR = BL.row(align = True)
            BLR.label(text="", icon = "ERROR")
            BLR.label(text="Keys setup can be drawing!")
            return
    
    def registrate(self):
        self.KEY_STORAGE[self.name] = self
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        
        if self.keyMap not in kc.keymaps:
            self.__guard = False 
            Log.print(self, f"KeyMap: {self.keyMap} doesn't exist!")
            return
        km = kc.keymaps[self.keyMap]

        kmi = km.keymap_items.new(
            idname = self.propertyName,
            type   = self.key,
            value  = self.value,
            ctrl   = self.ctrl,
            shift  = self.shift
            )
        kmi.active = True

        if not self.__guard:
            Log.print(self, f"Key: {self.name} haven't registrate!", Log.LogType.ERROR)

    def unregistrate(self):
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        if self.keyMap not in kc.keymaps:
            return
        for km in kc.keymaps:
            for kmi in km.keymap_items:
                if kmi.name != self.name:
                    continue
                km.keymap_items.remove(kmi)
        
    @classmethod
    def globalUnregistrate(self):
        Log.print(self, 'Global Keys Data - unregisterate initiated!', useGlobalDEBUG=True)
        for key in self.KEY_STORAGE.values():
            key.unregistrate()

    @staticmethod
    def swithKMIActiveState(keyName, state, mapArea = None):
        '''This method set active value of KeyMap Item by the state. If forced mapArea name - method switched only in this area'''
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user

        if mapArea and keyName in kc[mapArea]:
            kc[mapArea][keyName]

        for km in kc.keymaps:
            if keyName not in km:
                continue
            km[mapArea].active = state

    class KeyAction:
        ANY          = 'ANY'
        PRESS        = 'PRESS'
        RELEASE      = 'RELEASE'
        CLICK        = 'CLICK'
        DOUBLE_CLICK = 'DOUBLE_CLICK'
        CLICK_DRAG   = 'CLICK_DRAG'
        NORTH        = 'NORTH'
        NORTH_EAST   = 'NORTH_EAST'
        EAST         = 'EAST'
        SOUTH_EAST   = 'SOUTH_EAST'
        SOUTH        = 'SOUTH'
        SOUTH_WEST   = 'SOUTH_WEST'
        WEST         = 'WEST'
        NORTH_WEST   = 'NORTH_WEST'
        NOTHING      = 'NOTHING'