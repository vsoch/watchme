'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.logger import (bot, RobotNamer)
from watchme.version import __version__
from watchme.defaults import (
    WATCHME_BASE_DIR,
    WATCHME_TASK_TYPES,
    WATCHME_NOTALLOWED_PARAMS
)

from watchme.command import (
    create_watcher,
    write_timestamp,
    get_watchers,
    git_commit,
    git_add
)

from configparser import NoOptionError

from .data import (
    export_dict
)

from .settings import (
    get_setting,
    get_section,
    has_setting,
    has_section,
    print_section,
    print_add_task,
    remove_setting,
    remove_section,
    set_setting
)

from .schedule import (
    remove_schedule,
    get_crontab,
    get_job,
    has_schedule,
    update_schedule,
    clear_schedule,
    schedule
)

from watchme.config import (
    read_config,
    write_config
)

from watchme.utils import (
    mkdir_p,
    write_file,
    write_json
)

import os
import re
import shutil
import json
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
        self.base = base
        self.repo = os.path.join(self.base, self.name)
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


    def edit_task(self, name, action, key, value=None):
        '''edit a task, meaning doing an addition (add), update (update), or
           "remove", All actions require a value other than remove.

           Parameters
           ==========
           name: the name of the task to update
           action: the action to take (update, add, remove) a parameter
           key: the key to update
           value: the value to update
        '''

        if not self.has_task(name):
            bot.exit('%s is not a task defined by %s' % (name, self.name))

        if action not in ['update', 'add', 'remove']:
            bot.exit('Action must be update, add, or remove')

        if action in ['update', 'add'] and value == None:
            bot.exit('A value must be provided for the %s action' % action)

        # Add, and it doesn't exist so it's okay
        if action == "add" and key not in self.config[name]:
            bot.info('Adding %s:%s to %s' % (key, value, name))
            self.set_setting(name, key, value)

        # Already exists, encourage user to update
        elif action == "add" and key in self.config[name]:
            bot.exit('%s already exists. Use "update" action to change.' % key)

        # Update, and it's a valid choice
        elif action == 'update' and key in self.config[name]:
            bot.info('Updating %s to %s in %s' % (key, value, name))
            self.set_setting(name, key, value)

        # Update, and it's not a valid choice
        elif action == 'update' and key not in self.config[name]:
            bot.exit('%s is not found in config, cannot be updated.' % key)

        # Remove, and it's a valid choice
        elif action == "remove" and key in self.config[name]:
            bot.info('Removing %s' % key)
            del self.config[name][key]

        # Remove, and it's not a valid choice
        elif action == "remove" and key not in self.config[name]:
            bot.exit('%s is not found in config, cannot be removed.' % key)
        self.save()


    def has_section(self, name):
        '''returns True or False to indicate if the watcher has a specified
           section. To get a task, use self.has_task.

           Parameters
           ==========
           name: the name of the section to check for.
        '''
        self.load_config()
        if name in self.config._sections:
            return True
        bot.warning('%s not found for watcher %s' %(name, self.name))
        return False


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
            key, value = pair.split('@', 1)
            key = key.lower()

            # All tasks are not allowed to have default params
            if key in WATCHME_NOTALLOWED_PARAMS:
                bot.error('%s is a default, not allowed setting by task.' % key)
                self.valid = False
            params[key] = value
        return params


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

        elif task_type == 'psutils':
            from .psutils import Task

        elif task_type == 'results':
            from .results import Task

        else:
            bot.exit('task_type %s not properly added to Watcher' % task_type)

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

        # If the task folder doesn't exist, recreate it.
        task_folder = os.path.join(self.repo, task.name)
        if not os.path.exists(task_folder):
            mkdir_p(task_folder)
            git_add(self.repo, task.name)

        # Commit changes
        git_commit(repo=self.repo, task=self.name,
                   message="ADD task %s" % task.name)

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
            bot.exit("%s:%s doesn't exist" % (self.name, repo))


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
            repo = os.path.join(self.repo, task)
            if os.path.exists(repo):
                shutil.rmtree(repo)

            bot.info('%s removed successfully.' % task)
            git_commit(self.repo, self.name, "REMOVE task %s" % task)

        else:
            bot.warning('Task %s does not exist.' % task)


# Inspect
    
    def inspect(self, tasks=None, create_command=False):
        '''inspect a watcher, or one or more tasks belonging to it. This means
           printing the configuration for the entire watcher (if tasks is None)
           or just for one or more tasks.
 
           Parameters
           ==========
           tasks: one or more tasks to inspect (None will show entire file)
           create_command: if True, given one or more tasks, print the command
                           to create them.
        '''
        self.load_config()
        if tasks == None:
            tasks = self.config.sections()

        # If the user supplied one task:
        if not isinstance(tasks, list):
            tasks = [tasks]

        # Show all sections
        for task in tasks:

            # If the user doesn't want to see the create command:
            if create_command is False:
                self.print_section(task)
                bot.newline()
            else:
                self.print_add_task(task)


    def list(self, quiet=False):
        '''list the watchers. If quiet is True, don't print to the screen.'''
        watchers = get_watchers(base=self.base, quiet=quiet)
        return watchers

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

    def _active_status(self, status='true', name=None):
        '''a general function to change the status, used by activate and
           deactivate.
 
           Parameters
           ==========
           status: must be one of true, false
           name: if not None, we are deactivating a task (not the watcher)
        '''
        # Load the configuration, if not loaded
        self.load_config()

        if name == None:
            name = 'watcher'

        # Cut out early if section not in config
        if name not in self.config._sections:
            bot.exit('%s is not a valid task or section' % name)     

        if status not in ['true', 'false']:
            bot.exit('status must be true or false.')

        # Update the status and alert the user
        self.set_setting(name, 'active', status)
        self.save()

        # Return the message for the commit
        message = "ACTIVE"
        if status == "false":
            message = "DEACTIVATE"

        # Add the task name
        if name != None:
            message = "%s task %s" %(message, name)

        bot.info('[%s|%s] active: %s' % (name, self.name, status)) 
        return message

    def activate(self, task=None):
        '''turn the active status of a watcher to True
        '''
        message = self._active_status('true', task)
        git_commit(self.repo, self.name, message)
   

    def deactivate(self, task=None):
        '''turn the active status of a watcher to false. If a task is provided,
           update the config value for the task to be false.
        '''
        # If no task defined, user wants to deactiate watcher
        message = self._active_status('false', task)
        git_commit(self.repo, self.name, message)


    def is_active(self, task=None):
        '''determine if the watcher is active by reading from the config directly
           if a task name is provided, check the active status of the task
        '''
        if task == None:
            task = 'watcher'
        if self.get_setting(task, 'active', default='true') == "true":
            return True
        return False


# Get a Decorator

    def get_decorator(self, name):
        '''instantiate a task object for a decorator. Decorators must start
           with "decorator-" and since they are run on the fly, we don't
           find them in the config.

           Parameters
           ==========
           name: the name of the task to load
        '''

        task = None

        # Only psutils has decorators
        if name.startswith('decorator-psutils'):
            from .psutils import Task

        else:
            bot.exit('Type %s is not recognized in get_decorator' % name)

        task = Task(name)
        return task


# Get and Prepare Tasks

    def has_task(self, name):
        '''returns True or False to indicate if the watcher has a specified
           task.
        '''
        self.load_config()
        if self.has_section(name) and name.startswith('task'):
            return True
        return False


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

            elif task_type == 'psutils':
                from .psutils import Task

            elif task_type == 'results':
                from .results import Task

            else:
                bot.exit('Type %s not properly set up in get_task' % task_type)

            # if not valid, will return None
            task = Task(name, params)

        return task


    def _task_selected(self, task, regexp=None, active=True):
        '''check if a task is active and (if defined) passes user provided
           task names or regular expressions.

           Parameters
           ==========
           task: the task object to check
           regexp: an optional regular expression (or name) to check
           active: a task is selected if it's active (default True)
        '''
        selected = True 

        # A task can be None if it wasn't found
        if task == None:
            selected = False

        # Is the task not active (undefined is active)?
        is_active = task.params.get('active', 'true')
        if is_active == "false" and active == True:
            bot.info('Task %s is not active.' % task)
            selected = False
        
        # The user wants to search for a custom task name
        if regexp != None and task != None:
            if not re.search(regexp, task.name):
                bot.info('Task %s is not selected to run.' % task)
                selected = False

        return selected


    def get_tasks(self, regexp=None, quiet=False, active=True):
        '''get the tasks for a watcher, possibly matching a regular expression.
           A list of dictionaries is returned, each holding the parameters for
           a task. "uri" will hold the task (folder) name, active

           Parameters
           ==========
           regexp: if supplied, the user wants to run only tasks that match
                   a particular pattern
           quiet: If quiet, don't print the number of tasks found
           active: only return active tasks (default True)
        '''
        self.load_config()

        tasks = []
        for section in self.config._sections:

            # Get the task based on the section name
            task = self.get_task(section)

            # Check that the task should be run, and is valid
            if task != None:
                if self._task_selected(task, regexp, active) and task.valid:
                    tasks.append(task)

        if quiet == False:
            bot.info('Found %s contender tasks.' % len(tasks))
        return tasks   


# Running Tasks

    def run_tasks(self, queue, parallel=True, show_progress=True):
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
        if parallel is True:
            return self._run_parallel(queue, show_progress)
        
        # Otherwise, run in serial
        results = {}

        # Progressbar
        total = len(queue)
        progress = 1

        for task in queue:
            prefix = "[%s:%s/%s]" % (task.name, progress, total)
            if show_progress is True:
                bot.show_progress(progress, total, length=35, prefix=prefix)
            else:
                bot.info('Running %s' % prefix)
            results[task.name] = task.run()
            progress += 1

        return results


    def _run_parallel(self, queue, show_progress=True):
        ''' run tasks in parallel using the Workers class. Returns a dictionary
            (lookup) wit results, with the key being the task name

            Parameters
            ==========
            queue: the list of task objects to run
        '''
        from watchme.tasks.worker import Workers

        # Run with multiprocessing
        funcs = {}
        tasks = {}

        for task in queue:

            # Export parameters and functions            
            funcs[task.name] = task.export_func()
            tasks[task.name] = task.export_params()

        workers = Workers(show_progress=show_progress)
        return workers.run(funcs, tasks)


    def run(self, regexp=None, parallel=True, test=False, show_progress=True):
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
           test: run in test mode (no saving of results)
           show_progress: if True, show progress bar instead of task information
                          (defaults to True)
        '''
        # Step 0: Each run session is given a fun name
        run_id = RobotNamer().generate()

        # Step 1: determine if the watcher is active.
        if self.is_active() == False and test is False:
            bot.exit('Watcher %s is not active.' % self.name)

        # Step 2: get the tasks associated with the run, a list of param dicts
        tasks = self.get_tasks(regexp=regexp)

        # Step 3: Run the tasks. This means preparing a list of funcs/params,
        # and then submitting with multiprocessing
        results = self.run_tasks(tasks, parallel, show_progress)

        # Finally, finish the runs.
        if test is False:
            self.finish_runs(results)
        else:
            # or print results to the screen
            print(json.dumps(results, indent=4))


    def finish_runs(self, results):
        '''finish runs should take a dictionary of results, with keys as the
           folder name, and for each, depending on the result type,
           write the result to file (or update file) and then commit
           to git.

           Parameters
           ==========
           results: a dictionary of tasks, with keys as the task name, and
                    values as the result.
        '''
        if results == None:
            return

        for name, result in results.items():
            task_folder = os.path.join(self.repo, name)

            if name.startswith('task'):
                task = self.get_task(name)
 
            # A decorator is run on the fly (not in config)
            elif name.startswith('decorator'):
                task = self.get_decorator(name)

            # We only allow tasks and decorators
            else:
                bot.warning('%s is not task or decorator, skipping.' % name)
                continue

            # Ensure that the task folder exists
            if not os.path.exists(task_folder):
                mkdir_p(task_folder)
                git_add(self.repo, task_folder)

            # Files to be added to the repo via git after
            files = task.write_results(result, self.repo)

            # Add files to git, and commit
            files.append(write_timestamp(repo=self.repo, task=name))
            git_add(repo=self.repo, files=files)
            git_commit(repo=self.repo,
                       task=self.name,
                       message="ADD results %s" % name)

# Identification

    def __repr__(self):
        return "[watcher|%s]" % self.name

    def __str__(self):
        return "[watcher|%s]" % self.name


# Settings

Watcher.remove_setting = remove_setting
Watcher.get_setting = get_setting
Watcher.get_section = get_section
Watcher.has_setting = has_setting
Watcher.has_section = has_section
Watcher.set_setting = set_setting
Watcher.remove_section = remove_section
Watcher.print_section = print_section
Watcher.print_add_task = print_add_task

# Schedule 

Watcher.remove_schedule = remove_schedule
Watcher.get_crontab = get_crontab
Watcher.update_schedule = update_schedule
Watcher.has_schedule = has_schedule
Watcher.get_job = get_job
Watcher.clear_schedule = clear_schedule
Watcher.schedule = schedule

# Data

Watcher.export_dict = export_dict
