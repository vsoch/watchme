'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme import get_watcher
from watchme.logger import bot

def main(args, extra):
    '''activate one or more watchers
    '''    
    # Required - will print help if not provided
    name = args.watcher[0]
    watcher = get_watcher(name, base=args.base, create=False)

    # If delete is true, remove entire watcher, only if not protected or frozen
    if args.delete:
        watcher.delete()    

    else:

        # Exit if the user doesn't provide any tasks to remove
        if extra is None:
            bot.exit('Provide tasks to remove, or --delete for entire watcher.')
    
        for task in extra:
     
            # Remove the task, if it exists
            watcher.remove_task(task)
