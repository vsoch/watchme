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

    watchers = args.watchers
    if len(watchers) == 0:
        bot.exit('You must provide one or more watchers to deactivate.')

    for name in watchers:
        watcher = get_watcher(name, base=args.base)
        watcher.deactivate()
