'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.command import (
    get_watchers,
    list_task,
    list_watcher,
    list_watcher_types
)
from watchme.logger import bot

def main(args, extra):
    '''list installed watchers
    '''
    if args.watchers == True:
        list_watcher_types()

    # Otherwise, we are listing installed watchers and tasks
    else:

        # If no watchers provided, list the watchers
        if extra == None:
            get_watchers(args.base)

        # One argument is the name of a watcher
        elif len(extra) == 1:
            list_watcher(extra[0], args.base)

        # Two arguments must be a watcher and task
        elif len(extra) == 2:
            list_task(extra[0], extra[1], args.base)

        else:
            bot.exit('Please provide none or all of <watcher> <task> to list.')
