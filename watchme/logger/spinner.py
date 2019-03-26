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

import sys
import time
import threading
from random import choice

class Spinner:
    spinning = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

    @staticmethod
    def balloons_cursor():
        while 1: 
            for cursor in '. o O @ *': yield cursor

    @staticmethod
    def changing_arrows():
        while 1: 
            for cursor in '<^>v': yield cursor

    def select_generator(self, generator):
        if generator == None:
            generator = choice(['cursor',
                                'arrow',
                                'balloons'])

        return generator

    def __init__(self, delay=None, generator=None):
        generator = self.select_generator(generator)

        if generator == 'cursor':
            self.spinner_generator = self.spinning_cursor()
        elif generator == 'arrow':
            self.spinner_generator = self.changing_arrows()
        elif generator == 'balloons':
            self.spinner_generator = self.balloons_cursor()
            if delay is None: delay = 0.2
        else:
            self.spinner_generator = self.spinning_cursor()

        if delay and float(delay):
            self.delay = delay

    def run(self):
        while self.spinning:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.spinning = True
        threading.Thread(target=self.run).start()

    def stop(self):
        self.spinning = False
        time.sleep(self.delay)
