---
title: Introduction
category: Getting Started
permalink: /getting-started/index.html
order: 1
---


You should first [install]({{ site.baseurl }}/install/) watchme.
This will place the executable `watchme` in your bin folder, which is the client
for setting up and running a watcher. You can jump into setting up your first
watcher below. If you are interested in using the watchme decorator to monitor
resource usage of a function, see the [psutils](http://localhost:4000/watchme/watchers/psutils/#1-the-monitor-pid-task)
page.

## Setup

 - [Background](#what-is-a-watcher): What is a watcher, exactly?
 - [Setup](#setup-watchme): Watchme on your computer, meaning setting a base with a default watcher
 - [Create a Watcher](#how-do-i-create-a-watcher): Create your first watcher to monitor one or more things
 - [Rename a Watcher](#how-do-i-rename-a-watcher): Rename a watching by changing the folder name

## Monitoring

 - [Monitor](#monitor-tasks-command-line) from the command line, on the fly.

## Tasks

 - [Add tasks](#how-do-i-add-tasks): to your watcher, such as monitoring a url or a data endpoint.
 - [Edit tasks](#how-do-i-edit-tasks): meaning an update, addition, or removal of parameters
 - [Task Parameters](#what-are-the-parameters-for-each-task) to customize your tasks.
 - [Inspect](#how-do-i-inspect-my-watcher) your watcher configuration easily.
 - [List](#how-do-i-list-watchers) your watchers
 - [Protect](#how-do-i-protect-or-freeze-my-watcher) or freeze your watcher against accidental deletion.
 - [Activate](#how-do-i-activate-my-watcher) or deactivate your watcher and/or associated tasks
 - [Run](#how-do-i-run-a-watcher): your watcher manually if you want to test or otherwise.
 - [Schedule](#how-do-i-schedule-my-watcher) your watcher to run at some frequency using cron.
 - [Remove](#how-do-i-remove-a-task-from-a-watcher) a task from a watcher, if it's not frozen
 - [Delete](#how-do-i-delete-a-watcher): a watcher repository

## Data and Sharing

 - [Export](#how-do-i-export-data): data for a particular result file and task.
 - [Get](#how-do-i-get-a-watcher) a watcher from GitHub, meaning cloning a repo to use.

or read about the following:

 - [Contribute a Task]({{ site.baseurl }}/contributing/watcher/) ranging from interacting with web APIs to local processes or networking.
 - [Concepts]({{ site.baseurl }}/getting-started/concepts/) including watchers and their types
 - [Variables and Environment]({{ site.baseurl }}/getting-started/environment/) change defaults and settings via environmnet variables, or set variables that work across watcher tasks.
 - [Interactive Python]({{ site.baseurl }}/getting-started/python/) specifically, interaction from within Python.

<a id="what-is-a-watcher">
### What is a Watcher?

A watcher is a configuration to check a resource like a website at some frequency.
We do this with a combination of cron jobs (scheduling) and git repositories (version
control). Your watchers will live by default in subfolders of `$HOME/.watchme`, and
it's easiest to keep this default. If you want to change the default, you
can do this with [environment]({{ site.baseurl }}/getting-started/environment/) variables.

For example, here is what a set of three watchers might look like in your watchme home.

```bash
.watchme
     jobs/
     pizzas/
     watcher/
```

What goes in each folder? It's actually a git repository, and this helps
to track changes for pages. We do this instead of saving duplicates of
the pages, and if you are doing research, you have a GitHub repository
that updates with each. 

<a id="setup-watchme">
### Setup WatchMe

The first thing you need to do is an initial setup of WatchMe, which will generate
your WatchMe home folder and a global configuration.

```bash
$ watchme init --help

usage: watchme init [-h] [--empty] [--watcher WATCHER] [--base BASE]

optional arguments:
  -h, --help         show this help message and exit
  --empty            don't create the default watcher folder
  --watcher WATCHER  the watcher to create (defaults to watcher)
  --base BASE        the watcher base (defaults to $HOME/.watchme)
```

Notice that you can change the default base, turn off generation of the default
watcher (named watcher) with `--empty` or provide a custom name (instead of watcher).
Let's use all the defaults and just run the init:

```bash
$ watchme init
Creating /home/vanessa/.watchme...
Adding watcher /home/vanessa/.watchme/watcher...
Generating watcher config /home/vanessa/.watchme/watcher/watchme.cfg
```

Notice how it created a default watcher called "watcher?" To take that off, do:

```bash
$ watchme init --empty
Creating /home/vanessa/.watchme...
```

and just the base directory will be created. Note that you can change the root
of this with --base:

```bash
$ watchme --base /home/vanessa/Desktop/.watchme init --empty
/home/vanessa/Desktop/.watchme
Creating /home/vanessa/Desktop/.watchme...
```

Notice how the `--base` argument comes before init? That's because it's a global
argument, meaning you can supply it to any command group (init, create, etc.). If 
you don't want to set it and want to change the default, remember that you can
export `WATCHME_BASE_DIR` in your bash profile for a permanent setting.
For the reminder of this tutorial, we will assume that you ran init without
`--empty`, and interact with a watcher named "watcher."

<a id="how-do-i-create-a-watcher">
### How do I create a watcher?

If you didn't create a watcher above (meaning you ran the init command with `--empty`)
this is ok! You can create as many watchers as you like with the "create" command.

```bash
$ watchme create --help
usage: watchme create [-h] [watchers [watchers ...]]

positional arguments:
  watchers    watchers to create (default: single watcher)

optional arguments:
  -h, --help  show this help message and exit
```

As an example (after running watchme init) let's create a watcher called "weather"

```bash
$ watchme create weather
Adding watcher /home/vanessa/.watchme/weather...
Generating watcher config /home/vanessa/.watchme/weather/watchme.cfg
```

You can then see an empty watcher directory is created with a configuration
file:

```bash
$ tree /home/vanessa/.watchme/
/home/vanessa/.watchme/
└── weather
    └── watchme.cfg
```

and what you can't see is that there is a Git repo (a .git folder) in the 
watcher directory too. Good job! The watcher is set up, and ready to add
tasks to it. 

<a id="how-do-i-rename-a-watcher">
### How do I rename a watcher?

The watcher name coincides with the folder name. For example, if you created
the "weather" watcher and want to change the name at a later point, just rename
the folder. For the remainder of this getting started guide, we will be using
a watcher named "watcher," so if you didn't create this watcher, you can 
either create it or rename an existing folder.


<a id="monitor-tasks-command-line">
### Monitor Tasks on The Fly

If you dont' want to use WatchMe for tasks, you can use it to monitor on the fly!
This could be a simple wrapper to any command:

```bash
$ watchme monitor singularity pull docker://busybox
[{"status": "running", "username": "sochat1", "cmdline": ["singularity", "pull", "docker://busybox"], "cpu_num": 29, "num_fds": 6, "create_time": 1659736689.01, "open_files": 0, "ionice": {"value": 4, "ioclass": "IOPRIO_CLASS_NONE"}, "name": "singularity", "cpu_affinity": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47], "exe": "/usr/bin/singularity", "cpu_percent": 0.0, "num_threads": 11, "io_counters": {"read_count": 21, "write_count": 0, "read_bytes": 0, "write_bytes": 0, "read_chars": 8671, "write_chars": 0}, "memory_full_info": {"rss": 24010752, "vms": 1356939264, "shared": 11788288, "text": 26202112, "lib": 0, "data": 1300967424, "dirty": 0, "uss": 23040000, "pss": 23040000, "swap": 0}, "num_ctx_switches": {"voluntary": 84, "involuntary": 1}, "terminal": "/dev/pts/53", "uids": {"real": 13754, "effetive": 13754, "saved": 13754}, "ppid": 848657, "pid": 848682, "memory_percent": 0.011313591754217435, "cpu_times": [0.01, 0.01, 0.0, 0.0, 0.0], "gids": {"real": 5782, "effetive": 5782, "saved": 5782}, "nice": 0, "connections": [], "cwd": "/home/sochat1", "SECONDS": "3"}]
```
Or an entire analysis (e.g., running a container) and taking samples
every second:

```bash
$ watchme monitor --seconds 1 singularity run watchme-mnist_latest.sif plots.png > mnist-external.json
```

For the interested reader, there is an [entire write-up here](https://vsoch.github.io/2019/watchme-monitor/).


<a id="how-do-i-add-tasks">
### How do I add tasks?

After creation, the watcher is empty. You need to add tasks for it to run. 
The configuration commands will vary based on the kind of task you want to add, 
and here is a quick example of adding a task to watch a url (the default task):

```bash
$ watchme add-task watcher task-singularity-release url@https://github.com/sylabs/singularity/releases
[task-singularity-release]
url  = https://github.com/sylabs/singularity/releases
active  = true
type  = urls
save_as = text
```

In the example above, we added a task called "task-singularity-release" to the default
watcher "watcher." The only required variable is the url, and we provided it
in the format `<key>@<value>`. This is how you will add any parameter to a task,
and the parameters allowed will vary based on the task type. We also specified that the page
we are going to retrieve is `save_as` text, meaning that it's not json (default).
In the above, we didn't define a `--type` variable. By default, the setting is `--type url`. After
you add a task, you can quickly verify it was added by looking at the configuration file
directly:


```bash
$ cat /home/vanessa/.watchme/watcher/watchme.cfg

[watcher]
active = false

[task-singularity-release]
url = https://github.com/sylabs/singularity/releases
active = true
type = urls
save_as = text
```

While you don't need to manually edit this file, there isn't any reason that you can't if you wanted to. 
To read more about the settings here, see the [watcher configuration]({{ site.baseurl }}/getting-started/watcher-config/) documentation.

The task is active by default (after you set up its schedule) and you can disable
this with --active false:

```bash
$ watchme add-task watcher task-singularity-release url@https://github.com/sylabs/singularity/releases --active false
```

The reason we save these parameters in the repo is that if you put it under version
control on GitHub (or similar), others will be able to reproduce your protocol.

<a id="how-do-i-edit-tasks">
### How do I edit tasks?

After you've added a task, you can easily update parameters. The format is:

```bash
$ watchme edit <watcher> <action> <task> <key> <value> 
```

Where action can be one of "update" or "add" or "remove." For example, add a value:

```bash
$ watchme edit watcher add task-harvard-hpc file_name file.txt
Adding file_name:file.txt to task-harvard-hpc
```

If you try adding again, it won't let you because the value exists.


```bash
$ watchme edit watcher add task-harvard-hpc file_name file.txt
ERROR file_name already exists. Use "update" action to change.
```

Instead, use update:

```bash
$ watchme edit watcher update task-harvard-hpc file_name churro.txt
Updating file_name to churro.txt in task-harvard-hpc
```

and when you have had enough, remove a parameter entirely:

```bash
$ watchme edit watcher remove task-harvard-hpc file_name
Removing file_name
```

<a id="what-are-parameters-for-each-task">
### What are the parameters for each task?

The parameters will vary based on the task type. When you are ready,
take a look at the [watchers]({{ site.baseurl }}/watchers/) page to choose a
task type that you want to configure.

<a id="how-do-i-inspect-my-watcher">
### How do I inspect my watcher?

If you don't want to directly inspect the watcher configuration file, there
are some easy functions you can run to show them on the screen. First, to
inspect an entire watcher:

```bash
$ watchme inspect watcher
[watcher]
active  = false

[task-singularity-release]
url = https://github.com/sylabs/singularity/releases
active = true
type = urls
```

You can also inspect a particular task alone:

```bash
$ watchme inspect watcher task-singularity-release
[task-singularity-release]
url = https://github.com/sylabs/singularity/releases
active = true
type = urls
```

If the task doesn't exist, it will tell you:

```bash
task-doesnt-exist
ERROR task-doesnt-exist is not a valid section.
```
<a id="how-do-i-list-my-watchers">
### How do I list my watchers?

You can quickly see the watchers installed to your watcher home with:

```bash
$ watchme list
watcher
purpleair
```

You can also list task folders and other files for a particular watcher:

```bash
$ watchme list github
watcher: /tmp/tmp.QG2Tuusrrb/github
data
  task-vsoch-scif
  task-singularity
  task-spack
  README.md
  .git
  task-sregistry
  task-spython
  task-sregistry-cli
  task-expfactory
  watchme.cfg
```

or finally, if you add a specific task folder, you can list the contents there.

```bash
$ watchme list github task-spython
task: /tmp/tmp.QG2Tuusrrb/github/task-spython
TIMESTAMP
  result.json
```

If you are interested in the configurations in watchme.cfg, then you can 
inspect further with [inspect](#how-do-i-inspect-my-watchers).

<a id="how-do-i-freeze-or-protect-my-watcher">
### How do I protect or freeze my watcher?

If you want to prevent deletion of your folder, you can protect it.

```bash
$ watchme protect watcher on
[watcher]
active  = false
protected  = on
```

protection means that you cannot delete the watcher, but you can edit the tasks. To
remove protection:

```bash
$ watchme protect watcher off
[watcher]
active  = false
protected  = off
```

Freezing is one step above protected - it means that you cannot delete *or* edit
the tasks for your watcher. You can also turn it on or off:

```bash
$ watchme protect watcher freeze
[watcher]
active  = false
frozen  = on

$ watchme protect watcher unfreeze
[watcher]
active  = false
```

Frozen takes preference to protected, if the settings don't agree.

<a id="how-do-i-activate-my-watcher">
### How do I activate my watcher?

By default, when you add a watcher, it isn't active. You can see this
by looking at the watcher configuration file in the `[watcher]` section:

```bash
$ watchme inspect watcher
[watcher]
active  = false
```

To activate or deactivate the entire watcher, run these commands:

```bash
$ watchme activate watcher
[watcher|watcher] active: true
$ watchme deactivate watcher
[watcher|watcher] active: false
```

If you want to activate or deactivate single tasks, just add the task name:

```bash
$ watchme deactivate watcher task-singularity-release
```

By default, when a task is added, it is active.

<a id="how-do-i-run-a-watcher">
### How do I run a watcher?

Typically, you would schedule your watcher with a cron job, and then forget about it.
However, you are also able to run the watcher manually, if you so desire (to test 
or otherwise.) To run manually:

```bash
# watchme run <watcher>
$ watchme run watcher
```

or to run as a test (not saving data):

```bash
$ watchme run watcher --test
```

where "watcher" corresponds with the watcher name. When this is done, if the watcher
has status "active" as true, all the associated tasks that are also active will be
run, and the repository updated with results. If you want to show variables
and names of the tasks instead of the default progress bar, do:


```bash
$ watchme run watcher --no-progress
```

You can also choose to run in serial, also with or without a progress bar:


```bash
$ watchme run watcher --no-progress --serial
```

After you run your watcher tasks, you will see a directory created named
based on the task, along with a result file (if successful) and a `TIMESTAMP`
file to indicate when the task was last run.

```bash
$ tree
.
├── task-harvard-hpc
│   ├── result.txt
│   └── TIMESTAMP
└── watchme.cfg
```

You can also confirm that the watcher has run and commit results to the repo.
Here we are in the watcher base folder, at `$HOME/.watchme/watcher`. We just
ran the watcher, and there were two tasks:

```bash
git log
commit c8929ea7caf71a4172195b618ff602f9b47686e1
Author: Vanessa Sochat <vsochat@stanford.edu>
Date:   Mon Apr 1 13:07:47 2019 -0400

    watchme watcher ADD results task-harvard-hpc

commit 95517ff8d4d39e326be5e9638969f385fbe05355
Author: Vanessa Sochat <vsochat@stanford.edu>
Date:   Mon Apr 1 13:07:47 2019 -0400

    watchme watcher ADD results task-singularity-release
```

We can see results were added for both.

<a id="how-do-i-schedule-my-watcher">
### How do I schedule my watcher?

Now that you've configured your watcher, you simply need to schedule it to run.
WatchMe uses [cron](https://en.wikipedia.org/wiki/Cron) to run scheduled jobs, but will handle the configuration for you. For example, here is how to schedule your watcher to
run at different standard time intervals:

```bash
#                  <name> <frequency>
$ watchme schedule watcher @hourly
$ watchme schedule watcher @daily
$ watchme schedule watcher @weekly
$ watchme schedule watcher @monthly
$ watchme schedule watcher @yearly
```

Notice how the times are prefixed with `@` to distinguish between watchers and
times? If you want to set a [custom cron string](https://crontab.guru/) you can do that too:

```bash
$ watchme schedule watcher 0 * * * * *
```

Here is how to schedule your watcher to run:

```bash
$ watchme schedule air-quality @hourly
```

And then check that an entry has been added to crontab:

```bash
$ crontab -l
@hourly watchme run air-quality # watchme-air-quality
```

You can check to see if cron is running (and the job ran):

```bash
# ubuntu
$ service cron status

# linux
$ service crond status
```

<a id="how-do-i-remove-a-task-from-my-watcher">
### How do I remove a task from a watcher?

To remove a task, just specify it:

```bash
$ watchme remove watcher task-reddit-hpc
task-reddit-hpc removed successfully.
```

If the task doesn't exist, it will tell you.

```bash
$ watchme remove watcher task-reddit-hpc
WARNING task-reddit-hpc does not exist.
```

If the watcher is frozen, it will not allow you to remove it.

```bash
$ watchme remove watcher task-reddit-hpc
ERROR watcher is frozen, unfreeze first.
```

<a id="how-do-i-delete-a-watcher">
### How do I delete a watcher?

To remove an entire watcher, specify `--delete`:

```bash
$ watchme remove watcher --delete
```

If the watcher is frozen, you need to unfreeze it first:

```bash
$ watchme remove  watcher --delete
ERROR watcher watcher is frozen, unfreeze to delete.

$ watchme protect watcher unfreeze
$ watchme remove  watcher --delete
Removing watcher watcher
```

The entire folder is now removed.

```bash
$ ls /home/vanessa/.watchme/
```

<a id="how-do-i-get-a-watcher">
### How do I get a watcher?

Not only can you share your watcher (configuration and data output) on a service
like GitHub thanks to version control, you can also easily grab someone else's
watcher repository!

```bash
$ watchme get https://www.github.com/vsoch/watchme-air-quality special-name
Added watcher watchme-air-quality
```

Conflrm that it was added:

```bash
$ watchme list
purpleair
watchme-air-quality
air-quality
watcher
```

You can also clone (and name it something else):

```bash
$ watchme get https://www.github.com/vsoch/watchme-air-quality special-name
Added watcher special-name
```
```bash
$ watchme list
purpleair
watchme-air-quality
special-name
air-quality
watcher
```

If you attempt to overwrite a folder that exists, you'll get a warning.

```bash
vanessa@vanessa-ThinkPad-T460s:~/Documents/Dropbox/Code/Python/watchme$ watchme get https://www.github.com/vsoch/watchme-air-quality special-name
ERROR /home/vanessa/.watchme/special-name exists. Use --force to overwrite
```

and need to use `--force` to remove first, and then clone the watcher to the same location.

```bash
$ watchme get https://www.github.com/vsoch/watchme-air-quality special-name --force
Added watcher special-name
```

You will still need to schedule the water to run (and update the .git folder cloned 
there) and activate it, in the case that it wasn't active in the repository.

<a id="how-do-i-export-data">
### How do I export data?

The core reason you would want to use WatchMe in the first place is to collect data
over time for some task. Let's say we have a result file, "oakland.txt" in
the task folder "task-air-oakland" for the "air-quality" watcher. We can
export that from the command line via:

```bash
# watchme export <watcher>   <task>           <filename>
$ watchme export air-quality task-air-oakland oakland.txt
git log --all --oneline --pretty=tformat:"%H" --grep "ADD results" cca3c4eb84d9c38527ec93a9a620bfab07d798f2..5d2b047dabe74e76e1585341bb956fd633bd0832 -- task-air-oakland/oakland.txt
{
    "commits": [
        "1ee8998dd036accada21c2968e1d270bed4ba058"
    ],
    "dates": [
        "2019-04-02 12:31:19 -0400"
    ],
    "content": [
        "30"
    ]
}
```

By default, it will print the result to the screen, unless you provide a `--out` to print it to file. 
Also notice that the git commands to get the list of commits are shown.
We only have one commit for the task file, but we can see that it has an associated date,
and the content of the file. For more than one commit, each of the entries in the output
dictionary would be a list.

<a id="exporting-json">
### Exporting Json

If your results files have json, you will get a funny looking unparsed json inside json.
If you know this about your task, add the `--json` flag so the entire thing is parsed
as a single (loadable) json file:

```bash
$ watchme export system task-cpu vanessa-thinkpad-t460s_vanessa.json  --json
```

## Licenses

This code is licensed under the Mozilla, version 2.0 or later [LICENSE](LICENSE).
