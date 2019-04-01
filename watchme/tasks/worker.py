'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.logger import bot
from watchme.defaults import WATCHME_WORKERS
import multiprocessing
import itertools
import time
import signal
import sys
import re
import os


class Workers(object):

    def __init__(self, workers=None, show_progress=False):

        if workers is None:
            workers = WATCHME_WORKERS
        self.workers = workers
        self.show_progress = show_progress
        bot.debug("Using %s workers for multiprocess." % (self.workers))

    def start(self):
        bot.debug("Starting multiprocess")
        self.start_time = time.time()

    def end(self):
        self.end_time = time.time()
        self.runtime = self.runtime = self.end_time - self.start_time
        bot.debug("Ending multiprocess, runtime: %s sec" % (self.runtime))

    def run(self, funcs, tasks):
        '''run will send a list of tasks, a tuple with arguments, through a function.
           the arguments should be ordered correctly.
        
           Parameters
           ==========
           funcs: the functions to run with multiprocessing.pool, a dictionary
                  with lookup by the task name
           tasks: a dict of tasks, each task name (key) with a 
                  tuple of arguments to process
        '''
        # Number of tasks must == number of functions
        assert(len(funcs)==len(tasks))

        # Keep track of some progress for the user
        progress = 1
        total = len(tasks)

        # if we don't have tasks, don't run
        if len(tasks) == 0:
            return

        # results will also have the same key to look up
        finished = dict()
        results = []

        try:
            prefix = "[%s/%s]" % (progress, total)
            if self.show_progress:
                bot.show_progress(0, total, length=35, prefix=prefix)
            pool = multiprocessing.Pool(self.workers, init_worker)

            self.start()
            for key, params in tasks.items():
                func = funcs[key]
                if not self.show_progress:
                    bot.info('Processing task %s:%s' % (key, params))
                result = pool.apply_async(multi_wrapper,
                                          multi_package(func, [params]))
                
                # Store the key with the result
                results.append((key, result))


            while len(results) > 0:
                pair = results.pop()
                key, result = pair
                result.wait()
                if self.show_progress:
                    bot.show_progress(progress, total, length=35, prefix=prefix)
                progress += 1
                prefix = "[%s/%s]" % (progress, total)
                finished[key] = result.get()

            self.end()
            pool.close()
            pool.join()

        except (KeyboardInterrupt, SystemExit):
            bot.error("Keyboard interrupt detected, terminating workers!")
            pool.terminate()
            sys.exit(1)

        except Exception as e:
            bot.error(e)

        return finished


# Supporting functions for MultiProcess Worker
def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def multi_wrapper(func_args):
    function, kwargs = func_args
    return function(**kwargs)

def multi_package(func, kwargs):
    zipped = zip(itertools.repeat(func), kwargs)
    return zipped
