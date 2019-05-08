'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme import get_watcher
from watchme.logger import bot

def main(args, extra):
    '''remove tasks or exporters from a watcher, or delete the entire watcher
    '''    
    # Required - will print help if not provided
    name = args.watcher[0]
    watcher = get_watcher(name, base=args.base, create=False)

    # If delete is true, remove entire watcher, only if not protected or frozen
    if args.delete:
        watcher.delete()    

    else:

        # Exit if the user doesn't provide any tasks to remove
        if extra == None:
            bot.exit('Provide tasks or exporters to remove, or --delete for entire watcher.')
    
        # Case 1: one argument indicates removing an entire task or exporter
        if len(extra) == 1:
     
            section = extra[0]

            # Remove the task or exporter, if it exists
            if section.startswith('task'):
                watcher.remove_task(section)

            elif section.startswith('exporter'):
                watcher.remove_exporter(section)

            else:
                bot.error("Task and exporters must begin with (task|exporter)-")

        # Case 2: two arguments indicate removing an exporter from a task
        elif len(extra) == 2:
            
            # Allow the user to specify either order
            extra.sort()               # task, exporter
            watcher.remove_task_exporter(extra[1], extra[0])
