#!/bin/bash

# Include help functions
. helpers.sh

echo
echo "************** START: test_utils.sh **********************"

# Create temporary testing directory
echo "Creating temporary directory to work in."
tmpdir=$(mktemp -d)
output=$(mktemp ${tmpdir:-/tmp}/watchme_test.XXXXXX)

export WATCHMEENV_density=0.24

echo "#### Testing watchme get_watchme_env"
runTest 0 $output python -c "from watchme.utils import get_watchme_env as ge;import sys;env = ge();print(env.get('density'))" | grep density || exit 1

echo "Finish testing utils"
rm -rf ${tmpdir}
