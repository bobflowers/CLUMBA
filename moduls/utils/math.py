
import re
from mathutils import *

class Math:
    
    @staticmethod
    def getRotationMatrix( points ):
        ''''This method return rotation matrix by 3 point. 
            !WARNING! Matrix in 3x3 scale'''
        v1 = points[ 1 ] - points[ 0 ]
        v2 = points[ 2 ] - points[ 0 ]

        vCrp = v1.cross( v2 )
        vCrp.normalized()

        v2 = Math.vectorToUnit( vCrp.cross( v1 ).normalized())
        v1 = Math.vectorToUnit( v1.normalized())

        vCrp = Math.vectorToUnit(vCrp)

        return Matrix( [ v1, v2, vCrp ] ).transposed()
                
    @staticmethod
    def vectorToUnit( vct: Vector ):
        '''Method retern vector in scale 1'''
        vct = vct.normalized()
        return vct * Vector( ( 1.0 / vct.magnitude, 1.0 / vct.magnitude, 1.0 / vct.magnitude ) )

    @staticmethod
    def getRoationMatrix( matrix: Matrix ):
        '''This method split position and rotatin from an import matrix'''
        matrix = matrix.to_3x3()

        for i in range( 3 ):
            matrix[ i ] = matrix[ i ] / matrix[ i ].magnitude
 
 
        return matrix.to_4x4()

    @staticmethod
    def scaleMatrix( matrix, vector ):

        for y in range( 3 ):
            matrix[ y ][ y ] *= vector[ y ] 

        return matrix 

    @staticmethod
    def lerp(a, b, v):
        #return a * (1 - v) + b * v
        return a + v * (b - a)
