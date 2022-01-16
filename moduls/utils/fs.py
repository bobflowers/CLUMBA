import os
import re
from .log import *
import json

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

class LineData:
    def __init__(self,file):
        self.filePath = file
        self.lineData = []

        self.readLineData()

    def readLineData(self):
        with open(self.filePath, "r", encoding='utf-8') as f:
            self.lineData = f.readlines()
        
    def write(self):
        with open(self.filePath, "w", encoding='utf-8') as f:
            f.write("")
        with open(self.filePath, "w", encoding='utf-8') as f:
            for line in self.lineData: 
                f.write(line + "\n")

    def jsonDump(self):
        if not self.filePath.endswith(".json"):
            return
        with open(self.filePath, "r", encoding='utf-8') as f:
            jsonLoad = json.load(f)
        return jsonLoad


    def clear(self):
        self.lineData = []