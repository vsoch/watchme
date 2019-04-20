'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

The watcher is actually a connection to crontab. This is what helps to schedule
the watched to check for changes at some frequency, and update the files.


'''

import errno
import os
import tempfile
import json
import io
import socket
import shutil
import sys
import getpass



from watchme.logger import bot

# FOLDER OPERATIONS ############################################################

def get_userhome():
    '''get the user home based on the effective uid
    '''
    return os.path.expanduser("~")

def get_user():
    '''return the active user'''
    return getpass.getuser()

def get_host():
    '''return the hostname'''
    return socket.gethostname()

def mkdir_p(path):
    ''' mkdir_p attempts to get the same functionality as mkdir -p

        Paramters
        =========
        param path: the path to create.
    '''
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            bot.error("Error creating path %s, exiting." % path)
            sys.exit(1)


# FILE OPERATIONS ##############################################################

def generate_temporary_file(folder=None, prefix='watchme', ext=None):
    '''write a temporary file, in base directory with a particular extension.
      
       Parameters
       ==========
       folder: the base directory to write in. 
       prefix: the prefix to use
       ext: the extension to use.

    '''        
    if folder == None:
        folder = tempfile.gettempdir()
    tmp = next(tempfile._get_candidate_names())
    tmp = '%s/%s.%s' %(folder, prefix, tmp)

    # Does the user want an extension?
    if ext != None:
        tmp = "%s.%s" %(tmp, ext)

    return tmp


def get_tmpdir(prefix="", create=True):
    '''get a temporary directory for an operation. If SREGISTRY_TMPDIR
       is set, return that. Otherwise, return the output of tempfile.mkdtemp

       Parameters
       ==========
       prefix: Given a need for a sandbox (or similar), we will need to 
       create a subfolder *within* the SREGISTRY_TMPDIR.
       create: boolean to determine if we should create folder (True)
    '''
    tmpdir = tempfile.gettempdir()
    prefix = prefix or "watchme-tmp"
    prefix = "%s.%s" %(prefix, next(tempfile._get_candidate_names()))
    tmpdir = os.path.join(tmpdir, prefix)

    if not os.path.exists(tmpdir) and create is True:
        os.mkdir(tmpdir)

    return tmpdir


def copyfile(source, destination, force=True):
    '''copy a file from a source to its destination.
    '''
    if os.path.exists(destination) and force is True:
        os.remove(destination)
    shutil.copyfile(source, destination)
    return destination


def write_file(filename, content, mode="w"):
    '''write_file will open a file, "filename" and write content, "content"
    and properly close the file
    '''
    with open(filename, mode) as filey:
        filey.writelines(content)
    return filename


def write_json(json_obj, filename, mode="w", print_pretty=True):
    ''' write_json will (optionally,pretty print) a json object to file
    
        Parameters
        ==========
        json_obj: the dict to print to json
        filename: the output file to write to
        pretty_print: if True, will use nicer formatting
    '''
    with open(filename, mode) as filey:
        if print_pretty:
            filey.writelines(print_json(json_obj))
        else:
            filey.writelines(json.dumps(json_obj))
    return filename


def print_json(json_obj):
    ''' just dump the json in a "pretty print" format
    '''
    return json.dumps(
                    json_obj,
                    indent=4,
                    separators=(
                        ',',
                        ': '))


def read_file(filename, mode="r", readlines=True):
    '''write_file will open a file, "filename" and write content, "content"
       and properly close the file
    '''
    with open(filename, mode) as filey:
        if readlines is True:
            content = filey.readlines()
        else:
            content = filey.read()
    return content


def read_json(filename, mode='r'):
    '''read_json reads in a json file and returns
       the data structure as dict.
    '''
    with open(filename, mode) as filey:
        data = json.load(filey)
    return data
