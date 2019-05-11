# Psutils

The psutils has one or more [tasks](tasks.py) that can be added to a watcher.
Unlike a traditional watcher task group, psutils also offers a decorator
to collect system metrics during the runtime of a function. The metrics
are saved to an existing watcher based on the function name, with
a folder starting with `decorator-`. For example, let's create a watcher
folder to use with a new decorator:

```bash
$ watchme create decorator
```

And then here is how we would use the psutils decorator with some long running
function:

```python
from watchme.watchers.psutils.decorators import monitor_resources

@monitor_resources('decorator', seconds=3)
def myfunc():
    long_list = []
    for i in range(100):
        long_list = long_list + (i*10)*['pancakes']
        sleep 10
```

The first parameter is the watcher name (it must exist), the second is
how often to collect metrics (in seconds) and the third is a single or list
of psutils tasks that you want to run.
