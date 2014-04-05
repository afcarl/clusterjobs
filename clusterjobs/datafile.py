import os
import cPickle
import bz2

import forest
from toolbox import gfx

def normpath(*path):
    return os.path.normpath(os.path.abspath(os.path.expanduser(os.path.join(*path))))

def buildpath(filepath, directory):
    filepath = os.path.expanduser(filepath)
    if directory != '' and not os.path.isabs(filepath):
        filepath = os.path.join(directory, filepath)
    return normpath(filepath)

def create_directories(filepaths):
    dirset = set()
    for filepath in filepaths:
        path = os.path.dirname(filepath)
        path = normpath(path)
        dirset.add(path)
    for path in dirset:
        if not os.path.exists(path):
            os.makedirs(path)

def load_file(filename, directory='', typename='unknown', verbose=True):
    """Compressed version of the file is searched first."""
    filepath = buildpath(filename, directory)
    try:
        with open(filepath+'.bz2', 'rb') as fp:
            data_bz2 = bz2.decompress(fp.read())
            data = cPickle.loads(data_bz2)
    except IOError:
        with open(filepath, 'rb') as f:
            data = cPickle.load(f)

    if verbose:
        print('{}exp:{} compiled {} loaded in {}{}{}'.format(gfx.purple, gfx.grey, typename, gfx.cyan, filepath, gfx.end))
    return data

def save_file(data, filename, directory='', typename='unknown', verbose=True, compressed=True):
    filepath = buildpath(filename, directory)
    if compressed:
        with open(filepath+'.bz2', 'wb') as fp:
            fp.write(bz2.compress(cPickle.dumps(data, cPickle.HIGHEST_PROTOCOL),9))
    else:
        with open(filepath,'wb') as f:
            cPickle.dump(data, f, cPickle.HIGHEST_PROTOCOL)
    if verbose:
        print('{}exp:{} compiled {} saved in {}{}{}'.format(gfx.purple, gfx.grey, typename, gfx.cyan, filepath, gfx.end))

def save_text(text, filename, directory='', typename='text', verbose=True):
    filepath = buildpath(filename, directory)
    with open(filepath, 'w') as f:
        f.write(text)
    if verbose:
        print('{}exp:{} text file saved in {}{}{}'.format(gfx.purple, gfx.grey, gfx.cyan, filepath, gfx.end))

def load_config(filename, directory=''):
    filepath = buildpath(filename, directory)

    with open(filepath,'r') as f:
        s = f.read()

    d = {}
    for line in s.split('\n'):
        try:
            key, value = line.split('=')
            key = key.strip()
            value = eval(value.strip(), {}, {})
            d[key] = value
        except ValueError:
            pass

    return forest.Tree(d)

def save_config(cfg, directory=''):
    filepath = buildpath(cfg.hardware.configfile, directory)

    cfg._to_file(filepath)
