'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from multiprocessing import (
    Process, 
    Queue
)
from watchme.logger import bot
from watchme.watchers.psutils import Task
from watchme import get_watcher
import functools
from time import sleep
import os


class ProcessRunner():

    def __init__(self, seconds=3, skip=[], include=[]):
        self.process = None
        self.seconds = seconds
        self.queue = Queue()
        self.set_custom(skip, include)
        self.timepoints = []

    def set_custom(self, skip, include):
        '''add list of variables to skip (task expects comma separated string)'''
        if isinstance(skip, list):
            skip = ','.join(skip)
        self.skip = skip

        if isinstance(include, list):
            include = ','.join(include)
        self.include = include

    @staticmethod
    def _wrapper(func, queue, args, kwargs):
        ret = func(*args, **kwargs)
        queue.put(ret)

    def run(self, func, *args, **kwargs):
        args2 = [func, self.queue, args, kwargs]
        p = Process(target=self._wrapper, args=args2)
        self.process = p
        p.start()

    def wait(self):

        # Parameters for the pid, and to skip sections of results
        params = {"skip": self.skip,
                  "pid": self.process.pid,
                  "include": self.include}

        # This particular decorator doesn't take input params
        task = Task("monitor_pid_task", params=params)

        # Export parameters and functions            
        function = task.export_func()
        params = task.export_params()

        # collect resources, then sleep
        while self.process.is_alive():
            self.timepoints = self.timepoints + function(params)
            sleep(seconds)

        # Get the result, and the timepoints
        result = self.queue.get()
        self.process.join()
        return result


def monitor_resources(watcher, seconds=3, skip=[]):
    '''a decorator to monitor a function every 3 (or user specified) seconds. 
       We include one or more task names that include data we want to extract.
       we get the pid of the running function, and then use the
       monitor_pid_task from psutils to watch it.

       Parameters
       ==========
       watcher: the watcher instance to use, used to save data to a "task"
                folder that starts with "decorator-<name<"
       seconds: how often to collect data during the run.
       skip: Fields in the result to skip (list).
    '''
    # Get a watcher to save results to
    watcher = get_watcher(watcher, create=False)

    # Define the wrapper function
    def decorator_monitor_resources(func):
        @functools.wraps(func)
        def wrapper_monitor_resources(*args, **kwargs):

            # Typically the task folder is the index, so we will create
            # indices that start with decorator-<task>
            results = {}

            # Start the function
            runner = ProcessRunner(seconds=seconds, skip=skip, include=include)
            runner.run(func, args, kwargs)
            result = runner.wait()

            # Save results (finishing runs) - key is folder created
            results['decorator-%s' % func.__name__] = runner.timepoints
            watcher.finish_runs(results)
            
            # Return function result to the user
            return result
        return wrapper_monitor_resources
    return decorator_monitor_resources
