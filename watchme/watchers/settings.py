'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.logger import bot
import os


def remove_setting(self, section, name, save=True):
    '''remove a setting from the configuration file

       Parameters
       ==========
       section: the name of the section (task)
       name: the name of the variable to remove
       save: save the configuration file (default is True)
    '''
    removed = False
    self.load_config()

    # Remove the named section, if it exists
    if section in self.config:
        if name.lower() in self.config[section]:
            removed = self.config.remove_option(section, name)

    # Does the user want to save the file?
    if removed and save:
        self.save()

    return removed


def remove_section(self, section, save=True):
    '''remove a setting from the configuration file

       Parameters
       ==========
       section: the name of the section (task)
       save: save the configuration file (default is True)
    '''
    removed = False
    self.load_config()

    # Remove the named section, if it exists
    if section in self.config:
        self.config.remove_section(section)
        removed = True

    # Does the user want to save the file?
    if removed and save:
        self.save()

    return removed

def print_section(self, section):
    '''print a section (usually a task) from a configuration file,
       if it exists.

       Parameters
       ==========
       section: the name of the section (task)
    '''
    self.load_config()

    if section in self.config:
        bot.info('[%s]' % section)
        for key in self.config[section]:
            value = self.config[section][key]
            bot.custom(prefix=key, message=" = %s" % value, color="CYAN")
    else:
        bot.exit('%s is not a valid section.' % section)

def get_setting(self, section, name, default=None):
    '''return a setting from the environment (first priority) and then
       secrets (second priority) if one can be found. If not, return None.

       Parameters
       ==========
       section: the section in the config, defaults to self.name
       name: they key (index) of the setting to look up
       default: (optional) if not found, return default instead.
    ''' 
    self.load_config()

    setting = None
    if section in self.config:
         if name.lower() in self.config[section]:
            setting = self.config[section][name.lower()]

    if setting is None and default is not None:
        setting = default

    return setting



def set_setting(self, section, key, value):
    '''set a key value pair in a section, if the section exists. Returns
       a boolean (True or False) to indicate if added.

       Parameters
       ==========
       section: the section in the config, defaults to self.name
       key: they key (index) of the setting to set
       value: the value to set.
    ''' 
    self.load_config()

    was_set = False
    if section in self.config:
        self.config[section][key] = value
        was_set = True

    return was_set


def get_section(self, name):
    '''get a section from the config, if it exists
    '''
    section = None
    self.load_config()
    if name in self.config.sections():
        section = self.config[name]
    return section