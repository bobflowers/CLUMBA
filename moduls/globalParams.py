import os 

class CLMBGlobalParams:
    SYSTEM_NAME = os.name

    DEBUG = True
    ADDONS_FOLDER = f'{os.path.split(os.path.split(__file__)[0])[0]}/addons/'
    CLUMBA_VERSION = "0.1.0"

    separatorLenght = 100