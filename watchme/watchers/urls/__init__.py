'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


'''

from watchme.tasks import TaskBase
from watchme.logger import bot
import os
import sys

class Task(TaskBase):

    required_params = ['url']

    def __init__(self, name, params=[], **kwargs): 

        self.type = 'urls'

        # Handles setting the name, setting params, and validate
        super(Task, self).__init__(name, params, **kwargs)

    def _validate(self):
        '''additional validation function, called by validate() of 
           superclass. Here we assume all required params are included.
        '''
        # The url must begin with http
        if not self.params['url'].startswith('http'):
            bot.exit('%s is not a valid url.' % self.params['url'])

    def run_task(self):
        '''run a function to run for a task. including:
           1. checking that the task is active
           2. checking that the watcher type matches
           3. validating the variables provided in the section
           4. running the task

           Parameters
           ==========
           section: the (dictionary) lookup of variables for a task,
                    each Task has a known set of variables to use.
        '''

    # TODO: need to step through running of task (should this be get_task?)
    # - write functions in "tasks" to import
