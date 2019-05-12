---
title: Example Watchers
category: Examples
permalink: /examples/index.html
order: 1
---

## Repository Examples

Here you can find example watcher repos:

 - [system](https://github.com/vsoch/watchme-system) for system, sensors, users, and networking monitoring using psutils tasks.
 - [results](https://github.com/vsoch/results-watcher) watcher can be run to quickly save any set of prefixed environment variables to a task folder.
 - [sklearn](https://github.com/vsoch/watchme-sklearn) demonstrates using WatchMe decorators monitor different sklearn functions on the fly. 
 - [air-quality](https://github.com/vsoch/watchme-air-quality) for watching a metric across a few cities.
 - [prices](https://github.com/vsoch/watchme-pusheen) an example for monitoring Pusheen prices across several vendors.
 - [repository](https://github.com/vsoch/watchme-github-repos) to show using WatchMe to track GitHub repository metadata.

For either of the above, you can easily install and activate the watcher to run on
your machine! See [here](https://vsoch.github.io/watchme/getting-started/#how-do-i-get-a-watcher).
For specific details about creating the watchers in question, see the README markdowns
in the repositories.

## Configuration Examples

The following example configurations are contributed by users over time. If you
have an example to contribute, please [open an issue](https://www.github.com/{{ site.repo }}/issues)
to share it.

### URL Watchers

The following are examples for [URL watchers](https://vsoch.github.io/watchme/watchers/urls/).
In the following example, the user is using the `get_url_selection` task to extract
a number (note the regular expression) from the text resulting from selecting the
class `.local-temp`. For this version of WatchMe the User-Agent header was not
automatically added, so he added it here as a `header_*` parameter.

```
[task-temperature]
url = https://www.accuweather.com/en/lu/luxembourg/228714/weather-forecast/228714
selection = .local-temp
get_text = true
func = get_url_selection
active = true
type = urls
regex = [0-9]+
header_user-agent = Mozilla/5.0
```
