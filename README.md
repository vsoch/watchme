# WatchMe

![https://raw.githubusercontent.com/vsoch/watchme/master/docs/assets/img/logo_small.gif](https://raw.githubusercontent.com/vsoch/watchme/master/docs/assets/img/logo_small.gif)

[![DOI](https://zenodo.org/badge/177837425.svg)](https://zenodo.org/badge/latestdoi/177837425)
[![DOI](http://joss.theoj.org/papers/10.21105/joss.01388/status.svg)](https://doi.org/10.21105/joss.01388)
[![CircleCI](https://circleci.com/gh/vsoch/watchme.svg?style=svg)](https://circleci.com/gh/vsoch/watchme)

Reproducible watching of web changes. Good for:

 1. Monitoring system resources (battery, network, memory, cpu, etc.)
 2. Waiting for job postings to change or appear
 3. Monitoring some subset of prices from different vendors
 4. Tracking changes in GitHub repositories (stars, etc.) over time

 - [documentation](https://vsoch.github.io/watchme)
 
WatchMe can watch for changes to an entire page, or a specific section of it.
It's appropriate for research use cases where you want to track changes in one
or more pages over time. WatchMe also comes with psutils (system tasks) built
in to allow for monitoring of system resources. Importantly, it is a tool that
implements *reproducible monitoring*, as all your watches, are stored in a 
configuration file that can easily be shared with others
to reproduce your watching protocol. For more information, see the
[documentation](https://vsoch.github.io/watchme). 
[Docker bases](https://quay.io/repository/vanessa/watchme?tab=tags) are
also available for monitoring processes inside containers.

## Limitations

Watchme uses [cron](http://man7.org/linux/man-pages/man5/crontab.5.html) for
scheduling jobs. This means that if a system was shutdown and then started again
after some time, watchme will not recover missing jobs during that period. If
you have ideas for how to better schedule jobs that you want added to the library,
please [open an issue](https://github.com/vsoch/watchme)!

## Licenses

This code is licensed under the MPL 2.0 [LICENSE](LICENSE).
