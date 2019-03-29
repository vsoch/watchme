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
This is the default watcher type, however we have plans to add other kinds of 
watchers as we think of them. When there are other watchers that you can choose 
from, you will be able to specify the kind when you create a new watcher.

> Where should I go next?

Read about the [Environment]({{ site.baseurl }}/getting-started/environment/) or go back to the
[Quick Start]({{ site.baseurl }}/getting-started/)
