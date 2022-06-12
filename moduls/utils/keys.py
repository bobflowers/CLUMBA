import bpy
import rna_keymap_ui

from .utils import Log
from ..globalParametrs import CLMBGlobalParams


class Key:
    KEY_STORAGE = {}
    __doc__ = 'Blender Reference: https://docs.blender.org/api/current/bpy.types.KeyMapItem.html'

    def __init__(self, operator, key, keyMap = "Window", action = 1, shift = False, ctrl = False, alt = False):
        ''' Blender Reference: https://docs.blender.org/api/current/bpy.types.KeyMapItem.html
            Action [ 0 - ANY, 1 - PRESS, 2 - RELEASE, 3 - CLICK, 4 - DOUBLE_CLICK, 5 - CLICK_DRAG, 6 - NORTH, 7 - NORTH_EAST, 8 - EAST, 9 - SOUTH_EAST, 10 - SOUTH, 11 - SOUTH_WEST, 12 - WEST, 13 - NORTH_WEST, 14 - NOTHING]'''
            
        self.__actionStorage = ['ANY', 'PRESS', 'RELEASE', 'CLICK', 'DOUBLE_CLICK', 'CLICK_DRAG', 'NORTH', 'NORTH_EAST',
                                'EAST', 'SOUTH_EAST', 'SOUTH', 'SOUTH_WEST', 'WEST', 'NORTH_WEST', 'NOTHING' ]
        self.__guard = True
        
        self.propertyName = operator.bl_idname
        self.name = operator.bl_idname
        if  hasattr(operator,"bl_label"):
            self.name = operator.bl_label
            
        self.keyMap = keyMap
        self.value = None
        self.shift = shift
        self.ctrl  = ctrl
        self.alt   = alt
        self.key = key.upper()

        #Check then correct state was selected state from 0-14
        if action >= 0 and action <= len(self.__actionStorage):
            self.value = self.__actionStorage[action]
        else:
            Log.print(self, f'Key: {action} is not detected. PLease make shure than index from {self.__actionStorage}',state=2)
            self.__guard = False

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
            Log.print(self, f"Key: {self.name} haven't registrate!", state=2)

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
        if CLMBGlobalParams.DEBUG:
            Log.print(self, 'Global Keys Data - unregisterate initiated!',state=0)
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