import os
from . import datafile

class Job(object):
    """"""

    def __init__(self, context, dependencies, args):
        self.uptodate = False # if the job status is uptodate.
        self.context = context
        self._dependencies = dependencies

        self._name = ''
        self._input_files  = []
        self._output_files = []
        self.prepare(args)

        status = 'unknown'

    def prepare(self, args):
        """ Probably a good time to initialize _name, _input_files
            _output_files and _dependencies.
        """
        raise NotImplementedError

    def prepare_hd(self):
        """ Probably a good time to write missing input files."""
        raise NotImplementedError

    @property
    def name(self):
        """Return the job name"""
        return self._name

    @property
    def dependencies(self):
        """Return all job dependencies"""
        return self._dependencies

    @property
    def input_files(self):
        """Return any additional necessary input files"""
        return self._input_files

    @property
    def output_files(self):
        """Return a list of the files created after completion"""
        return self._output_files

    def add_input_file(self, filepath):
        self._input_files.append(filepath)

    def add_output_file(self, filepath):
        self._output_files.append(filepath)

    def qsub_options(self):
        if 'qsub.resources' in self.cfg:
            options = ['{}={}'.format(key, value) for key, value in self.cfg.qsub.resources.items()]
            if len(options) > 0:
                return '-l {}'.format(','.join(sorted(options)))
        return ''

    def command(self):
        """Return the command line necessary to start the job"""
        raise NotImplementedError

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return str(self.name)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
