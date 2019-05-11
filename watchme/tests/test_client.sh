#!/bin/bash

# Include help functions
. helpers.sh

echo
echo "************** START: test_client.sh **********************"

# Create temporary testing directory
echo "Creating temporary directory to work in."
tmpdir=$(mktemp -d)
output=$(mktemp ${tmpdir:-/tmp}/watchme_test.XXXXXX)

echo "Testing help commands..."

# Test help for all commands
for command in init get export create add-task inspect list protect remove run activate deactivate schedule edit;
    do
    runTest 0 $output watchme $command --help 
done

echo "#### Testing WATCHME_BASE_DIR setting"

# set the watchme base, create watcher
echo "#### Testing watchme create"
export WATCHME_BASE_DIR="${tmpdir}"
runTest 0 $output watchme create watcher

# Does the watcher directory exist, and the config file?
runTest 0 $output test -d "$tmpdir/watcher"
runTest 0 $output test -d "$tmpdir/watcher/.git"
runTest 0 $output test -f "$tmpdir/watcher/watchme.cfg"

# Test downloading another watcher
echo "#### Testing watchme get"
runTest 0 $output watchme get https://www.github.com/vsoch/watchme-github-repos
runTest 0 $output test -d "$tmpdir/watchme-github-repos/.git"
runTest 0 $output test -f "$tmpdir/watchme-github-repos/watchme.cfg"

echo "With a custom name..."
runTest 0 $output watchme get https://www.github.com/vsoch/watchme-github-repos github
runTest 0 $output test -d "$tmpdir/github/.git"
runTest 0 $output test -f "$tmpdir/github/watchme.cfg"

echo "#### Testing watchme export"
runTest 0 $output watchme export github task-singularity result.json --json
runTest 0 $output watchme export github task-singularity result.json
runTest 0 $output watchme export github task-singularity TIMESTAMP
runTest 255 $output watchme export github task-singularity doesnt-exist.json

echo "#### Testing watchme inspect"
runTest 0 $output watchme inspect github task-sregistry
runTest 255 $output watchme inspect github task-doesntexist
runTest 255 $output watchme inspect github invalid-task

echo "#### Testing watchme list"
runTest 0 $output watchme list
runTest 0 $output watchme list github
runTest 0 $output watchme list github task-sregistry

echo "#### Testing watchme protect and freeze"
runTest 0 $output watchme protect watchme-github-repos on
runTest 255 $output watchme remove watchme-github-repos --delete
runTest 0 $output watchme protect watchme-github-repos off
runTest 0 $output watchme protect watchme-github-repos freeze
runTest 255 $output watchme remove watchme-github-repos --delete
runTest 0 $output watchme protect watchme-github-repos unfreeze
runTest 0 $output watchme protect watchme-github-repos off
runTest 0 $output watchme remove watchme-github-repos --delete

echo "#### Testing watchme activate and deactivate"
runTest 0 $output watchme deactivate github
runTest 255 $output watchme run github
runTest 0 $output watchme activate github
runTest 0 $output watchme deactivate github task-singularity

echo "#### Testing watchme run"
runTest 0 $output watchme run github task-spython --test
runTest 0 $output watchme run github task-expfactory
runTest 0 $output watchme run github task-expfactory --no-progress
runTest 0 $output watchme run github task-expfactory --serial
runTest 0 $output watchme run github task-doesntexist

echo "Finish testing basic client"
rm -rf ${tmpdir}
