#!/usr/bin/env python3
"""
VM Readiness Checker
Check if virtual machines are ready and operational
"""

import json
import sys
from datetime import datetime


def load_vm_config(config_file='vm_config.json'):
    """Load VM configuration from JSON file"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        print("Please create a vm_config.json file with your VM details.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{config_file}'")
        sys.exit(1)


def check_vm_readiness(vm_name, vm_config):
    """Check if a VM is ready based on configuration"""
    status = {
        'name': vm_name,
        'ready': True,
        'checks': [],
        'timestamp': datetime.now().isoformat()
    }
    
    # Check if VM has required configuration
    required_fields = ['cpu', 'memory', 'disk']
    for field in required_fields:
        if field not in vm_config:
            status['checks'].append({
                'check': field,
                'status': 'MISSING',
                'message': f'{field} configuration not found'
            })
            status['ready'] = False
        else:
            status['checks'].append({
                'check': field,
                'status': 'OK',
                'value': vm_config[field]
            })
    
    # Check VM status
    if 'status' in vm_config:
        vm_status = vm_config['status'].lower()
        if vm_status == 'running':
            status['checks'].append({
                'check': 'VM Status',
                'status': 'OK',
                'message': 'VM is running'
            })
        elif vm_status == 'stopped':
            status['checks'].append({
                'check': 'VM Status',
                'status': 'ERROR',
                'message': 'VM is stopped'
            })
            status['ready'] = False
        else:
            status['checks'].append({
                'check': 'VM Status',
                'status': 'WARNING',
                'message': f'VM status is {vm_status}'
            })
            status['ready'] = False
    else:
        status['checks'].append({
            'check': 'VM Status',
            'status': 'MISSING',
            'message': 'VM status not configured'
        })
        status['ready'] = False
    
    return status


def print_vm_status(status):
    """Print VM status in a readable format"""
    print(f"\n{'='*60}")
    print(f"VM Readiness Report: {status['name']}")
    print(f"Timestamp: {status['timestamp']}")
    print(f"{'='*60}")
    
    if status['ready']:
        print("✓ VM is READY")
    else:
        print("✗ VM is NOT READY")
    
    print(f"\nChecks:")
    for check in status['checks']:
        check_status = check['status']
        symbol = '✓' if check_status == 'OK' else '✗'
        print(f"  {symbol} {check['check']}: {check_status}", end='')
        if 'value' in check:
            print(f" ({check['value']})", end='')
        if 'message' in check:
            print(f" - {check['message']}", end='')
        print()
    
    print(f"{'='*60}\n")


def main():
    """Main function to check VM readiness"""
    # Load configuration (support command line argument for config file)
    config_file = sys.argv[1] if len(sys.argv) > 1 else 'vm_config.json'
    config = load_vm_config(config_file)
    
    # Check if VMs are defined
    if 'vms' not in config or not config['vms']:
        print("Error: No VMs defined in configuration")
        sys.exit(1)
    
    # Check each VM
    all_ready = True
    for vm_name, vm_config in config['vms'].items():
        status = check_vm_readiness(vm_name, vm_config)
        print_vm_status(status)
        if not status['ready']:
            all_ready = False
    
    # Exit with appropriate code
    if all_ready:
        print("All VMs are ready! ✓")
        sys.exit(0)
    else:
        print("Some VMs are not ready. Please check the status above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
