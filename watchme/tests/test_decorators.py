#!/usr/bin/python

# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from watchme import get_watcher
from watchme.command import create_watcher
import unittest
import tempfile
import shutil


print("########################################################### test_client")


class TestDecorators(unittest.TestCase):

    def setUp(self):
        self.base = tempfile.mkdtemp()
        self.repo = create_watcher('pancakes', base=self.base)
        self.cli = get_watcher('pancakes', base=self.base)
        
    def tearDown(self):
        shutil.rmtree(self.base)

    def test_psutils_monitor(self):
        '''test creation function, and basic watcher config'''
        print("Testing psutilsc.decorators.TerminalRunner")
        from watchme.watchers.psutils.decorators import TerminalRunner
        runner = TerminalRunner('sleep 2')
        runner.run()
        timepoints = runner.wait()
        self.assertTrue(len(timepoints)==1)

if __name__ == '__main__':
    unittest.main()
