# WatchMe

![docs/assets/img/logo_small.gif](docs/assets/img/logo_small.gif)

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

## Licenses

This code is licensed under the MPL 2.0 [LICENSE](LICENSE).
