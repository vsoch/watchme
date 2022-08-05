# CHANGELOG

This is a manually generated log to track changes to the repository for each release. 
Each section should include general headers such as **Implemented enhancements** 
and **Merged pull requests**. All closed issued and bug fixes should be 
represented by the pull requests that fixed them.
Critical items to know are:

 - renamed commands
 - deprecated / removed commands
 - changed defaults
 - backward incompatible changes
 - changed behaviour

## [master](https://github.com/vsoch/watchme/tree/master)
 - ensuring a better error message is given when watchme config missing (0.0.29)
 - updating documentation to match library, more notes (0.0.28)
 - addition of GPU task, including terminal and process monitor (0.0.27)
 - adding linting, cleaning up an error for psutils watcher (0.0.26)
 - loop values should be checked for None first (0.0.25)
 - Connections aren't being parsed (0.0.24)
 - But with printing output to screen for monitor (should be json) (0.0.23)
 - Adding terminal monitor command group (0.0.22)
 - Print of task should be "add-task" (0.0.21)
 - Custom WATCHME_ENV variables added to monitoring decorator/task (0.0.20)
 - Adding decorator for system (psutils) monitoring (0.0.19)
 - Reorganizing task functions to belong with TaskBase (0.0.17)
 - Adding option for regular expression for URL wachers, user agent header (0.0.16)
 - requests is missing from install dependencies (0.0.15)
 - small bug fixes (0.0.14)
 - added headers, params, and json args for post and get urls. (0.0.13)
 - added ability to specify URL params for Get and Get with selector functions (0.0.12)
 - first beta release of watchme, all commands and docs (0.0.11)
 - adding changelog, and original skeleton for client  (0.0.1)
