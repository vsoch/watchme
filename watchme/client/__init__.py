#!/usr/bin/env python

'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.logger import bot
from watchme.defaults import ( 
    WATCHME_WATCHER, 
    WATCHME_TYPES, 
    WATCHME_DEFAULT_TYPE
)
import watchme
import argparse
import sys
import os


def get_parser():
    parser = argparse.ArgumentParser(description="WatchMe Command Line Tool")

    # Global Variables

    parser.add_argument('--debug', dest="debug", 
                        help="use verbose logging to debug.", 
                        default=False, action='store_true')

    parser.add_argument('--version', dest="version", 
                        help="show version and exit.", 
                        default=False, action='store_true')

    parser.add_argument('--quiet', dest="quiet", 
                        help="suppress additional output.", 
                        default=False, action='store_true')

    parser.add_argument('--watcher', dest="watcher", 
                        help="the watcher to create (defaults to watcher)", 
                        default=None, type=str)

    parser.add_argument('--base', dest="base", 
                        help="the watcher base (defaults to $HOME/.watchme)", 
                        default=None, type=str)

    description = 'actions for WatchMe Command Line Tool'

    subparsers = parser.add_subparsers(help='watchme actions',
                                       title='actions',
                                       description=description,
                                       dest="command")

    # init

    init = subparsers.add_parser("init",
                                 help="initialize watchme")
 
    init.add_argument('--empty', dest="create_empty", 
                      help="don't create the default watcher folder", 
                      default=False, action='store_true')

    # create

    create = subparsers.add_parser("create",
                                   help="create a new watcher")


    create.add_argument('--type', dest="watcher_type",
                        choices=WATCHME_TYPES, 
                        default=WATCHME_DEFAULT_TYPE)

    create.add_argument('watchers', nargs="*",
                        help='watchers to create (default: single watcher)')


    # activate

    activate = subparsers.add_parser("activate",
                                     help="activate a new watcher")

    activate.add_argument('watchers', nargs="*",
                          help='watchers to activate')

    # deactivate

    deactivate = subparsers.add_parser("deactivate",
                                       help="deactivate a watcher")

    deactivate.add_argument('watchers', nargs="*",
                            help='watchers to deactivate')

    return parser


def get_subparsers(parser):
    '''get_subparser will get a dictionary of subparsers, to help with printing help
    '''

    actions = [action for action in parser._actions 
               if isinstance(action, argparse._SubParsersAction)]

    subparsers = dict()
    for action in actions:
        # get all subparsers and print help
        for choice, subparser in action.choices.items():
            subparsers[choice] = subparser

    return subparsers



def main():
    '''the main entry point for the WatchMe Command line application.
    '''

    # Customize parser

    parser = get_parser()
    subparsers = get_subparsers(parser)

    def help(return_code=0):
        '''print help, including the software version and active client 
           and exit with return code.
        '''

        version = watchme.__version__
        
        bot.custom(message='Command Line Tool v%s' % version,
                   prefix='\n[WatchMe] ', 
                   color='CYAN')

        parser.print_help()
        sys.exit(return_code)
    
    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        help()
    try:
        args, unknown = parser.parse_known_args()
    except:
        sys.exit(0)

    extras = None
    if len(unknown) > 0:
        extras = unknown

    # if environment logging variable not set, make silent

    if args.debug is False:
        os.environ['MESSAGELEVEL'] = "INFO"

    # Show the version and exit
    if args.version is True:
        print(watchme.__version__)
        sys.exit(0)

    if args.command == "init": from .init import main
    if args.command == "create": from .create import main
    if args.command == "activate": from .activate import main
    if args.command == "deactivate": from .deactivate import main

    # Pass on to the correct parser
    return_code = 0
    try:
        main(args, extras)
        sys.exit(return_code)
    except UnboundLocalError:
        return_code = 1

    help(return_code)

if __name__ == '__main__':
    main()
