__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020-2021, Vanessa Sochat"
__license__ = "MPL 2.0"

from watchme.tasks import TaskBase


class Task(TaskBase):
    """a results task aims to use WatchMe as a database, meaning the functions
    are optimized to collect and record results."""

    required_params = []

    def __init__(self, name, params=None, **kwargs):

        if params is None:
            params = []

        self.type = "results"

        # Handles setting the name, setting params, and validate
        super(Task, self).__init__(name, params, **kwargs)

    def export_func(self):
        """this function should return the correct task (from the tasks.py
        in the same folder) based on some logic of the params that are given
        by the user (self.params). If there is only one kind of function for
        the task, it's fairly easy to import and return it here. This
        function should take no arguments, but instead use the self.params
        already provided in the client.
        """
        name = self.params.get("func", "from_env_task")

        if name == "from_env_task":
            from .tasks import from_env_task as func
        else:
            func = None

        return func
