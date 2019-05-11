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
import json
import os


print("########################################################### test_client")


class TestClient(unittest.TestCase):

    def setUp(self):
        self.base = tempfile.mkdtemp()
        self.repo = create_watcher('pancakes', base=self.base)
        self.cli = get_watcher('pancakes', base=self.base)
        
    def tearDown(self):
        shutil.rmtree(self.base)

    def test_create(self):
        '''test creation function, and basic watcher config'''
        print("Testing watcher creation")
        self.assertTrue(os.path.exists(self.repo))        
        self.assertTrue(os.path.exists(os.path.join(self.repo, 'watchme.cfg')))  
        already_exists = create_watcher('pancakes', base=self.base)
        self.assertEqual(already_exists, None)
        self.assertEqual(self.cli.name, 'pancakes')
        self.assertEqual(self.cli.base, self.base)

    def test_activate(self):
        print("Testing watcher activation")
        self.assertEqual(self.cli.is_active(), False)
        self.cli.activate()
        self.assertEqual(self.cli.is_active(), True)
        self.cli.deactivate()
        self.assertEqual(self.cli.is_active(), False)

    def test_freeze(self):
        print("Testing watcher freezing")
        self.assertEqual(self.cli.is_frozen(), False)
        self.cli.freeze()
        self.assertEqual(self.cli.is_frozen(), True)
        self.cli.unfreeze()
        self.assertEqual(self.cli.is_frozen(), False)

        print("Testing watcher protect")
        self.assertEqual(self.cli.is_protected(), False)
        self.cli.protect("on")
        self.assertEqual(self.cli.is_protected(), True)
        self.cli.protect("off")
        self.assertEqual(self.cli.is_protected(), False)

    def test_watcher_task(self):
        '''test adding a task
        '''
        print("Testing watcher.add_task")
        self.cli.add_task('task-pancakes', 'urls', params=['url@https://www.google.com'])
        self.assertTrue(os.path.exists(os.path.join(self.repo, 'task-pancakes')))

        print("Testing task activation")
        self.assertEqual(self.cli.is_active('task-pancakes'), True)
        self.cli.deactivate('task-pancakes')
        self.assertEqual(self.cli.is_active('task-pancakes'), False)
        self.cli.activate('task-pancakes')
        self.assertEqual(self.cli.is_active('task-pancakes'), True)

        print("Testing has_task")
        self.assertTrue(self.cli.has_task('task-pancakes'))
        self.assertEqual(self.cli.has_task('task_pancakes'), False)

        print("Testing settings")
        self.cli.protect("off")
        off = self.cli.get_setting('watcher', 'protected')
        self.assertEqual(off, "off")
        self.cli.set_setting('watcher', 'protected', 'on')
        on = self.cli.get_setting('watcher', 'protected')
        self.assertEqual(on, "on")

        print('Testing get_section')
        section = self.cli.get_section('watcher')
        self.assertEqual(section.name, 'watcher')
        section = self.cli.get_section('task-pancakes')
        self.assertEqual(section.name, 'task-pancakes')
        section = self.cli.get_section('doesntexist')
        self.assertEqual(section, None)

        print('Testing get_task')
        task = self.cli.get_task('pancakes')
        self.assertEqual(task, None)
        task = self.cli.get_task('task-pancakes')
        tasks = self.cli.get_tasks()
        self.assertTrue(isinstance(tasks, list))
        self.assertEqual(len(tasks), 1)

        print('Testing Task')
        self.assertEqual(task.name, 'task-pancakes')
        params = task.export_params()
        print(params)
        correct = {'active': 'true',
                   'type': 'urls',
                   'url': 'https://www.google.com'}
        for key, value in correct.items():
            self.assertTrue(key in params)
            self.assertEqual(value, params[key])
        self.assertTrue(task.valid)
        self.assertEqual(task.type, 'urls')

        print("Testing inspect and list")
        self.cli.inspect()
        watchers = self.cli.list()
        self.assertTrue('pancakes' in watchers)
        self.assertTrue(isinstance(watchers, list))

    def test_schedule(self):
        self.assertEqual(self.cli.has_schedule(), False)


if __name__ == '__main__':
    unittest.main()
