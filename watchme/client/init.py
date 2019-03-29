'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.command.create import ( 
    create_watcher_base, 
    create_watcher
)


def main(args, extra):
    '''init means creating the watcher base, and the first (default) watcher.
    '''    

    # Create the base
    create_watcher_base(args.watcher, args.base)

    # Create the first default watcher
    if not args.create_empty:
        create_watcher(args.watcher)

    
