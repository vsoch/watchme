__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from multiprocessing import Process, Queue
from watchme.logger import bot
from time import sleep
import shlex
import subprocess
import os


class DecoratorBase:
    def __init__(self, seconds=3, skip=None, include=None, only=None):

        # Replace Nones with lists
        only = none_to_list(only)
        include = none_to_list(include)
        skip = none_to_list(skip)

        self.seconds = seconds
        self.timepoints = []

        # Export seconds to the environment
        os.environ["WATCHMEENV_SECONDS"] = str(self.seconds)

        # Ensure we have csv lists
        self.only = self._parse_custom(only)
        self.skip = self._parse_custom(skip)
        self.include = self._parse_custom(include)

    def _parse_custom(self, listy):
        """parse an actual list (['one','two','three']) into
        a csv list. If we don't have a list, ignore and assume already
        parsed that way.

        Parameters
        ==========
        listy: the actual list
        """
        if listy is None:
            listy = []
        if isinstance(listy, list):
            listy = ",".join(listy)
        return listy

    def run(self, *args, **kwargs):
        """run should be implemented by the subclass to run the function or
        process being monitored
        """
        bot.exit("run function must be implemented by subclass.")

    def wait(self, *args, **kwargs):
        """wait should be run after run to monitor the process being run."""
        bot.exit("wait function must be implemented by subclass.")


class TerminalRunner(DecoratorBase):
    def __init__(self, cmd, **kwargs):
        self.cmd = shlex.split(cmd)
        self.process = None

        # Handles setting the skip, include, and only parameters
        super(TerminalRunner, self).__init__(**kwargs)

    def run(self):
        """run the user provided function"""
        try:
            self.process = subprocess.Popen(
                self.cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
            )
        except FileNotFoundError:
            self.cmd.pop(0)
            self.process = subprocess.Popen(
                self.cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
            )

    def wait(self, task_name):
        """wait should monitor the running task. run should be called first.

        Parameters
        ==========
        task_name: should correspond with the task func (e.g.,
                   monitor_pid_task for psutils, or
                   monitor_gpu for gpu tasks.
        """

        # Parameters for the pid, and to skip sections of results
        params = {
            "skip": self.skip,
            "pid": self.process.pid,
            "include": self.include,
            "only": self.only,
            "func": task_name,
        }

        # This particular decorator doesn't take input params
        task = get_task(task_name, params)

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
        """run the user provided function. When we run, we save the function
        run to self.func, where we can derive the name in self.wait.
        """
        self.func = func
        args2 = [func, self.queue, args, kwargs]
        p = Process(target=self._wrapper, args=args2)
        self.process = p
        p.start()

    def wait(self, task_name):
        """watch should monitor the running task. run should be called first.

        Parameters
        ==========
        task_name: should correspond with the task func (e.g.,
                   monitor_pid_task for psutils, or
                   monitor_gpu for gpu tasks.
        """

        # Parameters for the pid, and to skip sections of results
        params = {
            "skip": self.skip,
            "pid": self.process.pid,
            "include": self.include,
            "only": self.only,
            "func": task_name,
        }

        # This particular decorator doesn't take input params
        task = get_task(task_name, params)

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


def get_task(task_name, params):
    """a helper function to return an instantiated task object, depending
    on the function name.

    Parameters
    ==========
    task_name: the name of the task to return
    params: parameters for the task
    """
    if task_name == "monitor_pid_task":
        from watchme.watchers.psutils import Task
    elif task_name == "gpu_task":
        from watchme.watchers.gpu import Task
    else:
        bot.exit("%s is not a known task." % task_name)
    return Task(task_name, params=params)


def none_to_list(value):
    """a helper so that function args can be None, and updated to a list."""
    if not value:
        value = []
    return value
