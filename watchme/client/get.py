__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from watchme.command import git_clone


def main(args, extra):
    """get a watcher using git, meaning clone to a temporary location and then
    copying the entire repo (or a subfolder) to the watcher base.
    """

    # Required - will print help if not provided
    repo = args.repo[0]

    # If a custom name is provided, add it
    if extra is not None:
        extra = extra.pop(0)

    # Clone the watcher, and optionally just one task
    git_clone(repo=repo, base=args.base, name=extra, force=args.force)
