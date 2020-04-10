---
title: Debugging
category: Getting Started
permalink: /getting-started/debugging/
order: 5
---

Let's say that you create a new watcher called tasks:

```bash
$ watchme create tasks
Adding watcher /home/vanessa/.watchme/tasks...
Generating watcher config /home/vanessa/.watchme/tasks/watchme.cfg
```

You add a task to watch a URL:

```
$ watchme add-task tasks task-watch-belta url@http://stopcovid.belta.by
[task-watch-belta]
url  = http://stopcovid.belta.by
active  = true
type  = urls
```

You activate the watcher:

```
$ watchme activate tasks
[watcher|tasks] active: true
```

And inspect it:

```
$ watchme inspect tasks
[watcher]
active  = true
type  = urls

[task-watch-belta]
url  = http://stopcovid.belta.by
active  = true
type  = urls
```

You want to manually run the task to test it, but you get an error:

```
$ watchme run tasks task-watch-belta 
Found 1 contender tasks.
[1/1] |===================================| 100.0% 
ERROR Error running task.
```

You realize that you should have done a test run (that doesn't try to save data)

```
$ watchme run tasks task-watch-belta --test
Found 1 contender tasks.
[1/1] |===================================| 100.0% 
ERROR Error running task.
```

but that gives you the same thing! And this is logical, because there is some error
with retrieving the URL and getting the result in the first place. The reason
that we aren't able to easily see the error output above is due to the fact 
that watchme is using multiprocessing to run tasks.

The way that you can get around this to debug the issue is to add the `--serial`
flag, which will run the task in serial:

```
$ watchme run tasks task-watch-belta --serial --test
Found 1 contender tasks.
[task-watch-belta:1/1] |===================================| 100.0% 
Traceback (most recent call last):
  File "/home/vanessa/anaconda3/bin/watchme", line 10, in <module>
    sys.exit(main())
  File "/home/vanessa/anaconda3/lib/python3.7/site-packages/watchme/client/__init__.py", line 350, in main
    main(args, extras)
  File "/home/vanessa/anaconda3/lib/python3.7/site-packages/watchme/client/run.py", line 29, in main
    show_progress=not args.no_progress)
  File "/home/vanessa/anaconda3/lib/python3.7/site-packages/watchme/watchers/__init__.py", line 791, in run
    results = self.run_tasks(tasks, parallel, show_progress)
  File "/home/vanessa/anaconda3/lib/python3.7/site-packages/watchme/watchers/__init__.py", line 731, in run_tasks
    results[task.name] = task.run()
  File "/home/vanessa/anaconda3/lib/python3.7/site-packages/watchme/tasks/__init__.py", line 110, in run
    return func(**params)
  File "/home/vanessa/anaconda3/lib/python3.7/site-packages/watchme/watchers/urls/tasks.py", line 47, in get_task
    result = parse_success_response(response, kwargs)
  File "/home/vanessa/anaconda3/lib/python3.7/site-packages/watchme/watchers/urls/helpers.py", line 75, in parse_success_response
    result = response.json()
  File "/home/vanessa/anaconda3/lib/python3.7/site-packages/requests/models.py", line 897, in json
    return complexjson.loads(self.text, **kwargs)
  File "/home/vanessa/anaconda3/lib/python3.7/json/__init__.py", line 348, in loads
    return _default_decoder.decode(s)
  File "/home/vanessa/anaconda3/lib/python3.7/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/home/vanessa/anaconda3/lib/python3.7/json/decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

In this case, we see that there is a bug that the result is expected to be json (but it's not!)
We need to change the save_as parameter to be "text" since it defaults to json. Let's do that:


```
$ watchme add-task tasks task-watch-belta url@http://stopcovid.belta.by
[task-watch-belta]
url  = http://stopcovid.belta.by
active  = true
type  = urls
save_as = text
```

You should then be able to run the same job in serial (or parallel) and get a successful run.

```bash
$ watchme run tasks task-watch-belta 
Found 1 contender tasks.
[1/1] |===================================| 100.0% 
```
