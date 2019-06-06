'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.command import get_watchers
from watchme import get_watcher
from watchme.watchers.psutils.decorators import TerminalRunner
import json

def main(args, extra):
    '''monitor a task (from the command line), meaning wrapping it with
       multiprocessing, getting the id, and returning a result (command line 
       or written to file)
    '''  
    # The first argument will either be part of a command, or a watcher
    watcher = args.watcher

    # The entire user command is the extra arguments
    command = extra

    # If the user provides a watcher, we are saving to it
    if watcher not in get_watchers(args.base, quiet=True):       
        command = [watcher] + command
        watcher = None
    else:
        watcher = get_watcher(watcher, base=args.base, create=False)

    command = ' '.join(command)
    runner = TerminalRunner(command, 
                            skip=args.skip,
                            include=args.include,
                            only=args.only,
                            seconds=args.seconds)
    runner.run()
    timepoints = runner.wait()

    # If we don't have a watcher, print to terminal
    if watcher is None or args.test is True:
        print(json.dumps(timepoints))

    # Otherwise save to watcher task folder
    else:
        name = args.name
        if name is None:
            name = command.replace(' ', '-')
        name = 'decorator-psutils-%s' % name
        watcher.finish_runs({name: timepoints})
