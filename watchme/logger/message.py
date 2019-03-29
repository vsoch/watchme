'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

The watcher is actually a connection to crontab. This is what helps to schedule
the watched to check for changes at some frequency, and update the files.

'''

import os
import sys
from .spinner import Spinner

ABORT = -5
CRITICAL = -4
ERROR = -3
WARNING = -2
LOG = -1
INFO = 1
CUSTOM = 1
QUIET = 0
VERBOSE = VERBOSE1 = 2
VERBOSE2 = 3
VERBOSE3 = 4
DEBUG = 5

PURPLE = "\033[95m"
YELLOW = "\033[93m"
RED = "\033[91m"
DARKRED = "\033[31m"
CYAN = "\033[36m"

class WatchMeMessage:

    def __init__(self, MESSAGELEVEL=None):
        self.level = get_logging_level()
        self.history = []
        self.errorStream = sys.stderr
        self.outputStream = sys.stdout
        self.colorize = self.useColor()
        self.colors = {ABORT: DARKRED,
                       CRITICAL: RED,
                       ERROR: RED,    
                       WARNING: YELLOW,  
                       LOG: PURPLE,      
                       CUSTOM: PURPLE,       
                       DEBUG: CYAN,      
                       'OFF': "\033[0m", # end sequence
                       'CYAN':CYAN,
                       'PURPLE':PURPLE,
                       'RED':RED,
                       'DARKRED':DARKRED,
                       'YELLOW':YELLOW}
                       

    # Colors --------------------------------------------

    def useColor(self):
        '''useColor will determine if color should be added
        to a print. Will check if being run in a terminal, and
        if has support for asci'''
        COLORIZE = get_user_color_preference()
        if COLORIZE is not None:
            return COLORIZE
        streams = [self.errorStream, self.outputStream]
        for stream in streams:
            if not hasattr(stream, 'isatty'):
                return False
            if not stream.isatty():
                return False
        return True

    def addColor(self, level, text):
        '''addColor to the prompt (usually prefix) if terminal
        supports, and specified to do so'''
        if self.colorize:
            if level in self.colors:
                text = "%s%s%s" % (self.colors[level],
                                   text,
                                   self.colors["OFF"])
        return text

    def emitError(self, level):
        '''determine if a level should print to
        stderr, includes all levels but INFO and QUIET'''
        if level in [ABORT,
                     ERROR,
                     WARNING,
                     VERBOSE,
                     VERBOSE1,
                     VERBOSE2,
                     VERBOSE3,
                     DEBUG]:
            return True
        return False

    def emitOutput(self, level):
        '''determine if a level should print to stdout
        only includes INFO'''
        if level in [LOG,
                     INFO]:
            return True
        return False

    def isEnabledFor(self, messageLevel):
        '''check if a messageLevel is enabled to emit a level
        '''
        if messageLevel <= self.level:
            return True
        return False

    def emit(self, level, message, prefix=None, color=None):
        '''emit is the main function to print the message
        optionally with a prefix
        :param level: the level of the message
        :param message: the message to print
        :param prefix: a prefix for the message
        '''
        if color is None:
            color = level

        if prefix is not None:
            prefix = self.addColor(color, "%s " % (prefix))
        else:
            prefix = ""
            message = self.addColor(color, message)

        # Add the prefix
        message = "%s%s" % (prefix, message)

        if not message.endswith('\n'):
            message = "%s\n" % message

        # If the level is quiet, only print to error
        if self.level == QUIET:
            pass

        # Otherwise if in range print to stdout and stderr
        elif self.isEnabledFor(level):
            if self.emitError(level):
                self.write(self.errorStream, message)
            else:
                self.write(self.outputStream, message)

        # Add all log messages to history
        self.history.append(message)

    def write(self, stream, message):
        '''write will write a message to a stream,
        first checking the encoding
        '''
        if isinstance(message, bytes):
            message = message.decode('utf-8')
        stream.write(message)

    def get_logs(self, join_newline=True):
        ''''get_logs will return the complete history, joined by newline
        (default) or as is.
        '''
        if join_newline:
            return '\n'.join(self.history)
        return self.history


    def show_progress(
            self,
            iteration,
            total,
            length=40,
            min_level=0,
            prefix=None,
            carriage_return=True,
            suffix=None,
            symbol=None):
        '''create a terminal progress bar, default bar shows for verbose+
        :param iteration: current iteration (Int)
        :param total: total iterations (Int)
        :param length: character length of bar (Int)
        '''
        percent = 100 * (iteration / float(total))
        progress = int(length * iteration // total)

        if suffix is None:
            suffix = ''

        if prefix is None:
            prefix = 'Progress'

        # Download sizes can be imperfect, setting carriage_return to False
        # and writing newline with caller cleans up the UI
        if percent >= 100:
            percent = 100
            progress = length

        if symbol is None:
            symbol = "="

        if progress < length:
            bar = symbol * progress + '|' + '-' * (length - progress - 1)
        else:
            bar = symbol * progress + '-' * (length - progress)

        # Only show progress bar for level > min_level
        if self.level > min_level:
            percent = "%5s" % ("{0:.1f}").format(percent)
            output = '\r' + prefix + \
                " |%s| %s%s %s" % (bar, percent, '%', suffix)
            sys.stdout.write(output),
            if iteration == total and carriage_return:
                sys.stdout.write('\n')
            sys.stdout.flush()

    # Logging ------------------------------------------

    def abort(self, message):
        self.emit(ABORT, message, 'ABORT')

    def critical(self, message):
        self.emit(CRITICAL, message, 'CRITICAL')

    def error(self, message):
        self.emit(ERROR, message, 'ERROR')

    def exit(self, message, error_code=255):
        self.emit(ERROR, message, 'ERROR')
        sys.exit(error_code)

    def warning(self, message):
        self.emit(WARNING, message, 'WARNING')

    def log(self, message):
        self.emit(LOG, message, 'LOG')

    def custom(self, prefix, message="", color=PURPLE):
        self.emit(CUSTOM, message, prefix, color)

    def info(self, message):
        self.emit(INFO, message)

    def newline(self):
        return self.info("")

    def verbose(self, message):
        self.emit(VERBOSE, message, "VERBOSE")

    def verbose1(self, message):
        self.emit(VERBOSE, message, "VERBOSE1")

    def verbose2(self, message):
        self.emit(VERBOSE2, message, 'VERBOSE2')

    def verbose3(self, message):
        self.emit(VERBOSE3, message, 'VERBOSE3')

    def debug(self, message):
        self.emit(DEBUG, message, 'DEBUG')

    def is_quiet(self):
        '''is_quiet returns true if the level is under 1
        '''
        if self.level < 1:
            return False
        return True


    # Terminal ------------------------------------------

    def table(self, rows, col_width=2):
        '''table will print a table of entries. If the rows is 
        a dictionary, the keys are interpreted as column names. if
        not, a numbered list is used.
        '''

        labels = [str(x) for x in range(1,len(rows)+1)]
        if isinstance(rows, dict):
            labels = list(rows.keys())
            rows = list(rows.values())

        for row in rows: 
            label = labels.pop(0)
            label = label.ljust(col_width)
            message = "\t".join(row)
            self.custom(prefix=label,
                        message=message)
        


def get_logging_level():
    '''get_logging_level will configure a logging to standard out based on the user's
    selected level, which should be in an environment variable called
    MESSAGELEVEL. if MESSAGELEVEL is not set, the maximum level
    (5) is assumed (all messages).
    '''
    try:
        level = int(os.environ.get("MESSAGELEVEL", INFO))

    except ValueError:

        level = os.environ.get("MESSAGELEVEL", INFO)
        if level == "CRITICAL":
            return CRITICAL
        elif level == "ABORT":
            return ABORT
        elif level == "ERROR":
            return ERROR
        elif level == "WARNING":
            return WARNING
        elif level == "LOG":
            return LOG
        elif level == "INFO":
            return INFO
        elif level == "QUIET":
            return QUIET
        elif level.startswith("VERBOSE"):
            return VERBOSE3
        elif level == "LOG":
            return LOG
        elif level == "DEBUG":
            return DEBUG

    return level


def get_user_color_preference():
    COLORIZE = os.environ.get('WATCHME_COLORIZE', None)
    if COLORIZE is not None:
        COLORIZE = convert2boolean(COLORIZE)
    return COLORIZE


def convert2boolean(arg):
    '''convert2boolean is used for environmental variables that must be
    returned as boolean'''
    if not isinstance(arg, bool):
        return arg.lower() in ("yes", "true", "t", "1", "y")
    return arg


WatchMeMessage.spinner = Spinner()
bot = WatchMeMessage()
