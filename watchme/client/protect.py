__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from watchme import get_watcher


def main(args, extra):
    """protect or freeze a watcher, or disable."""
    # Required - will print help if not provided
    name = args.watcher[0]
    watcher = get_watcher(name, base=args.base, create=False)

    if args.action in ["on", "off"]:
        watcher.protect(args.action)
    elif args.action == "freeze":
        watcher.freeze()
    elif args.action == "unfreeze":
        watcher.unfreeze()
