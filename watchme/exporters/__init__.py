'''

Copyright (C) 2019 Vanessa Sochat
Copyright (C) 2019 Antoine Solnichkin

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.logger import bot

class ExporterBase(object):

    required_params = []

    def __init__(self, name, params={}, **kwargs):

        self.name = name
        self.valid = False
        self.params = {}
        self.set_params(params)
        self.validate()

            
    def get_type(self):
        '''get the exporter type.
        '''
        return self.type

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


    def push(self, result):
        '''push dummy function, optional for subclass to implement.
        '''
        bot.warning('push is not implemented for %s' % self.type)


    def export(self, result, task):
        '''the export function is the entrypoint to export data for an
           exporter. Based on the data type, we call any number of supporting
           functions. If True is returned, the data is exported. If False is
           returned, there was an error. If None is returned, there is no
           exporter defined for the data type.

           Parameters
           ==========
           result: the result object to export, a string, list, dict, or file
           task: the task object associated.
        '''
        bot.warning('export is not implemented for %s' % self.type)


    def export_params(self, active="true"):
        '''export parameters, meaning returning a dictionary of the task
           parameters plus the addition of the task type and active status.
        '''
        params = self.params.copy()
        params['active'] = active
        params['type'] = self.type
        return params

    # Validation

    # For now, it should always be valid as no required parameters are defined.
    def validate(self):
        '''validate the parameters set for the Exporter. Exit if there are any
           errors. Ensure required parameters are defined, and have correct
           values.
        '''
        self.valid = True

        for param in self.required_params:
            if param not in self.params:
                bot.error('Missing required parameter: %s' % param)
                self.valid = False

        # If the exporter has some custom validation, do it here
        if self.valid is True and hasattr(self, "_validate"):
            self._validate()
