---
title: Watcher Contribution
category: Contributing
order: 2
---

Along with contributing documentation and general code, the cool thing about watchme
is that it's fairly easy to add a new kind of watcher task! Follow this guide for instructions.

## 1. Add a Task Folder

First, create a new folder under `watchme/tasks` that corresponds with the name of your
task. For example, the urls watcher is located at `watchme/tasks/urls`. 

## 2. Add your Task

In the `__init__.py`
in that folder you should put your watcher class called "Task" that instantiates the TaskBase
class as a parent:

```python
'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


'''
from watchme.tasks import TaskBase
from watchme.logger import bot
import os
import sys

class Task(TaskBase):

    required_params = ['url']

    def __init__(self, name, params=[], **kwargs): 

        self.type = 'urls'

        # Handles setting the name, setting params, and validate
        super(Task, self).__init__(name, params, **kwargs)

```

Under `self.type` you should put the name, which is usually the same as the folder
(urls shown above). If you have any required parameters (the minimum set for the
task to run) put them under `required_params`.

## 2. Write a validation function

The parent class is already going to check that the user has provided the `required_params`,
so you can implement an (optional) `_validate` function that does additional input
checks. This check will be performed both when the user adds a new task, and when 
a task is run, in the case that the user decided to manually edit a configuration 
file and invalidate a task.

```python
    def _validate(self):
        '''additional validation function, called by validate() of 
           superclass. Here we assume all required self.params are included.
           If an parameter is found to be invalid, self.valid should be set
           to False
        '''
        # The url must begin with http
        if not self.params['url'].startswith('http'):
            bot.error('%s is not a valid url.' % self.params['url'])
            self.valid = False
```

If one or more parameters are found to be invalid, you should set self.valid to False.
You don't need to exit from the function. You also don't need to have this function if no further validation is needed.

### 3. Write a function to run your task

The watcher client is going to be assembling the list of tasks to run, and then
running them. Specifically, it's going to be creating an instance of your Task
class, and handing it the entire (dictionary) of parameters as key value pairs:

```python
task = Task(params)
```

In the example above, params looks like this:

```python
{
    "url": "https://www.reddit.com/r/hpc",
    "active": "true",
    "type": "urls",
    "uri": "task-reddit-hpc"
}
```

The user generated this task at the command line only providing a url:

```bash
$ watchme add task-reddit-hpc url@https://www.reddit.com/r/hpc
```

And the variables for active, the unique resource identifier (uri) and the
task type were added either as a default setting (type) or a default variable
set by the watcher (active and uri). If your watcher were called something
different (e.g., network) then the command would have looked like this:

```bash
$ watchme add task-reddit-hpc url@https://www.reddit.com/r/hpc --type network
```

It follows that in the instantiation of your class, it must return a task object.
If the `task.valid` is True, you are good to go. If `task.valid` is False, the
task won't be run. 

### 4. Write Task Functions

The multiprocessing workers are going to expect, for each task, to be able
to export a set of parameters (dictionary of key value pairs, usually just
the task.params object) and a function to run. Thus, we use the following
functions:

```python
task.export_params()
```

This function is already implemented, and will return the task.params. 

```python
task.export_func()
```

This function is required to be implemented by your Task subclass. The function
should expect to take one or more keyword arguments. If your task type just
has one function, it's fairly straight forward to import and return the function. 
If you choose between one or more functions based on user variables, you can implement
that logic here, and return the correct one. Where should you store the task
functions? You can put them in a `tasks.py` located in the same folder:

```bash
watchme/
  watchers/
    urls/
      __init__.py
      tasks.py
```

#### Rules for Tasks

The following rules should pertain to writing tasks:

  1. The input variables must coincide with the variables named by the task.params. The task should accept some exploded list of of **kwargs to be flexible to do this.
  2. The task should return some finished file object, string, or other text matter that the watcher can then update in the repository.
    a. If you want to write json data, return a dictionary
    b. If you want to download an actual file, return the full path. It will be found to exist, and moved to the correct watcher folder.
    c. If a string is provided and it doesn't exist as a path, it's assumed to be some text to write to file.
  3. If the function is not successful, return None.

#### Variables for Tasks

You should tell your users (in the task function header, and documentation for it)
what variables are allowed to be set for the task. If the variable is defined
in the task.kwargs (from the watcher configuration) your function can check for it,
and return a default. For example, let's say I wanted to give my users the optional
to disable ssl checking when downloading an object. I would tell them to set
`disable_ssl_check` when they create the task:

```bash
$ watchme add task-dangerous url@https://www.download/big/thing disable_ssl_check@true
```

And then my function could check for it, and set a default.

```python
verify = True
if "disable_ssl_check" in kwargs:
    verify = False
```

As another example, let's say the task will by default write the content to a file.
If you wanted the user to be able to specify writing binary, you could tell them about
a `write_format` variable:

```python
write_format = kwargs.get('write_format', 'w')
```

It would always default to "w" unless otherwise specified:

```bash
$ watchme add task-download-binary url@https://www.download/big/thing write_format@wb
```

### 5. Write Documentation

Finally, you should write up all of the usage examples and variables into 
a documentation file for the watcher! These are located under `docs/_docs/watcher-tasks` 
and the file should be named according to the task type. For example, the "urls"
task shown above has a file named `docs/_docs/watcher-tasks/urls.md`. In the front
end matter, you should only need to change the title, and the permalink for your 
type (it should be in the format `/watchers/<name>`:

```
---
title: URLS
category: Watcher Tasks
permalink: /watchers/urls/
order: 2
---
```

Then in the index.md in that same folder, add a link for your watcher page:

```
 - [url watcher]({{ site.baseurl }}/watchers/urls/) to watch for changes in web content
```

Write as much detail in the documentation as you think necessary. Generally, you want
to say:

 - required and optional parameters
 - usage examples
 - functions available for the task, and how to specify them using the parameter "func"
