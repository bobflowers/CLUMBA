import os
from .fs import *
from .log import Log
from ..globalParametrs import CLUMBA_VERSION, ADDONS_FOLDER

class CLMBInternal:
    '''Internal methods for CLUMBA'''

    def checkClumbaVersion(version):
        '''Check CLUMBA version'''
        CLMBCurent = CLUMBA_VERSION.split(".")
        versionSplit = version.split(".")
        for i in range(len(versionSplit)):
            if int(versionSplit[i]) > int(CLMBCurent[i]):
                Log.print("Version Control (checkClumbaVersion)", f'Addon require new version of CLUMBA. Curent {CLUMBA_VERSION} Addon {version} Please Update CLUMBA')
                return False
        return True

    def isCLUMBAddon(addon):
        '''Validate CLUMBA addon'''
        if "main" not in dir(addon):
            Log.print(__package__, f'Import {addon} is not CLUMBA addon!')
            return False
        if not CLMBInternal.checkClumbaVersion(addon.main.CLMBVersion):
            return False
        return True

    def firstFileCheck(file):
        '''This method check #CLUMBA in the first line'''
        with open(file, "r") as f:
            lines = f.readline()
            if "CLUMBA" in lines:
                return True
        return False

    def scanAddonsFolder():
        '''This method return py files with CLUMBA in first line'''
        def recursive(path = "", lvl = 0, data = None):
            if data == None:
                data = []
            for i in os.listdir(ADDONS_FOLDER + path):
                if os.path.isdir(ADDONS_FOLDER + path + i) and lvl < 1:
                    recursive(f'{path}{i}/',lvl + 1, data)
                if i.endswith(".py") and CLMBInternal.firstFileCheck(f'{ADDONS_FOLDER}{path}/{i}'):
                    data.append(path+i)
            return data
        #print(recursive())

        return recursive()

