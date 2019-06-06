'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme import get_watcher

def main(args, extra):
    '''deactivate one or more watchers
    '''    
    # Doesn't work if watcher not provided
    watcher = args.watcher[0]
    watcher = get_watcher(watcher, base=args.base)
        
    # The user is deactivating the entire watcher
    if extra is None:
        watcher.deactivate()       
    else:
        for name in extra:
            watcher.deactivate(name)
