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

    def __init__(self, name, params={}, **kwargs): 

        self.type = 'urls'

        # Handles setting the name, setting params, and validate
        super(Task, self).__init__(name, params, **kwargs)

    def _validate(self):
        '''additional validation function, called by validate() of 
           superclass. Here we assume all required self.params are included.
           If an parameter is found to be invalid, self.valid should be set
           to False
        '''
        # The url must begin with http
        if not self.params['url'].startswith('http'):
            bot.error('%s is not a valid url.' % self.params['url'])
            self.valid = False

    def export_func(self):
        '''this function should return the correct task (from the tasks.py
           in the same folder) based on some logic of the params that are given
           by the user (self.params). If there is only one kind of function for
           the task, it's fairly easy to import and return it here. This
           function should take no arguments, but instead use the self.params
           already provided in the client.
        '''
        name = self.params.get('func', 'get_task')

        if name == 'get_task':
            from .tasks import get_task as func
        elif name == 'download_task':
            from .tasks import download_task as func
        elif name == 'post_task':
            from .tasks import post_task as func
        elif name == "get_url_selection":
            from .tasks import get_url_selection as func
        else:
            func = None

        bot.debug('function name is %s' % name)
        return func
