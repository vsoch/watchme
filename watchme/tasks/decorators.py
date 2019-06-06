'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.logger import bot
import os

class DecoratorBase(object):

    def __init__(self, seconds=3, skip=None, include=None, only=None):
 
        # Replace Nones with lists
        only = none_to_list(only)
        include = none_to_list(include)
        skip = none_to_list(skip)

        self.seconds = seconds
        self.timepoints = []

        # Export seconds to the environment
        os.environ["WATCHMEENV_SECONDS"] = str(self.seconds)

        # Ensure we have csv lists
        self.only = self._parse_custom(only)
        self.skip = self._parse_custom(skip)
        self.include = self._parse_custom(include)

    def _parse_custom(self, listy):
        '''parse an actual list (['one','two','three']) into 
           a csv list. If we don't have a list, ignore and assume already
           parsed that way.
 
           Parameters
           ==========
           listy: the actual list
        '''
        if listy is None:
            listy = []
        if isinstance(listy, list):
            listy = ','.join(listy)
        return listy

    def run(self, *args, **kwargs):
        '''run should be implemented by the subclass to run the function or
           process being monitored
        '''
        bot.exit('run function must be implemented by subclass.')

    def wait(self, *args, **kwargs):
        '''wait should be run after run to monitor the process being run.'''
        bot.exit('wait function must be implemented by subclass.')


def none_to_list(value):
    '''a helper so that function args can be None, and updated to a list.
    '''
    if not value:
        value = []
    return value
