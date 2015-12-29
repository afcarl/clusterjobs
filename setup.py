import os
from setuptools import setup

import versioneer

def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as f:
        text = f.read()
    return text

setup(
    name         = "clusterjobs",
    version      = "1.0",
    cmdclass     = versioneer.get_cmdclass(),
    author       = "Fabien Benureau",
    author_email = "fabien.benureau@inria.fr",
    description  = "A python library for creating, scheduling and monitoring cluster jobs",
    license      = "Open Science License",
    keywords     = "clusters science",
    url          = "github.com/humm/clusterjobs",
    packages     = ['clusterjobs'],
    long_description=read('readme.md'),
    classifiers = [],
)
