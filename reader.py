from .model import *
from .lta.parser import parse
from mathutils import Vector, Matrix, Quaternion
from .helpers import chunks

class AsciiModelReader(object):

    def __init__(self):
        pass

    def from_file(self, path):
        model = Model()
        with open(path, 'rb') as f:
            text = f.read().decode('ascii')
            tree = parse(text)
            model0 = tree['lt-model-0']
            shapes = model0.get_keys('shape')
            for s in shapes:
                shape = Shape()
                shape.name = s[1]
                geometry = s.geometry
                mesh = geometry.mesh
                # Vertices
                vertices = mesh.vertex[1]
                shape.vertices = [Vector(map(float, vertex)) for vertex in vertices]
                # Triangles
                faces = list(map(int, mesh['tri-fs'][1]))
                shape.faces = list(chunks(faces, 3))
                shape.material_index = int(s['material-index'][1])
                # UVs
                for uvs in mesh.get_keys('uvs_\d'):
                    shape.uvs.append(uvs[1])
                # hierarchy
                hierarchy = model0.hierarchy
                children = hierarchy.children
                print(children)
                #transform = children.transform
                # TODO: recursive, it seems?
                model.shapes.append(shape)
        return model