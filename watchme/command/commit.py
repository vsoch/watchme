'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''
from watchme.utils import ( 
    run_command, 
    write_file,
    get_tmpdir
)
from watchme.logger import bot
from watchme.defaults import WATCHME_BASE_DIR
import os
from datetime import datetime
import shutil
import time

def git_pwd(func):
    '''ensure that we are in the repo present working directory before running
       a git command. Return to where we were before after completion.
       The repo is always the first (positional or keyword) argument.
    '''      
    def git_pwd_inner(*args, **kwargs): 

        # Repo is either provided as a keyword argument, or the first positionl
        repo = kwargs.get('repo', args[0])

        # Keep a record of the present working directory
        pwd = os.getcwd()
        os.chdir(repo)
          
        # Run the git command         
        func(*args, **kwargs) 

        # Return to where we were before
        os.chdir(pwd)
    
    return git_pwd_inner


@git_pwd
def git_commit(repo, task, message):
    '''Commit to the git repo with a particular message. folder.

       Parameters
       ==========
       repo: the repository to commit to.
       task: the name of the task to add to the commit message
       message: the message for the commit, passed from the client
    '''
    # Commit with the watch group and date string
    message = 'watchme %s %s' %(task, message)

    # Commit
    command = 'git commit -a -m "%s"' % message
    bot.debug(command)
    run_command(command)

@git_pwd
def write_timestamp(repo, task, filename='TIMESTAMP'):
    '''write a file that includes the last run timestamp. This should be written
       in each task folder after a run.

       Parameters
       ==========
       repo: the repository to write the TIMESTAMP file to
       task: the name of the task folder to write the file to
       filename: the filename (defaults to TIMESTAMP)
    '''
    ts = time.time()
    strtime = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    filename = os.path.join(repo, task, filename)
    write_file(filename, strtime)  
    git_add(repo, filename)


def git_clone(repo, name=None, base=None, force=False):
    '''clone a git repo to a destination. The user can provide the following
       groupings of arguments:

       base without name: destination is ignored, the repo is cloned (named as
       it is) to the base. If the folder exists, --force must be used to remove
       it first.

       base with name: destination is ignored, repo is cloned (and named based
       on name variable) to the base. The same applies for force.

       dest provided: the repo is cloned to the destination, if it doesn't exist
       and/or force is True.

       Parameters
       ==========
       name: the name of the watcher to add
       base: the base of the watcher (defaults to $HOME/.watchme
       force: remove first if already exists
    '''
    if base == None:
        base = WATCHME_BASE_DIR

    # Derive the repository name
    if name == None:
        name = os.path.basename(repo).replace('.git', '')

    # First clone to temporary directory
    tmpdir = get_tmpdir()
    command = 'git clone %s %s' % (repo, tmpdir)    
    bot.debug(command)
    run_command(command)

    # ensure there is a watchme.cfg
    if not os.path.exists(os.path.join(tmpdir, 'watchme.cfg')):
        shutil.rmtree(tmpdir)
        bot.exit('No watchme.cfg found in %s, aborting.' % repo)

    # If it's good, move the repository
    dest = os.path.join(base, name)

    # Don't allow for overwrite
    if os.path.exists(dest): 
        if force is False:
            shutil.rmtree(tmpdir)        
            bot.exit('%s exists. Use --force to overwrite' % dest)
        else:
            shutil.rmtree(dest)

    # Move the repository there
    shutil.move(tmpdir, dest)
    bot.info('Added watcher %s' % name)
    

@git_pwd
def git_add(repo, files):
    '''add one or more files to the git repo.

       Parameters
       ==========
       repo: the repository to commit to.
       files: one or more files to add.
    '''
    if not isinstance(files, list):
        files = [files]

    for f in files:
        command = 'git add %s' % f
        bot.debug(command)
        run_command(command)
