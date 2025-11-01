# VMs - Virtual Machine Readiness Checker

A simple tool to check if your virtual machines are ready and operational.

## Description

This repository provides a VM readiness checker that validates if your virtual machines are properly configured and running. It checks various aspects of VM configuration including status, CPU, memory, and disk allocation.

## Quick Start

### Prerequisites

- Python 3.6 or higher

### Usage

1. Configure your VMs in `vm_config.json`:

```json
{
  "vms": {
    "vm-name": {
      "status": "running",
      "cpu": "4 cores",
      "memory": "8GB",
      "disk": "100GB",
      "ip": "192.168.1.100",
      "os": "Ubuntu 22.04"
    }
  }
}
```

2. Run the readiness check:

```bash
python3 check_vm_status.py
```

### Configuration Fields

- **status**: VM status (running, stopped, etc.)
- **cpu**: CPU allocation (e.g., "4 cores")
- **memory**: Memory allocation (e.g., "8GB")
- **disk**: Disk allocation (e.g., "100GB")
- **ip**: (Optional) VM IP address
- **os**: (Optional) Operating system

## Output

The script will check each VM and report:
- ✓ VM is READY - All checks passed
- ✗ VM is NOT READY - Some checks failed

Example output:
```
============================================================
VM Readiness Report: vm-01
Timestamp: 2025-11-01T12:00:00.000000
============================================================
✓ VM is READY

Checks:
  ✓ cpu: OK (4 cores)
  ✓ memory: OK (8GB)
  ✓ disk: OK (100GB)
  ✓ VM Status: OK - VM is running
============================================================
```

## Exit Codes

- `0`: All VMs are ready
- `1`: One or more VMs are not ready or error occurred

## License

MIT