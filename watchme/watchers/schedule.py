'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.logger import bot
from crontab import CronTab
from watchme.utils import ( which, get_user )

# Scheduling


def remove_schedule(self, name=None, quiet=False):
    '''remove a scheduled item from crontab, this is based on the watcher
       name. By default, we use the watcher instance name, however you
       can specify a custom name if desired.
    '''
    if name == None:
        name = self.name

    cron = self.get_crontab()

    comment = 'watchme-%s' % self.name
    found = False
    for job in cron.find_comment(comment):
        found = True
        cron.remove(job)
    
    if found is True:
        bot.info('Removed schedule for watcher %s' % name)
        cron.write_to_user(user=True)
    return cron


def has_schedule(self, must_exist=False):
    '''determine if a watcher already has a schedule, as a warning to the user.
    '''
    if self.get_job(must_exist=False) == None:
        return False
    return True


def get_job(self, must_exist=True):
    '''return the job to the user, or None
    '''
    # Find the job based on a standard of comment
    cron = self.get_crontab()
    comment = 'watchme-%s' % self.name
    job = list(cron.find_comment(comment)) or [None]
    job = job[0]

    # Return None, or the actual cron job
    if job == None and must_exist == True:
        bot.warning('%s does not have a cron job configured' % self.name)
    
    return job


def get_crontab(self):  
    '''get an instance of the user's crontab. We use the running user.
    '''
    # Create an instance of the user's crontab
    return CronTab(user=True)


def update_schedule(self, minute=12, hour='*', month='*', day='*'):
    '''update a scheduled item from the crontab, with a new entry. This
       first looks for the entry (and removes it) and then clls the new_
       schedule function to write a new one. This function is intended
       to be used by a client from within Python, and isn't exposed from
       the command line.
    '''
    job = self.get_job(must_exist=True)

    # Update the job if found
    if job != None:
        return self.schedule(minute=minute,
                             hour=hour,
                             month=month, 
                             day=day,
                             job=job,
                             force=True)

    bot.warning('%s does not have a current schedule to update.' % self.name)

def clear_schedule(self):
    '''clear all cron jobs associated with the watcher. To remove jobs
       associated with a single watcher, use remove_schedule
    '''
    cron = self.get_crontab()
    bot.info('Clearing jobs associated with all watchers')
    cron.remove_all(comment='watchme-*')

    # Save new cron
    cron.write_to_user(user=True)
    return cron


def schedule(self, 
             minute=12, 
             hour=0, 
             month='*', 
             day='*', 
             weekday='*',
             job=None,
             force=False):
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
       weekday: must be between 0 and 6 or *
       job: if provided, assumes we are updated an existing entry.
    '''
    cron = self.get_crontab()

    # Cut out early if the job already exists, and force is false
    if self.has_schedule() and not force:
        bot.exit('%s already has a schedule. Use --force to update.' % self.name)

    # Remove any previous schedules
    cron = self.remove_schedule(quiet=True)

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

    # Day must be in range 1 through 31, or *
    if weekday not in ['*'] + list(range(7)):
        bot.exit('weekday must be in [0..6] or equal to *')

    # The command will run the watcher, watcher.cfg controls what happens
    whereis = which('watchme')
    command = '%s run %s' % (whereis, self.name)
    comment = 'watchme-%s' % self.name

    if job == None:
        job  = cron.new(command=command, comment=comment)

    # Set the time, and then write the job to file
    job.setall(minute, hour, day, month, weekday)
    job.enable()
    cron.write_to_user(user=True)
    bot.info(job)    

    return job
