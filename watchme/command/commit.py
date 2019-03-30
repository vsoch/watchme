'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.utils import run_command
from watchme.logger import bot
import os

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
    run_command('git commit -C %s -a -m "%s"' % (repo, message))
