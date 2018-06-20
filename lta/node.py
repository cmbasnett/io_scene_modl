import re

class LTANode(object):

    def __init__(self, elements):
        if not isinstance(elements, list):
            raise ValueError
        self.elements = elements

    def __getattr__(self, item):
        try:
            return next(x for x in self.elements if isinstance(x, LTANode) and len(x) > 0 and isinstance(x[0], str) and x[0] == item)
        except StopIteration:
            raise KeyError

    def __getitem__(self, key):
        if isinstance(key, str):
            return self.__getattr__(key)
        elif isinstance(key, int):
            return self.elements[key]
        else:
            raise TypeError

    def __iter__(self):
        yield from self.elements

    def __len__(self):
        return len(self.elements)

    def __str__(self):
        return str(self.elements)

    def __repr__(self):
        return str(self.elements)

    def __contains__(self, item):
        try:
            self.__getattr__(item)
            return True
        except KeyError:
            return False

    def get_element(self, index):
        return self.elements[index]

    def get_keys(self, pattern):
        return filter(lambda x: isinstance(x, LTANode) and len(x) > 0 and isinstance(x[0], str) and re.match(pattern, x[0]) is not None, self.elements)
