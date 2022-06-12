import bpy
import os
from .fs import *
from .utils import Utils, Log
from ..globalParams import CLMBGlobalParams

class CLMBAddon:
    def __init__(self, name, version, path = ""):
        self.name = name
        self.path = path
        self.disable = False
        self.version = version
        self.description = None

        self.__CLMBClassesForRegistration   = []
        self.__CLMBAttributeForRegistration = []
        self.__CLMBHandlersForRegistration  = []

    def __repr__(self):
        return f'Addon: {self.name}'

    def checkClumbaVersion(self):
        '''Check CLUMBA version'''
        CLMBCurent = CLMBGlobalParams.CLUMBA_VERSION.split(".")
        versionSplit = self.version.split(".")
        for i in range(len(versionSplit)):
            if int(versionSplit[i]) > int(CLMBCurent[i]):
                Log.print("Version Control (checkClumbaVersion)", f'Addon require new version of CLUMBA. Curent {CLMBGlobalParams.CLUMBA_VERSION} Addon {self.version} Please Update CLUMBA')
                return False
        self.disable = True

    @staticmethod
    def __appendingRules(values, dataContainer, allowedType):
        if type(values) is list:
            dataContainer += Utils.cleanListByType(values, allowedType)
        elif Utils.checkType(values,allowedType):
            dataContainer.append(values)
        else:
            Log.print("CHECKING TYPE (appendingRules)", f"Object: {values} (type: {type(values)}) can't be registrated!",Log.LogType.ERROR, useGlobalDEBUG=True)

    def appendClass(self, classes):
        '''Method for applying classes to queue for registration. Method expect method ore list of methods'''
        if type(classes) is list:
            self.__CLMBClassesForRegistration += classes
        else:
            self.__CLMBClassesForRegistration.append(classes)

    def appendAtributes(self, attributes):
        self.__appendingRules(attributes, self.__CLMBAttributeForRegistration, CLMBAttribute)

    def appendHandlers(self, handlers):
        self.__appendingRules(handlers, self.__CLMBHandlersForRegistration, CLMBHandler.Handler)
    
    def getClasses(self):
        if self.disable:
            return []
        return self.__CLMBClassesForRegistration
    
    def getAtributes(self):
        if self.disable:
            return []
        return self.__CLMBAttributeForRegistration

    def getHandlers(self):
        if self.disable:
            return []
        return self.__CLMBHandlersForRegistration

    def CLMBAPreferencesDraw(self, layout):
       BL = layout.box()
       BLR = BL.row(align = True)
       BLR.label(text="", icon = "QUESTION")
       BLR.label(text=f"Addon: {self.name}")      

    def CLMBARightHandUI(self, layout):
        pass


class CLMBHandler:
    class Handler:
        def __init__(self, handlerType, function):
            self.handlerType = handlerType
            self.function = function

        def __repr__(self):
            return f'Handler Type:{self.handlerType} Function:{self.function.__name__}'

        def registrate(self):
            attr = getattr(bpy.app.handlers, self.handlerType)
            attr.append(self.function)

        def unRegistrate(self):
            attr = getattr(bpy.app.handlers, self.handlerType)
            attr.remove(self.function)
        
    class HandlersTypes:
        __doc__ = 'https://docs.blender.org/api/current/bpy.app.handlers.html'
        class Anotation:
            anotationPost = "annotation_post"
            annotationPre = "annotation_pre"
        class Depsgraph:
            depsgraphUpdatePost = "depsgraph_update_post"
            depsgraphUpdatePre  = "depsgraph_update_post"
        class FrameChanges:
            frameChangePost = "frame_change_post"
            frameChangePre  = "frame_change_pre"
        class LoadFactory:
            loadFactoryPreferencesPost = "load_factory_preferences_post"
            loadFactoryStartupPost     = "load_factory_startup_post"
        class Loading:
            loadPost = "load_post"
            loadPre  = "load_pre"
        class Redo:
            redoPost = "redo_post"
            redoPre  = "redo_pre"
        class Undo:
            undoPost = "undo_post"
            undoPre  = "undo_pre"
        class Render:
            renderCancel   = "render_cancel"
            renderComplete = "render_complete"
            renderInit     = "render_init"
            renderPost     = "render_post"
            renderPre      = "render_pre"
            renderStats    = "render_stats"
            renderWrite    = "render_write"
        class Save:
            savePost = "save_post"
            savePre  = "save_pre"
        class Other:
            version_update       = "version_update"
            xr_session_start_pre = "xr_session_start_pre"
            persistent           = "persistent"
            
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
            self.obj = getattr( self.root, baseObject)
            if '_PropertyDeferred' in str(type(self.obj)):
                self.badQueryGuard = False
        except BaseException as e:
            Log.print("CLMBAttribute",e,Log.LogType.CRITICAL) 
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