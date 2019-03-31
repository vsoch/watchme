---
title: Introduction
category: Getting Started
permalink: /getting-started/index.html
order: 1
---


You should first [install]({{ site.baseurl }}/install/) watchme.
This will place the executable `watchme` in your bin folder, which is the client
for setting up and running a watcher. You can jump into setting up your first
watcher below:

 - [Background](#what-is-a-watcher): What is a watcher, exactly?
 - [Setup](#setup-watchme): Watchme on your computer, meaning setting a base with a default watcher
 - [Create a Watcher](#how-do-i-create-a-watcher): Create your first watcher to monitor one or more things
 - [Add tasks](#how-do-i-add-tasks): to your watcher, such as monitoring a url or a data endpoint.
 - [Task Parameters](#what-are-the-parameters-for-each-task) to customize your tasks.
 - [Inspect](#how-do-i-inspect-my-watcher) your watcher configuration easily.
 - [List](#how-do-i-list-watchers) your watchers
 - [Protect](#how-do-i-protect-or-freeze-my-watcher) or freeze your watcher against accidental deletion.
 - [Schedule](#how-do-i-schedule-my-watcher) your watcher to run at some frequency using cron.
 - [Remove](#how-do-i-remove-a-task-from-a-watcher) a task from a watcher, if it's not frozen
 - [Delete](#how-do-i-delete-a-watcher): a watcher repository

or read about the following:

 - [Concepts]({{ site.baseurl }}/getting-started/concepts/) including watchers and their types
 - [Environment]({{ site.baseurl }}/getting-started/environment/) change defaults and settings via environmnet variables.
 - [Interactive Python]({{ site.baseurl }}/getting-started/python/) specifically, interaction from within Python.

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

### How do I create a watcher?

If you didn't create a watcher above, or want to create

```bash
$ watchme init
Creating /home/vanessa/.watchme...
Adding watcher /home/vanessa/.watchme/watcher...
Generating watcher config /home/vanessa/.watchme/watcher/watchme.cfg
```

You can then see an empty watcher directory is created with a configuration
file:

```bash
$ tree /home/vanessa/.watchme/
/home/vanessa/.watchme/
└── watcher
    └── watchme.cfg
```

and what you can't see is that there is a Git repo (a .git folder) in the 
watcher directory too. Good job! The watcher is set up, and ready to add
tasks to it.

### How do I add tasks?

After creation, the watcher is empty. You need to add tasks for it to run. 
The configuration commands will vary based on the kind of task you want to add, 
and here is a quick example of adding a task to watch a url (the default task):

```bash
$ watchme add watcher task-reddit-hpc url@https://www.reddit.com/r/hpc
[task-reddit-hpc]
url  = https://www.reddit.com/r/hpc
active  = true
type  = urls
```

In the example above, we added a task called "task-reddit-hpc" to the default
watcher "watcher." The only required variable is the url, and we provided it
in the format `<key>@<value>`. This is how you will add any parameter to a task,
and the parameters allowed will vary based on the task type. In the above, we didn't
define a `--type` variable. By default, the setting is `--type url`. After
you add a task, you can quickly verify it was added by looking at the configuration file
directly:


```bash
$ cat /home/vanessa/.watchme/watcher/watchme.cfg

[watcher]
active = false

[task-reddit-hpc]
url = https://www.reddit.com/r/hpc
active = true
type = urls
```

While you don't need to manually edit this file, there isn't any reason that you can't if you wanted to. 
To read more about the settings here, see the [watcher configuration]({{ site.baseurl }}/getting-started/watcher-config/) documentation.

The task is active by default (after you set up its schedule) and you can disable
this with --active false:

```bash
$ watchme add watcher task-reddit-hpc url@https://www.reddit.com/r/hpc --active false
```

The reason we save these parameters in the repo is that if you put it under version
control on GitHub (or similar), others will be able to reproduce your protocol.

### What are the parameters for each task?

The parameters will vary based on the task type. When you are ready,
take a look at the [watchers]({{ site.baseurl }}/watchers/) page to choose a
task type that you want to configure.


### How do I inspect my watcher?

If you don't want to directly inspect the watcher configuration file, there
are some easy functions you can run to show them on the screen. First, to
inspect an entire watcher:

```bash
$ watchme inspect watcher
[watcher]
active  = false

[task-reddit-hpc]
url  = https://www.reddit.com/r/hpc
active  = true
type  = urls
```

You can also inspect a particular task alone:

```bash
$ watchme inspect watcher task-reddit-hpc
[task-reddit-hpc]
url  = https://www.reddit.com/r/hpc
active  = true
type  = urls
```

If the task doesn't exist, it will tell you:

```bash
task-doesnt-exist
ERROR task-doesnt-exist is not a valid section.
```

### How do I list my watchers?

You can quickly see the watchers installed to your watcher home with:

```bash
$ watchme list
watcher
purpleair
```

And logically, you can then inspect further with [inspect](#how-do-i-inspect-my-watchers)

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


## Licenses

This code is licensed under the Affero GPL, version 3.0 or later [LICENSE](LICENSE).
The SIF Header format is licesed by [Sylabs](https://github.com/sylabs/sif/blob/master/pkg/sif/sif.go).
