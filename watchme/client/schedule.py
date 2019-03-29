'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme import get_watcher
from watchme.logger import bot

def main(args, extra):
    '''activate one or more watchers
    '''    
    # Required - will print help if not provided
    name = args.watcher[0]

    # Exit if the user doesn't provide a time
    if extra == None:
        bot.exit('Please provide a time frame (@daily, @hourly, @weekly, etc.)')
              
    # Determine the time to use
    if '@daily' in extra:
        minute, hour, month, day, weekday = 0, 0, '*', '*', '*'
    elif "@hourly" in extra:
        minute, hour, month, day, weekday = 0, '*', '*', '*', '*'
    elif "@weekly" in extra:
        minute, hour, month, day, weekday = 0, 0, '*', '*', 0
    elif "@monthly" in extra:
        minute, hour, month, day, weekday = 0, 0, 1, '*', '*'
    elif "@yearly" in extra:
        minute, hour, month, day, weekday = 0, 0, 1, 1, '*'
    else:
        if len(extra) != 5:
            message = '''Please enter a frequency (@weekly) or use a valid 
                         cron timestamp (see https://crontab.guru/).'''
            bot.exit(message)
        minute, hour, month, day, weekday = extra

    # Schedule the watcher
    watcher = get_watcher(name, base=args.base) 
    watcher.schedule(minute, hour, month, day, weekday, force=args.force)
