'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.command import (
    get_watchers,
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

        # Otherwise, list the tasks of the watcher
        else:
            for watcher in extra:
                list_watcher(watcher, args.base)
