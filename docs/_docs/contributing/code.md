---
title: Github Contribution
category: Contributing
order: 3
---


To contribute to code, you should first *fork* the <a href="https://www.github.com/{{ site.repo }}" target="_blank">{{ site.title }}</a> repository by clicking the *fork* button on the top right of the page. Once forked, you will want to clone the fork of the repository to your computer:

```bash
git clone https://github.com/<username>/{{ site.reponame }}
cd {{ site.reponame }}/
```

The main python module, watchme, is in the top level folder. You should checkout a branch,
push the branch to your remote, and when you are ready, open a pull request against
the master branch of vsoch/watchme.

```bash
git checkout -b add/my-feature
git commit -a -m 'adding my new feature!'
git push origin add/my-feature
```
