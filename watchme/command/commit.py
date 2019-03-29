'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.utils import run_command
from watchme.logger import bot
import os

def github_commit(name, base=None):
    '''Commit to the Github repo in folder. If folder isn't defined, assume
       present working directory
    '''
    if base == None:
        base = os.getcwd()
    
    #TODO: define nice datestring here

    # Commit with the watch group and date string
    message = 'watchme %s %s' %(name, date)
    run_command('git commit -a -m "%s"' % message)
