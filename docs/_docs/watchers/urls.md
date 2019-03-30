---
title: URLS
category: Watchers
permalink: /watchers/urls
order: 2
---


The URL watcher will watch for changes in web content. To set up a task of this
type, you need to minimally provide a url to watch for changes. Given that we
have created a watcher called "watcher":

```bash
$ watchme create watcher
```

## Add a Task

You would then want to add a task to it. The general format to add a task looks
like this:

```bash
$ watchme add <watcher> task-<name> key1@value1 key2@value2
```

The key and value pairs are going to vary based on the watcher, however
since a URL task is going to watch for changes at a url (at a frequency 
determined by the watcher schedule), it follows that adding the task minimally 
requires a url parameter:

```bash
$ watchme add watcher task-reddit-hpc url@https://www.reddit.com/r/hpc
[task-reddit-hpc]
url  = https://www.reddit.com/r/hpc
active  = true
type  = urls
```

In the above, we added the task "task-reddit-hpc" to the watcher called "watcher"
and we defined the parameter "url" to be `https://www.reddit.com/r/hpc`.
As a confirmation that the task was added, the configuration is printed to the screen.

### Verify the Addition

We can also confirm this section has been written to file:

```bash
$ cat /home/vanessa/.watchme/watcher/watchme.cfg 
[watcher]
active = false

[task-reddit-hpc]
url = https://www.reddit.com/r/hpc
active = true
type = urls
```

You don't actually need to use watchme to write these files - you can write
the sections in a text editor if you are comfortable with the format.
The sections are always validated when the watcher is run.

### Force Addition

If for some reason you want to overwrite a task, you need to use force. Here is
what it looks like when you don't, and the task already exists:

```bash
$ watchme add watcher task-reddit-hpc url@https://www.reddit.com/r/hpc
ERROR task-reddit-hpc exists, use --force to overwrite.
```

### Active Status

If you want to change the default active status, use `--active false`. By default,
tasks added to watchers are active. Here is what the same command above would have 
looked like setting active to false:

```bash
$ watchme add watcher task-reddit-hpc url@https://www.reddit.com/r/hpc --active false
[task-reddit-hpc]
url  = https://www.reddit.com/r/hpc
active  = false
type  = urls
```

### Task Parameters

A urls task has the following custom parameters. Note that "active" and "type" are
added to all tasks, and indicate if the task is active, and the type to use to
drive its running. 

| Name | Required | Default | Example |Validation|
|------|----------|---------|---------|-----------|
| url  | True     |undefined|url@https://www.reddit.com/r/hpc| starts with http |


We will be adding more variables to customize the url watcher as watchme
is developed.
