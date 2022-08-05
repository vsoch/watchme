__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020-2021, Vanessa Sochat"
__license__ = "MPL 2.0"

from watchme.tasks import TaskBase
from watchme.utils import get_user, get_host


class Task(TaskBase):

    required_params = []

    def __init__(self, name, params=None, **kwargs):

        if params is None:
            params = {}

        self.type = "psutils"

        # If the user doesn't provide a file name, name based on task
        if "_save" in kwargs:
            if "file_name" not in params:
                params["file_name"] = "%s_%s.json" % (
                    get_host().lower(),
                    get_user().lower(),
                )

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
        name = self.params.get("func", "cpu_task")

        if name == "cpu_task":
            from .tasks import cpu_task as func
        elif name == "memory_task":
            from .tasks import memory_task as func
        elif name == "monitor_pid_task":
            from .tasks import monitor_pid_task as func
        elif name == "net_task":
            from .tasks import net_task as func
        elif name == "python_task":
            from .tasks import python_task as func
        elif name == "sensors_task":
            from .tasks import sensors_task as func
        elif name == "system_task":
            from .tasks import system_task as func
        elif name == "users_task":
            from .tasks import users_task as func
        else:
            func = None

        return func
