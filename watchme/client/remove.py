__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from watchme import get_watcher
from watchme.logger import bot


def main(args, extra):
    """activate one or more watchers"""
    # Required - will print help if not provided
    name = args.watcher[0]
    watcher = get_watcher(name, base=args.base, create=False)

    # If delete is true, remove entire watcher, only if not protected or frozen
    if args.delete:
        watcher.delete()

    else:

        # Exit if the user doesn't provide any tasks to remove
        if extra is None:
            bot.exit("Provide tasks to remove, or --delete for entire watcher.")

        for task in extra:

            # Remove the task, if it exists
            watcher.remove_task(task)
