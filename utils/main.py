import pickle
import pathlib
import functools


@functools.cache
def deserialize(filepath):
    return pickle.load(open(filepath, 'rb'))

def current_filepath(file):
    return pathlib.Path(file).parent 
