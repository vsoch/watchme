'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.logger import bot
from watchme.defaults import ( 
    WATCHME_WATCHER, 
    WATCHME_BASE_DIR,
    WATCHME_DEFAULT_TYPE
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

def generate_watcher_config(path, watcher_type=None):
    '''generate a watcher config, meaning a watcher folder in the watchme
       base folder.

       Parameters
       ==========
       path: the path to the watcher repository
    '''
    check_exists(path)
    configfile = get_configfile_template()
    watcher_config = os.path.join(path, 'watchme.cfg')
    if not os.path.exists(watcher_config):
        bot.info('Generating watcher config %s' % watcher_config)
        shutil.copyfile(configfile, watcher_config)

    # Complete generation includes the watcher type
    if watcher_type == None:
        watcher_type = WATCHME_DEFAULT_TYPE
    
    # The template config has the section, but just in case
    config = read_config(configfile)
    if 'watcher' not in config.sections():
        config.add_section('watcher')
    config['watcher']['type'] = watcher_type

    # Save to file
    write_config(watcher_config, config)

# CONFIG HELPERS ###############################################################

def check_exists(filename):
    '''a general helper function to check for existence, and exit if not found.
    '''
    if not os.path.exists(filename):
        bot.exit('Cannot find %s' % filename)
