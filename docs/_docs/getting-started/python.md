---
title: Interactive Python
category: Getting Started
permalink: /getting-started/python/
order: 4
---

If you are a developer (or just want to use python to interact with your watchers
and tasks) here are some ways that you can do that.

## Instantiate a Watcher

Let's say we have a watcher named "watcher" in the default base at $HOME/.watchme.
We can instantiate it easily (this is from an interactive Python terminal):


```python
from watchme import get_watcher
watcher = get_watcher('watcher')
# [watcher|watcher]
```

## Inspection

You can check the tasks that the watcher has:

```python
watcher.inspect()
[watcher]
active  = false

[task-harvard-hpc]
url  = https://www.rc.fas.harvard.edu/about/people/
active  = true
type  = urls
```

or for a specific task:

```python
watcher.inspect('task-reddit-hpc')
[task-harvard-hpc]
url  = https://www.rc.fas.harvard.edu/about/people/
active  = true
type  = urls
```

or use a list to inspect more than one.

## Get tasks

You can get a task instance by asking for it by name:

```python
task = watcher.get_task('task-harvard-hpc')
[task|task-reddit-hpc]
```

If the task doesn't exist, or isn't valid, you'll get an error message and
None will be returned. You can also ask for all tasks that the watcher has,
that are valid:

```python
tasks = watcher.get_tasks()
Found 1 contender tasks.
```

## Run a task

To run a task manually, you can either run all tasks from the watcher (done with
multiprocessing):

```bash
watcher.run()
```

And when you do this, the watcher's repository will be updated with data
and the running timestamp. If you want to run a task and return a result
without updating / interacting with the watcher, just run the task directly:

```python
task.run()
```

## Get function to run it

To hand the task off to multiprocessing, we need to hand over a function,
and a set of variables to provide to it. You can do this with two functions:

```python
params = task.export_params()
func = task.export_func(**params)
```

The export_func function should take all of the (exploded) params.

**under development**


Read about [Concepts]({{ site.baseurl }}/getting-started/concepts/),
[Environment]({{ site.baseurl }}/getting-started/environment/) or go back to the
[Quick Start]({{ site.baseurl }}/getting-started/)

