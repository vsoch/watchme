'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''


from watchme.logger import bot
from subprocess import (
    Popen,
    PIPE,
    STDOUT
)
import os
import re
import shlex


# User Prompts

def confirm_prompt(prompt):
    '''A wrapper around choice_prompt, but ask the user specifically for a
       yes / no response that is converted to boolean for the calling agent.

       Parameters
       ==========
       prompt: the prompt to ask the user    
    '''
    choice = choice_prompt(prompt, choices = ["Y", "N", "y", "n"])
    return convert2boolean(choice)


def choice_prompt(prompt, choices=None, choice=None):
    '''Ask the user for a prompt, and only return when one of the requested
       options is provided.

       Parameters
       ==========
       prompt: the prompt to ask the user
       choices: a list of choices that are valid, defaults to [Y/N/y/n]
    
    '''
    if not choices:
        choices = ["y", "n", "Y", "N"]

    print(prompt)
    get_input = getattr(__builtins__, 'raw_input', input)
    pretty_choices = '/'.join(choices)
    message = 'Please enter your choice [%s] : ' %(pretty_choices)
    while choice not in choices:
        choice = get_input(message).strip()

        # If the option isn't valid, this is shown next
        message = "Please enter a valid option in [%s]" %(pretty_choices)    
    return choice


def regexp_prompt(prompt, regexp='.', answer=''):
    '''Ask the user for a text entry that matches a regular expression

       Parameters
       ==========
       prompt: the prompt to ask the user
       regexp: the regular expression to match. defaults to anything.
    
    '''
    get_input = getattr(__builtins__, 'raw_input', input)
    while not re.search(regexp, answer):
        answer = get_input(prompt + ': ').strip()
        # If the option isn't valid, this is shown next
        message = "Your entry must match the regular expression %s" % regexp    

    return answer


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


def convert2boolean(arg):
    '''
    convert2boolean is used for environmental variables
    that must be returned as boolean
    '''
    if not isinstance(arg, bool):
        return arg.lower() in ("yes", "true", "t", "1", "y")
    return arg
