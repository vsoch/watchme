---
title: Installation
category: Installation
permalink: /install/index.html
order: 1
---


## Dependencies

The only dependency for watchme is to have [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) 
and [crontab](https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-on-a-vps) on your system. Git is used for version control of the pages you are watching, and crontab is
used for scheduling your watches.

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
