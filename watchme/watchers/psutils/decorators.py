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
from functools import wraps
from watchme.logger import bot
from watchme.watchers.psutils import Task
from watchme.tasks.decorators import DecoratorBase
from watchme import get_watcher
from time import sleep
import shlex
import subprocess


class TerminalRunner(DecoratorBase):

    def __init__(self, cmd, **kwargs):
        self.cmd = shlex.split(cmd)
        self.process = None

        # Handles setting the skip, include, and only parameters
        super(TerminalRunner, self).__init__(**kwargs)

    def run(self):
        '''run the user provided function
        '''
        try:
            self.process = subprocess.Popen(self.cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        except FileNotFoundError:
            self.cmd.pop(0)
            self.process = subprocess.Popen(self.cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

    def wait(self):
        '''wait should monitor the running task. run should be called first.
        '''
        # Parameters for the pid, and to skip sections of results
        params = {"skip": self.skip,
                  "pid": self.process.pid,
                  "include": self.include,
                  "only": self.only,
                  'func': 'monitor_pid_task'}

        # This particular decorator doesn't take input params
        task = Task("monitor_pid_task", params=params)

        # Export parameters and functions            
        function = task.export_func()
        params = task.export_params()

        # collect resources, then sleep
        while self.process.poll() is None:

            # Function returns dictionary, we append to list of timepoints
            self.timepoints.append(function(**params))
            sleep(self.seconds)

        # Get the timepoints
        return self.timepoints


class ProcessRunner(DecoratorBase):

    def __init__(self, **kwargs):
        self.process = None
        self.queue = Queue()

        # Handles setting the seconds, skip, include, and only parameters
        super(ProcessRunner, self).__init__(**kwargs)

    @staticmethod
    def _wrapper(func, queue, args, kwargs):
        ret = func(*args, **kwargs)
        queue.put(ret)

    def run(self, func, *args, **kwargs):
        '''run the user provided function
        '''
        args2 = [func, self.queue, args, kwargs]
        p = Process(target=self._wrapper, args=args2)
        self.process = p
        p.start()

    def wait(self):
        '''watch should monitor the running task. run should be called first.
        '''

        # Parameters for the pid, and to skip sections of results
        params = {"skip": self.skip,
                  "pid": self.process.pid,
                  "include": self.include,
                  "only": self.only,
                  'func': 'monitor_pid_task'}

        # This particular decorator doesn't take input params
        task = Task("monitor_pid_task", params=params)

        # Export parameters and functions            
        function = task.export_func()
        params = task.export_params()

        # collect resources, then sleep
        while self.process.is_alive():

            # Function returns dictionary, we append to list of timepoints
            self.timepoints.append(function(**params))
            sleep(self.seconds)

        # Get the result, and the timepoints
        result = self.queue.get()
        self.process.join()
        return result


def monitor_resources(*args, **kwargs):
    '''a decorator to monitor a function every 3 (or user specified) seconds. 
       We include one or more task names that include data we want to extract.
       we get the pid of the running function, and then use the
       monitor_pid_task from psutils to watch it. The functools "wraps"
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
       name: the suffix of the decorator-psutils-<name> folder. If not provided,
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
                bot.error("A watcher name is required for the psutils decorator.")
                return result

            # Get a watcher to save results to
            watcher = get_watcher(args[0], create=kwargs.get('create', False))

            # Start the function
            runner = ProcessRunner(seconds=kwargs.get('seconds', 3),
                                   skip=kwargs.get('skip', []),
                                   include=kwargs.get('include', []),
                                   only=kwargs.get('only', []))

            runner.run(func, *fargs, **fkwargs)
            result = runner.wait()

            # Save results (finishing runs) - key is folder created
            name = kwargs.get('name', func.__name__)
            key = 'decorator-psutils-%s' % name
            results = {key: runner.timepoints}
            watcher.finish_runs(results)
            
            # Return function result to the user
            return result
        return wrapper
    return inner
