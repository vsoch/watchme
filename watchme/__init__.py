__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from watchme.version import __version__


def get_watcher(name="watcher", base=None, create=False, quiet=True, **kwargs):
    """
    get the correct watcher depending on the environment variable
    WATCHME_WATCHER or default to "watcher"

    Parameters
    ==========
    name: the name of the watcher, will be made all lowercase
    base: the watcher base, if not defined, will use WATCHER_BASE_DIR envar
    create: if the watcher folder doesn't exist, create it (default False)
            for all interactions with a watcher other than create, we should
            exit if the watcher the user wants doesn't exist.
    quiet: if True, suppress most output about the client (e.g. speak)
    """
    from watchme.watchers import Watcher

    Watcher.name = name.lower()
    Watcher.quiet = quiet

    # Initialize the watcher
    return Watcher(create=create, base=base)
