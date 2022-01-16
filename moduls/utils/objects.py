import bmesh
from mathutils import *

from CLUMBA.moduls.utils.math import Math

class Objects:

    @staticmethod
    def resetPivot(obj):
        baseLocation = Vector((obj.location))
        baseScale = Vector((obj.scale))
        data = obj.data

        bm = bmesh.new()
        bm.from_mesh(data)

        for i in bm.verts:
            i.co = i.co @ Math.getRoationMatrix(  obj.matrix_world.inverted() )

        bm.to_mesh(data)
        bm.free()

        obj.matrix_world = Matrix()
        obj.location = baseLocation