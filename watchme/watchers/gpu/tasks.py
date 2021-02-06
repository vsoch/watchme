__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020-2021, Vanessa Sochat"
__license__ = "MPL 2.0"

from watchme.utils import get_watchme_env
from .pynvml import nvmlInit, nvmlShutdown
from watchme.watchers.gpu import pynvml


def gpu_task(**kwargs):
    """Get variables about the gpu of the host. No parameters are required.
    We've already instantited the Task object and have checked that
    the calling host has nvml GPU

    Parameters
    ==========
    skip: an optional list of (comma separated) fields to skip. Can be in
          net_io_counters,net_connections,net_if_address,net_if_stats
    """
    nvmlInit()

    results = {}

    # A comma separated list of parameters to not include
    skip = kwargs.get("skip", "")
    skip = skip.split(",")

    # Run through high level metrics
    funcs = {
        "nvml_driver_version": pynvml.nvmlSystemGetDriverVersion,
        "nvml_system_nvml_version": pynvml.nvmlSystemGetNVMLVersion,
        "nvml_deviceCount": pynvml.nvmlDeviceGetCount,
        "nvml_hic_version": pynvml.nvmlSystemGetHicVersion,
        "nvml_unit_count": pynvml.nvmlUnitGetCount,
    }

    for name, func in funcs.items():
        try:
            results[name] = func()
        except:
            nvmlInit()

    # Look at individual devices
    funcs = {
        "nvml_device_board_id": pynvml.nvmlDeviceGetBoardId,
        "nvml_device_multi_gpu_board": pynvml.nvmlDeviceGetMultiGpuBoard,
        "nvml_device_brand": pynvml.nvmlDeviceGetBrand,
        "nvml_device_serial": pynvml.nvmlDeviceGetSerial,
        "nvml_device_set_cpu_affinite": pynvml.nvmlDeviceSetCpuAffinity,
        "nvml_device_minor_number": pynvml.nvmlDeviceGetMinorNumber,
        "nvml_device_uuid": pynvml.nvmlDeviceGetUUID,
        "nvml_device_inforom_version": pynvml.nvmlDeviceGetInforomImageVersion,
        "nvml_device_inforam_checksum": pynvml.nvmlDeviceGetInforomConfigurationChecksum,
        "nvml_device_display_mode": pynvml.nvmlDeviceGetDisplayMode,
        "nvml_device_display_active": pynvml.nvmlDeviceGetDisplayActive,
        "nvml_device_persistence_mode": pynvml.nvmlDeviceGetPersistenceMode,
        "nvml_device_supported_memory_clocks": pynvml.nvmlDeviceGetSupportedMemoryClocks,
        "nvml_device_fan_speed": pynvml.nvmlDeviceGetFanSpeed,
        "nvml_device_performance_state": pynvml.nvmlDeviceGetPerformanceState,
        "nvml_device_management_mode": pynvml.nvmlDeviceGetPowerManagementMode,
        "nvml_device_power_managerment_mode": pynvml.nvmlDeviceGetPowerManagementMode,
        "nvml_device_power_management_limit": pynvml.nvmlDeviceGetPowerManagementLimit,
        "nvml_device_power_management_limit_constraints": pynvml.nvmlDeviceGetPowerManagementLimitConstraints,
        "nvml_device_power_management_default_limit": pynvml.nvmlDeviceGetPowerManagementDefaultLimit,
        "nvml_device_enforced_power_limit": pynvml.nvmlDeviceGetEnforcedPowerLimit,
        "nvml_device_power_usage": pynvml.nvmlDeviceGetPowerUsage,
        "nvml_device_gpu_operation_mode": pynvml.nvmlDeviceGetGpuOperationMode,
        "nvml_device_current_operation_mode": pynvml.nvmlDeviceGetCurrentGpuOperationMode,
        "nvml_device_pending_gpu_operation_mode": pynvml.nvmlDeviceGetPendingGpuOperationMode,
        "nvml_device_memory_info": pynvml.nvmlDeviceGetMemoryInfo,
        "nvml_device_bar1_memory_info": pynvml.nvmlDeviceGetBAR1MemoryInfo,
        "nvml_device_compute_mode": pynvml.nvmlDeviceGetComputeMode,
        "nvml_device_ecc_mode": pynvml.nvmlDeviceGetEccMode,
        "nvml_device_current_ecc_mode": pynvml.nvmlDeviceGetCurrentEccMode,
        "nvml_device_pending_ecc_mode": pynvml.nvmlDeviceGetPendingEccMode,
        "nvml_device_utilization_rates": pynvml.nvmlDeviceGetUtilizationRates,
        "nvml_device_encoder_utilization": pynvml.nvmlDeviceGetEncoderUtilization,
        "nvml_device_decoder_utilization": pynvml.nvmlDeviceGetDecoderUtilization,
        "nvml_device_pci_replay_counter": pynvml.nvmlDeviceGetPcieReplayCounter,
        "nvml_device_driver_model": pynvml.nvmlDeviceGetDriverModel,
        "nvml_device_current_driver_model": pynvml.nvmlDeviceGetCurrentDriverModel,
        "nvml_device_pending_driver_model": pynvml.nvmlDeviceGetPendingDriverModel,
        "nvml_device_vbios_version": pynvml.nvmlDeviceGetVbiosVersion,
        "nvml_device_compute_running_processes": pynvml.nvmlDeviceGetComputeRunningProcesses,
        "nvml_device_grapics_running_processes": pynvml.nvmlDeviceGetGraphicsRunningProcesses,
        "nvml_device_auto_boosted_clocks_enabled": pynvml.nvmlDeviceGetAutoBoostedClocksEnabled,
        "nvml_device_supported_event_types": pynvml.nvmlDeviceGetSupportedEventTypes,
        "nvml_device_current_pcie_link_generation": pynvml.nvmlDeviceGetCurrPcieLinkGeneration,
        "nvml_device_max_pcie_link_generation": pynvml.nvmlDeviceGetMaxPcieLinkGeneration,
        "nvml_device_curr_pcie_link_width": pynvml.nvmlDeviceGetCurrPcieLinkWidth,
        "nvml_device_max_pcie_link_width": pynvml.nvmlDeviceGetMaxPcieLinkWidth,
        "nvml_device_supported_clocks_throttle_reasons": pynvml.nvmlDeviceGetSupportedClocksThrottleReasons,
        "nvml_device_current_clocks_throttle_reasons": pynvml.nvmlDeviceGetCurrentClocksThrottleReasons,
        "nvml_device_index": pynvml.nvmlDeviceGetIndex,
        "nvml_device_accounting_mode": pynvml.nvmlDeviceGetAccountingMode,
        "nvml_device_accounting_pids": pynvml.nvmlDeviceGetAccountingPids,
        "nvml_device_accounting_buffer_size": pynvml.nvmlDeviceGetAccountingBufferSize,
    }

    # Functions that need additional args
    # nvmlDeviceGetCpuAffinity(handle, cpuSetSize):
    # nvmlDeviceGetInforomVersion(handle, infoRomObject)
    # nvmlDeviceGetClockInfo(handle, type)
    # nvmlDeviceGetMaxClockInfo(handle, type)
    # nvmlDeviceGetApplicationsClock(handle, type)
    # nvmlDeviceGetDefaultApplicationsClock(handle, type)
    # nvmlDeviceGetSupportedGraphicsClocks(handle, memoryClockMHz)
    # nvmlDeviceGetTemperature(handle, sensor)
    # nvmlDeviceGetTemperatureThreshold(handle, threshold)
    # nvmlDeviceGetTotalEccErrors(handle, errorType, counterType)
    # nvmlDeviceGetMemoryErrorCounter(handle, errorType, counterType, locationType)
    # nvmlDeviceRegisterEvents(handle, eventTypes, eventSet):
    # nvmlEventSetWait(eventSet, timeoutms):
    # nvmlDeviceOnSameBoard(handle1, handle2):
    # nvmlDeviceGetAccountingStats(handle, pid):

    # Setting functions that return None
    # nvmlDeviceSetCpuAffinity(handle)
    # nvmlDeviceClearCpuAffinity(handle)
    # nvmlDeviceValidateInforom(handle)
    # nvmlUnitSetLedState(unit, color):
    # nvmlDeviceSetPersistenceMode(handle, mode):
    # nvmlDeviceSetComputeMode(handle, mode):
    # nvmlDeviceSetEccMode(handle, mode):
    # nvmlDeviceClearEccErrorCounts(handle, counterType):
    # nvmlDeviceSetDriverModel(handle, model):
    # nvmlDeviceSetAutoBoostedClocksEnabled(handle, enabled):
    # nvmlDeviceSetDefaultAutoBoostedClocksEnabled(handle, enabled, flags):
    # nvmlDeviceSetApplicationsClocks(handle, maxMemClockMHz, maxGraphicsClockMHz):
    # nvmlDeviceResetApplicationsClocks(handle):
    # nvmlDeviceSetPowerManagementLimit(handle, limit):
    # nvmlDeviceSetGpuOperationMode(handle, mode):
    # nvmlDeviceSetAccountingMode(handle, mode):
    # nvmlDeviceClearAccountingPids(handle):

    device_count = results["nvml_deviceCount"]

    devices = {}
    for i in range(device_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        name = pynvml.nvmlDeviceGetName(handle)
        devices[name] = {}
        for key, func in funcs.items():
            try:

                result = func(handle)

                # Special parsing of the result depending on the type
                if isinstance(result, map):
                    result = list(result)

                if key == "nvml_device_bar1_memory_info":
                    result = {
                        "bar1Free": result.bar1Free,
                        "bar1Total": result.bar1Total,
                        "bar1Used": result.bar1Used,
                    }

                if key == "nvml_device_utilization_rates":
                    result = {"gpu": result.gpu, "memory": result.memory}

                elif key == "nvml_device_memory_info":
                    result = {
                        "free": result.free,
                        "total": result.total,
                        "used": result.used,
                    }

                devices[name][key] = result
            except:
                nvmlInit()

    nvmlShutdown()

    results["devices"] = devices
    return _filter_result(results, skip)


def _filter_result(results, skip):
    """a helper function to filter a dictionary based on a list of keys to
    skip. We also add variables from the environment.

    Parameters
    ==========
    results: a dictionary of results
    skip: a list of keys to remove/filter from the result.
    """

    # Add any environment variables prefixed wit WATCHMEENV_
    environ = get_watchme_env()
    results.update(environ)

    for key in skip:
        if key in results:
            del results[key]

    return results
