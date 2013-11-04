import os
import cPickle
import treedict

from toolbox import gfx

def normpath(path):
    return os.path.normpath(os.path.abspath(os.path.expanduser(path)))

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
    filepath = buildpath(filename, directory)
    with open(filepath, 'r') as f:
        data = cPickle.load(f)
    if verbose:
        print('{}exp:{} compiled {} loaded in {}{}{}'.format(gfx.purple, gfx.grey, typename, gfx.cyan, filepath, gfx.end))
    return data

def save_file(data, filename, directory='', typename='unknown', verbose=True):
    filepath = buildpath(filename, directory)
    with open(filepath,'w') as f:
        cPickle.dump(data, f)
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

    return treedict.TreeDict().fromdict(d)

def save_config(cfg, directory=''):
    filepath = buildpath(cfg.hardware.configfile, directory)

    with open(filepath,'w') as f:
        f.write(cfg.makeReport())
