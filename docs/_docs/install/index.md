---
title: Installation
category: Installation
permalink: /install/index.html
order: 1
---


## Dependencies

The only dependency for watchme is to have [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) 
and [crontab](https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-on-a-vps) on your system. Git is used for version control of the pages you are watching, and crontab is
used for scheduling your watches. If you want to install a custom exporter or
watcher, see [installing extras](#installing-extras) below.

## Install

WatchMe can be installed natively (python 3 recommended) with pip:

```bash
pip install watchme
```

or you can clone and install from source:

```bash
$ git clone https://www.github.com/vsoch/watchme
$ cd watchme
$ python setup.py install
```

When you have installed WatchMe, there will be an executable "watchme"
placed in your bin folder:

```bash
which watchme
/home/vanessa/anaconda3/bin/watchme
```

and you should be able to run the executable and see the usage:

```bash
$ watchme

[WatchMe]  Command Line Tool v0.0.1
usage: watchme [-h] [--debug] [--version] [--quiet] {init,create} ...

WatchMe Command Line Tool

optional arguments:
  -h, --help     show this help message and exit
  --debug        use verbose logging to debug.
  --version      show version and exit.
  --quiet        suppress additional output.

actions:
  actions for HelpMe Command Line Tool

  {init,create}  watchme actions
    init         initialize watchme
    create       create a new watcher
```


If you have any questions or issues, please [open an issue]({{ site.repo }}/issues).

## Installing Extras

If you want to install all of watchme's exporters and watchers:

```bash
$ pip install watchme[all]
```

To install all watchers only:

```bash
$ pip install watchme[watchers]
```

To install all exporters only:

```bash
$ pip install watchme[exporters]
```

To install a specific exporter:

```bash
$ pip install watchme[exporter-pushgateway]
```

or a specific watcher task group:

```bash
$ pip install watchme[watcher-urls-dynamic]
$ pip install watchme[watcher-psutils]
```

To see all of the choices, see [here](https://github.com/vsoch/watchme/blob/master/setup.py#L109) in the setup file.
