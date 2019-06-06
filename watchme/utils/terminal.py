'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''


from subprocess import (
    Popen,
    PIPE,
    STDOUT
)
import os
import re
import shlex

# Terminal Commands

def which(software, strip_newline=True):
    '''get_install will return the path to where an executable is installed.
    '''
    if software is None:
        software = "watchme"
    cmd = 'which %s' % software
    try:
        result = run_command(cmd)
        if strip_newline is True:
            result['message'] = result['message'].strip('\n')
        if "message" in result:
            return result['message']
        return result

    except: # FileNotFoundError
        return None


def get_installdir():
    '''get_installdir returns the installation directory of the application
    '''
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def run_command(cmd, sudo=False):
    '''run_command uses subprocess to send a command to the terminal.

    Parameters
    ==========
    cmd: the command to send, should be a list for subprocess
    error_message: the error message to give to user if fails,
    if none specified, will alert that command failed.

    '''

    cmd = shlex.split(cmd)

    if sudo is True:
        cmd = ['sudo'] + cmd

    try:
        output = Popen(cmd, stderr=STDOUT, stdout=PIPE)

    except FileNotFoundError:
        cmd.pop(0)
        output = Popen(cmd,stderr=STDOUT,stdout=PIPE)

    t = output.communicate()[0],output.returncode
    output = {'message':t[0],
              'return_code':t[1]}

    if isinstance(output['message'], bytes):
        output['message'] = output['message'].decode('utf-8')

    return output


# Environment

def convert2boolean(arg):
    '''
    convert2boolean is used for environmental variables
    that must be returned as boolean
    '''
    if not isinstance(arg, bool):
        return arg.lower() in ("yes", "true", "t", "1", "y")
    return arg


def get_watchme_env(prefix="WATCHMEENV_"):
    '''get any environment variables that start with WATCMEENV_, return the
       dictionary to the user.
    '''
    environ = {}

    # First extract variables from the environment
    for key, value in os.environ.items():

        # Variables that are specified, or start with WATCHMEENV included
        if key.startswith(prefix):

            # Replace the WATCHMEENV_ if present
            key = re.sub("^%s" % prefix, "", key)

            # Don't include empty strings
            if value not in ["", None]:

                environ[key] = value

    return environ
