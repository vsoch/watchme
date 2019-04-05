'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme import get_watcher
from watchme.logger import bot

def main(args, extra):
    '''run a watcher, optionally supplying one or more regular expressions to
       check for.
    '''    
    # Required - will print help if not provided
    name = args.watcher[0]
    watcher = get_watcher(name, base=args.base, create=False)
    
    # If a set of task names or regular expressions are provided:
    if extra != None:
        extra = "(%s)" % '|'.join(extra)

    # Run the watcher, providing regular expressions to match tasks
    watcher.run(regexp=extra, 
                parallel=not args.serial, 
                test=args.test,
                show_progress=not args.no_progress)

