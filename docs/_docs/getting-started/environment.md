---
title: Environment
category: Getting Started
permalink: /getting-started/environment/
order: 3
---


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


#### Watcher Folder

Thus, if you want to change the default
folder base ($HOME/.watchme) you can do the following:

```bash
export WATCHME_BASE_DIR=$HOME/.creepywatcher
```

If you decide to make this change, it's important to write this into your .bashrc
or equivalent, otherwise the default will be used. 

#### Default Watcher

If you want to set a default watcher (different than "watcher") to 
interact with, you can do that too:

```bash
export WATCHME_WATCHER=pizzas
```

And remember that you don't have to do this - you can specify the watcher
name on the command line to setup and create commands.


> Where should I go next?

Read about [Concepts]({{ site.baseurl }}/getting-started/concepts/) or go back to the
[Quick Start]({{ site.baseurl }}/getting-started/)

