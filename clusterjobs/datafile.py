import sys
import os
import bz2
import tempfile
try:
    import cPickle as pickle
except ImportError:
    import pickle

import scicfg
from .color import COLORS_OUT as colors

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

def isfile(filepath):
    return os.path.isfile(filepath) or os.path.isfile(filepath + '.bz2')

def load_file(filename, directory='', typename='data', verbose=True):
    """Compressed version of the file is searched first."""
    filepath = buildpath(filename, directory)
    try:
        with open(filepath+'.bz2', 'rb') as fp:
            data_bz2 = bz2.decompress(fp.read())
            if sys.version_info.major == 2:
                data = pickle.loads(data_bz2)
            else: # py3k
                data = pickle.loads(data_bz2, encoding='latin-1')
    except EOFError:
        os.remove(filepath+'.bz2')
        raise EOFError('the file seemed corrupt and was deleted.')
    except IOError:
        with open(filepath, 'rb') as f:
            data = pickle.load(f)

    if verbose:
        print('{}exp:{} {} loaded in {}{}{}'.format(colors['magenta'], colors['grey'], typename, colors['cyan'], filepath, colors['end']))
    return data

def save_file(data, filename, directory='', typename='data', verbose=True, compressed=True):
    filepath = buildpath(filename, directory)
    temp = tempfile.NamedTemporaryFile(dir=os.path.dirname(filepath), suffix='.tempfile', delete=False)

    # protocol=2 to be able to open file from py2k
    protocol = 2
    if compressed:
        temp.write(bz2.compress(pickle.dumps(data, protocol),9))
        filepath += '.bz2'
    else:
        temp.write(pickle.dump(data, f, protocol))

    os.rename(temp.name, filepath)
    if verbose:
        print('{}exp:{} {} saved in {}{}{}'.format(colors['magenta'], colors['grey'], typename, colors['cyan'], filepath, colors['end']))

def save_text(text, filename, directory='', typename='text', verbose=True):
    filepath = buildpath(filename, directory)
    with open(filepath, 'w') as f:
        f.write(text)
    if verbose:
        print('{}exp:{} text saved in {}{}{}'.format(colors['magenta'], colors['grey'], colors['cyan'], filepath, colors['end']))

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
        print('{}exp:{} config loaded in {}{}{}'.format(colors['magenta'], colors['grey'], colors['cyan'], filepath, colors['end']))

    return scicfg.SciConfig(d)

def save_config(cfg, filename='', directory=''):
    filepath = buildpath(filename, directory)

    cfg._to_file(filepath)
