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
    '''push one or more watchers to an exporter endpoint
    '''    
    # Required - will print help if not provided
    name = args.watcher[0]
    task = args.task[0]
    exporter = args.exporter[0]
    filename = args.filename[0]

    # Example command to show task- and exporter-
    example = 'watchme push <watcher> <task> <exporter> <filename>'

    if not task.startswith('task'):
        bot.exit('Task name must start with "task", e.g., %s' % example)

    if not exporter.startswith('exporter'):
        bot.exit('Exporter name must start with "exporter", e.g., %s' % example)

    # Get the watcher to interact with, must already exist
    watcher = get_watcher(name, base=args.base, create=False) 

    # Push to the exporter (not the default git)
    result = watcher.push(task=task,
                          exporter=exporter,
                          filename=filename,
                          name=name,
                          export_json=args.json,
                          base=args.base)
