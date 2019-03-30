'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme import get_watcher
from watchme.logger import bot

def main(args, extra):
    '''protect or freeze a watcher, or disable.
    '''    
    # Required - will print help if not provided
    name = args.watcher[0]
    watcher = get_watcher(name, base=args.base, create=False)

    if args.action in ['on', 'off']:
        watcher.protect(args.action)
    elif args.action == "freeze":
        watcher.freeze()
    elif args.action == "unfreeze":
        watcher.unfreeze()
