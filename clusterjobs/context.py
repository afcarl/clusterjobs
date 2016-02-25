import os

from . import datafile
from . import qstat


class Env(object):

    def __init__(self, user = 'user'):
        self.user = user
        self.qsub = qstat.qsub_available()

    def running_jobs(self):
        return qstat.get_running_jobs(self.user)

    @classmethod
    def file_exists(cls, filepath):
        return os.path.isfile(filepath) or os.path.isfile(filepath+'.bz2')

class Context(object):

    def __init__(self, rootdir, reldir):
        self.rootdir = os.path.expanduser(rootdir)
        self.reldir  = os.path.expanduser(reldir)
        self.fulldir = os.path.join(rootdir, reldir)
        self.qsub = qstat.qsub_available()

    # def _prepare(self):
    #     if not os.path.exists(self.dir):
    #         os.makedirs(self.dir)
    #     assert os.path.isdir(self.dir)

    def file_exists(self, rel_filepath):
        assert not os.path.isabs(rel_filepath)
        filepath = os.path.join(self.fulldir, rel_filepath)
        return os.path.isfile(filepath) or os.path.isfile(filepath+'.bz2')

    def fullpath(self, filepath):
        """Return the filepath prefixed py fulldir"""
        filepath = os.path.expanduser(filepath)
        if not os.path.isabs(filepath):
            filepath = os.path.join(self.fulldir, filepath)
        return datafile.normpath(filepath)

    def rootpath(self, filepath):
        """Retur the filepath prefixed py rootdir"""
        filepath = os.path.expanduser(filepath)
        if not os.path.isabs(filepath):
            filepath = os.path.join(self.rootdir, filepath)
        return datafile.normpath(filepath)

    def relpath(self, filepath):
        """Return the filepath prefixed by reldir"""
        filepath = os.path.expanduser(filepath)
        if not os.path.isabs(filepath):
            filepath = os.path.join(self.reldir, filepath)
        return os.path.normpath(filepath)
