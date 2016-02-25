"""Test the code of MotorSet"""
from __future__ import print_function, division
import unittest
import os

import dotdot
from clusterjobs import datafile

user = os.path.expanduser('~')

class TestDatafile(unittest.TestCase):

    def test_normpath(self):
        self.assertEqual(datafile.normpath('/usr/local/', 'include/eigen', 'eigen.h'),
                         '/usr/local/include/eigen/eigen.h')
        self.assertEqual(datafile.normpath('/usr/local/', 'include/eigen', 'eigen.h'),
                         '/usr/local/include/eigen/eigen.h')
        self.assertEqual(datafile.normpath('~/usr/local/'),
                         user + '/usr/local')


if __name__ == '__main__':
    unittest.main()
