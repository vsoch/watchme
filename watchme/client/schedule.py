__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from watchme import get_watcher
from watchme.logger import bot


def main(args, extra):
    """activate one or more watchers"""
    # Required - will print help if not provided
    name = args.watcher[0]

    # Exit if the user doesn't provide a time
    if extra is None:
        bot.exit("Please provide a time frame (@daily, @hourly, @weekly, etc.)")

    # Determine the time to use
    if "@daily" in extra:
        minute, hour, month, day, weekday = 0, 0, "*", "*", "*"
    elif "@hourly" in extra:
        minute, hour, month, day, weekday = 0, "*", "*", "*", "*"
    elif "@weekly" in extra:
        minute, hour, month, day, weekday = 0, 0, "*", "*", 0
    elif "@monthly" in extra:
        minute, hour, month, day, weekday = 0, 0, 1, "*", "*"
    elif "@yearly" in extra:
        minute, hour, month, day, weekday = 0, 0, 1, 1, "*"
    else:
        if len(extra) != 5:
            message = """Please enter a frequency (@weekly) or use a valid 
                         cron timestamp (see https://crontab.guru/)."""
            bot.exit(message)
        minute, hour, month, day, weekday = extra

    # Schedule the watcher
    watcher = get_watcher(name, base=args.base)
    watcher.schedule(minute, hour, month, day, weekday, force=args.force)
