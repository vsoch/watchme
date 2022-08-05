__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from watchme import get_watcher


def main(args, extra):
    """activate one or more watchers"""
    # Required - will print help if not provided
    name = args.watcher[0]
    watcher = get_watcher(name, base=args.base, create=False)

    # If user wants to see create command, must have list of tasks
    if args.create_command is True and extra is None:
        extra = [x.name for x in watcher.get_tasks()]

    # Show the create command, or inspect a task
    watcher.inspect(extra, create_command=args.create_command)
