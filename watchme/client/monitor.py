__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from watchme.command import get_watchers
from watchme import get_watcher
from watchme.tasks.decorators import TerminalRunner
import json


def main(args, extra):
    """monitor a task (from the command line), meaning wrapping it with
    multiprocessing, getting the id, and returning a result (command line
    or written to file)
    """
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

    command = " ".join(command)
    runner = TerminalRunner(
        command,
        skip=args.skip,
        include=args.include,
        only=args.only,
        seconds=args.seconds,
    )
    runner.run()
    timepoints = runner.wait(args.func)

    # The output folder depends on the watcher func
    prefix = "decorator-psutils"
    if args.func == "gpu_task":
        prefix = "decorator-gpu"

    # If we don't have a watcher, print to terminal
    if watcher is None or args.test is True:
        print(json.dumps(timepoints))

    # Otherwise save to watcher task folder
    else:
        name = args.name
        if name is None:
            name = command.replace(" ", "-")
        name = "%s-%s" % (prefix, name)
        watcher.finish_runs({name: timepoints})
