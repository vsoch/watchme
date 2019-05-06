'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme import get_watcher
from watchme.logger import bot
from watchme.defaults import WATCHME_EXPORTERS

def main(args, extra):
    '''add an exporter to a watcher, optionally with params and tasks
    '''    

    # Required - will print help if not provided
    name = args.watcher[0]
    exporter = args.name[0]

    # Are we adding an extra task or exporter?
    if not exporter.startswith('exporter'):
        bot.error('Exporter name must start with exporter-<name>')
        bot.exit('watchme add-exporter watcher exporter-pushgateway task1 task2 task3')

    # Extra parameters are parameters for the exporter, or task names
    if extra == None:
        extra = []

    # Type can also be an argument (required for exporter)
    exporter_type = args.exporter_type

    # Go through extras and determine params and tasks
    params = []
    tasks = []
    for param in extra:
        if param.startswith('type@'):
            exporter_type = param.replace('type@', '')
        elif param.startswith('task'):
             tasks.append(param)      
        else:
            params.append(param)

    # Get the watcher to interact with, must already exist
    watcher = get_watcher(name, base=args.base, create=False) 

    # Double check the exporter type
    if exporter_type not in WATCHME_EXPORTERS:
        choices = ','.join(WATCHME_EXPORTERS)
        bot.exit("%s is not a valid exporter, %s" %(exporter_type, choices))

    # Add the exporter, optionally with tasks                  
    watcher.add_exporter(name=exporter,
                         exporter_type=exporter_type,
                         params=params,
                         tasks=tasks,
                         force=args.force,
                         active=args.active)
