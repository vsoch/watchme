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
pip install watchme[watcher-psutils]
```

Next, create a watcher for your tasks to live under:

```bash
$ watchme create system
```

Now let's walk through each of the tasks. If you aren't familiar with how
to add a task and otherwise manage them, see the [getting started]({{ site.baseurl }}/getting-started/)
docs. Here are the functions exposed by psutils:

 - [Monitor Pid Task](#1-the-monitor-pid-task)
 - [CPU Task](#2-the-cpu-task)
 - [Memory Task](#3-the-memory-task)
 - [Network Task](#4-the-network-task)
 - [Python Task](#5-the-python-task)
 - [Sensors Task](#6-the-sensors-task)
 - [System Task](#7-the-system-task)
 - [Users Task](#8-the-users-task)


## Add a Task

Remember that we are going to be added tasks to our watcher, "system" above.
The general format to add a task looks like this:

```bash
$ watchme add-task <watcher> <task-name> key1@value1 key2@value2
```

The key and value pairs are going to vary based on the watcher task.

### Task Parameters

The set of psutil tasks don't have any required arguments, but for each you can define
a comma separated list of entries to skip.

| Name | Required | Default | Example | Notes|
|------|----------|---------|---------|-----------|
| skip  | No     |undefined|skip@ | varies by task (see below) |

Also note that for all of the tasks below, you need to select the type of task with `--type psutils`.

### Task Environment

For any task, if you have a variable exporter to the environment that starts
with `WATCHMENV_`, it will be found and added to the result. For example,
`WATCHMENV_result_id=123` will be saved to the results dictionary with key
"result_id" set to "123."


### Return Values

All of the return values here will be dictionaries, meaning appropriate to export to json.
You shouldn't need to define a `file_name` parameter, as it will be set automatically to
be your host plus username. However, you are free to set this parameter to change this 
value.


### 1. The Monitor Pid Task

This task is useful for monitoring a specific process. You can run it as a
task (discussed first) or a decorator to a function to enable continuous monitoring.
Either way, you will want to create your watcher first:

```bash
$ watchme create system
```

#### Run as a Task

To run as a task, you will want to provide `func@monitor_pid_task` when you create the task. 
You are also required to add a pid, and this can be a number, or the name of the process.
Either way, likely you would be running this for a long running
process, and in the case of providing an integer, you would need to update
the pid of the process when you restart your computer. Here is an example
adding a process name I know will be running when my computer starts:

```bash
$ watchme add-task system task-monitor-slack --type psutils func@monitor_pid_task pid@slack
[task-monitor-slack]
func  = monitor_pid_task
pid  = slack
active  = true
type  = psutils
```

If you choose a process name, remember that different processes can have the same
name (for example, think about the case of having multiple Python interpreters open!)
This means that watchme will select the first in the list that it finds. If you
have preference for a specific one, then it's recommended that you provide the
process id directly.

##### Customize

You can also add a parameter called "skip", including one or more (comma separate)
indices in the results to skip.

```bash
$ watchme add-task system task-monitor-slack --type psutils func@monitor_pid_task pid@slack skip@cpu_freq,cpu_percent
```

By default, you'll get a lot of data! You should skip those you don't need:

 - cmdline
 - cpu_num
 - memory_percent
 - cwd
 - nice
 - username
 - pid
 - create_time
 - memory_full_info
 - terminal
 - connections
 - gids
 - status
 - cpu_times
 - name
 - ppid
 - num_ctx_switches
 - cpu_percent
 - cpu_affinity
 - num_fds
 - exe
 - uids
 - ionice
 - io_counters
 - open_files
 - num_threads


We purposefully don't include the environment (environ) because it tends to not change,
and more importantly, we want to not expose sensitive information. If you want
to add this back in, you can do that:

```bash
$ watchme add system task-monitor-slack --type psutils func@monitor_pid_task pid@slack include@environ
```

We don't show threads because it would make the data too big, but we do include `num_threads`.

To test out the task, you can do the following:

```bash
$ watchme run system task-monitor-slack --test
```

You'll see the results.json print to the screen! When it's time to use the
watcher, you can [active and schedule it](#verify-the-addition).

#### Use as a Decorator

Although the parameters are not stored in the `watchme.cfg`, if you use
the decorator to run the same task, the .git repository is still used
as a database, and you can collect data to monitor your different Python
functions on the fly. Specifically, the decorator is going to use
multiprocessing to run your function, and then watch it via the process id (pid).
You get to choose how often (in seconds) you want to record metrics like
memory, io counters, and cpu, and threads. See [here](https://gist.github.com/vsoch/19957205764ab12a153ddbecd837ffb3#file-result-json) 
for an example of default output for one timepoint.
This decorator function uses the same task function, that we discussed first,
but with a different invocation.


```python
from watchme.watchers.psutils.decorators import monitor_resources
from time import sleep

@monitor_resources('system', seconds=3)
def myfunc():
    long_list = []
    for i in range(100):
        long_list = long_list + (i*10)*['pancakes']
        print("i is %s, sleeping 10 seconds" % i)
        sleep(10)
```

The first argument is the name of the watcher (e.g., system) and you are also allowed
to specify the following arguments (not shown):

 - include: a list of keys to add back in (e.g., "environ")
 - skip: a list of keys to skip (see section above for default)
 - create: create the watcher if it doesn't exist (default is False, must exist)
 - only: forget about include/skip, **only** include these fields
 - name: if you want to call the result folder something other than the function name

Why don't you need specify a pid? Your running function will produce the 
process id, so you don't need to provide it. Let's run this script. You can get 
the full thing [from the gist here](https://gist.github.com/vsoch/19957205764ab12a153ddbecd837ffb3).
You'll notice in the gist example we demonstrate "myfunc" taking arguments too.

```bash
$ python test_psutils_decorator.py
Calling myfunc with 2 iters
Generating a long list, pause is 2 and iters is 2
i is 0, sleeping 2 seconds
i is 1, sleeping 2 seconds
Result list has length 10
```

Great! So it ran for the watcher we created called `system`, but where
are the results? Let's take a look in our watcher folder:

```bash
~/.watchme/system$ tree
.
├── decorator-psutils-myfunc
│   ├── result.json
│   └── TIMESTAMP
├── task-monitor-slack
│   ├── result.json
│   └── TIMESTAMP
└── watchme.cfg

2 directories, 5 files
```

In addition to the task that we ran, "task-monitor-slack," we also have
results in a new "decorator-psutils-myfunc" folder. You've guessed it right -
the decorator namespace creates folders of the format `decorator-psutils-<name>`,
where name is the name of the function, or a "name" parameter you provide to the
decorator.

> What is a result?

Remember that we are monitoring our function every 3 seconds, so for a function
that lasts about 10, we will record process metrics three times. 
How would we export that data? Like this:

```bash
$ watchme export system decorator-psutils-myfunc result.json --json
```

We ask for `--json` because we know the result is provided in json.
For the above export, we will find three commits, each with a commit id,
timestamp, and full result:

```
git log --all --oneline --pretty=tformat:"%H" --grep "ADD results" 7a7cb5535c96e06433af9c47485ba253137e580f..03b793dfe708c310f32526041775ec38449ccd54 -- decorator-psutils-myfunc/result.json
{
    "commits": [
        "03b793dfe708c310f32526041775ec38449ccd54",
        "71012b7f2b5d247318b2dcf187ee2c823ad7ef63",
        "e1d06f86eac18cc6d54d3c8a62aeede7f8b85bac"
    ],
    "dates": [
        "2019-05-11 12:31:49 -0400",
        "2019-05-11 12:31:20 -0400",
        "2019-05-11 12:28:45 -0400"
    ],
    "content": [
        {
            "cpu_percent": 0.0,
            "cpu_num": 3,
...
```

And each entry coincides with one collection of data during the task run. You
can plot different metrics over time to see the change in the process resource
usage. If you are interested in what a (default) output will look like,
see the [gist here](https://gist.github.com/vsoch/19957205764ab12a153ddbecd837ffb3#file-result-json).

### 2. The CPU Task

This task will report basic cpu parameters. You add it by selection of the
parameter `func@cpu_task`

```bash
$ watchme add-task system task-cpu --type psutils func@cpu_task
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
$ watchme add-task system task-cpu --type psutils func@cpu_task skip@cpu_freq,cpu_percent
```

For more information on the psutil functions for cpu, see [here](https://psutil.readthedocs.io/en/latest/#cpu).


### 3. The Memory Task

This task will report stats on virtual memory. You add it by selection of the
parameter `func@memory_task`

```bash
$ watchme add-task system task-memory --type psutils func@memory_task
[task-memory]
func  = memory_task
active  = true
type  = psutils
```

You don't need to use "skip" for this task because there is only one entry
returned in the dictionary ("virtual_memory") so if you don't want this information,
just don't run the task.

For more information on the psutil functions for memory, see [here](https://psutil.readthedocs.io/en/latest/#memory).


### 4. The Networking Task

This task will report a bunch of network statistics. This is one that you might want to be
careful with, since it exports a lot of your host networking information that might be sensitive
if freely available. I would [read about](https://psutil.readthedocs.io/en/latest/#network) 
the different parameters here first. stats on virtual memory. You add it by selection of the
parameter `func@net_task`. In the example below, I'm going to skip 'net_if_address' and "net_connections"

```bash
$ watchme add-task system task-network --type psutils func@net_task skip@net_connections,net_if_address
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


### 5. The Python Task

This task will report information about install location, modules, and version
of the Python running the task. To set up this task:

```bash
$ watchme add-task system task-python --type psutils func@python_task
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


### 6. The Sensors Task

This is one of the coolest! You can actually use psutil to get information on your
system fans, temperature, and even battery. Set up the task like this:

```bash
$ watchme add-task system task-sensors --type psutils func@sensors_task
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


### 7. The System Task

The system task will provide (basic) system information. This is another task
that if you see something missing (that you think should be there) you should
[open an issue]({{ site.repo }}/issues). Here is how to add the task:

```bash
$ watchme add-task system task-system --type psutils func@system_task
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


### 8. The Users Task

The last is the user task, which will export active users on the system. It's 
likely that this task result won't change over time.

```bash
$ watchme add-task system task-users --type psutils func@users_task
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
