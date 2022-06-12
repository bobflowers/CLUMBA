
import bpy
import random

from .utils import Log

class Mesh:

    @staticmethod
    def isSameMesh(first, second, full = False):
        '''This method compare two meshes by vertex, edges and poligon cound. 
            In full mode method compare position of 10 random vertices'''
        if len( first.vertices ) != len( second.vertices ):
            Log.print("Mesh.isSameMesh", "Vertex Data Not Same!")
            return False
        elif len( first.edges ) != len( second.edges ):
            Log.print("Mesh.isSameMesh", "Edges Data Not Same!")
            return False
        elif len( first.polygons ) != len( second.polygons):
            Log.print("Mesh.isSameMesh", "Poligon Data Not Same!")
            return False

        if full:
            indexFoeCheck = [] # vertex index
            while indexFoeCheck < range( int( len( first.polygons ) * 0.5 ) ):
                value = random.randint( 0, len( first.polygons ) - 1 )
                if value in indexFoeCheck:
                    continue
                indexFoeCheck.append(indexFoeCheck)

            for index in indexFoeCheck:
                if first.vertices[index].co != second.vertices[index].co:
                    Log.print("Mesh.isSameMesh", "Vertex Data Position Not Same!")
                    return False
                    
        return True

    
class DepthGraph:
    class DepthGraphObject:
        def __init__(self, obj):
            self.obj = obj
            self.mesh = bpy.data.meshes.new_from_object( self.obj )

            self.mesh.name = "TemporraryMesh"
        
        def __repr__(self):
            return f'Name: {self.mesh.name} Vert Count {len( self.mesh.vertices )} Edges Count {len( self.mesh.edges )} Polygons Count {len( self.mesh.polygons )}'

        def __del__(self):
            self.obj.to_mesh_clear()
            bpy.data.meshes.remove(self.mesh)

    @staticmethod
    def getEvaluatedDataFormObject(context,obj):
        depsgraph = context.evaluated_depsgraph_get()
        return DepthGraph.DepthGraphObject( obj.evaluated_get(depsgraph) )