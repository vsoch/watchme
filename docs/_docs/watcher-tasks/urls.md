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
$ watchme add-task <watcher> task-<name> key1@value1 key2@value2
```

The key and value pairs are going to vary based on the watcher, however
since a URL task is going to watch for changes at a url (at a frequency 
determined by the watcher schedule), it follows that adding the task minimally 
requires a url parameter. 


### Task Parameters

A urls task has the following parameters shared across functions. 

| Name | Required | Default | Example | Notes|
|------|----------|---------|---------|-----------|
| url  | Yes     |undefined|url@https://www.reddit.com/r/hpc| validated starts with http |
| func | No    |get_task |func@download_task| must be defined in tasks.py |
| regex | No    |undefined |regex@[0-9]+| if text, filter to regular expression |

#### Task Headers

For some tasks, you can add one or more headers to the request by specifying `header_<name>`.
For example, to add the header "Token" I could do `header_Token=123456`.
By default, each task has the User-Agent header added, as it typically helps. 
If you want to disable this, add the header_User-Agent to be empty, or change
it to something else.


#### Lists of URL Parameters

For the "Get" and "Get with selection" tasks, you might want to include url parameters. For example,
you might want to loop through a set of pages, meaning ending the url with ?page=1 through ?page=9. 
You can do that with the `url_param_<name>` prefix. As an example, here is how we would
do that. The following task loops through 7 pages of Pusheen dolls, and collects the text value (get_text@true)
from the result of selection page elements by the .money class.

```bash
$ watchme add-task pusheen task-pusheencom url@https://shop.pusheen.com/collections/pusheen func@get_url_selection get_text@true selection@.money url_param_page@1,2,3,4,5,6,7
```

Specifically, note how we specified the "page" parameter for the url, with commas separated each call separately.

```bash
url_param_page@1,2,3,4,5,6,7
```

If you wanted to add another parameter (for each page) you can think of the commas as indexing. So you might do this:

```bash
url_param_name@V,V,V,V,V,V,V
```

or to skip the third page call (page=3) for the name parameter, just leave it empty:


```bash
url_param_name@V,V,,V,V,V,V
```

## Tasks Available

 - [Get Task](#1-get-a-url-task) appropriate if you want to perform a GET (e.g., download a page)
 - [Post Task](#2-post-to-a-url-task) is appropriate for POST requests. The default return value expects json.
 - [Download Task](#3-download-content) to download content, such as a direct link to a file.
 - [Page Select Task](#4-select-on-a-page-task) allows you to specify a javascript selector to return a subset of content

For all tasks above, the Watcher runs them using multiprocessing so you can assume efficiency.

### 1. Get a URL Task

This task will watch for changes at an entire URL, meaning tracking the entire page.
For example, here is a page I wanted to watch for changes:

```bash
$ watchme add-task watcher task-get url@https://httpbin.org/get
[task-get]
url  = https://httpbin.org/get
active  = true
type  = urls
```

In the above, we added the task "task-get" to the watcher called "watcher"
and we defined the parameter "url" to be `https://httpbin.org/get`.
As a confirmation that the task was added, the configuration is printed to the screen.
This task is appropriate for content that you want returned as a string, and then
saved to a text file to the repository. By default, it will be saved as result.txt.
If you want to customize the extension (e.g., get a json object and save as result.json)
specify the save_as parameter:

```bash
$ watchme add-task watcher task-get url@https://httpbin.org/get save_as@json
```

If you anticipate a list of results and want to save to separate jsons (one per entry)
then specify save_as@jsons

```bash
$ watchme add-task watcher task-get url@https://httpbin.org/get save_as@jsons
```

Thus, the following custom parameters can be added:

| Name | Required | Default | Example | Notes|
|------|----------|---------|---------|-----------|
| save_as | No | unset |save_as@json| default saves to json, set as text for raw text. |
| file_name | No | unset |file_name@image.png| the filename to save, only for download_task |
| url_param_<name>| No | unset| url_param_name@V,V,V,V,V,V,V | use commas to separate separate url calls |
| header_* | No | unset | header_Accept@json | Define 1 or headers |

If you specify "save_as" to be json, you will get a results.json unless you specify another
file name. 


### 2. Post to a URL Task

This task will post to get changes from a URL, ideal for watching restful API
endpoints. For example, here is a page I wanted to watch for changes:

```bash
$ watchme add-task watcher task-api-post url@https://httpbin.org/post file_name@post-latest.json func@post_task

[task-api-post]
url  = https://httpbin.org/post
file_name  = post-latest.json
func  = post_task
active  = true
type  = urls
```

Since we are using the task "post_task" it defaults to saving json, so I don't need to set
"save_as" (unless you want to save to a different type). Notice that I've specified a custom file_name too. 

In the above, we added the task "task-api-post" to the watcher called "watcher"
and we defined the parameter "url" to be the endpoint that we want to post to. 
The following custom parameters can be added:

| Name | Required | Default | Example | Notes|
|------|----------|---------|---------|-----------|
| save_as | No | unset |save_as@json| default saves to text, or can be specified as json. |
| file_name | No | unset |file_name@image.png| the filename to save, only for download_task |
| json_param_* | No | unset | json_param_page@1 | Define 1 or more parameters (json/data) for the post |
| header_* | No | unset | header_Accept@json | Define 1 or headers |

You can define parameters for the POST with one or more definitions of `json_param_<name>`, where
the name corresponds with the variable name you want (the json_param_ portion is removed). If you
want to do multiple POSTS with different sets of parameters, you can separate them by commas. The same
is True for headers, except you can only define one set shared across POSTS. Use
 `header_<name>` to define one or more.

### 3. Download Content

You might also want to download some content or object, and save it to file
to track changes over time. You can do this by using the urls type watcher and
specifying the variable func to be "download_task":

```bash
$ watchme add-task watcher task-download url@https://httpbin.org/image/png func@download_task file_name@image.png
[task-download]
url  = https://httpbin.org/image/png
func  = download_task
file_name = image.png
active  = true
type  = urls
```

| Name | Required | Default | Example | Notes|
|------|----------|---------|---------|-----------|
| no_verify_ssl | No | unset |no_verify_ssl@true| |
| write_format | No | unset |write_format@wb| only for download_task |
| file_name | No | unset |file_name@image.png| the filename to save, only for download_task |
| header_* | No | unset | header_Accept@json | Define 1 or headers |


### 4. Select on a Page Task

You might be interested in scraping one div (or general selection, such as a section
identified by a class or id) on a page. For this purpose, you can use the function
`get_url_selection`. Note that you will need to install an extra set of dynamic 
packages to do this:

```bash
$ pip install watchme[watcher-urls-dynamic]
```

This task will watch for changes based on a selection from a page. For example, 
let's say there is a text value on a page with an air quality value. We would want
to define this as the selection:

```bash
$ watchme create air-quality
$ watchme add-task air-quality task-air-oakland url@http://aqicn.org/city/california/alameda/oakland-west func@get_url_selection selection@#aqiwgtvalue file_name@oakland.txt get_text@true
[task-air-oakland]
url  = http://aqicn.org/city/california/alameda/oakland-west
func  = get_url_selection
selection  = #aqiwgtvalue
file_name  = oakland.txt
get_text  = true
active  = true
type  = urls
```

We set "get_text" to true (or anything) so that we are sure to grab the text content of our
selection. The following parameters apply for this function:

| Name | Required | Default | Example | Notes|
|------|----------|---------|---------|-----------|
| selection | Yes | unset | #idname|  |           |
| get_text | No | unset | get_text@true | if found, return text from the selection |
| attributes | No | unset | style,id or id | for some selection, return attributes |
| file_name | No | unset |file_name@image.png| the filename to save, only for download_task |
| url_param_<name>| No | unset| url_param_name@V,V,V,V,V,V,V | use commas to separate separate url calls |
| header_* | No | unset | header_Accept@json | Define 1 or headers |

We can run the task:

```bash
$ watchme activate air-quality
$ watchme run air-quality
```

and then see the result!

```bash
$ tree $HOME/.watchme/air-quality
├── task-air-oakland
│   ├── oakland.txt
│   └── TIMESTAMP
└── watchme.cfg
```

The file itself has the value of 30, the air quality in Oakland today.
I would next want to schedule this at some frequency to collect data 
consistently when my computer is on.

```bash
$ watchme schedule air-quality @hourly
```

### Verify the Addition

We can also confirm this section has been written to file, either by looking
at a watcher directly:

```bash
$ cat /home/vanessa/.watchme/watcher/watchme.cfg 
[watcher]
active = false

[task-get]
url  = https://httpbin.org/get
active  = true
type  = urls
```

or using inspect:

```bash
$ watchme inspect air-quality
```

You don't actually need to use watchme to write these files - you can write
the sections in a text editor if you are comfortable with the format.
The sections are always validated when the watcher is run.


### Force Addition

If for some reason you want to overwrite a task, you need to use force. Here is
what it looks like when you don't, and the task already exists:

```bash
$ watchme add-task watcher task-reddit-hpc url@https://www.reddit.com/r/hpc
ERROR task-reddit-hpc exists, use --force to overwrite.
```

### Active Status

If you want to change the default active status, use `--active false`. By default,
tasks added to watchers are active. Here is what the same command above would have 
looked like setting active to false:

```bash
$ watchme add-task watcher task-reddit-hpc url@https://www.reddit.com/r/hpc --active false
[task-reddit-hpc]
url  = https://www.reddit.com/r/hpc
active  = false
type  = urls
```
