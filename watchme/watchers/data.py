'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.logger import bot
from watchme.utils import ( 
    which, 
    get_user
)
from watchme.command import (
    get_commits,
    git_show,
    git_date
)
import os
import json

# Default (git) Data Exports

def export_dict(self, task,
                      filename, 
                      name=None,
                      export_json=False,
                      from_commit=None,
                      to_commit=None,
                      base=None):
    '''Export a data frame of changes for a filename over time.

       Parameters
       ==========
       task: the task folder for the watcher to look in
       name: the name of the watcher, defaults to the client's
       base: the base of watchme to look for the task folder
       from_commit: the commit to start at
       to_commit: the commit to go to
       grep: the expression to match (not used if None)
       filename: the filename to filter to. Includes all files if not specified.
    '''
    if name == None:
        name = self.name

    if base == None:
        base = self.base

    # Quit early if the task isn't there
    if not self.has_task(task):
        bot.exit('%s is not a valid task for %s' % (task, name))

    repo = os.path.join(base, self.name)
    if not os.path.exists(repo):
        bot.exit('%s does not exist.' % repo)

    filepath = os.path.join(base, self.name, task, filename)

    # Ensure that the filename exists in the repository
    if not os.path.exists(filepath):
        bot.exit('%s does not exist for watcher %s' %(filepath, name))

    # Now filepath must be relative to the repo
    filepath = os.path.join(task, filename)

    commits = get_commits(repo=repo,
                          from_commit=from_commit, 
                          to_commit=to_commit,
                          grep="ADD results %s" % task,
                          filename=filepath)

    # Keep lists of commits, dates, content    
    result = {'commits': [], 'dates': [], 'content': []}

    # Empty content (or other) returns None
    for commit in commits:
        content = git_show(repo=repo, commit=commit, filename=filepath)

        if export_json is True:
            content = json.loads(content)

        result['content'].append(content)
        result['dates'].append(git_date(repo=repo, commit=commit))
        result['commits'].append(commit)
    return result


# Exporter Functions

    # Add the exporter, optionally with tasks                  
    watcher.add_exporter(exporter=exporter,
                         exporter_type=exporter_type,
                         params=params,
                         tasks=tasks,
                         force=args.force,
                         active=args.active)


def add_exporter(self, name, exporter_type, params, tasks, force=False, active="true"):
    '''add an exporter, meaning an extra plugin to push data to a remote.

       Parameters
       ==========
       name: the name of the exporter to add, should start with exporter-
       exporter_type: must be in WATCHME_EXPORTERS, meaning a client exists
       params: list of parameters to be validated (key@value)
       tasks: list of task names to add the exporter to
       force: if task already exists, overwrite
       active: add the task as active (default "true")
    '''
    # Check again, in case user calling from client
    if not name.startswith('exporter'):
        bot.exit('Exporter name must start with "exporter" (e.g., exporter-grafana)')

    # Ensure it's a valid type
    if exporter_type not in WATCHME_EXPORTERS:
        bot.exit('%s is not a valid type: %s' % WATCHME_EXPORTERS)

    # Validate variables provided for task
    if task_type.startswith('pushgateway'):
        from watchme.exporters.pushgateway import Exporter

    else:
        bot.exit('exporter_type %s not installed' % exporter_type)

    # Convert list to dictionary
    params = self._get_params_dict(params)

    # Creating the exporter will validate parameters
    exporter = Exporter(name, params=params)

    # Exit if the exporter is not valid
    if not exporter.valid:
        bot.exit('%s is not valid, will not be added.' % exporter)

    # Write to file (all tasks get active = True added, and type)
    self._add_exporter(exporter, force, active, tasks)



def _add_exporter(self, exporter, force=False, active='true', tasks=[]):
    '''add a new exporter to the watcher, meaning we:

       1. Check first that the task doesn't already exist (if the task
          exists, we only add if force is set to true)
       2. Validate the task (depends on the task)
       3. write the task to the helper config file, if valid.

       Parameters
       ==========
       task: the Task object to add, should have a name and params and
             be child of watchme.tasks.TaskBase
       force: if task already exists, overwrite
       active: add the task as active (default "true")
    '''
    self.load_config()

    if active not in ["true", "false"]:
        bot.exit('Active must be "true" or "false"')

    # Don't overwrite a section that already exists
    if exporter.name in self.config.sections():
        if not force:
            bot.exit('%s exists, use --force to overwrite.' % task.name)
        self.remove_section(exporter.name, save=False)

    # Add the new section
    self.config[exporter.name] = exporter.export_params(active=active)
    self.print_section(exporter.name)

    # Add the exporter to any tasks
    for task in tasks:
        if task in self.config.sections():
            exporters = self.get_setting(task, "exporters", default=[])
            if exporter.name not in exporters:
                exporters.append(exporter.name)
                self.set_setting(task, "exporters", exporters)
        else:
            bot.warning("Task %s not found installed, skipping adding exporter to it." % task)

    # Save all changes
    self.save()

    # Commit changes
    git_commit(repo=self.repo, task=self.name,
               message="ADD exporter %s" % exporter.name)

# Get Exporters


def get_exporter(self, name):
    '''get a particular task, based on the name. This is where each type
       of class should check the "type" parameter from the config, and
       import the correct Task class.

       Parameters
       ==========
       name: the name of the task to load
       save: if saving, will be True
    '''
    self.load_config()

    exporter = None

    # Only sections that start with task- are considered tasks
    if name in self.config._sections and name.startswith('exporter'):

        # Task is an ordered dict, key value pairs are entries
        params = self.config._sections[name]

        # Get the task type (if removed, consider disabled)
        exporter_type = params.get('type', '')

        # If we get here, validate and prepare the task
        if exporter_type.startswith("pushgateway"):
            from watchme.exporters.pushgateway import Exporter

        else:
            bot.exit('%s is not a valid exporter type.' % exporter_type)

        # if not valid, will return None (or exit)
        exporter = Exporter(name, params)

    return exporter



def export_runs(self, results):
    ''' export data retrieved to the set of exporters defined and active,
        which can vary based on the task. The export will be run if:

         1. The task has a list of one or more exporters to use.
         2. Any given exporter is defined also in the watchme.cfg
         3. The exporter is active.
     
        If the user does not wish to export data for a specific task,
        the exporter can be turned off (active set to false), the exporter
        name can be removed from "exporters" or the exporter- configuration
        can be removed from the file entirely.
    '''
    for name, result in results.items():

        task = self.get_task(name, save=True)

        # Get exporters added to task
        exporters = self.get_setting(task.name, 'exporters', [])
            
        # Validate each exporter exists and is active, then run.
        for exporter in exporters:

            # Check 1: The exporter must be defined
            if not self.has_section(exporter):
                bot.warning("%s not defined in watchme.cfg for %s" %(exporter, task))
                continue

            # Check 2: It must be active
            # Be more conservative to run an export, default to false
            if self.get_setting(exporter, "active", default="false") == "false":
                bot.warning("%s is defined but not active for %s" %(exporter, task))
                continue

            # If we get here, safe to instantiate the exporter. 
            try:
                client = self.get_exporter(exporter)
            except:
                bot.warning("Check parameters for %s, client did not validate." % exporter) 
                continue

            # A client with "None" indicates a dependency is likely missing          
            if client == None:
                bot.warning("Check dependencies for %s.." % exporter) 
                continue

            # Case 1. The result is a list
            if isinstance(result, list):
                
                # Get rid of Nones, if the user accidentally added
                result = [r for r in result if r]

                if len(result) == 0:
                    bot.error('%s returned empty list of results.' % name)

                # Only save if the export type is not json, and the result is a text string
                elif not task.params.get('save_as') == 'json' and not os.path.exists(result[0]):
                    bot.debug('Exporting list to ' + client.name)
                    client._save_text_list(name, result)

            # Case 2. The result is a string
            elif isinstance(result, str):
                
                # Only export if it's not a file path (so it's a string)
                if not(os.path.exists(result)):
                    client._save_text(result)
            
            # Case 3. The result is a dictionary or a file, ignore for now.
