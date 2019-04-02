'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme import get_watcher
from watchme.logger import bot
from watchme.command import get_watchers


def main(args, extra):
    '''activate one or more watchers
    '''    
    # Required - will print help if not provided
    name = args.watcher[0]
    watcher = get_watcher(name, base=args.base, create=False)

    # If user wants to see create command, must have list of tasks
    if args.create_command is True and extra is None:
        extra = [x.name for x in watcher.get_tasks()]

    # Show the create command, or inspect a task
    watcher.inspect(extra, create_command=args.create_command)
