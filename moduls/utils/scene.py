import bpy

class Scene:
    
    @staticmethod
    def getTimeFrameNumeratick(context):
        class Item:
            def __init__(self, start, end):
                self.start  = start
                self.end    = end 
                self.lenght = end - start
            
            def __repr__(self):
                return f'Time Line Start: {self.start} End: {self.end} Lenght: {self.lenght}'

        scene = context.scene

        return Item(scene.frame_start, scene.frame_end)
                
        
        