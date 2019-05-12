'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.utils import (
    get_tmpdir,
    get_watchme_env,
    write_file
)
import os
import shutil


def from_env_task(**kwargs):
    '''Get some set of variables from the environment. We look for those
       defined in kwargs, but also any in the environment that start with
       the prefix WATCHMENEV_. They are saved to files that are equivalently
       named, and the idea is that we can track a changing (single) result,
       meaning that the timestamp is meaningful, or we can track
       values for many different results, so the timestamps just serve to
       record when each was recorded.

       Parameters
       ==========
       *: any number of parameters from the task configuration that will
          be looked for in the environment.
    '''
    results = []
 
    # Create a temporary directory for results
    tmpdir = get_tmpdir()

    # First extract variables from the environment
    environ = get_watchme_env()
    for key, value in environ.items():
 
        # Write the result to file (don't include extension)
        filename = os.path.join(tmpdir, key)
        write_file(filename, value)
        results.append(filename)

    # If no results, return None
    if len(results) == 0:
        shutil.rmtree(tmpdir)

    return results
