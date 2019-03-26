'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.logger import bot
from watchme.defaults import WATCHME_WATCHER
from watchme.utils import ( 
    get_installdir, 
    read_file 
)
import configparser
import getpass
import shutil
import os


def get_configfile():
    '''return the full path to the default configuration file
    '''
    return _get_config('watchme.cfg')

def get_watcherfile():
    '''return a watcher template to store variables for a specific watcher.
    '''
    return _get_config('watcher.cfg')


def _get_config(name):
    '''shared function to return a file in the config directory
    '''
    return os.path.abspath(os.path.join(get_installdir(), 'config', name))


def generate_config(path):
    '''generate the master configuration file in path using the 
       default configuration "watchme.cfg" as template. This is a master
       configuration file that will list the watchers, and the user
       specific settings. Since this config is outside of the repos with
       watcher data, it only holds user-specific variables like the names
       of the watchers, and if each is active.
    '''
    template = get_configfile()
    configfile = os.path.join(path, template)

    # Exit if path doesn't exist
    if not os.path.exists(path):
        bot.exit('%s does not exist.' % path)

    # Look for folders, and if found, update the config
    
    # Finally, copy the master template there.
    shutil.copyfile(template, configfile)  
