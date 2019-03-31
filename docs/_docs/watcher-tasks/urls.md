---
title: URLS
category: Watcher Tasks
permalink: /watchers/urls/
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
requires a url parameter. 


### 1. Watch a URL Task

This task will watch for changes at an entire URL, meaning tracking the entire page.
For example, here is a page I wanted to watch for changes:

```bash
$ watchme add watcher task-harvard-hpc url@https://www.rc.fas.harvard.edu/about/people/
[task-harvard-hpc]
url  = https://www.rc.fas.harvard.edu/about/people/
active  = true
type  = urls
```

In the above, we added the task "task-harvard-hpc" to the watcher called "watcher"
and we defined the parameter "url" to be `https://www.rc.fas.harvard.edu/about/people/`.
As a confirmation that the task was added, the configuration is printed to the screen.

### 2. Download Content

You might also want to download some content or object, and save it to file
to track changes over time. You can do this by using the urls type watcher and
specifying the variable func to be "download_task":

```bash
$ watchme add watcher task-harvard-hpc url@https://www.rc.fas.harvard.edu/about/people/ func@download_task
```

### Verify the Addition

We can also confirm this section has been written to file:

```bash
$ cat /home/vanessa/.watchme/watcher/watchme.cfg 
[watcher]
active = false

[task-harvard-hpc]
url  = https://www.rc.fas.harvard.edu/about/people/
active  = true
type  = urls
```

You don't actually need to use watchme to write these files - you can write
the sections in a text editor if you are comfortable with the format.
The sections are always validated when the watcher is run.

### Task Parameters

A urls task has the following custom parameters. Note that "active" and "type" are
added to all tasks, and indicate if the task is active, and the type to use to
drive its running. 

| Name | Required | Default | Example | Notes|
|------|----------|---------|---------|-----------|
| url  | Yes     |undefined|url@https://www.reddit.com/r/hpc| validated starts with http |
| func | No    |get_task |func@download_task| must be defined in tasks.py |
| no_verify_ssl | No | unset |no_verify_ssl@true| |
| write_format | No | unset |write_format@wb| only for download_task |

We will be adding more variables to customize the url watcher as watchme
is developed.

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
