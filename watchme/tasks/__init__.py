'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

# Multiprocess Workers
from .worker import Workers

class TaskBase(object):

    params = dict()

    def __init__(self, name, params=[], **kwargs):

        # Ensure subclass was created correctly
        for required in ['required_params', 'type']:
            if not hasattr(self, required):
                bot.exit('A Task must have a %s attribute.' % required)

        self.name = name
        self.set_params(params)
        self.validate()


    def get_type(self):
        '''get the watcher type.
        '''
        return self.type


# Parameters

    def set_params(self, params):
        '''iterate through parameters, ensure they are valid

           Parameters
           ==========
           params: a list of key@value pairs to set.
        '''
        for pair in params:
            if "@" not in pair:
                bot.exit('incorrectly formatted param, must be key@value')
            key,value = pair.split('@', 1)
            self.params[key.lower()] = value


    def export_params(self, active="true"):
        '''export parameters, meaning returning a dictionary of the task
           parameters plus the addition of the task type and active status.
        '''
        params = self.params.copy()
        params['active'] = active
        params['type'] = self.type
        return params


    def validate(self):
        '''validate the parameters set for the Task. Exit if there are any
           errors. Ensure required parameters are defined, and have correct
           values.
        '''
        for param in self.required_params:
            if param not in self.params:
                bot.exit('Missing required parameter: %s' % param)

        # The url must begin with http
        if not self.params['url'].startswith('http'):
            bot.exit('%s is not a valid url.' % self.params['url'])

        # Call subclass validation function
        self._validate()

    def _validate(self):
        '''validation function intended to be implemented by subclass.
        '''
        pass
