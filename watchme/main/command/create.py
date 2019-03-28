'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.utils import ( run_command, mkdir_p )
from watchme.defaults import ( WATCHME_WATCHER, WATCHME_BASE_DIR )
from watchme.logger import bot
from watcher.config import generate_config
import os


def create_watcher(name=None):
    '''create a watcher, meaning a folder with a configuration and
       initialized git repo.

       Parameters
       ==========
       name: the watcher to create, uses default or WATCHME_WATCHER
    '''
    if name == None:
        name = WATCHME_WATCHER

    # Create the repository folder
    repo = os.path.join(WATCHME_BASE_DIR, name)

    if not os.path.exists(repo):

        bot.info('Adding watcher %s...' % repo)
        mkdir_p(repo)

        # Ensure no gpg signing happens
        run_command("git --git-dir=%s init" % repo)
        run_command("git --git-dir=%s config commit.gpgsign false" % repo)
    
        # Add the watcher configuration file
        generate_config(repo)


def create_watcher_base(name=None):
    '''create a watch base and default repo, if it doesn't already exist.

       Parameters
       ==========
       name: the watcher to create, uses default or WATCHME_WATCHER
    '''
    if not os.path.exists(WATCHME_BASE_DIR):
        bot.info('Creating %s...' % WATCHME_BASE_DIR)
        mkdir_p(WATCHME_BASE_DIR)

    # Create the first (default) repo.
    create_watcher(name)
