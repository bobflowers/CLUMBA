import bpy
from ..globalParametrs import CLMBGlobalParams

class Log():
    @staticmethod
    def __printStr(cls, text, state):
        stateForImplement = ""
        if state:
            stateForImplement = f"[{state}]"
        if type(cls) == str:
            return f'[{cls}]{stateForImplement}: {text}'
        elif hasattr(cls, "bl_idname"):
            base = cls.bl_idname.split("_")[2:]
            name = ""
            for i in range(len(base)):
                name += base[i] 
                if i != len(base)-1:
                    name += "_"
            return f'[{name}]{stateForImplement}: {text}'
        else:
            return f'[{cls.__module__}]{stateForImplement}: {text}'

    @staticmethod
    def print(cls, text, showInBlender = False, state=None):
        '''STATE 0 - INFO 1 - WARN  2 - ERROR 3 - CRITICAL'''
        if state == 0:
            state = "INFO"
        elif state == 1:
            state = "WARN"
        elif state == 2:
            state = "ERROR"
        elif state == 3:
            state = "CRITICAL"
        text = Log.__printStr(cls, text, state)
        print(text)
