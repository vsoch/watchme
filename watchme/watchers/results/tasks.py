__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020-2021, Vanessa Sochat"
__license__ = "MPL 2.0"

from watchme.utils import get_tmpdir, get_watchme_env, write_file
import os
import shutil


def from_env_task(**kwargs):
    """Get some set of variables from the environment. We look for those
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
    """
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
