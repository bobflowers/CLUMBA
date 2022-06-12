import os
from .utils import Log
import json

class fs:
    @staticmethod
    def getFileList(path, extension):
        if not os.path.isdir(path):
            Log.print("fs.getFileList", "Path not Exist!", Log.LogType.ERROR)
            return
        data = []
        for file in os.listdir(path):
            if file.endswith(extension):
                data.append(file)
        return data

    @staticmethod
    def jsonDump(filePath):
        if not filePath.endswith(".json"):
            return
        with open(filePath, "r", encoding='utf-8') as f:
            jsonLoad = json.load(f)
        return jsonLoad

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

    def clear(self):
        self.lineData = []