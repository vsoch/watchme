'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from functools import wraps
from watchme.logger import bot
from watchme.tasks.decorators import ProcessRunner
from watchme import get_watcher


def monitor_gpu(*args, **kwargs):
    '''a decorator to monitor a function every 3 (or user specified) seconds. 
       We include one or more task names that include data we want to extract.
       we get the pid of the running function, and then use the
       gpu_task from gpu to watch it. The functools "wraps"
       ensures that the (fargs, fkwargs) are passed from the calling function
       despite the wrapper. The following parameters can be provided to
       "monitor resources"

       Parameters
       ==========
       watcher: the watcher instance to use, used to save data to a "task"
                folder that starts with "decorator-<name<"
       seconds: how often to collect data during the run.
       only: ignore skip and include, only include this custom subset
       skip: Fields in the result to skip (list).
       include: Fields in the result to include back in (list).
       create: whether to create the watcher on the fly (default False, must
               exist)
       name: the suffix of the decorator-gpu-<name> folder. If not provided,
             defaults to the function name
    '''
    def inner(func):

        @wraps(func)
        def wrapper(*fargs, **fkwargs):

            # Typically the task folder is the index, so we will create
            # indices that start with decorator-<task>
            result = None

            # The watcher is required, first keyword argument
            if not args:
                bot.error("A watcher name is required for the gpu decorator.")
                return result

            # Get a watcher to save results to
            watcher = get_watcher(args[0], create=kwargs.get('create', False))

            # Start the function
            runner = ProcessRunner(seconds=kwargs.get('seconds', 3),
                                   skip=kwargs.get('skip', []),
                                   include=kwargs.get('include', []),
                                   only=kwargs.get('only', []))

            runner.run(func, *fargs, **fkwargs)
            result = runner.wait("gpu_task")

            # Save results (finishing runs) - key is folder created
            name = kwargs.get('name', func.__name__)
            key = 'decorator-gpu-%s' % name
            results = {key: runner.timepoints}
            watcher.finish_runs(results)
            
            # Return function result to the user
            return result
        return wrapper
    return inner
