from .model import *
from .lta import helper
from .lta.parser import parse
from mathutils import Vector, Matrix, Quaternion
from .helpers import chunks

from pprint import pprint

class AsciiModelReader(object):

    def __init__(self):
        pass

    def from_file(self, path):
        model = Model()
        with open(path, 'rb') as f:
            text = f.read().decode('ascii')
            tree = parse(text)
            model0 = helper.get_key(tree, 'lt-model-0')
            shapes = helper.get_keys(model0, 'shape')
            for s in shapes:
                shape = Shape()
                shape.name = s[1]
                geometry = helper.get_key(s, 'geometry')
                mesh = helper.get_key(geometry, 'mesh')
                # Vertices
                vertices = helper.get_key(mesh, 'vertex')[1]
                shape.vertices = [Vector(map(float, vertex)) for vertex in vertices]
                # Triangles
                faces = list(map(int, helper.get_key(mesh, 'tri-fs')[1]))
                shape.faces = list(chunks(faces, 3))
                shape.material_index = int(helper.get_key(s, 'material-index')[1])
                # UVs
                for uvs in helper.get_keys(mesh, 'uvs_\d'):
                    shape.uvs.append(uvs[1])
                    pprint(uvs[1])
                model.shapes.append(shape)
        return model