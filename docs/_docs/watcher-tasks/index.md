---
title: Watcher Tasks
category: Watcher Tasks
permalink: /watchers/index.html
order: 1
---

At this point, you've followed the [getting started]({{ site.baseurl }}/getting-started/)
guide to [install]({{ site.baseurl }}/install/) watchme and create your first 
set of watchers. Now, it's time to configure your new watcher, meaning
defining a set of tasks for it to do. Your watcher can have one or more tasks,
and each has a defined type that the watcher knows how to run.
We just have support for watching web urls, task type "urls":

 - [urls]({{ site.baseurl }}/watchers/urls/) to watch for changes in web content
 - [psutils]({{ site.baseurl }}/watchers/psutils) to monitor system, sensors, python, and network
