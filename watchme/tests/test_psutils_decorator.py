#!/usr/bin/env python

from watchme.watchers.psutils.decorators import monitor_resources
from time import sleep

# Here we create a decorator to monitor "my func." Specifically, we:
# - want to use the watcher "decorator" that already exists. If we want to
#   create on the fly, we would set creat=True
# - will record metrics every 3 seconds
# - to have somewhat of an impact on system resources we make a long list
# - we test to ensure that something is returned ("Hello!")

@monitor_resources('system', seconds=3)
def myfunc(iters, pause):
    long_list = []
    print("Generating a long list, pause is %s and iters is %s" % (pause, iters))
    for i in range(iters):
        long_list = long_list + (i*10)*['pancakes']
        print("i is %s, sleeping %s seconds" % (i, pause))
        sleep(pause)

    return len(long_list)

# ensure the function runs when the file is called
if __name__ == '__main__':
    print("Calling myfunc with 2 iters")
    result = myfunc(2, 2)
    print("Result list has length %s" % result)
