---
title: Introduction
category: Getting Started
permalink: /getting-started/index.html
order: 1
---


You should first [install]({{ site.baseurl }}/install/) watchme.
This will place the executable `watchme` in your bin folder, which is the client
for setting up and running a watcher. You can jump into setting up your first
watcher below, or read about the following:

 - [Concepts]({{ site.baseurl }}/getting-started/concepts/) including watchers and their types
 - [Environment]({{ site.baseurl }}/getting-started/environment/) change defaults and settings via environmnet variables.

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
watcher directory too. 

### How do I configure my watcher?

After creation, the watcher doesn't do much. It doesn't have a schedule to run,
or any things to watch. When you do this, your specifications will be saved in
the `watchme.cfg` you see in the folder above. When first created, this configuration file doesn't do much. But after you've set up your watcher, if you put the repository on GitHub, others could reproduce your protocol. 

> Do I need to manually edit this file?

While you don't need to manually edit this file, there isn't any reason that you can't if you wanted to. To read more about the settings here, see the [watcher configuration]({{ site.baseurl }}/getting-started/watcher-config/) documentation.


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

## Licenses

This code is licensed under the Affero GPL, version 3.0 or later [LICENSE](LICENSE).
The SIF Header format is licesed by [Sylabs](https://github.com/sylabs/sif/blob/master/pkg/sif/sif.go).
