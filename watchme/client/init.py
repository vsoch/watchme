__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from watchme.command.create import create_watcher_base, create_watcher


def main(args, extra):
    """init means creating the watcher base, and the first (default) watcher."""

    # Create the base
    create_watcher_base(args.watcher, args.base)

    # Create the first default watcher
    if not args.create_empty:
        create_watcher(args.watcher)
