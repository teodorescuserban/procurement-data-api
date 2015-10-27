import os

def resolve_file(filename):
    fullpath = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(fullpath, filename)
