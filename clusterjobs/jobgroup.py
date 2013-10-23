from __future__ import print_function

from . import context
from . import datafile

from toolbox import gfx

class JobBatch(object):
    """We assume that group are dependencies-tight."""

    def __init__(self, env):
        self.env = env
        self.jobs = []
        self.jobs_byname = {}

    def clear(self):
        self.jobs = []
        self.jobs_byname = {}

    def add_job(self, job):
        self.jobs.append(job)
        assert job.name not in self.jobs_byname, 'error: {} already in {}'.format(job.name, self.jobs_byname)
        self.jobs_byname[job.name] = job

    def add_grp(self, grp):
        for jobname, job in grp.jobs_byname.items():
            if jobname in self.jobs_byname:
                myjob = self.jobs_byname[jobname]
                assert myjob == job
            else:
                self.jobs_byname[jobname] = job


    def update_group(self):
        """ For each job, determine if the job status.

            The status of a job can be finished|running|ready|waiting|unknown.
        """
        running = self.env.running_jobs()
        running_names = set([name for name, jobid in running])

        for job in self.jobs:
            if job.name in running_names:
                job.status = 'running'
                job.uptodate = True
            else:
                job.uptodate = False

        for job in self.jobs:
            self.update_job(job)

    def _inflate_dep(self, dep):
        if type(dep) is str:
            return self.jobs_byname[dep]
        return dep

    def update_job(self, job):
        """We assume that if a job is running, its status is already set and updated."""
        if not job.uptodate:
            if all(self.env.file_exists(output_file) for output_file in job.output_files):
                job.status = 'finished'
            else:
                depjobs = [self._inflate_dep(dep) for dep in job.dependencies]
                for dep in depjobs:
                    self.update_job(dep)
                if (all(dep.status == 'finished' for dep in depjobs)
                    and all(self.env.file_exists(input_file) for input_file in job.input_files)):
                    job.status = 'ready'
                else:
                    job.status = 'waiting'
            job.uptodate = True

    def prepare_hds(self):
        self.create_directories()
        for job in self.jobs:
            job.prepare_hd()

    def to_run(self):
        job_to_run = []
        for job in self.jobs:
            if job.status == 'ready':
                job_to_run.append(job)
        return sorted(job_to_run)

    def run_script(self):
        script = ''
        for job in self.to_run():
            script += job.command() + '\n'
        return script

    def print_status(self, done=True, waiting=True):
        statuses = {'ready'   : '{}READY{}'.format(gfx.yellow, gfx.end),
                    'waiting' : '{}WAIT {}'.format(gfx.red,    gfx.end),
                    'finished': '{}DONE {}'.format(gfx.green,  gfx.end),
                    'running' : '{}ON   {}'.format(gfx.blue,   gfx.end),
                    'unknonw' : '{}???  {}'.format(gfx.grey,   gfx.end)}
        counts = {'ready'   : 0,
                  'waiting' : 0,
                  'finished': 0,
                  'running' : 0,
                  'unknonw' : 0}

        for job in self.jobs:
            counts[job.status] += 1
            if job.status == 'finished':
                if done:
                    print(statuses[job.status], ' ', job.name)
            elif job.status == 'waiting':
                if waiting:
                    print(statuses[job.status], ' ', job.name)
            else:
                print(statuses[job.status], ' ', job.name)

        print('done/on/ready/waiting: {}/{}/{}/{}'.format(
                gfx.green  + str(counts['finished']) + gfx.end,
                gfx.blue   + str(counts['running'] ) + gfx.end,
                gfx.yellow + str(counts['ready']   ) + gfx.end,
                gfx.red    + str(counts['waiting'] ) + gfx.end))

    def create_directories(self):
        filepaths = []
        for job in self.jobs:
            for outfile in job.output_files:
                filepaths.append(outfile)
            for infile in job.input_files:
                filepaths.append(infile)
        datafile.create_directories(filepaths)
