
# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


__version__ = "0.0.20"
AUTHOR = 'Vanessa Sochat'
AUTHOR_EMAIL = 'vsochat@stanford.edu'
NAME = 'watchme'
PACKAGE_URL = "http://www.github.com/vsoch/watchme"
KEYWORDS = 'web, changes, cron, reproducible, version-control'
DESCRIPTION = "reproducible monitoring client with exporters"
LICENSE = "LICENSE"

INSTALL_REQUIRES = (
    ('python-crontab', {"min_version": "2.3.6"}),
    ('configparser', {"min_version": "3.5.3"}),
    ('requests', {"min_version": "2.21.0"})
)

## beautiful soup selection task

INSTALL_URLS_DYNAMIC = (
    ('beautifulsoup4', {'min_version': '4.6.0'}),
    ('lxml', {'min_version': '4.1.1'}),
)

INSTALL_PSUTILS = (
    ('psutil', {'min_version': '5.4.3'}),
)

# Install all watchers and exporters
INSTALL_ALL = (INSTALL_REQUIRES +
               INSTALL_PSUTILS +
               INSTALL_URLS_DYNAMIC)

# Install all watchers
INSTALL_WATCHERS = (INSTALL_REQUIRES +
                    INSTALL_PSUTILS +
                    INSTALL_URLS_DYNAMIC)
