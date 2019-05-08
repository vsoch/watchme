'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme import get_watcher
from watchme.logger import bot

def main(args, extra):
    '''add a task for a watcher
    '''    
    # Required - will print help if not provided
    name = args.watcher[0]
    task = args.task[0]

    if not task.startswith('task'):
        example = 'watchme add-task watcher task-cpu func@cpu_task type@psutils'
        bot.exit('Task name must start with "task", e.g., %s' % example)

    # Exit if the user doesn't provide any parameters
    if extra == None:
        bot.exit('Please provide parameters to add to your watcher (key@value)')
              
    # Type can also be an argument
    watcher_type = args.watcher_type
    params = []
    for param in extra:
       if param.startswith('type@'):
           watcher_type = param.replace('type@', '')
       else:
           params.append(param)

    # Get the watcher to interact with, must already exist
    watcher = get_watcher(name, base=args.base, create=False) 

    # Add the task. Will exit if not a valid type, or parameters
    watcher.add_task(task=task,
                     task_type=watcher_type,
                     params=params,
                     force=args.force,
                     active=args.active)
