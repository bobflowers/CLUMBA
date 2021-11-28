import os
from .log import *

class fs:
    def getFileList(path, extension):
        if not os.path.isdir(path):
            print(CMBPrintStr("fs.getFileList", "Path not Exist!"))
            return
        data = []
        for file in os.listdir(path):
            if file.endswith(extension):
                data.append(file)
        return data