---
title: Github Contribution
category: Contributing
order: 2
---


To contribute to code, you should first *fork* the <a href="https://www.github.com/{{ site.repo }}" target="_blank">{{ site.title }}</a> repository by clicking the *fork* button on the top right of the page. Once forked, you will want to clone the fork of the repository to your computer:

```bash
git clone https://github.com/<username>/{{ site.reponame }}
cd {{ site.reponame }}/
```

The main python module, sif, is in the top level folder. You should checkout a branch,
push the branch to your remote, and when you are ready, open a pull request against
the master branch of singularityhub/sif.

```bash
git checkout -b add/my-feature
git commit -a -m 'adding my new feature!'
git push origin add/my-feature
```

## Development Tips

For development, it's helpful to first pull an image with 3.0:

```bash
$ singularity pull --name boxes.simg docker://vanessa/boxes
```

or with Docker

```bash
$ docker run -v $PWD/:/tmp singularityware/singularity:3.0 pull --name boxes.simg docker://vanessa/boxes
```

And then open up ipython, and start like this:

```python
from sif.main import SIFHeader

image = 'boxes.simg'

self = SIFHeader(image)
```

By instantiating the header as self, you can easily copy paste code
into your terminal to test and debug.
