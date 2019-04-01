'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''
from watchme.utils import ( 
    run_command, 
    write_file
)
from watchme.logger import bot
import os
from datetime import datetime
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


def git_clone(repo, dest=None):
    '''clone a git repo to a destination. If not provided, create a temporary
       directory.
    '''
    pass


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
