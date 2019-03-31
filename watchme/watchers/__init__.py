'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.logger import ( bot, RobotNamer )
from watchme.version import __version__
from watchme.defaults import (
    WATCHME_BASE_DIR,
    WATCHME_TASK_TYPES,
    WATCHME_NOTALLOWED_PARAMS
)

from watchme.command import (
    create_watcher,
    git_commit
)

from configparser import NoOptionError

from .settings import (
    get_setting,
    set_setting,
    get_section,
    print_section,
    remove_setting,
    remove_section
)

from .schedule import (
    remove_schedule,
    get_crontab,
    update_schedule,
    clear_schedule,
    schedule
)

from watchme.config import (
    read_config,
    write_config
)

import os
import re
import shutil
import sys


class Watcher(object):

    repo=None
    configfile=None

    def __init__(self, name=None, 
                       base=None, 
                       create=False, **kwargs):
        '''the watcher base loads configuration files for the user (in $HOME)
           and module, and then stores any arguments given from the caller

           Parameters
           ==========
           name: the watcher name, defaults to github
           base: the watcher base, will default to $HOME/.watchme
           create: boolean to create the watcher if doesn't exist (default False)
           kwargs: should include command line arguments from the client.

        '''
        # Set the watcher base
        self._set_base(base, create)
        self._version = __version__

        # Load the configuration
        self.load_config()


    def _set_base(self, base=None, create=False):
        ''' set the base for the watcher, ensuring that it exists.

            Parameters
            ==========
            base: the base folder of watcher repos. Uses $HOME/.watchme default
            create: create the watcher if it doesn't exist (default is False)
        '''
        if base == None:
            base = WATCHME_BASE_DIR

        # Does the watcher exist?
        self.repo = os.path.join(base, self.name)
        self.configfile = os.path.join(self.repo, 'watchme.cfg')

        # If the watcher doesn't exist and we need to create:
        if not os.path.exists(self.repo) or not os.path.exists(self.configfile):
            if create is True:
                create_watcher(self.name)   
            else:
                bot.exit('Watcher %s does not exist. Use watchme create.' % self.name)


# Config

    def save(self):
        '''save the configuration to file.'''
        write_config(self.configfile, self.config)


    def load_config(self):
        '''load a configuration file, and set the active setting for the watcher
           if the file doesn't exist, the function will exit and prompt the user 
           to create the watcher first. If the watcher section isn't yet defined,
           it will be written with a default active status set to false.
        '''
        if not hasattr(self, 'config'):
           
            # Load the configuration file if it exists (will exit if not found)
            if self.configfile != None:
                self.config = read_config(self.configfile)

            # The watcher section is added by default, args for the watcher
            if 'watcher' not in self.config.sections():
                self.config.add_section('watcher')
                self.set_setting('watcher', 'active', 'false')

                # Only update the config if we've changed it
                self.save()


    def _get_params_dict(self, pairs):
        '''iterate through parameters, make keys lowercase, and ensure
           valid format.

           Parameters
           ==========
           pairs: a list of key@value pairs to set.
        '''
        params = {}
        for pair in pairs:
            if "@" not in pair:
                bot.exit('incorrectly formatted param, must be key@value')
            key,value = pair.split('@', 1)
            key = key.lower()

            # All tasks are not allowed to have default params
            if key in WATCHME_NOTALLOWED_PARAMS:
                bot.error('%s is a default, not allowed setting by task.' % key)
                self.valid = False
            self.params[key] = value



# Add Tasks

    def add_task(self, task, task_type, params, force=False, active="true"):
        '''add a task, meaning ensuring that the type is valid, and that
           the parameters are valid for the task.

           Parameters
           ==========
           task: the Task object to add, should have a name and params and
                 be child of watchme.tasks.TaskBase
           task_type: must be in WATCHME_TASK_TYPES, meaning a client exists
           params: list of parameters to be validated (key@value)
           force: if task already exists, overwrite
           active: add the task as active (default "true")
           
        '''
        # Check again, in case user calling from client
        if not task.startswith('task'):
            bot.exit('Task name must start with "task" (e.g., task-reddit)')
       
        # Ensure it's a valid type
        if task_type not in WATCHME_TASK_TYPES:
            bot.exit('%s is not a valid type: %s' % WATCHME_TASK_TYPES)

        # Validate variables provided for task
        if task_type.startswith('url'):
            from .urls import Task

        # Convert list to dictionary
        params = self._get_params_dict(params)

        # Creating the task will validate parameters
        newtask = Task(task, params=params)

        # Exit if the new task is not valid
        if not newtask.valid:
            bot.exit('%s is not valid, will not be added.' % task)

        # Write to file (all tasks get active = True added, and type)
        self._add_task(newtask, force, active)


    def _add_task(self, task, force=False, active='true'):
        '''add a new task to the watcher, meaning we:

           1. Check first that the task doesn't already exist (if the task
              exists, we only add if force is set to true)
           2. Validate the task (depends on the task)
           3. write the task to the helper config file, if valid.

           Parameters
           ==========
           task: the Task object to add, should have a name and params and
                 be child of watchme.tasks.TaskBase
           force: if task already exists, overwrite
           active: add the task as active (default "true")
        '''
        self.load_config()

        if active not in ["true", "false"]:
            bot.exit('Active must be "true" or "false"')

        # Don't overwrite a section that already exists
        if task.name in self.config.sections():
            if not force:
                bot.exit('%s exists, use --force to overwrite.' % task.name)
            self.remove_section(task.name, save=False)

        # Add the new section
        self.config[task.name] = task.export_params(active=active)
        self.print_section(task.name)
        self.save()
        git_commit(self.repo, self.name, "ADD task %s" % task.name)

# Delete

    def delete(self):
        '''delete the entire watcher, only if not protected. Cannot be undone.
        '''
        self.load_config()

        # Check for protection
        if self.is_frozen():
            bot.exit('watcher %s is frozen, unfreeze to delete.' % self.name)
        elif self.is_protected():
            bot.exit('watcher %s is protected, turn off protection to delete.' % self.name)

        repo = os.path.dirname(self.configfile)

        # Ensure repository exists before delete
        if os.path.exists(repo):
            bot.info('Removing watcher %s' % self.name)
            shutil.rmtree(repo)
        else:
            bot.exit("%s:%s doesn't exist" %(self.name, repo))


    def remove_task(self, task):
        '''remove a task from the watcher repo, if it exists, and the
           watcher is not frozen.

           Parameters
           ==========
           task: the name of the task to remove
        '''
        if self.get_section(task) != None:
            if self.is_frozen():
                bot.exit('watcher is frozen, unfreeze first.')
            self.remove_section(task)

            # If the task has a folder, remove the entire thing
            repo = os.path.join(self.base, task)
            if os.path.exists(repo):
                shutil.rmtree(repo)

            bot.info('%s removed successfully.' % task)
            git_commit(self.repo, self.name, "REMOVE task %s" % task)

        else:
            bot.warning('Task %s does not exist.' % task)


# Inspect
    
    def inspect(self, tasks=None):
        '''inspect a watcher, or one or more tasks belonging to it. This means
           printing the configuration for the entire watcher (if tasks is None)
           or just for one or more tasks.
 
           Parameters
           ==========
           tasks: one or more tasks to inspect (None will show entire file)
        '''
        self.load_config()
        if tasks == None:
            tasks = self.config.sections()

        # If the user supplied one task:
        if not isinstance(tasks, list):
            tasks = [tasks]

        # Show all sections
        for task in tasks:
            self.print_section(task)
            bot.newline()
 

# Protection

    def protect(self, status="on"):
        '''protect a watcher, meaning that it cannot be deleted. This does
           not influence removing a task. To freeze the entire watcher,
           use the freeze() function.
        '''        
        self._set_status('watcher', 'protected', status)
        git_commit(self.repo, self.name, "PROTECT %s" % status)
        self.print_section('watcher')


    def freeze(self):
        '''freeze a watcher, meaning that it along with its tasks cannot be 
           deleted. This does not prevent the user from manual editing.
        '''
        self._set_status('watcher', 'frozen', 'on')
        git_commit(self.repo, self.name, "FREEZE")
        self.print_section('watcher')

    def unfreeze(self):
        '''freeze a watcher, meaning that it along with its tasks cannot be 
           deleted. This does not prevent the user from manual editing.
        '''
        self._set_status('watcher', 'frozen', 'off')
        git_commit(self.repo, self.name, "UNFREEZE")
        self.print_section('watcher')

    def _set_status(self, section, setting, value):
        '''a helper function to set a status, ensuring that status value
           is in "on" or "off"

           Parameters
           ==========
           status: one of "on" or "off"
           name: a value to set status for.
        '''
        if value not in ['on', 'off']:
            bot.exit('Status must be "on" or "off"')
        self.set_setting(section, setting, value)
        self.save()
        

    def is_protected(self):
        '''return a boolean to indicate if the watcher is protected or frozen.
           protected indicates no delete to the watcher, but allowed delete
           to tasks, frozen indicates no change of anything.
        '''
        protected = False
        for status in ['protected', 'frozen']:
            if self.get_setting('watcher', status) == "on":
                protected = True
        return protected
        

    def is_frozen(self):
        '''return a boolean to indicate if the watcher is frozen.
           protected indicates no delete to the watcher, but allowed delete
           to tasks, frozen indicates no change of anything.
        '''
        if self.get_setting('watcher', 'frozen') == "on":
            return True
        return False

# Status

    def _active_status(self, status='true'):
        '''a general function to change the status, used by activate and
           deactivate.
 
           Parameters
           ==========
           status: must be one of true, false
        '''
        if status not in ['true', 'false']:
            bot.exit('status must be true or false.')

        # Load the configuration, if not loaded
        self.load_config()

        # Update the status and alert the user
        self.set_setting('watcher','active', status)
        self.save()

        bot.info('[watcher|%s] active: %s' % (self.name, status)) 


    def activate(self):
        '''turn the active status of a watcher to True
        '''
        self._active_status('true')
        git_commit(self.repo, self.name, "ACTIVATE")
   
    def deactivate(self):
        '''turn the active status of a watcher to false
        '''
        self._active_status('false')
        git_commit(self.repo, self.name, "DEACTIVATE")


    def is_active(self):
        '''determine if the watcher is active by reading from the config directly
        '''
        if self.get_setting('watcher', 'active', 'true'):
            return True
        return False


# Get and Prepare Tasks

    def get_task(self, name):
        '''get a particular task, based on the name. This is where each type
           of class should check the "type" parameter from the config, and
           import the correct Task class.

           Parameters
           ==========
           name: the name of the task to load
        '''
        self.load_config()

        task = None

        # Only sections that start with task- are considered tasks
        if name in self.config._sections and name.startswith('task'):

            # Task is an ordered dict, key value pairs are entries
            params = self.config._sections[name]

            # Get the task type (if removed, consider disabled)
            task_type = params.get('type', '')

            # If we get here, validate and prepare the task
            if task_type.startswith("url"):
                from .urls import Task

            # if not valid, will return None
            task = Task(name, params)

        return task


    def _task_selected(self, task, regexp=None):
        '''check if a task is active and (if defined) passes user provided
           task names or regular expressions.

           Parameters
           ==========
           task: the task object to check
           regexp: an optional regular expression (or name) to check
        '''
        selected = True 

        # A task can be None if it wasn't found
        if task == None:
            selected = False

        # Is the task not active (undefined is active)?
        active = task.params.get('active', 'true')
        if active == "false":
            bot.info('Task %s is not active.' % name)
            selected = False
        
        # The user wants to search for a custom task name
        if regexp != None:
            if not re.search(regexp, name):
                bot.info('Task %s is selected to run.' % name)
                selected = False

        return selected


    def get_tasks(self, regexp=None):
        '''get the tasks for a watcher, possibly matching a regular expression.
           A list of dictionaries is returned, each holding the parameters for
           a task. "uri" will hold the task (folder) name, active

           Parameters
           ==========
           regexp: if supplied, the user wants to run only tasks that match
                   a particular pattern
        '''
        self.load_config()

        tasks = []
        for section in self.config._sections:

            # Get the task based on the section name
            task = self.get_task(section)

            # Check that the task should be run, and is valid
            if task != None:
                if self._task_selected(task, regexp) and task.valid:
                    tasks.append(task)

        bot.info('Found %s contender tasks.' % len(tasks))
        return tasks   


# Running Tasks

    def run_tasks(self, queue, parallel):
        '''this run_tasks function takes a list of Task objects, each
           potentially a different kind of task, and extracts the parameters
           with task.export_params(), and the running function with 
           task.export_func(), and hands these over to the multiprocessing
           worker. It's up to the Task to return some correct function
           from it's set of task functions that correspond with the variables.

           Examples
           ========

           funcs
           {'task-reddit-hpc': <function watchme.watchers.urls.tasks.get_task>}

           tasks
           {'task-reddit-hpc': [('url', 'https://www.reddit.com/r/hpc'),
                                ('active', 'true'),
                                ('type', 'urls')]}
        ''' 
        from watchme.tasks.worker import Workers

        # Run with multiprocessing
        funcs = {}
        tasks = {}

        for task in queue:

            # Export parameters and functions
            params = task.export_params()
            
            funcs[task.name] = task.export_func()
            tasks[task.name] = [(k,v) for k, v  in params.items()]


        workers = Workers()
        return workers.run(funcs, tasks)


    def run(self, regexp=None, parallel=True):
        '''run the watcher, which should be done via the crontab, including:

             - checks: the instantiation of the client already ensures that 
                       the watcher folder exists, and has a configuration,
                       and it loads.
             - parse: parse the tasks to be run
             - start: run the tasks that are defined for the watcher.
             - finish: after completion, commit to the repository changed files

           Parameters
           ==========
           regexp: if supplied, the user wants to run only tasks that match
                   a particular pattern         
           parallel: if True, use multiprocessing to run tasks (True)
                     each watcher should have this setup ready to go. 
        '''
        # Step 0: Each run session is given a fun name
        run_id = RobotNamer().generate()

        # Step 1: determine if the watcher is active.
        if not self.is_active():
            bot.info('Watcher %s is not active.' % self.name)
            return

        # Step 2: get the tasks associated with the run, a list of param dicts
        tasks = self.get_tasks()

        # Step 3: Run the tasks. This means preparing a list of funcs/params,
        # and then submitting with multiprocessing
        results = self.run_tasks(tasks, parallel)

        print(results)
 
        # Finally, finish the runs.
        #self.finish_runs(results)


# Identification

    def __repr__(self):
        return "[watcher|%s]" %self.name

    def __str__(self):
        return "[watcher|%s]" %self.name


# Settings

Watcher.remove_setting = remove_setting
Watcher.get_setting = get_setting
Watcher.get_section = get_section
Watcher.set_setting = set_setting
Watcher.remove_section = remove_section
Watcher.print_section = print_section

# Schedule 

Watcher.remove_schedule = remove_schedule
Watcher.get_crontab = get_crontab
Watcher.update_schedule = update_schedule
Watcher.clear_schedule = clear_schedule
Watcher.schedule = schedule
