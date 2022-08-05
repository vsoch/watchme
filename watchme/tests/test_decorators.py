#!/usr/bin/python

__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from watchme import get_watcher
from watchme.command import create_watcher
import unittest
import tempfile
import shutil


print("####################################################### test_decorators")


class TestDecorators(unittest.TestCase):
    def setUp(self):
        self.base = tempfile.mkdtemp()
        self.repo = create_watcher("pancakes", base=self.base)
        self.cli = get_watcher("pancakes", base=self.base)

    def tearDown(self):
        shutil.rmtree(self.base)

    def test_psutils_monitor(self):
        """test creation function, and basic watcher config"""
        print("Testing psutilsc.decorators.TerminalRunner")
        from watchme.tasks.decorators import TerminalRunner

        runner = TerminalRunner("sleep 2")
        runner.run()
        timepoints = runner.wait("monitor_pid_task")
        self.assertTrue(len(timepoints) == 1)


if __name__ == "__main__":
    unittest.main()
