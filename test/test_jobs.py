"""Mock jobs for testing code"""

import random
import os

import dotdot
from clusterjobs import job
from clusterjobs import jobgroup
from clusterjobs import context

#ctxt = context.Context('/tmp/clusterjobs-{}/'.format(random.random()), 'fbenurea')
env = context.Env(user='fbenurea')

class FirstJobs(job.Job):

    def prepare(self, name):
        self._filename = 'first/f{:02d}'.format(name)
        self._name = self._filename
        self.add_output_file(self._filename)

    def prepare_hd(self):
        pass

    def command(self):
        return 'touch {}'.format(os.path.join(self.context.dir, self._filename))

class SecondJobs(FirstJobs):

    def prepare(self, key):
        self._filename = 'second/s{:02d}'.format(key)
        self._name = self._filename
        self._dependencies = ['first/f{:02d}'.format(key)]

ctxt = context.Context('/tmp/clusterjobs-000/')

jobgrp = jobgroup.JobBatch(env)
for i in range(20, 0, -1):
    jobgrp.add_job(FirstJobs(ctxt, (), i))
    jobgrp.add_job(SecondJobs(ctxt, (), i))


jobgrp.update_group()
jobgrp.create_directories()
print(jobgrp.run_script())
