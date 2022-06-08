import os
from .fs import *
from .log import Log
from ..globalParametrs import CLMBGlobalParams
from abc import ABC, abstractmethod 

class CLMBAddon:
    def __init__(self, name, version, path = ""):
        self.name = name
        self.path = path
        self.disable = False
        self.version = version
        self.description = None

        self.__CLMBClassesForRegistration = []
        self.__CLMBAttributeForRegistration = []

    def __repr__(self):
        return f'Addon: {self.name}'

    def checkClumbaVersion(self):
        '''Check CLUMBA version'''
        CLMBCurent = CLMBGlobalParams.CLUMBA_VERSION.split(".")
        versionSplit = self.version.split(".")
        for i in range(len(versionSplit)):
            if int(versionSplit[i]) > int(CLMBCurent[i]):
                Log.print("Version Control (checkClumbaVersion)", f'Addon require new version of CLUMBA. Curent {CLMBGlobalParams.CLUMBA_VERSION} Addon {version} Please Update CLUMBA')
                return False
        self.disable = True

    def appendClass(self, classes):
        '''Method for applying classes to queue for registration. Method expect method ore list of methods'''
        if type(classes) is list:
            self.__CLMBClassesForRegistration += classes
        else:
            self.__CLMBClassesForRegistration.append(classes)
    
    def getClasses(self):
        return self.__CLMBClassesForRegistration
    
    def appendAtributes(self, attributes):
        if type(attributes) is list:
            self.__CLMBAttributeForRegistration += attributes
        else:
            self.__CLMBAttributeForRegistration.append(attributes)
    
    def getAtributes(self):
        return self.__CLMBAttributeForRegistration

    def CLMBAPreferencesDraw(self, layout):
       BL = layout.box()
       BLR = BL.row(align = True)
       BLR.label(text="", icon = "QUESTION")
       BLR.label(text=f"Addon: {self.name}")      

    def CLMBARightHandUI(self, layout):
        pass

class CLMBAttribute:
    def __init__(self,root, obj ,name, prop):
        self.root = root
        self.obj = obj
        self.name = name
        self.prop = prop

        self.badQueryGuard = True

        #self.tryInitBaseObject( obj )

    def __repr__(self):
       return f'{self.obj}.{self.name}'

    def tryInitBaseObject( self, baseObject):
        try: 
            #print(f"Name: {self.root} Type: {type(baseObject)}")
            self.obj = getattr( self.root, baseObject)
            if '_PropertyDeferred' in str(type(self.obj)):
                self.badQueryGuard = False
        except BaseException as e:
            Log.print("CLMBAttribute",e,state=3) 
            self.badQueryGuard = False

    def registrate(self):
        self.tryInitBaseObject( self.obj )
        if self.badQueryGuard:
            setattr( self.obj, self.name, self.prop )
            return True
        else:
            Log.print("CLMBAttribute", f"Object {self.obj}.{self.name} hasn't registred and destroyed!" )
            return False

    def unRegistrate(self):
        if self.badQueryGuard:
            delattr( self.obj, self.name )


class CLMBInternal:
    '''Internal methods for CLUMBA'''
    @staticmethod
    def isCLUMBAddon(addon):
        '''Validate CLUMBA addon'''
        from CLUMBA.moduls.utils.internal import CLMBAddon

        if type(addon) is type(CLMBAddon):
            Log.print(__package__, f'Import {addon} is not CLUMBA addon!')
            return False
        if addon.disable:
            return False
        return True

    @staticmethod
    def firstFileCheck(file):
        '''This method check #CLUMBA in the first line'''
        with open(file, "r") as f:
            lines = f.readline()
            if "CLUMBA" in lines:
                return True
        return False

    @staticmethod
    def scanAddonsFolder():
        '''This method return py files with CLUMBA in first line'''
        def recursive(path = "", lvl = 0, data = None):
            if data == None:
                data = []
            for i in os.listdir(CLMBGlobalParams.ADDONS_FOLDER + path):
                if os.path.isdir(CLMBGlobalParams.ADDONS_FOLDER + path + i) and lvl < 1:
                    recursive(f'{path}{i}/',lvl + 1, data)
                if i.endswith(".py") and CLMBInternal.firstFileCheck(f'{CLMBGlobalParams.ADDONS_FOLDER}{path}/{i}'):
                    data.append(path+i)
            return data

        return recursive()