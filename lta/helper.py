import re

def get_key(node, name):
    try:
        return next(x for x in node if isinstance(x, list) and len(x) > 0 and isinstance(x[0], str) and x[0] == name)
    except StopIteration:
        raise KeyError

def get_keys(node, pattern):
    return filter(lambda x: isinstance(x, list) and len(x) > 0 and isinstance(x[0], str) and re.match(pattern, x[0]) is not None, node)


