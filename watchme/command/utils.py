'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.defaults import (
    WATCHME_BASE_DIR, 
    WATCHME_TASK_TYPES
)

from watchme.utils import ( get_tmpdir, run_command )
from watchme.logger import bot

import os
import re
import shutil
import sys

def get_watchers(base=None, quiet=False):
    '''list the watchers installed at a base. If base is not defined,
       the default base is used.

       Parameters
       ==========
       base: the watchme base, defaults to $HOME/.watchme
    '''
    if base == None:
        base = WATCHME_BASE_DIR

    if os.path.exists(base):
        watchers = os.listdir(base)
        if quiet == False:
            bot.info('\n'.join(watchers))
        return watchers
    else:
        bot.exit('%s does not exist.' % base)


def list_watcher(watcher, base=None):
    '''list the contents (tasks) of a single watcher.

       Parameters
       ==========
       base: the watchme base, defaults to $HOME/.watchme
    '''
    if base == None:
        base = WATCHME_BASE_DIR

    repo = os.path.join(base, watcher)
    return _general_list(repo, 'watcher', base)


def list_task(watcher, task, base=None):
    '''list the contents (result files) of a task folder beloning to a watcher.

       Parameters
       ==========
       watcher: the watcher folder to use
       task: the task folder within
       base: the watchme base, defaults to $HOME/.watchme
    '''
    if base == None:
        base = WATCHME_BASE_DIR

    task_folder = os.path.join(base, watcher, task)
    return _general_list(task_folder, 'task', base)


def _general_list(path, prefix='path', base=None):
    '''a shared function for listing (and returning) files.

       Parameters
       ==========
       path: the full path to list, if it exists
       prefix: a prefix to print for the type
       base: the watchme base, defaults to $HOME/.watchme
    '''
    if base == None:
        base = WATCHME_BASE_DIR

    if os.path.exists(path):
        files = os.listdir(path)
        bot.custom(prefix="%s:" % prefix, message="%s" % path, color="CYAN")
        bot.info('\n  '.join(files))
    else:
        bot.exit('%s does not exist.' % base)


def list_watcher_types():
    '''list the exporter options provided by watchme
    '''
    bot.custom(prefix="watchme:", message="watcher task types", color="CYAN")
    bot.info('\n  '.join(WATCHME_TASK_TYPES))


def clone_watcher(repo, base=None, name=None):
    '''clone a watcher from Github (or other version control with git)
       meaning that we clone to a temporary folder, and then move
       to a new folder. By default, the user gets all tasks associated
       with the watcher, along with the git folder so that removing
       is also done with version control.

       Parameters
       ==========
       repo: the repository to clone
       base: the watchme base, defaults to $HOME/.watchme
       name: a new name for the watcher, if a rename is desired.
    '''    
    if base == None:
        base = WATCHME_BASE_DIR

    # clone_watcher(repo=repo, base=args.base, name=extra)
    # STOPPED HERE - need to test this.

    # Validate the repository address
    if not re.search('^git@|http', repo):
        bot.exit('Please provide a valid url to git repository')

    # if the name is None, use the repo name
    if name == None:
        name = os.path.basename(repo) 

    # Ensure we aren't overwriting
    dest = os.path.join(base, name)
    if os.path.exists(dest):
        bot.exit('%s already exists, choose a different watcher name.' % name)

    clone_dest = get_tmpdir(prefix="watchme-clone", create=False)
    run_command("git clone %s %s" %(repo, clone_dest))

    # Valid by default - will copy over if valid
    valid = True    

    # Iterate over watchers
    watchers = os.listdir(clone_dest)
    for watcher in watchers:
        watcher = os.path.join(clone_dest, watcher)
        tasks = os.listdir(watcher)

        # Check that tasks include watchme.cfg
        for task in tasks:
            if not task.startswith('task'):
                continue
            task_folder = os.path.join(watcher, task)
            content = os.listdir(task_folder)
            if 'watcher.cfg' not in content:
                bot.error('%s is missing a watcher.cfg' % task)
                valid = False 
                break
                
    if valid:
        shutil.move(clone_dest, dest)
        
    if os.path.exists(clone_dest):
        shutil.rmtree(clone_dest)
