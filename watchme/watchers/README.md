# Watchers

Each of these is a Watcher that the user can request.

 - [urls](urls) to watch for changes in websites (default)
 - [psutils](psutils) to get basic system statistics

## Watcher Base

The watcher base is defined in the [init](__init__.py) file here. 

 - [schedules](schedule.py) to interact with cronjobs
 - [exporters](data.py) (extras) and the default export of temporal data
 - [settings](settings.py) meaning add/remove from the watchme.cfg
