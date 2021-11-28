import bpy

class Log():
    def printStr(cls, text):
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

    def print(cls, text, showInBlender = False):
        text = Log.printStr(cls, text)
        print(text)
        if showInBlender:
            pass
            #operator = bpy.ops.info.log_to_info('INVOKE_DEFAULT')
            #operator.text = text
