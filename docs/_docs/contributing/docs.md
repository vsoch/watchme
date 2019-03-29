---
title: Contributing to Documentation
category: Contributing
order: 3
---

It's so great that you want to contribute! The documentation here includes information
about using and developing {{ site.title }}, and they are hosted on Github, meaning that you
can easily contribute via a [pull request](https://help.github.com/articles/about-pull-requests/).

## Getting Started

### Installing Dependencies

Initially (on OS X), you will need to setup [Brew](http://brew.sh/) which is a 
package manager for OS X and [Git](https://git-scm.com/). To install Brew and Git, 
run the following commands:

```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install git
```

If you are on Debian/Ubuntu, then you can easily install git with `apt-get`

```bash
apt-get update && apt-get install -y git
```

### Fork the repo

To contribute to the web based documentation, you should obtain a GitHub account and *fork* the <a href="https://www.github.com/{{ site.repo }}" target="_blank">{{ site.title }} Documentation</a> repository by clicking the *fork* button on the top right of the page. Once forked, you will want to clone the fork of the repo to your computer. Let's say my GitHub username is *meatball*:

```bash
git clone https://github.com/meatball/{{ site.reponame }}
cd {{ site.reponame }}/
```

### Install a local Jekyll server
This step is required if you want to render your work locally before committing the changes. This is highly recommended to ensure that your changes will render properly and will be accepted.

```bash
brew install ruby
gem install jekyll
gem install bundler
bundle install
```

The documentation is located in the "docs" subfolder, so after cloning the repository,
you can change the directory to there and then run the jekyll serve.
Specifically, you can see the site locally by running the server with jekyll:

```bash
cd docs
bundle exec jekyll serve
```

This will make the site viewable at <a href="http://localhost:4000/{{ site.title }}/" target="_blank">http://localhost:4000/{{ site.title }}/</a>.
