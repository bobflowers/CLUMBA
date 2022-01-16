from os import error
import bpy
from CLUMBA.moduls.globalParametrs import DEBUG

class Log():
    @staticmethod
    def __printStr(cls, text):
        if type(cls) == str:
            return f'[{cls}]: {text}'
        elif hasattr(cls, "bl_idname"):
            base = cls.bl_idname.split("_")[2:]
            name = ""
            for i in range(len(base)):
                name += base[i] 
                if i != len(base)-1:
                    name += "_"
            return f'[{name}]: {text}'
        else:
            return f'[{cls.__module__}]: {text}'

    @staticmethod
    def print(cls, text, showInBlender = False):
        if not DEBUG:
            return
        text = Log.__printStr(cls, text)
        print(text)
