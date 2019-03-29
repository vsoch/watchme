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


## Licenses

This code is licensed under the Affero GPL, version 3.0 or later [LICENSE](LICENSE).
The SIF Header format is licesed by [Sylabs](https://github.com/sylabs/sif/blob/master/pkg/sif/sif.go).
