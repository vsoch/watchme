'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.logger import ( bot, RobotNamer )
from watchme.version import __version__
from watchme.defaults import WATCHME_BASE_DIR

from watchme.command.create import create_watcher
from configparser import NoOptionError

from .settings import (
    get_setting,
    get_settings,
    get_and_update_setting,
    load_config,
    load_config_user,
    load_envars,
    remove_setting,
    update_settings
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
import sys


class WatcherBase(object):

    repo = None
    configfile = None

    def __init__(self, name=None, 
                       base=None, 
                       create=False, 
                       watcher_type = None, **kwargs):
        '''the watcher base loads configuration files for the user (in $HOME)
           and module, and then stores any arguments given from the caller

           Parameters
           ==========
           name: the watcher name, defaults to github
           base: the watcher base, will default to $HOME/.watchme
           create: boolean to create the watcher if doesn't exist (default False)
           watcher_type: defaults to "urls" (only option at the moment)
           kwargs: should include command line arguments from the client.

        '''
        # Set the watcher base
        self._set_base(base, create)
        self._version = __version__

        # If the watcher needs to load secrets from the environment, etc.
        self.load_secrets()

        # Load the configuration
        self.load_config(watcher_type)


    def _set_base(self, base=None, create=False):
        ''' set the base for the watcher, ensuring that it exists.
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
                bot.exit('%s does not exist. Use watchme create.' % self.name)


    def load_secrets(self):
        '''the subclass helper should implement this function to load 
           environment variables, etc. from the user.
        '''
        pass


    def load_config(self, watcher_type=None):
        '''load a configuration file, and set the active setting for the watcher
           if the file doesn't exist, the function will exit and prompt the user 
           to create the watcher first. If the watcher section isn't yet defined,
           it will be written with a default active status set to false.
        '''
        # Load the configuration file if it exists (will exit if not found)
        if self.configfile != None:
            self.config = read_config(self.configfile)

        # The watcher section is added by default, args for the watcher
        if 'watcher' not in self.config.sections():
            self.config.add_section('watcher')
            self.config['watcher']['active'] = "false"

            # Does the watcher type not exist?
            if 'type' not in self.config['watcher']:
                self.config['watcher']['type'] = watcher_type or WATCHME_DEFAULT_TYPE

            # Only update the config if we've changed it
            write_config(self.configfile, self.config)


# Status

    def activate(self):
        '''turn the active status of a watcher to True
        '''
        if not hasattr(self, 'config'):
            self.load_config()
        self.config['watcher']['active'] = "true"
            
   
    def deactivate(self):
        '''turn the active status of a watcher to false
        '''
        if not hasattr(self, 'config'):
            self.load_config()
        self.config['watcher']['active'] = "false"

    def is_active(self):
        '''determine if the watcher is active by reading from the config directly
        '''
        if not hasattr(self, 'config'):
            self.load_config()
        if self.config['watcher']['active'] == "true":
            return True
        return False

    def get_type(self):
        '''get the watcher type.
        '''
        if not hasattr(self, 'config'):
            self.load_config()
        return self.config['watcher']['type']

# Actions

    def get_tasks(self, regexp=None):
        '''get the tasks for a watcher, possibly matching a regular expression.
        '''
        if not hasattr(self, 'config'):
            self.load_config()

        tasks = []
        for section in config._sections:

            task = config._sections[section]

            # A task must start with task-
            if not section.startswith('task-'):
                continue

            # The user wants to search for a custom task name
            if regexp != None:
                if re.search(regexp, section):
                    tasks.append(task)
            else:
                tasks.append(task)

        return tasks       
   

    def _run_tasks(self, task):
        '''this run_task function should be implemented by the Watcher, as
           tasks for different watchers will be different
        '''
        pass

    def run_tasks(self, tasks, parallel):
        '''this run_task function should be implemented by the Watcher, as
           tasks for different watchers will be different
        ''' 
        self.start()        
        self._run_tasks()
        # TODO: need to figure out multiprocessing here.

    def run(self, parallel=True):
        '''run the watcher, which should be done via the crontab, including:

             - checks: the instantiation of the client already ensures that 
                       the watcher folder exists, and has a configuration,
                       and it loads.
             - parse: parse the tasks to be run
             - start: run the tasks that are defined for the watcher.
             - finish: after completion, commit to the repository changed files

           Parameters
           ==========
           parallel: if True, use multiprocessing to run tasks (True)
                     each watcher should have this setup ready to go. 
        '''
        # Step 0: Each run session is given a fun name
        self.run_id = RobotNamer().generate()

        # Step 1: determine if the watcher is active.
        if not self.is_active():
            bot.info('Watcher %s is not active.' % self.name)
            return

        # Step 2: get the tasks associated with the run
        tasks = self.get_tasks()

        # TODO: need to run these with multiprocessing, but first
        # need to create the tasks.
        self.run_tasks(tasks, parallel)

        # bwaarg write the rest!

    def start(self, positionals=None):
        '''start the helper flow. We check helper system configurations to
           determine components that should be collected for the submission.
           This is where the client can also pass on any extra (positional)
           arguments in a list from the user.
        '''
        bot.info('[watchme|%s]' %(self.name))

    def _start(self, positionals=None):
        '''_start should be implemented by the subclass, and print any extra
           information for the helper to the user
        '''
        pass

# identification

    def __repr__(self):
        return "[helper|%s]" %self.name

    def __str__(self):
        return "[helper|%s]" %self.name


# Settings

WatcherBase._load_config = load_config
WatcherBase._load_envars = load_envars
WatcherBase._remove_setting = remove_setting
WatcherBase._get_setting = get_setting
WatcherBase._get_settings = get_settings
WatcherBase._get_and_update_setting = get_and_update_setting
WatcherBase._update_settings = update_settings

# Schedule 

WatcherBase.remove_schedule = remove_schedule
WatcherBase.get_crontab = get_crontab
WatcherBase.update_schedule = update_schedule
WatcherBase.clear_schedule = clear_schedule
WatcherBase.schedule = schedule
