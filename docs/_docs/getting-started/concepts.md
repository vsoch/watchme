---
title: Concepts
category: Getting Started
permalink: /getting-started/concepts/
order: 2
---


What does WatchMe actually do? It comes down to helping you to create configurations
to check web pages or other system content for changes. The checks are done with
cron jobs, and the changes tracked with version control.

### Watcher

A watcher comes down to a GitHub repository (stored in the WatchMe home directory,
discussed under [Environment](#environment) that tracks changes for one or more
items of interest. You can create as many watchers as you like, and you can choose
to push to a service like GitHub (or not). The watcher has a particular configuration
file, one called `watcher.cfg`, that will tell the software how to run the watcher.
What does this mean? It means you can push your watcher configuration and items
to GitHub, and someone else can install the software and reproduce your watching.
Cool!

### Watcher Types

So far, we've talked about looking for changes in "pages," or websites. 
This is the default watcher type, however there are other kinds of 
tasks that a watcher might run. When you create a new watcher, you can
specify the type with the `--type` argument.

### Decorators

A watchme decorator is a monitor that can be used to run some task over
one of your python functions. For example, the `psutils` watcher type
has a decorator to record resource information about a running process (your
function) while it's running.

> Where should I go next?

Read about the [Environment]({{ site.baseurl }}/getting-started/environment/) or go back to the
[Quick Start]({{ site.baseurl }}/getting-started/)
