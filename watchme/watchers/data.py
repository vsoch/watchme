__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from watchme.logger import bot
from watchme.command import get_commits, git_show, git_date
import os
import json

# Data Exports


def export_dict(
    self,
    task,
    filename,
    name=None,
    export_json=False,
    from_commit=None,
    to_commit=None,
    base=None,
):
    """Export a data frame of changes for a filename over time.

    Parameters
    ==========
    task: the task folder for the watcher to look in
    name: the name of the watcher, defaults to the client's
    base: the base of watchme to look for the task folder
    from_commit: the commit to start at
    to_commit: the commit to go to
    grep: the expression to match (not used if None)
    filename: the filename to filter to. Includes all files if not specified.
    """
    if name is None:
        name = self.name

    if base is None:
        base = self.base

    # Quit early if the task isn't there
    if not self.has_task(task) and not task.startswith("decorator"):
        bot.exit("%s is not a valid task or decorator for %s" % (task, name))

    repo = os.path.join(base, self.name)
    if not os.path.exists(repo):
        bot.exit("%s does not exist." % repo)

    filepath = os.path.join(base, self.name, task, filename)

    # Ensure that the filename exists in the repository
    if not os.path.exists(filepath):
        bot.exit("%s does not exist for watcher %s" % (filepath, name))

    # Now filepath must be relative to the repo
    filepath = os.path.join(task, filename)

    commits = get_commits(
        repo=repo,
        from_commit=from_commit,
        to_commit=to_commit,
        grep="ADD results %s" % task,
        filename=filepath,
    )

    # Keep lists of commits, dates, content
    result = {"commits": [], "dates": [], "content": []}

    # Empty content (or other) returns None
    for commit in commits:
        content = git_show(repo=repo, commit=commit, filename=filepath)

        if export_json is True:
            content = json.loads(content)

        # If it's a list, add it to content
        if isinstance(content, list):
            result["content"] += content
        # Otherwise, append
        else:
            result["content"].append(content)

        result["dates"].append(git_date(repo=repo, commit=commit))
        result["commits"].append(commit)
    return result
