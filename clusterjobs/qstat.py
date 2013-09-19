"""Preparing the context, and launching the qsub command appropriately"""

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '../../..')))

import re
import subprocess
import xml.etree.ElementTree as ET
#import config

is_qsub_available = None
def qsub_available():
    global is_qsub_available
    if is_qsub_available is None:
        devnull = open(os.devnull)
        is_qsub_available = subprocess.call(['which', 'qsub'], stdout=devnull, stderr=devnull) == 0
    return is_qsub_available

def get_running_jobs(owner):
    """Get running jobs from qstat from a specific owner"""
    try:
        p = subprocess.Popen(["qstat", "-x"], stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
    except OSError:
        return tuple()

    try:
        jobs = ET.fromstring(stdout)
    except ET.ParseError:
        print("# warning: error parsing qstat xml output (of length {})".format(len(stdout)))
        return []


    my_jobs = []
    for job in jobs:
        if owner+'@' == job.find('Job_Owner').text[:len(owner+'@')]:
            my_jobs.append((job.find('Job_Name').text, job.find('Job_Id')))

    return my_jobs

