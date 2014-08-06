import os
import cPickle
import bz2
import tempfile

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

def load_file(filename, directory='', typename='data', verbose=True):
    """Compressed version of the file is searched first."""
    filepath = buildpath(filename, directory)
    try:
        with open(filepath+'.bz2', 'rb') as fp:
            data_bz2 = bz2.decompress(fp.read())
            data = cPickle.loads(data_bz2)
    except EOFError:
        os.remove(filepath+'.bz2')
        raise EOFError('the file seemed corrupt and was deleted.')
    except IOError:
        with open(filepath, 'rb') as f:
            data = cPickle.load(f)

    if verbose:
        print('{}exp:{} {} loaded in {}{}{}'.format(gfx.purple, gfx.grey, typename, gfx.cyan, filepath, gfx.end))
    return data

def save_file(data, filename, directory='', typename='data', verbose=True, compressed=True):
    filepath = buildpath(filename, directory)
    temp = tempfile.NamedTemporaryFile(dir=os.path.dirname(filepath), suffix='.tempfile', delete=False)

    if compressed:
        temp.write(bz2.compress(cPickle.dumps(data, cPickle.HIGHEST_PROTOCOL),9))
        filepath += '.bz2'
    else:
        temp.write(cPickle.dump(data, f, cPickle.HIGHEST_PROTOCOL))

    os.rename(temp.name, filepath)
    if verbose:
        print('{}exp:{} {} saved in {}{}{}'.format(gfx.purple, gfx.grey, typename, gfx.cyan, filepath, gfx.end))

def save_text(text, filename, directory='', typename='text', verbose=True):
    filepath = buildpath(filename, directory)
    with open(filepath, 'w') as f:
        f.write(text)
    if verbose:
        print('{}exp:{} text saved in {}{}{}'.format(gfx.purple, gfx.grey, gfx.cyan, filepath, gfx.end))

def load_config(filename, directory='', verbose=True):
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

    if verbose:
        print('{}exp:{} config loaded in {}{}{}'.format(gfx.purple, gfx.grey, gfx.cyan, filepath, gfx.end))

    return forest.Tree(d)

def save_config(cfg, filename='', directory=''):
    filepath = buildpath(filename, directory)

    cfg._to_file(filepath)
