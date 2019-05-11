'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.command import git_clone
from watchme.logger import bot

def main(args, extra):
    '''get a watcher using git, meaning clone to a temporary location and then
       copying the entire repo (or a subfolder) to the watcher base.
    '''    

    # Required - will print help if not provided
    repo = args.repo[0]
    
    # If a custom name is provided, add it
    if extra != None:
        extra = extra.pop(0)

    # Clone the watcher, and optionally just one task
    git_clone(repo=repo, base=args.base, name=extra, force=args.force)
