#!/bin/bash
# If the modules changed, the content of "source" should be backed up and
# new files generated (to update) by doing:
#
# sphinx-apidoc -o source/ ../watchme

HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE=$(dirname $HERE)
cd $HERE
cd $BASE && python setup.py install && cd $HERE && make html
rm -rf $BASE/docs/api

# Create new folders
mkdir -p $BASE/docs/api

# Rename folders
find $HERE/_build/html -exec sed -i -e 's/_static/assets/g' {} \;
find $HERE/_build/html -exec sed -i -e 's/_modules/modules/g' {} \;

# Copy to new locations
mv $HERE/_build/html/_static $BASE/docs/api/assets
mv $HERE/_build/html/_modules $BASE/docs/api/modules
cp -R $HERE/_build/html/* $BASE/docs/api
