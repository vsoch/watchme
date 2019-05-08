'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


'''

from watchme.tasks import TaskBase
from watchme.logger import bot
from watchme.utils import ( get_user, get_host )
import os
import sys

class Task(TaskBase):
    '''a results task aims to use WatchMe as a database, meaning the functions
       are optimized to collect and record results.'''

    required_params = []

    def __init__(self, name, params={}, **kwargs): 

        self.type = 'results'

        # Handles setting the name, setting params, and validate
        super(Task, self).__init__(name, params, **kwargs)

    def export_func(self):
        '''this function should return the correct task (from the tasks.py
           in the same folder) based on some logic of the params that are given
           by the user (self.params). If there is only one kind of function for
           the task, it's fairly easy to import and return it here. This
           function should take no arguments, but instead use the self.params
           already provided in the client.
        '''
        name = self.params.get('func', 'from_env_task')

        if name == 'from_env_task':
            from .tasks import from_env_task as func
        else:
            func = None

        return func
