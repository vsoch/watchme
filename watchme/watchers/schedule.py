'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.logger import bot
from crontab import CronTab

# Scheduling


def remove_schedule(self, name=None, user=None):
    '''remove a scheduled item from crontab, this is based on the watcher
       name. By default, we use the watcher instance name, however you
       can specify a custom name if desired.
    '''
    if name == None:
        name = self.name

    bot.info('Clearing jobs associated with watcher %s' % name)
    cron = self.get_crontab(user)
    job = cron.find_comment('watchme-%s' % name)
    cron.remove(job)
    return cron


def get_crontab(self, user=None):  
    '''get an instance of the user's crontab. If no user is defined, we use
       the running user.
    '''

    cron = self.get_crontab(user)

    # If no user provided, just default to running user
    if user == None:
        user = True

    # Create an instance of the user's crontab
    return CronTab(user=user)


def update_schedule(self, minute=12, hour='*', month='*', day='*', user=None):
    '''update a scheduled item from the crontab, with a new entry. This
       first looks for the entry (and removes it) and then clls the new_
       schedule function to write a new one.
    '''
    cron = self.get_crontab(user)
    comment = 'watchme-%s' % self.name
    job = cron.find_comment(comment)

    # TODO: check what this returns if not defined

    self.new_schedule(minute=minute,
                      hour=hour,
                      month=month, 
                      day=day,
                      user=user,
                      job=job)          

def clear_schedule(self):
    '''clear all cron jobs associated with the watcher. To remove jobs
       associated with a single watcher, use remove_schedule
    '''
    cron = self.get_crontab(user)
    bot.info('Clearing jobs associated with all watchers')
    cron.remove_all(comment='watchme-*')
    return cron


def new_schedule(self, 
                 minute=12, 
                 hour=0, 
                 month='*', 
                 day='*', 
                 user=None,
                 job=None):
    '''schedule the watcher to run at some frequency to update record of pages.
       By default, the task will run at 12 minutes passed midnight, daily.
       You can change the variables to change the frequency. See
       https://crontab.guru/ to get a setting that works for you.

            Hourly:	0 * * * *
            Daily:	0 0 * * *    (midnight) default
            weekly	0 0 * * 0
            monthly	0 0 1 * *
            yearly	0 0 1 1 *

       Parameters
       ==========
       minute: must be within 1 and 60, or set to "*" for every minute
       hour: must be within 0 through 23 or set to *
       month: must be within 1 and 12, or *
       day: must be between 1 and 31, or *
       user: if not defined, use running user.
       job: if provided, assumes we are updated an existing entry.
    '''
    cron = self.get_crontab(user)

    # minute must be between * or 0 through 59, or *
    if minute not in ['*'] + list(range(60)):
        bot.exit('minute must be in [0..59] or equal to *')

    # Hour must be between 0 through 23, or *
    if hour not in ['*'] + list(range(24)):
        bot.exit('hour must be in [0..23] or equal to *')
  
    # Day must be in range 1 through 31, or *
    if day not in ['*'] + list(range(1,32)):
        bot.exit('day must be in [1..31] or equal to *')

    # Day must be in range 1 through 31, or *
    if month not in ['*'] + list(range(1,13)):
        bot.exit('month must be in [1..12] or equal to *')

    # The command will run the watcher, watcher.cfg controls what happens
    command = 'watchme run %s' % self.name
    comment = 'watchme-%s' % self.name

    if job == None:
        job  = cron.new(command=command, comment=comment)

    # Set the time, and then write the job to file
    job.setall(minute, hour, day, month, None)
    job.enable()
        
    return job
