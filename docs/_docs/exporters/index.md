---
title: WatchMe Exporters
category: Exporters
permalink: /exporters/index.html
order: 1
---

Once you've followed the [getting started]({{ site.baseurl }}/getting-started/)
guide to [install]({{ site.baseurl }}/install/) watchme and have created your first 
set of watchers, you might want to do more! Specifically, you can add 
extra exporters to push your data to custom locations. The following exporters
are available:

 - [pushgateway]({{ site.baseurl }}/exporters/pushgateway/) to push data to a Prometheus gateway.

And instructions for using a general exporter, either in sync with running a task
or separately, are provided below.


## List Exporters

To see exporters available, you can list them:

```bash
$ watchme list --exporters
watchme: exporters
pushgateway
```

An exporter is like a task in that it can be activated
(or not), and you can define more than one for any particular watcher.

## Add an Exporter

The most basic thing to do is to add an exporter to a watcher. You should
read the documentation for your exporter of interest (linked above) to
know the required parameters for the exporter (it varies). 
Adding an exporter is similar to adding a task! The command asks you to
name the exporter, and the watcher to which you are adding it:

```bash
$ watchme add-exporter <watcher> <exporter>
```

Most likely the exporter requires parameters, so you add these in the same way
you added parameters to a task. Notice that "type" is essential to designate the
type that you want (the list at the top of the page):

```bash
$ watchme add-exporter <watcher> exporter-<name> param@value type@<exporter_type>
```

If you already have tasks defined that you want the exporter added to, just add them to the command:

```bash
$ watchme add-exporter <watcher> exporter-<name> param@value type@<exporter_type> <tasks>
```

If you've already added the exporter to the watcher and want to add it to a task:

```bash
$ watchme add-exporter <watcher> <exporter> <task>
```

Watchme will know that you aren't adding a new exporter (but instead using
an existing one) because you haven't provided a `type@<exporter_type>`
variable. If you want to re-create an exporter that already exists, you
can issue the same command but you'll need `--force`.

```bash
$ watchme add-exporter <watcher> exporter-<name> param@value type@<exporter_type> --force
``` 

## Remove an Exporter

If you change your mind, you can remove an exporter from a watcher entirely:

```bash
$ watchme remove <watcher> <exporter>
```

You can also remove it from a specific task (but not from the watcher entirely)

```bash
$ watchme remove <watcher> <exporter> <task>
```


## Run the Exporter

By default, an exporter will run with a task. This means that you should
run the task to run the exporter. If the watcher is active, and the task
is active, and the exporter is defined for the task, it will run.

```bash
$ watchme activate <watcher>
$ watchme run <watcher> <task>
```

If an exporter doesn't run successfully, it will be disabled for the task.
This is in case you forget about it.
