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
        repo = kwargs.get('repo', '')

        # If provided as a positional argument
        if repo == '' and len(args) > 0:
            repo = args[0]

        # Keep a record of the present working directory
        pwd = os.getcwd()
        os.chdir(repo)
          
        # Run the git command         
        result = func(*args, **kwargs) 

        # Return to where we were before
        os.chdir(pwd)
        return result
    
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
    return filename


@git_pwd
def git_date(repo, commit):
    '''get the date for a particular commit.
    
       Parameters
       ==========
       repo: the full path to the repository
       commit: the commit to get the date for
    '''
    command = 'git show -s --format=' + "%ci " + commit
    bot.debug(command)
    result = run_command(command)
    if result['return_code'] == 0:
        return result['message'].strip('\n')
    

@git_pwd
def git_show(repo, commit, filename):
    '''git show is used to pipe the content of a file at a particular commit
       to the screen (and calling python client). We must be in the $PWD of the
       repo for this to work.

       Parameters
       ==========
       repo: the repository to interact with
       commit: the commit to investigate for the file
       filename: the relative path to the file
    '''
    command = 'git show %s:%s' %(commit, filename)
    bot.debug(command)
    result = run_command(command)
    if result['return_code'] == 0:
        return result['message'].strip('\n')



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

    # Ensure we don't sign gpg key
    run_command("git --git-dir=%s/.git config commit.gpgsign false" % dest)
    bot.info('Added watcher %s' % name)
    

@git_pwd
def get_commits(repo, from_commit=None, to_commit=None, grep=None, filename=None):
    '''get commits, starting from and going to a particular commit. if grep
       is defined, filter commits to those with messages that match that
       particular expression

       Parameters
       ==========
       from_commit: the commit to start at
       to_commit: the commit to go to
       grep: the expression to match (not used if None)
       filename: the filename to filter to. Includes all files if not specified.
    '''
    command = 'git log --all --oneline --pretty=tformat:"%H"' 

    # The earliest commit
    if from_commit == None:
        from_commit = get_earliest_commit()

    # The latest commit
    if to_commit == None:
        to_commit = get_latest_commit()

    # A regular expression to search for (and filter commits)
    if grep != None:
        command = "%s --grep \"ADD results\"" % command

    # Add the commit range
    command = "%s %s..%s" % (command, from_commit, to_commit)

    if filename != None:
        command = "%s -- %s" %(command, filename)

    bot.info(command)
    results = run_command(command)['message']
    results = [x for x in results.split('\n') if x]
    return results


def get_earliest_commit():
    '''get the earliest commit for a repository. This is intended to be used
       when in the present working directory

       Parameters
       ==========
       repo: the repository path to get the commit from
    '''
    commit = run_command('git rev-list --max-parents=0 HEAD')['message']
    return commit.strip('\n')


def get_latest_commit():
    '''get the latest commit for a repository in the present working directory

       Parameters
       ==========
       repo: the repository path to get the commit from
    '''
    commit = run_command('git log -n 1 --pretty=format:"%H"')['message']
    return commit.strip('\n')

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
