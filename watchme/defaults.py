'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

The watcher is actually a connection to crontab. This is what helps to schedule
the watched to check for changes at some frequency, and update the files.


'''

from watchme.utils import get_userhome
import tempfile
import os
import sys


################################################################################
# environment / options
################################################################################


def getenv(variable_key, default=None, required=False, silent=True):
    ''' attempt to get an environment variable. If the variable
        is not found, None is returned.

        Parameters
        ==========
        variable_key: the variable name
        required: exit with error if not found
        silent: Do not print debugging information for variable
    '''
    variable = os.environ.get(variable_key, default)
    if variable is None and required:
        bot.error("Cannot find environment variable %s, exiting." %variable_key)
        sys.exit(1)

    if not silent and variable is not None:
            bot.verbose("%s found as %s" %(variable_key,variable))

    return variable



################################################################################
# Helpme

USERHOME = get_userhome()

WATCHME_WATCHER = getenv('WATCHME_WATCHER', 'watcher')
_config = os.path.join(USERHOME, ".watchme")
WATCHME_BASE_DIR = getenv('WATCHME_BASE_DIR', _config)
WATCHME_WORKERS = int(getenv('WATCHME_WORKERS', 9))

# The types of valid watchers (currently only urls). Corresponds with
# a folder under "main/watchers"
WATCHME_TASK_TYPES = ['urls', 'url', 'psutils', 'results']
WATCHME_DEFAULT_TYPE = "urls"

# Parameters not allowed for task clients, set by TaskBase
WATCHME_NOTALLOWED_PARAMS = ['type', 'active']
