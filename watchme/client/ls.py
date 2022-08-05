__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from watchme.command import get_watchers, list_task, list_watcher, list_watcher_types
from watchme.logger import bot


def main(args, extra):
    """list installed watchers"""
    if args.watchers is True:
        list_watcher_types()

    # Otherwise, we are listing installed watchers and tasks
    else:

        # If no watchers provided, list the watchers
        if extra is None:
            get_watchers(args.base)

        # One argument is the name of a watcher
        elif len(extra) == 1:
            list_watcher(extra[0], args.base)

        # Two arguments must be a watcher and task
        elif len(extra) == 2:
            list_task(extra[0], extra[1], args.base)

        else:
            bot.exit("Please provide none or all of <watcher> <task> to list.")
