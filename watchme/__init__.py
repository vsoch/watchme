'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


'''

from watchme.version import __version__
from watchme.defaults import (
    WATCHME_DEFAULT_TYPE,
    WATCHME_TYPES,
    WATCHME_BASE_DIR
)

def get_watcher(name="watcher", 
                watcher_type=None, 
                base=None,
                create=False,
                quiet=True, **kwargs):
    '''
       get the correct watcher depending on the environment variable
       WATCHME_WATCHER or default to "watcher"

       Parameters
       ==========
       name: the name of the watcher, will be made all lowercase
       watcher_type: if desired, choose a watcher type. Currently only
                     one is supported, urls
       base: the watcher base, if not defined, will use WATCHER_BASE_DIR envar
       create: if the watcher folder doesn't exist, create it (default False)
       quiet: if True, suppress most output about the client (e.g. speak)

    '''
    # Watcher type, first priority is command line
    if watcher_type == None:
        watcher_type = WATCHME_DEFAULT_TYPE

    # Choose the watcher type (currently only available are urls)
    if "url" in watcher_type: from watchme.watchers.urls import Watcher
    else: Watcher = None

    # If no Watcher selected, exit with error
    if Watcher == None:
        types = ','.join(WATCHME_TYPES)
        bot.exit('%s is not a valid watcher. Choices are %s' %(watcher_type,
                                                               types))
    Watcher.name = name.lower()
    Watcher.quiet = quiet
    Watcher.base = base

    # Initialize the watcher
    return Watcher(create=create)
