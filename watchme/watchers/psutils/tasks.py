'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from subprocess import (
    check_output, 
    CalledProcessError
)
from watchme.logger import bot
import os
import psutil

def monitor_pid_task(**kwargs):
    '''monitor a specific process. This function can be used as a task, or
       is (most likely used) for the psutils.decorators. A pid parameter
       is required.

       Parameters
       ==========
       skip: an optional list of (comma separated) fields to skip. Can be in
             net_io_counters,net_connections,net_if_address,net_if_stats
       pid: the process id or name (required)
    '''
    pid = kwargs.get('pid', None)

    bot.debug(kwargs)

    # Helper function to get list from one,two,three
    def get_list(name):
        csv_list = kwargs.get(name, '')
        return [x for x in csv_list.split(',') if x]

    # A comma separated list of parameters to skip
    skip = get_list('skip')
    include = get_list('include')
    only = get_list('only')

    # Only continue given that argument is provided
    if pid == None:   
        bot.warning("A 'pid' parameter is required to use the monitor_pid_task function.")
        return pid

    # The user is allowed to provide a process name, or a number
    try:
        pid = int(pid)
    except ValueError:
        pid = _get_pid(pid)

    # But if it's stil no good (None) we exit.
    if pid == None:
        bot.warning("'pid' must be a running process or process name.")
        return pid

    ps = psutil.Process(pid)
    bot.debug(ps)

    results = {}

    for key, val in ps.as_dict().items():

        # First priority goes to a custom set
        if len(only) > 0 and key in only:
            bot.debug('skipping %s' % key)
            continue 

        # The user requested to skip
        elif key in skip or key in ['threads']:
            continue

        # Keep count of threads
        elif key in ["open_files"]:
            results[key] = len(val)

        # Don't risk exposing sensitive information
        elif key == "environ":
            if key in include:
                results[key] = val

        # Skip over ones that are too detailed
        elif key in ['memory_maps']:
            continue

        # I assume this included all that are in pmem too
        elif isinstance(val, psutil._pslinux.pfullmem):
            results[key] = {"rss": val.rss,
                            "vms": val.vms,
                            "shared": val.shared,
                            "text": val.text,
                            "lib": val.lib,
                            "data": val.data,
                            "dirty": val.dirty,
                            "uss": val.uss,
                            "pss": val.pss,
                            "swap": val.swap}

        elif isinstance(val, psutil._common.pgids) or isinstance(val, psutil._common.puids):
            results[key] = {"real": val.real,
                            "effetive":val.effective,
                            "saved": val.saved}

        elif isinstance(val, psutil._common.pcputimes):
            results[key] = {"user": val.user,
                            "system": val.system,
                            "children_user": val.children_user,
                            "children_system": val.children_system}

        elif isinstance(val, psutil._common.pctxsw):
            results[key] = {"voluntary": val.voluntary,
                            "involuntary":val.involuntary}

        elif isinstance(val, psutil._common.pionice):
            results[key] = {"ioclass":val.ioclass.name,
                            "value": val.value}

        # pfullmem (first above) should cover this
        elif isinstance(val, psutil._pslinux.pmem):
            continue

        elif isinstance(val, psutil._pslinux.pio):
            results[key] = {"read_count": val.read_count,
                            "write_count": val.write_count,
                            "read_bytes": val.read_bytes,
                            "write_bytes": val.write_bytes,
                            "read_chars": val.read_chars,
                            "write_chars": val.write_chars}
        else:
            results[key] = val

    return results

def cpu_task(**kwargs):
    '''Get variables about the cpu of the host. No parameters are required.

       Parameters
       ==========
       skip: an optional list of (comma separated) fields to skip. Can be in
             net_io_counters,net_connections,net_if_address,net_if_stats
    '''
    result = {}

    # A comma separated list of parameters to not include
    skip = kwargs.get('skip', '')
    skip = skip.split(',')

    result['cpu_freq'] = dict(psutil.cpu_freq()._asdict())
    result['cpu_percent'] = psutil.cpu_percent()
    result['cpu_count'] = psutil.cpu_count()
    result['cpu_stats'] = dict(psutil.cpu_stats()._asdict())
    result['cpu_times'] = dict(psutil.cpu_times()._asdict())
    result['cpu_times_percent'] = dict(psutil.cpu_times_percent()._asdict())
    return _filter_result(result, skip)


def python_task(**kwargs):
    '''Get modules, version, etc. about currently running python

       Parameters
       ==========
       skip: an optional list of (comma separated) fields to skip. Can be in
             net_io_counters,net_connections,net_if_address,net_if_stats
    '''
    # A comma separated list of parameters to not include
    skip = kwargs.get('skip', '')
    skip = skip.split(',')

    result = {'modules': list(psutil.os.sys.modules),
              'version': psutil.os.sys.version,
              'path': psutil.os.sys.path,
              'prefix': psutil.os.sys.prefix,
              'executable': psutil.os.sys.executable,
              'copyright': psutil.os.sys.copyright }

    return _filter_result(result, skip)


def system_task(**kwargs):
    '''Get basic system info, unlikely to change.

       Parameters
       ==========
       skip: an optional list of (comma separated) fields to skip. Can be in
             net_io_counters,net_connections,net_if_address,net_if_stats
    '''
    # A comma separated list of parameters to not include
    skip = kwargs.get('skip', '')
    skip = skip.split(',')

    result = {}
    result['platform'] = psutil.os.sys.platform
    result['api_version'] = psutil.os.sys.api_version
    result['maxsize'] = psutil.os.sys.maxsize
    result['bits_per_digit'] = psutil.os.sys.int_info.bits_per_digit
    result['sizeof_digit'] = psutil.os.sys.int_info.sizeof_digit
 
    vinfo = psutil.os.sys.version_info
    result['version_info'] = {'major': vinfo.major,
                              'minor': vinfo.minor,
                              'micro': vinfo.micro,
                              'releaselevel': vinfo.releaselevel,
                              'serial': vinfo.serial}

    result['sep'] = psutil.os.sep
    uname = psutil.os.uname()
    result['uname'] = {'sysname': uname.sysname,
                       'nodename': uname.nodename,
                       'version': uname.version,
                       'release': uname.release,
                       'machine': uname.machine}


    return _filter_result(result, skip)


def memory_task(**kwargs):
    '''Get values for memory of the host. No parameters are required.
    '''

    result = {}
    # gives an object with many fields
    result['virtual_memory'] = dict(psutil.virtual_memory()._asdict())

    return result


def users_task(**kwargs):
    '''Get values for current users
    '''

    result = {'users': []}
    for user in psutil.users():
        result['users'].append(dict(user._asdict()))
    return result


def sensors_task(**kwargs):
    '''Get values from system sensors like fans, temperature, battery
    '''

    # A comma separated list of parameters to not include
    skip = kwargs.get('skip', '')
    skip = skip.split(',')

    result = {}
    result['sensors_temperatures'] = {}
    result['sensors_fans'] = {}

    # battery
    battery = psutil.sensors_battery()
    if battery != None:
        result['sensors_battery'] = {'percent': battery.percent,
                                     'secsleft': str(battery.secsleft),
                                     'power_plugged': battery.power_plugged}

    # fans
    for name, entry in psutil.sensors_fans().items():
        entries = []
        for e in entry:
            item = {'label': e.label,
                    'current': e.current}
            entries.append(item)
        result['sensors_fans'][name] = entries

    # temperature
    for name, entry in psutil.sensors_temperatures().items():
        entries = []
        for e in entry:
           temp = {'label': e.label,
                   'current': e.current,
                   'high': e.high,
                   'critical': e.critical}
           entries.append(temp)
        result['sensors_temperatures'][name] = entries

    return _filter_result(result, skip)



def net_task(**kwargs):
    '''Get values for networking on the host

       Parameters
       ==========
       skip: an optional list of (comma separated) fields to skip. Can be in
             net_io_counters,net_connections,net_if_address,net_if_stats
    '''
    result = {}

    # A comma separated list of parameters to not include
    skip = kwargs.get('skip', '')
    skip = skip.split(',')

    result['net_connections'] = []
    result['net_if_address'] = {}
    result['net_if_stats'] = {}

    for net in psutil.net_connections():
        net_result = {'df': net.fd,
                      'family': str(net.family),
                      'type': str(net.type),
                      'laddr_ip': net.laddr.ip,
                      'laddr_port': net.laddr.port,
                      'raddr': net.raddr,
                      'status': net.status,
                      'pid': net.pid}
        result['net_connections'].append(net_result)

    for name, entry in psutil.net_if_addrs().items():
        entries = []
        for e in entry:
            item = {'family': str(e.family),
                    'address': e.address,
                    'netmask': e.netmask,
                    'broadcast': e.broadcast,
                    'ptp': e.ptp}
            entries.append(item)
        result['net_if_address'][name] = entries

    for name, entry in psutil.net_if_stats().items():
        item = {'isup': entry.isup,
                'duplex': str(entry.duplex),
                'speed': entry.speed,
                'mtu': entry.mtu}
        result['net_if_stats'][name] = item

    netio = psutil.net_io_counters()
    result['net_io_counters'] = {'bytes_sent': netio.bytes_sent,
                                 'bytes_recv': netio.bytes_recv,
                                 'packets_sent': netio.packets_sent,
                                 'packets_recv': netio.packets_recv,
                                 'errin': netio.errin,
                                 'errout': netio.errout,
                                 'dropin': netio.dropin,
                                 'dropout': netio.dropout}

    # Remove those not wanted
    return _filter_result(result, skip)


def disk_task(**kwargs):
    '''Get values for disks on the host

       Parameters
       ==========
       disk_usage: an optional path to get disk usage for.
       skip: an optional list of (comma separated) fields to skip. Can be in
             net_io_counters,net_connections,net_if_address,net_if_stats

    '''
    # A comma separated list of parameters to not include
    skip = kwargs.get('skip', '')
    skip = skip.split(',')
    path = kwargs.get('disk_usage', '/')

    result = {}
    result['disk_to_counters'] = dict(psutil.disk_io_counters()._asdict())
    result['disk_partitions'] = []
    for disk in psutil.disk_partitions():
        disk_result = {'device': disk.device,
                       'mountpoint': disk.mountpoint,
                       'fstype': disk.fstype,
                       'opts': disk.opts}
        result['disk_partitions'].append(disk_result)
    result['disk_usage'] = dict(psutil.disk_usage(path)._asdict())

    # Remove those not wanted
    return _filter_result(result, skip)


def _filter_result(result, skip):
    '''a helper function to filter a dictionary based on a list of keys to 
       skip.
    
       Parameters
       ==========
       result: a dictionary of results
       skip: a list of keys to remove/filter from the result.
    '''
    for key in skip:
        if key in result:
            del result[key]

    return result


def _get_pid(name):
    '''used to get the pid of a process, by name
       
       Parameters
       ==========
       name: the name of the process to get.
    '''
    try:
        pid = check_output(["pidof", name])
        pid = pid.decode('utf-8').strip('\n').split(' ') 
        if len(pid) > 1:
            bot.warning("More than one pid found for %s, using first." % name)
        pid = int(pid[0])

    except CalledProcessError:
        bot.error("%s does not exist." % name)
        pid = None
    return pid
