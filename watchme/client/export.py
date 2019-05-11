'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme import get_watcher
from watchme.utils import ( write_json, generate_temporary_file )
from watchme.logger import bot
import json
import os

def main(args, extra):
    '''export temporal data for a watcher
    '''    
    # Required - will print help if not provided
    name = args.watcher[0]
    task = args.task[0]
    filename = args.filename[0]

    if not task.startswith('task') and not task.startswith('decorator'):
        example = 'watchme export watcher task-reddit result.txt'
        bot.exit('Task name must start with "task" or "decorator": %s' % example)

    # Use the output file, or a temporary file
    out = args.out

    # Get the watcher to interact with, must already exist
    watcher = get_watcher(name, base=args.base, create=False) 

    if out is not None:
        if os.path.exists(out) and args.force is False:
            bot.exit('%s exists! Use --force to overwrite.' % out)

    # Export the data to file
    result = watcher.export_dict(task=task,
                                 filename=filename,
                                 name=name,
                                 export_json=args.json,
                                 base=args.base)

    if result != None:

        if out == None:
            print(json.dumps(result, indent=4))
        else:
            write_json(result, out)
            bot.info('Result written to %s' % out)
