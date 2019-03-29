'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.logger import bot
from watchme.defaults import ( 
    WATCHME_WATCHER, 
    WATCHME_BASE_DIR
)
from watchme.utils import ( 
    get_installdir, 
    read_file 
)
import configparser
import getpass
import shutil
import os


# CONFIG TEMPLATES #############################################################

def get_configfile_template():
    '''return the full path to the default configuration file
    '''
    return _get_config('watchme.cfg')

def _get_config(name):
    '''shared function to return a file in the config directory
    '''
    return os.path.abspath(os.path.join(get_installdir(), 'config', name))


# ACTIVE CONFIG FILES ##########################################################

def get_configfile(name, base=None):
    '''return the full path to a specific watcher configuration
    '''
    if base == None:
        base = WATCHME_BASE_DIR

    configfile = os.path.join(base, name, 'watchme.cfg')
    check_exists(filename)
    return configfile
    

# CONFIG IO ####################################################################

def write_config(filename, config, mode="w"):
    '''use configparser to write a config object to filename
    '''
    with open(filename, mode) as filey:
        config.write(filey)
    return filename


def read_config(filename):
    '''use configparser to write a config object to filename
    '''
    check_exists(filename)
    config = configparser.ConfigParser()
    config.read(filename)
    return config


# WATCHER CONFIG ###############################################################

def generate_watcher_config(path):
    '''generate a watcher config, meaning a watcher folder in the watchme
       base folder.

       Parameters
       ==========
       path: the path to the watcher repository
    '''
    check_exists(path)
    configfile = get_watcherfile_template()
    watcher_config = os.path.join(path, 'watchme.cfg')
    if not os.path.exists(watcher_config):
        bot.info('Generating watcher config %s' % watcher_config)
        shutil.copyfile(configfile, watcher_config)



# MASTER CONFIG ###############################################################

def init_config(path):
    '''generate the master configuration file in path using the 
       default configuration "watchme.cfg" as template. This is a master
       configuration file that will list the watchers, and the user
       specific settings. Since this config is outside of the repos with
       watcher data, it only holds user-specific variables like the names
       of the watchers, and if each is active (true / false)

       Parameters
       ==========
       path: the path to the folder (watchme base) to put the config file
    '''
    template = get_configfile_template()
    configfile = os.path.join(path, template)

    # Exit if path doesn't exist
    if not os.path.exists(path):
        bot.exit('%s does not exist.' % path)

    # Finally, copy the master template there, if not already there
    if not os.path.exists(configfile):
        configfile = shutil.copyfile(template, configfile) 
    return configfile


# CONFIG HELPERS ###############################################################

def check_exists(filename):
    '''a general helper function to check for existence, and exit if not found.
    '''
    if not os.path.exists(filename):
        bot.exit('Cannot find %s' % filename)
