---
title: Watcher Configuration
category: Getting Started
permalink: /getting-started/watcher-config/
order: 4
---

## The Watcher

When you create a watcher, you'll notice it's configuration file, `watchme.cfg`
in the watcher folder:

```bash
$ tree /home/vanessa/.watchme/
/home/vanessa/.watchme/
└── watcher
    └── watchme.cfg
```

and what you can't see is that there is a Git repo (a .git folder) in the 
watcher directory too. 

### Active

By default, the watcher simply has a status, active or not.

```
[watcher]
active = false
```

When you first create a watcher, it will not be active. When you activate a watcher,
this coincides with generating a cron job to run the command for it, and the cron
job will run a watchme command to read this configuration file. This means that you
can change the active status at any time that you need (manually or via `watchme activate <name>` and the cron job will run and essentially do nothing.


### Protected

You can optionally protect a watcher, meaning that you can't delete it. Protected
means that you can't delete the watcher, but you can edit the tasks.

```
[watcher]
active = true
protected = "on"
```

If the parameter is missing or defined with value "off", both coincide with 
not protected.

### Frozen

If you want to freeze the configuration entirely, you should freeze it. This
means that you cannot delete the watcher folder, or edit anything in the
configuration file (other than the frozen status).

```
[watcher]
active = true
frozen = "on"
```

If the parameter is missing or defined with value "off", both coincide with 
not frozen.

### Tasks

Each action done by a watcher is called a task. A task is identified by
starting with "task" in the configuration:

```
[task-reddit]
url = https://www.reddit.com/r/hpc
active = false
```

Akin to the watcher itself, each task can also be active or not. The
variables within the task will vary based on the kind of watcher. For example,
the above is from the urls watcher type, since it will watch web pages for changes.

## Licenses

This code is licensed under the Mozilla, version 2.0 or later [LICENSE](LICENSE).
