'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.command import create_watcher

def main(args, extra):
    '''create means creating one or more watchers.
    '''    

    watchers = args.watchers
    if len(watchers) == 0:
        watchers = ['watcher']

    for watcher in watchers:
        create_watcher(watcher)
