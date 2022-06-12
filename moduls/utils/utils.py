from ..globalParams import CLMBGlobalParams

class Utils:

    class Struct:
        def __init__(self,**attributes):
            print(attributes)
            for name, attr in attributes.items():
                setattr(self,name,attr)

    @staticmethod
    def delListItem(lst, itemForDelete):
        if type(lst) != list:
            return lst

        for i in range(len(lst)):
            if i >= len(lst):
                return lst
            if lst[i] == itemForDelete:
                del lst[i]                

        return lst
    
    @staticmethod
    def cleanListByType(values, allowedType):
        data = []
        for i in range(len(values)):
            if Utils.checkType( values[0], allowedType):
                data.append(values[0])
            else:
                Log.print("CHECKING TYPE (cleanListByType)", f"Object: {str(values[0])} (type: {type(values[0])}) was skipped!",Log.LogType.ERROR, useGlobalDEBUG=True)
            del values[0]
        return data

    @staticmethod
    def checkType(value, types):
        if type(types) in (list,tuple):
            for i in types:
                if type(value) is i:
                    return True
        if type(value) is types:
            return True
        return False
        
    @staticmethod
    def getSeparatorLine(text="", separatorSymbol="="):
        if text:
            if len(text) >= CLMBGlobalParams.separatorLenght:
                text = text[:CLMBGlobalParams.separatorLenght-5]
                text += "..."
            textTemp = text
            text = " " + textTemp + " "
        else:
            return str(separatorSymbol*CLMBGlobalParams.separatorLenght)
            
        symbolLengh = ( CLMBGlobalParams.separatorLenght - len(text) ) * 0.5
        if ( symbolLengh % 2 ):
            return f'{separatorSymbol * int(symbolLengh+1) }{text}{separatorSymbol * int(symbolLengh) }'
        else:
            return f'{separatorSymbol * int(symbolLengh) }{text}{separatorSymbol * int(symbolLengh) }'
        
class Log:
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
    def print(cls, text, state=None, useGlobalDEBUG = False):
        '''STATE 0 - INFO 1 - WARN  2 - ERROR 3 - CRITICAL'''
        if useGlobalDEBUG and not CLMBGlobalParams.DEBUG:
            return
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

    class LogType:
        INFO  = 0
        WARN  = 1
        ERROR = 2
        CRITICAL = 3 