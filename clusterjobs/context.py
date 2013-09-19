import os

from . import qstat


class Env(object):

    def __init__(self, user = 'user'):
        self.user = user
        self.qsub = qstat.qsub_available()

    def running_jobs(self):
        return qstat.get_running_jobs(self.user)

    def file_exists(self, filepath):
        return os.path.isfile(filepath)

class Context(object):

    def __init__(self, rootdir):
        self.dir = os.path.expanduser(rootdir)
        self._prepare()
        self.qsub = qstat.qsub_available()

    def _prepare(self):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        assert os.path.isdir(self.dir)

    def file_exists(self, rel_filepath):
        assert not os.path.isabs(rel_filepath)
        return os.path.isfile(os.path.join(self.dir, rel_filepath))
