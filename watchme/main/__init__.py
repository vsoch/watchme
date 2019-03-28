'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.defaults import (
    WATCHME_DEFAULT_TYPE,
    WATCHME_TYPES
)

def get_watcher(name="watcher", watcher_type=None, quiet=True, **kwargs):
    '''
       get the correct watcher depending on the environment variable
       WATCHME_WATCHER or default to "watcher"

       Parameters
       ==========
       quiet: if True, suppress most output about the client (e.g. speak)

    '''
    # Default watcher name
    from watchme.defaults import ( WATCHME_WATCHER, WATCHME_DEFAULT_TYPE )

    # Watcher type, first priority is command line
    if watcher_type == None:
        watcher_type = WATCHME_DEFAULT_TYPE

    # If no obvious credential provided, we can use HELPME_CLIENT
    if "url" in watcher_type: 
        from watchme.main.watchers.urls import Watcher
    else:
        types = ','.join(WATCHME_TYPES)
        bot.exit('%s is not a valid watcher. Choices are %s' %(watcher_type,
                                                               types))

    Watcher.name = watcher
    Watcher.quiet = quiet

    # Initialize the watcher
    return Watcher()
