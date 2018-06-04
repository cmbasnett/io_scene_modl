import struct

'''
Utility functions for reading from the file.
'''
def unpack(fmt, f):
    return struct.unpack(fmt, f.read(struct.calcsize(fmt)))


def pack(fmt, f, values):
    f.write(struct.pack(fmt, values))


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]
