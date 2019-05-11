#!/bin/bash

echo
echo "************** START: test_watchers.sh **********************"

# Include help functions
. helpers.sh

# Create temporary testing directory
echo "Creating temporary directory to work in."
tmpdir=$(mktemp -d)
output=$(mktemp ${tmpdir:-/tmp}/watchme_test.XXXXXX)

# set the watchme base, create watcher
echo "Creating dummy watcher..."
export WATCHME_BASE_DIR="${tmpdir}"
runTest 0 $output watchme create watcher
runTest 0 $output test -f "$tmpdir/watcher/watchme.cfg"

echo "#### Testing urls tasks..."

echo "get task..."
runTest 255 $output watchme add-task watcher task-missing-param
runTest 0 $output watchme add-task watcher task-get url@https://httpbin.org/get
runTest 255 $output watchme add-task watcher task-get url@https://httpbin.org/get
runTest 0 $output watchme add-task watcher task-get url@https://httpbin.org/get --force
runTest 0 $output test -d "$tmpdir/watcher/task-get"
runTest 0 $output watchme run watcher task-get --test
runTest 0 $output watchme activate watcher
runTest 0 $output watchme run watcher task-get
ls "$tmpdir/watcher/task-get/"
runTest 0 $output test -f "$tmpdir/watcher/task-get/result.json"
runTest 0 $output test -f "$tmpdir/watcher/task-get/TIMESTAMP"

echo "post task"
runTest 0 $output watchme add-task watcher task-api-post url@https://httpbin.org/post file_name@post-latest.json func@post_task
runTest 0 $output watchme run watcher task-api-post --test
runTest 0 $output watchme run watcher task-api-post
runTest 0 $output test -f "$tmpdir/watcher/task-api-post/post-latest.json"
runTest 0 $output test -f "$tmpdir/watcher/task-api-post/TIMESTAMP"

echo "download task"
runTest 0 $output watchme add-task watcher task-download url@https://httpbin.org/image/png func@download_task file_name@image.png
runTest 0 $output watchme run watcher task-download --test
runTest 0 $output watchme run watcher task-download
runTest 0 $output test -f "$tmpdir/watcher/task-download/image.png"
runTest 0 $output test -f "$tmpdir/watcher/task-download/TIMESTAMP"

echo "get_url_selection task"
runTest 0 $output watchme add-task watcher task-air-oakland url@http://aqicn.org/city/california/alameda/oakland-west func@get_url_selection selection@#aqiwgtvalue file_name@oakland.txt get_text@true regex@[0-9]+
runTest 0 $output watchme run watcher task-air-oakland --test
runTest 0 $output watchme run watcher task-air-oakland
runTest 0 $output test -f "$tmpdir/watcher/task-air-oakland/oakland.txt"
runTest 0 $output test -f "$tmpdir/watcher/task-air-oakland/TIMESTAMP"

echo "#### Testing psutils tasks..."
runTest 0 $output watchme create system
runTest 0 $output watchme activate system

runTest 0 $output watchme add-task system task-monitor-python --type psutils func@monitor_pid_task pid@python
runTest 0 $output watchme add-task system task-cpu --type psutils func@cpu_task
runTest 0 $output watchme add-task system task-memory --type psutils func@memory_task
runTest 0 $output watchme add-task system task-network --type psutils func@net_task skip@net_connections,net_if_address
runTest 0 $output watchme add-task system task-python --type psutils func@python_task
runTest 0 $output watchme add-task system task-sensors --type psutils func@sensors_task
runTest 0 $output watchme add-task system task-system --type psutils func@system_task
runTest 0 $output watchme add-task system task-users --type psutils func@users_task

for task in monitor-python cpu memory network python sensors system users; do
    runTest 0 $output watchme run system task-$task --test
    runTest 0 $output watchme run system task-$task
    runTest 0 $output test -f "$tmpdir/system/task-$task/result.json"
    runTest 0 $output test -f "$tmpdir/system/task-$task/TIMESTAMP"
done

echo "#### Testing psutils decorator..."
runTest 0 $output python test_psutils_decorator.py
runTest 0 $output test -d "$tmpdir/system/decorator-psutils-myfunc"
runTest 0 $output test -f "$tmpdir/system/decorator-psutils-myfunc/result.json"
runTest 0 $output test -f "$tmpdir/system/decorator-psutils-myfunc/TIMESTAMP"

echo "#### Testing results task..."

runTest 0 $output watchme create results-watcher
runTest 0 $output watchme activate results-watcher

echo "from_env task..."

runTest 0 $output watchme add-task results-watcher task-hpc-job --type results func@from_env_task
export WATCHMEENV_density=0.45
export WATCHMEENV_weight=32
runTest 0 $output watchme run results-watcher task-hpc-job --test
runTest 0 $output watchme run results-watcher task-hpc-job
runTest 0 $output test -f "$tmpdir/results-watcher/task-hpc-job/density"
runTest 0 $output test -f "$tmpdir/results-watcher/task-hpc-job/weight"
runTest 0 $output test -f "$tmpdir/results-watcher/task-hpc-job/TIMESTAMP"

echo "Finish testing watchers!"
rm -rf ${tmpdir}
