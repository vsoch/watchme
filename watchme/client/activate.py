__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from watchme import get_watcher


def main(args, extra):
    """activate one or more watchers"""
    # Doesn't work if watcher not provided
    watcher = args.watcher[0]
    watcher = get_watcher(watcher, base=args.base)

    # The user is deactivating the entire watcher
    if extra is None:
        watcher.activate()
    else:
        for name in extra:
            watcher.activate(name)
