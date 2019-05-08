---
title: results
category: Watcher Tasks
permalink: /watchers/results/
order: 3
---

The results watcher is optimized to use WatchMe as a database. The various
functions coincide with where data is expected to come from, and there
is flexibility to customize format and file naming. You don't need
any extra dependencies to use it, other than having watchme installled.

```bash
$ pip install watchme
```

Next, create a watcher for your tasks to live under:

```bash
$ watchme create results-watcher
```

Now let's walk through each of the tasks. If you aren't familiar with how
to add a task and otherwise manage them, see the [getting started]({{ site.baseurl }}/getting-started/)
docs. Here are the functions exposed by the results group:

 - [From Environment](#the-from-env-task)

## Add a Task

We are going to be added tasks to our watcher, "results-watcher" above.
The general format to add a task looks like this:

```bash
$ watchme add-task <watcher> <task-name> key1@value1 key2@value2
```

The key and value pairs are going to vary based on the watcher task.

### 1. The From Env Task

This task does exactly what it sounds like - it finds results from the environment.
You can specify it to watchme via `func@from_env_task`

```bash
$ watchme add-task results-watcher task-hpc-job --type results func@from_env_task
func  = from_env_task
active  = true
type  = results
```

The task itself is really simple - it's going to scrape the environment
for variables that begin with `WATCHMEENV_`. Let's say that I'm running a job
on my research cluster, the process could export some number of results, let's
say one is a density and the other is a weight.

```
export WATCHMEENV_density=0.45
export WATCHMEENV_weight=32
```

The export makes the variables available to any child processes of the job, but
they won't leak into other running processes. I might finish running the job, 
and then have watchme issue a command directly to save the result. Let's
activate the watcher to test it out:

```bash
$ watchme activate results-watcher
```

And here you can export any number of `WATCHMEENV_` variables in your environment, and then
run watchme like this to test:

```bash
$ watchme run results-watcher task-hpc-job
```

The task will find the environment variables, and then save the results to
the GitHub repository according to the environment variable name under
the task folder. In this case we would see:

```
$ tree task-hpc-job/
task-hpc-job/
├── density
├── TIMESTAMP
└── weight
```

How cool is that! You could use this so that each timepoint represents
a single database entry (and for example, export a `WATCHMEENV_ID` to
provide an identifier for the unit) or you could have each environment
variable coincide with the same measurment, perhaps changing over time. 
Take a look at the git log too - you'll see that every change and entry
is recorded for you, and ready to push to GitHub to share.

The cool thing about this task is that you likely wouldn't want to schedule it
to run, you would have it run after or during some job or process that you
want to record. Just for example, let's export another set of values,
and then show you how to export the entire data structure for each file:

```bash
export WATCHMEENV_density=0.55
export WATCHMEENV_weight=34
watchme run results-watcher task-hpc-job
```

To export data, the format is:

```bash
$ watchme export results-watcher task-hpc-job density
git log --all --oneline --pretty=tformat:"%H" --grep "ADD results" 384d7bdc6e54af6266377b30ff0d47a40c4fc28d..732dee443caa19f0e50ec1e9b89ca3a542459cc7 -- task-hpc-job/density
{
    "commits": [
        "732dee443caa19f0e50ec1e9b89ca3a542459cc7",
        "c0861ed8ebe473cc3efa1db5f84e10d05d61bbc8"
    ],
    "dates": [
        "2019-05-08 15:16:14 -0400",
        "2019-05-08 15:11:32 -0400"
    ],
    "content": [
        "0.55",
        "0.45"
    ]
}
```

There you go!
