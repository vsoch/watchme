'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme import get_watcher
from watchme.logger import bot

def main(args, extra):
    '''edit the configuration for a watcher task
    '''    
    # Required - will print help if not provided
    name = args.watcher[0]
    action = args.action[0]
    task = args.task[0]

    # Get the watcher (exits if doesn't exist)
    watcher = get_watcher(name, base=args.base) 

    # Exit if the user doesn't provide a time
    if extra == None:
        bot.exit('Please provide one or more items to %s' % action)

    key = extra[0]
    value = None
    if action in ['add', 'update']:
        if len(extra) != 2:
            bot.exit('You must do watchme <watcher> add <key> <value>')                 
        value = extra[1]

    # Ensure the task exists        
    watcher.edit_task(task, action, key, value)
