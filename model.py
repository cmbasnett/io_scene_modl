
class Shape(object):
    def __init__(self):
        self.name = ''
        self.material_index = -1
        self.vertices = []
        self.faces = []
        self.uvs = []

class Model(object):
    def __init__(self):
        self.name = ''
        self.shapes = []