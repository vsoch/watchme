'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.logger import bot
from watchme.utils import (
    write_file,
    write_json
)

import shutil
import os

class TaskBase(object):

    def __init__(self, name, params={}, **kwargs):

        # Ensure subclass was created correctly
        for req in ['required_params', 'type', 'export_func']:
            if not hasattr(self, req):
                bot.exit('A Task must have a %s function or attribute.' % req)

        self.name = name
        self.valid = False
        self.params = {}
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
        if func != None:
            return func(**params)
        bot.error('Cannot find function.')



# Saving


    def _save_list(self, results, repo, func, file_name):
        '''general function to perform saving a list of content to json,
           text, or moving paths. Used by save_file_list, save_json_list,
           and save_text_list.

           Parameters
           ==========
           results: list of results, assumed to be the correct type
           repo: the repository base with the task folder
           func: the function to call.
           file_name: the base file name to use.
        '''
        file_name, ext = os.path.splitext(file_name)
        files = []

        for r in range(len(results)):
            result = results[r]
            filename = "%s-%s%s" %(file_name, str(r), ext)
            saved = func(result, repo, filename)
            files.append(saved)

        return files

    def _save_text(self, result, repo, file_name=None):
        '''save a general text object to file.
 
           Parameters
           ==========
           result: the result object to save, should be path to a file
           repo: the repository base with the task folder
        '''
        file_name = self.params.get('file_name', file_name) or 'result.txt'
        task_folder = os.path.join(repo, self.name)
        destination = os.path.join(task_folder, file_name)
        write_file(destination, result)
        return destination

    def _save_file(self, result, repo, file_name=None):
        '''for a result that exists, move the file to final destination.
 
           Parameters
           ==========
           result: the result object to save, should be path to a file
           repo: the repository base with the task folder
        '''
        if os.path.exists(result):
            name = os.path.basename(result)
            file_name = self.params.get('file_name', file_name) or name
            task_folder = os.path.join(repo, self.name)

            # HOME/.watchme/watcher/<task>/<result>
            destination = os.path.join(task_folder, file_name)
            shutil.move(result, destination)

            # <task>/<result>     
            return os.path.join(name, file_name)

        bot.warning('%s does not exist.' % result)
        
    def _save_json(self, result, repo, file_name=None):
        '''for a result that is a dictionary or list, save as json
 
           Parameters
           ==========
           result: the result object to save, should be dict or list
        '''
        file_name = self.params.get('file_name', file_name) or 'result.json'
        destination = os.path.join(repo, self.name, file_name)
        write_json(result, destination)
        return destination


    def _save_json_list(self, results, repo):
        '''A wrapper around save json for a list, handles file naming.
 
           Parameters
           ==========
           results: the results to save, should a list
        '''
        file_name = self.params.get('file_name', 'result.json')
        return self._save_list(results, repo, self._save_json, file_name)


    def _save_file_list(self, results, repo):
        '''for a list of results that exist, move the files to 
           final destination.
 
           Parameters
           ==========
           results: list of paths to a file, those not existing are skipped
           repo: the repository base with the task folder
        '''
        file_name = self.params.get('file_name', os.path.basename(result))
        return self._save_list(results, repo, self._save_file, file_name)


    def _save_text_list(self, results, repo):
        '''for a list of general text results, write them to output files.
 
           Parameters
           ==========
           results: list of string results to write to file
           repo: the repository base with the task folder
        '''
        file_name = self.params.get('file_name', 'result.txt')
        return self._save_list(results, repo, self._save_text, file_name)
