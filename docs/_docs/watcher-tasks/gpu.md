---
title: gpu
category: Gpu Tasks
permalink: /watchers/gpu/
order: 4
---

The gpu watcher will help to monitor gpu devices (memory, power, versions, limits).
This watcher must obviously be run on a machine with one or more GPU devices.

Let's first create a watcher for your tasks to live under:

```bash
$ watchme create gpu
```

Now let's walk through the `gpu_task`, which is currently
the only one available for the gpu watcher. If you aren't familiar with how
to add a task and otherwise manage them, see the [getting started]({{ site.baseurl }}/getting-started/).

 - [GPU Task](#1-the-gpu-task)


## Add a Task

Remember that we are going to be added tasks to our watcher, "gpu" above.
The general format to add a task looks like this:

```bash
$ watchme add-task <watcher> <task-name> key1@value1 key2@value2
```

The key and value pairs are going to vary based on the watcher task.

### Task Parameters

The gpu task doesn't have any required arguments, but you can define
a comma separated list of entries to skip.

| Name | Required | Default | Example | Notes|
|------|----------|---------|---------|-----------|
| skip  | No     |undefined|skip@ | varies by task (see below) |

Also note that for all of the tasks below, you need to select the type of task with `--type gpu`.

### Task Environment

For any task, if you have a variable exporter to the environment that starts
with `WATCHMEENV_`, it will be found and added to the result. For example,
`WATCHMEENV_result_id=123` will be saved to the results dictionary with key
"result_id" set to "123."

### Return Values

All of the return values here will be dictionaries, meaning appropriate to export to json.
You shouldn't need to define a `file_name` parameter, as it will be set automatically to
be your host plus username. However, you are free to set this parameter to change this 
value.


### 1. The GPU Task

This task is useful for monitoring a specific process that uses a GPU. You can run it as a
task (discussed first) or a decorator to a function to enable continuous monitoring.
Either way, you will want to create your watcher first:

```bash
$ watchme create gpu
```

#### Run on the Fly, Python

It's most likely you want to run and monitor a command on the fly, either from
within Python or the command line. First, let's take a look at running from
within Python. We are going to use a `TerminalRunner` to run the command:

```python
from watchme.tasks.decorators import TerminalRunner
runner = TerminalRunner('sleep 5')
runner.run()
timepoints = runner.wait('gpu_task')
```

You'll get a list of timepoints, collected at intervals of 3 seconds! Here
is a look at the first timepoint:

```python
In [3]: timepoints[0]                                                                                                       
Out[3]: 
{'nvml_driver_version': '418.67',
 'nvml_system_nvml_version': '10.418.67',
 'nvml_deviceCount': 1,
 'nvml_unit_count': 0,
 'devices': {'Tesla V100-SXM2-32GB': {'nvml_device_board_id': 6656,
   'nvml_device_multi_gpu_board': 0,
   'nvml_device_brand': 2,
   'nvml_device_serial': '0323518083147',
   'nvml_device_set_cpu_affinite': None,
   'nvml_device_minor_number': 0,
   'nvml_device_uuid': 'GPU-be7b9ac8-f75e-1960-c52d-85429b4c86b1',
   'nvml_device_inforom_version': 'G503.0203.00.04',
   'nvml_device_inforam_checksum': 0,
   'nvml_device_display_mode': 1,
   'nvml_device_display_active': 0,
   'nvml_device_persistence_mode': 1,
   'nvml_device_supported_memory_clocks': [877],
   'nvml_device_performance_state': 0,
   'nvml_device_management_mode': 1,
   'nvml_device_power_managerment_mode': 1,
   'nvml_device_power_management_limit': 300000,
   'nvml_device_power_management_limit_constraints': [150000, 300000],
   'nvml_device_power_management_default_limit': 300000,
   'nvml_device_enforced_power_limit': 300000,
   'nvml_device_power_usage': 45297,
   'nvml_device_memory_info': {'free': 34058207232,
    'total': 34058272768,
    'used': 65536},
   'nvml_device_bar1_memory_info': {'bar1Free': 34357047296,
    'bar1Total': 34359738368,
    'bar1Used': 2691072},
   'nvml_device_compute_mode': 3,
   'nvml_device_ecc_mode': [1, 1],
   'nvml_device_current_ecc_mode': 1,
   'nvml_device_pending_ecc_mode': 1,
   'nvml_device_utilization_rates': {'gpu': 0, 'memory': 0},
   'nvml_device_encoder_utilization': [0, 167000],
   'nvml_device_decoder_utilization': [0, 167000],
   'nvml_device_pci_replay_counter': 0,
   'nvml_device_vbios_version': '88.00.43.00.03',
   'nvml_device_compute_running_processes': [],
   'nvml_device_grapics_running_processes': [],
   'nvml_device_supported_event_types': 31,
   'nvml_device_current_pcie_link_generation': 3,
   'nvml_device_max_pcie_link_generation': 3,
   'nvml_device_curr_pcie_link_width': 16,
   'nvml_device_max_pcie_link_width': 16,
   'nvml_device_supported_clocks_throttle_reasons': 511,
   'nvml_device_current_clocks_throttle_reasons': 1,
   'nvml_device_index': 0,
   'nvml_device_accounting_mode': 0,
   'nvml_device_accounting_pids': [],
   'nvml_device_accounting_buffer_size': 4000}},
 'SECONDS': '3'}
```

Do you need to add data to the structure? Just export it with prefix `WATCHMEENV_*`

```python
os.environ['WATCHMEENV_AVOCADO'] = '5'
```

and it will appear in the result.

#### Run on the Fly, Command Line

If you choose, the same function can be run via the watchme command line client.
If you provide no additional arguments, it will print the data structure to
the screen:

```bash
$ watchme monitor --func gpu_task sleep 2
[{"nvml_driver_version": "418.67", "nvml_system_nvml_version": "10.418.67", "nvml_deviceCount": 1, "nvml_unit_count": 0, "devices": {"Tesla V100-SXM2-32GB": {"nvml_device_board_id": 6656, "nvml_device_multi_gpu_board": 0, "nvml_device_brand": 2, "nvml_device_serial": "0323518083147", "nvml_device_set_cpu_affinite": null, "nvml_device_minor_number": 0, "nvml_device_uuid": "GPU-be7b9ac8-f75e-1960-c52d-85429b4c86b1", "nvml_device_inforom_version": "G503.0203.00.04", "nvml_device_inforam_checksum": 0, "nvml_device_display_mode": 1, "nvml_device_display_active": 0, "nvml_device_persistence_mode": 1, "nvml_device_supported_memory_clocks": [877], "nvml_device_performance_state": 0, "nvml_device_management_mode": 1, "nvml_device_power_managerment_mode": 1, "nvml_device_power_management_limit": 300000, "nvml_device_power_management_limit_constraints": [150000, 300000], "nvml_device_power_management_default_limit": 300000, "nvml_device_enforced_power_limit": 300000, "nvml_device_power_usage": 45327, "nvml_device_memory_info": {"free": 34058207232, "total": 34058272768, "used": 65536}, "nvml_device_bar1_memory_info": {"bar1Free": 34357047296, "bar1Total": 34359738368, "bar1Used": 2691072}, "nvml_device_compute_mode": 3, "nvml_device_ecc_mode": [1, 1], "nvml_device_current_ecc_mode": 1, "nvml_device_pending_ecc_mode": 1, "nvml_device_utilization_rates": {"gpu": 0, "memory": 0}, "nvml_device_encoder_utilization": [0, 167000], "nvml_device_decoder_utilization": [0, 167000], "nvml_device_pci_replay_counter": 0, "nvml_device_vbios_version": "88.00.43.00.03", "nvml_device_compute_running_processes": [], "nvml_device_grapics_running_processes": [], "nvml_device_supported_event_types": 31, "nvml_device_current_pcie_link_generation": 3, "nvml_device_max_pcie_link_generation": 3, "nvml_device_curr_pcie_link_width": 16, "nvml_device_max_pcie_link_width": 16, "nvml_device_supported_clocks_throttle_reasons": 511, "nvml_device_current_clocks_throttle_reasons": 1, "nvml_device_index": 0, "nvml_device_accounting_mode": 0, "nvml_device_accounting_pids": [], "nvml_device_accounting_buffer_size": 4000}}, "SECONDS": "3"}]
```

Want to add an environment variable? The same applies - you can export `WATCHMEENV_*` and they will be added to results.

```bash
$ export WATCHMEENV_AVOCADOS=3
$ watchme monitor --func gpu_task sleep 2
```

If you want to save to a watcher, then provide the watcher name as the first argument.
For example, here we run a task on the fly, and save the result to the watcher "decorator."
Since we don't provide a `--name` argument, the name defaults to a derivation of the command run.

```bash
$ watchme create decorators
$ watchme monitor --func gpu_task decorators sleep 5
```

List the folders in the watcher named "decorators" to see the newly added result:

```bash
$ watchme list decorators
$ watchme list decorators
watcher: /home/users/vsochat/.watchme/decorators
  decorator-gpu-sleep-5
  .git
  watchme.cfg
```

And then use export to export the data!

```bash
$ watchme export decorators decorator-gpu-sleep-5 result.json --json
git log --all --oneline --pretty=tformat:"%H" --grep "ADD results" fd52cbf5d3cd325acdd2709bfc202d32ab721327..b579418f862e69e58d9e3464bc7981580a04cb3a -- decorator-gpu-sleep-5/result.json
{
    "commits": [
        "b579418f862e69e58d9e3464bc7981580a04cb3a"
    ],
    "dates": [
        "2019-07-11 09:31:55 -0700"
    ],
    "content": [
        {
            "nvml_driver_version": "418.67",
            "nvml_system_nvml_version": "10.418.67",
            "nvml_deviceCount": 1,
            "nvml_unit_count": 0,
            "devices": {
                "Tesla V100-SXM2-32GB": {
                    "nvml_device_board_id": 6656,
                    "nvml_device_multi_gpu_board": 0,
                    "nvml_device_brand": 2,
                    "nvml_device_serial": "0323518083147",
                    "nvml_device_set_cpu_affinite": null,
                    "nvml_device_minor_number": 0,
                    "nvml_device_uuid": "GPU-be7b9ac8-f75e-1960-c52d-85429b4c86b1",
                    "nvml_device_inforom_version": "G503.0203.00.04",
                    "nvml_device_inforam_checksum": 0,
                    "nvml_device_display_mode": 1,
                    "nvml_device_display_active": 0,
                    "nvml_device_persistence_mode": 1,
                    "nvml_device_supported_memory_clocks": [
                        877
                    ],
...    
    ]
}

```

For both of the command line above, you can define `--name` to give
a custom name, or `--seconds` to set the interval at which to collect metrics
(default is 3).

```bash
$ watchme monitor --func gpu_task sleep 5 --seconds 1
```

And along with the interactive Python version, you can optionally specify
a comma separated value string of keys to include, skip, or only use.
Here we skip two fields:

```bash
$ watchme monitor --func gpu_task sleep 5 --seconds 1 --skip nvml_device_supported_memory_clocks
```

And don't forget you can use the default "func" argument (monitor_pid_task)
to look at cpu metrics:

```bash
$ watchme monitor sleep 2
[{"ionice": {"value": 4, "ioclass": "IOPRIO_CLASS_NONE"}, "nice": 0, "open_files": 0, "cpu_affinity": [0], "cpu_times": {"user": 0.0, "system": 0.0, "children_user": 0.0, "children_system": 0.0}, "memory_full_info": {"rss": 376832, "vms": 110555136, "shared": 290816, "text": 24576, "lib": 0, "data": 331776, "dirty": 0, "uss": 106496, "pss": 120832, "swap": 0}, "create_time": 1562862319.59, "username": "vsochat", "pid": 124761, "ppid": 124759, "cpu_percent": 0.0, "gids": {"real": 32264, "effetive": 32264, "saved": 32264}, "status": "sleeping", "memory_percent": 0.00018733631362330647, "cwd": "/scratch/users/vsochat/WORK/watchme", "uids": {"real": 9182, "effetive": 9182, "saved": 9182}, "name": "sleep", "terminal": "/dev/pts/0", "cmdline": ["sleep", "2"], "exe": "/usr/bin/sleep", "num_ctx_switches": {"voluntary": 13, "involuntary": 3}, "io_counters": {"read_count": 6, "write_count": 0, "read_bytes": 0, "write_bytes": 0, "read_chars": 2012, "write_chars": 0}, "num_fds": 3, "cpu_num": 0, "num_threads": 1, "connections": [], "SECONDS": "3"}]
```

And there you have it! With these methods to monitor any process on the fly at
a particular interval, you are good to go! 


#### Run as a Task

To run as a task, you will want to provide `func@gpu_task` when you create the task. 
You are also required to add a pid, and this can be a number, or the name of the process.
Either way, likely you would be running this for a long running
process, and in the case of providing an integer, you would need to update
the pid of the process when you restart your computer. Here is an example
adding a process name I know will be running when my computer starts:

```bash
$ watchme add-task gpu task-monitor-python --type gpu func@gpu_task pid@python
[task-monitor-python]
func  = gpu_task
pid  = python
skip  = nvml_device_uuid
active  = true
type  = gpu
```

If you choose a process name, remember that different processes can have the same
name (for example, think about the case of having multiple Python interpreters open!)
This means that watchme will select the first in the list that it finds. If you
have preference for a specific one, then it's recommended that you provide the
process id directly.

##### Customize

You can also add a parameter called "skip", including one or more (comma separate)
indices in the results to skip.

```bash
$ watchme add-task gpu task-monitor-python --type gpu func@gpu_task pid@python skip@nvml_device_uuid
```

To test out the task, you can do the following:

```bash
$ watchme run gpu task-monitor-python --test
```

You'll see the results.json print to the screen! When it's time to use the
watcher, you can [active and schedule it](#verify-the-addition).

#### Use as a Decorator

Although the parameters are not stored in the `watchme.cfg`, if you use
the decorator to run the same task, the .git repository is still used
as a database, and you can collect data to monitor your different Python
functions on the fly. Specifically, the decorator is going to use
multiprocessing to run your function, and then watch it via the process id (pid).
You get to choose how often (in seconds) you want to record metrics like
memory, io counters, and cpu, and threads. See [here](https://gist.github.com/vsoch/bf13c7eb1318503effd22e0e0b4190bf) 
for an example of default output for one timepoint.
This decorator function uses the same task function, that we discussed first,
but with a different invocation.


```python
from watchme.watchers.gpu.decorators import monitor_gpu
from time import sleep

@monitor_gpu('gpu', seconds=3)
def myfunc():
    long_list = []
    for i in range(5):
        long_list = long_list + (i*10)*['pancakes']
        print("i is %s, sleeping 10 seconds" % i)
        sleep(10)
```

The first argument is the name of the watcher (e.g., gpu) and you are also allowed
to specify the following arguments (not shown):

 - include: a list of keys to add back in (e.g., "environ")
 - skip: a list of keys to skip (see section above for default)
 - create: create the watcher if it doesn't exist (default is False, must exist)
 - only: forget about include/skip, **only** include these fields
 - name: if you want to call the result folder something other than the function name

Why don't you need specify a pid? Your running function will produce the 
process id, so you don't need to provide it. Let's run this script. You can get 
the full thing [from the gist here](https://gist.github.com/vsoch/bf13c7eb1318503effd22e0e0b4190bf).
You'll notice in the gist example we demonstrate "myfunc" taking arguments too.

```bash
$ python test_monitor_gpu.py 
Calling myfunc with 2 iters
Generating a long list, pause is 2 and iters is 2
i is 0, sleeping 2 seconds
i is 1, sleeping 2 seconds
Result list has length 10
```

Great! So it ran for the watcher we created called `gpu`, but where
are the results? Let's take a look in our watcher folder:

```bash
~/.watchme/gpu$ tree
.
├── decorator-gpu-myfunc
│   ├── result.json
│   └── TIMESTAMP
├── task-monitor-python
└── watchme.cfg
```

In addition to the task that we ran, "task-monitor-python," we also have
results in a new "decorator-gpu-myfunc" folder. You've guessed it right -
the decorator namespace creates folders of the format `decorator-gpu-<name>`,
where name is the name of the function, or a "name" parameter you provide to the
decorator.

> What is a result?

Remember that we are monitoring our function every 3 seconds, so for a function
that lasts about 10, we will record process metrics three times. 
How would we export that data? Like this:

```bash
$ watchme export gpu decorator-gpu-myfunc result.json --json
```

We ask for `--json` because we know the result is provided in json.
For the above export, we will find three commits, each with a commit id,
timestamp, and full result.


### Verify the Addition

Once you add one or more tasks, you can inspect your watcher configuration
file at $HOME/.watchme/gpu/watchme.cfg:

```bash
$ cat $HOME/.watchme/gpu/watchme.cfg
```

You can also use inspect:

```bash
$ watchme inspect gpu
```

At this point, you can test running the watcher with the `--test` flag for
run:

```bash
$ watchme run gpu --test
```

and when you are ready, activate the entire watcher to run:

```bash
$ watchme activate gpu
$ watchme run gpu
```

And don't forget to set a schedule to automated it (if appropriate)

```bash
$ watchme schedule gpu @hourly
$ crontab -l
@hourly /home/vanessa/anaconda3/bin/watchme run gpu # watchme-gpu
```

Every time your task runs, new files (or old files will be updated) and
you can choose to push the entire watcher folder to GitHub to have
reproducible monitoring! Since the parameter result files are named
based on your host and username, others could fork the repo, run
on their system, and pull request to combine data.

When you are ready, [read more](https://vsoch.github.io/watchme/getting-started/index.html#how-do-i-export-data) about exporting data.
