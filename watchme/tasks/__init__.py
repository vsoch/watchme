'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.logger import bot

class TaskBase(object):

    params = {}
    valid = False

    def __init__(self, name, params={}, **kwargs):

        # Ensure subclass was created correctly
        for req in ['required_params', 'type', 'export_func']:
            if not hasattr(self, req):
                bot.exit('A Task must have a %s function or attribute.' % req)

        self.name = name
        self.set_params(params)
        self.validate()

    def get_type(self):
        '''get the watcher type.
        '''
        return self.type


# Identification

    def __repr__(self):
        return "[task|%s]" %self.name

    def __str__(self):
        return "[task|%s]" %self.name


# Parameters

    def set_params(self, params):
        '''iterate through parameters, set into dictionary.

           Parameters
           ==========
           params: a list of key@value pairs to set.
        '''
        for key,value in params.items():
            key = key.lower()
            self.params[key] = value


    def export_params(self, active="true"):
        '''export parameters, meaning returning a dictionary of the task
           parameters plus the addition of the task type and active status.
        '''
        params = self.params.copy()
        params['active'] = active
        params['type'] = self.type
        return params


# Validation

    def validate(self):
        '''validate the parameters set for the Task. Exit if there are any
           errors. Ensure required parameters are defined, and have correct
           values.
        '''
        self.valid = True

        for param in self.required_params:
            if param not in self.params:
                bot.error('Missing required parameter: %s' % param)
                self.valid = False

        # Call subclass validation function
        self._validate()

    def _validate(self):
        '''validation function intended to be implemented by subclass.
        '''
        pass


# Run Single Task

    def run(self):
        '''run an isolated task, meaning no update or communication with
           the watcher. This will return the raw result.
        '''
        params = self.export_params()
        func = self.export_func()
        return func(**params)
