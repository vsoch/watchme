---
title: psutils
category: Watcher Tasks
permalink: /watchers/psutils/
order: 2
---

The psutils watcher is one of @vsoch favorites. It will help to monitor
general system resources (memory, networks, sensors, cpu, users) along with 
basic python environment. If your python installation doesn't have the `psutil`
module, install as follows:

```bash
pip install watchme[psutils]
```

Next, create a watcher for your tasks to live under:

```bash
$ watchme create system
```

Now let's walk through each of the tasks. If you aren't familiar with how
to add a task and otherwise manage them, see the [getting started]({{ site.baseurl }}/getting-started/)
docs. Here are the functions exposed by psutils:

 - [CPU Task](#the-cpu-task)
 - [Memory Task](#the-memory-task)
 - [Network Task](#the-network-task)
 - [Python Task](#the-python-task)
 - [Sensors Task](#the-sensors-task)
 - [System Task](#the-system-task)
 - [Users Task](#the-users-task)


## Add a Task

Remember that we are going to be added tasks to our watcher, "system" above.
The general format to add a task looks like this:

```bash
$ watchme add <watcher> <task-name> key1@value1 key2@value2
```

The key and value pairs are going to vary based on the watcher task.

### Task Parameters

The set of psutil tasks don't have any required arguments, but for each you can define
a comma separated list of entries to skip.

| Name | Required | Default | Example | Notes|
|------|----------|---------|---------|-----------|
| skip  | No     |undefined|skip@ | varies by task (see below) |

Also note that for all of the tasks below, you need to select the type of task with `--type psutils`.

### Return Values

All of the return values here will be dictionaries, meaning appropriate to export to json.
You shouldn't need to define a `file_name` parameter, as it will be set automatically to
be your host plus username. However, you are free to set this parameter to change this 
value.

### 1. The CPU Task

This task will report basic cpu parameters. You add it by selection of the
parameter `func@cpu_task`

```bash
$ watchme add system task-cpu --type psutils func@cpu_task
[watcher|system]
[task-cpu]
func  = cpu_task
active  = true
type  = psutils
```

In the above, we added the task "task-cpu" to the watcher called "system"
If you don't define `file_name` it will be saved as a json file in the task
folder, named according to your user and host. The following attributes
will be retrieved (and you can remove any with the comma separated list "skip."

 - cpu_freq
 - cpu_percent
 - cpu_count
 - cpu_stats
 - cpu_times
 - cpu_times_percent

For example, to skip the first two, you would add the watcher like this:

```bash
$ watchme add system task-cpu --type psutils func@cpu_task skip@cpu_freq,cpu_percent
```

For more information on the psutil functions for cpu, see [here](https://psutil.readthedocs.io/en/latest/#cpu).


### 2. The Memory Task

This task will report stats on virtual memory. You add it by selection of the
parameter `func@memory_task`

```bash
$ watchme add system task-memory --type psutils func@memory_task
[task-memory]
func  = memory_task
active  = true
type  = psutils
```

You don't need to use "skip" for this task because there is only one entry
returned in the dictionary ("virtual_memory") so if you don't want this information,
just don't run the task.

For more information on the psutil functions for memory, see [here](https://psutil.readthedocs.io/en/latest/#memory).


### 3. The Networking Task

This task will report a bunch of network statistics. This is one that you might want to be
careful with, since it exports a lot of your host networking information that might be sensitive
if freely available. I would [read about](https://psutil.readthedocs.io/en/latest/#network) 
the different parameters here first. stats on virtual memory. You add it by selection of the
parameter `func@net_task`. In the example below, I'm going to skip 'net_if_address' and "net_connections"

```bash
$ watchme add system task-network --type psutils func@net_task skip@net_connections,net_if_address
[task-network]
func  = net_task
skip  = net_connections,net_if_address
active  = true
type  = psutils
```

All the possible attributes you can get are:

 - net_connections
 - net_if_address
 - net_if_stats
 - net_io_counters

If you want to see what is exported, just try importing the task into a python
terminal and running it:

```python
from watchme.watchers.psutils.tasks import net_task
net_task()
```

For more information on the psutil functions for networking, see [here](https://psutil.readthedocs.io/en/latest/#network).


### 4. The Python Task

This task will report information about install location, modules, and version
of the Python running the task. To set up this task:

```bash
$ watchme add system task-python --type psutils func@python_task
[task-python]
func  = python_task
active  = true
type  = psutils
```

All the possible attributes you can get (and disclude with the skip parmeter are):

 - modules
 - version
 - path
 - prefix
 - executable
 - copyright


Most of these functions fall under `psutil.os` and `psutil.os.sys`. There are quite
a few, so if you think something is missing please [open an issue]({{ site.repo }}/issues).


### 5. The Sensors Task

This is one of the coolest! You can actually use psutil to get information on your
system fans, temperature, and even battery. Set up the task like this:

```bash
$ watchme add system task-sensors --type psutils func@sensors_task
[task-sensors]
func  = sensors_task
active  = true
type  = psutils
```

All the possible attributes you can get (and disclude with the skip parmeter are):

 - sensors_temperatures
 - sensors_fans
 - sensors_battery

See the [sensors](https://psutil.readthedocs.io/en/latest/#sensors) documentation
for details on what is included.


### 6. The System Task

The system task will provide (basic) system information. This is another task
that if you see something missing (that you think should be there) you should
[open an issue]({{ site.repo }}/issues). Here is how to add the task:

```bash
$ watchme add system task-system --type psutils func@system_task
[task-system]
func  = system_task
active  = true
type  = psutils
```

All the possible attributes you can get (and disclude with the skip parmeter are):

 - platform
 - api_version
 - maxsize
 - bits_per_digit
 - sizeof_digit
 - version_info
 - sep
 - uname

See the [system](https://psutil.readthedocs.io/en/latest/#other-system-info) documentation
for details on what is included. A lot of these params are taken from `psutil.sys`.


### 7. The Users Task

The last is the user task, which will export active users on the system. It's 
likely that this task result won't change over time.

```bash
$ watchme add system task-users --type psutils func@users_task
[task-users]
func  = users_task
active  = true
type  = psutils
```

There is only one entry in the result (users) so if you don't want this,
just don't run the task. users is a function under 
the [system](https://psutil.readthedocs.io/en/latest/#other-system-info) documentation. 


### Verify the Addition

Once you add one or more tasks, you can inspect your watcher configuration
file at $HOME/.watchme/system/watchme.cfg:

```bash
$ cat $HOME/.watchme/system/watchme.cfg
```

You can also use inspect:

```bash
$ watchme inspect system
```

At this point, you can test running the watcher with the `--test` flag for
run:

```bash
$ watchme run system --test
```

and when you are ready, activate the entire watcher to run:

```bash
$ watchme activate system
$ watchme run system
```

And don't forget to set a schedule to automated it:

```bash
$ watchme schedule system @hourly
$ crontab -l
@hourly /home/vanessa/anaconda3/bin/watchme run system # watchme-system
```

Every time your task runs, new files (or old files will be updated) and
you can choose to push the entire watcher folder to GitHub to have
reproducible monitoring! Since the parameter result files are named
based on your host and username, others could fork the repo, run
on their system, and pull request to combine data.

When you are ready, [read more](https://vsoch.github.io/watchme/getting-started/index.html#how-do-i-export-data) about exporting data.
