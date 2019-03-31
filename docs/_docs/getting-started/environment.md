---
title: Environment
category: Getting Started
permalink: /getting-started/environment/
order: 3
---

WatchMe has a set of environment variables that can alter default base organization
and setup, along with variables that can be set across watcher tasks to change how the outputs
are saved there.

## Organization

WatchMe will default to saving your configuration in a subfolder of your home,
$HOME/.watchme, and with the configurations for your watchers 
(the groups of pages to watch, and the frequencies). For example, if you have
a watcher called jobs, one called watcher (this is the default) and one called 
pizzas, your .watchme folder would looklike this:

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

### Watcher Folder

Thus, if you want to change the default
folder base ($HOME/.watchme) you can do the following:

```bash
export WATCHME_BASE_DIR=$HOME/.creepywatcher
```

If you decide to make this change, it's important to write this into your .bashrc
or equivalent, otherwise the default will be used. 

### Default Watcher

If you want to set a default watcher (different than "watcher") to 
interact with, you can do that too:

```bash
export WATCHME_WATCHER=pizzas
```

And remember that you don't have to do this - you can specify the watcher
name on the command line to setup and create commands.


## Variables

By default, when you run a task for a watcher, it will save the result
in the watcher folder, in a folder named for the task. For example, if we run
the task "task-harvard-hpc" for a watcher called "watcher," the result
will (without any special change) save like this:

```bash
.watchme/
    watcher/
       watchme.cfg
       task-harvard-hpc/
          result.txt        
```

Of course this isn't ideal for all use cases! If you want a custom file name for the
task, just use the variable `file_name` when you create the watcher. Let's say we want to
use the default urls watcher to post to some endpoint, and save the result as
json with a custom file name:

```bash
$ watchme add watcher task-api-post url@https://singularityhub.github.io/registry/vanessa/fortune/manifests/latest/ file_name@manifest-latest.json save_as@json func@post_task
```

"save_as" is custom for the urls watcher (so json is returned) but for any watcher
that is saving some file, you can customize the `file_name` variable:

| Name | Required | Default | Example | Notes|
|------|----------|---------|---------|-----------|
| file_name | No | unset |file_name@image.png| the filename to save, only for download_task |


> Where should I go next?

Read about [Concepts]({{ site.baseurl }}/getting-started/concepts/) or go back to the
[Quick Start]({{ site.baseurl }}/getting-started/)
