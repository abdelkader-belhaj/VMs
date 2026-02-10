#!/usr/bin/env python3
"""
Vérificateur d'état de préparation des VMs
Vérifie si les machines virtuelles sont prêtes et opérationnelles
"""

import json
import sys
from datetime import datetime


def load_vm_config(config_file='vm_config.json'):
    """Charger la configuration des VMs depuis un fichier JSON"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erreur: Fichier de configuration '{config_file}' introuvable.")
        print("Veuillez créer un fichier vm_config.json avec les détails de vos VMs.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Erreur: JSON invalide dans '{config_file}'")
        sys.exit(1)


def check_vm_readiness(vm_name, vm_config):
    """Vérifier si une VM est prête selon sa configuration"""
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
                'status': 'MANQUANT',
                'message': f'Configuration {field} introuvable'
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
                'check': 'Statut VM',
                'status': 'OK',
                'message': "La VM est en cours d'exécution"
            })
        elif vm_status == 'stopped':
            status['checks'].append({
                'check': 'Statut VM',
                'status': 'ERREUR',
                'message': 'La VM est arrêtée'
            })
            status['ready'] = False
        else:
            status['checks'].append({
                'check': 'Statut VM',
                'status': 'ATTENTION',
                'message': f'Le statut de la VM est {vm_status}'
            })
            status['ready'] = False
    else:
        status['checks'].append({
            'check': 'Statut VM',
            'status': 'MANQUANT',
            'message': 'Statut VM non configuré'
        })
        status['ready'] = False
    
    return status


def print_vm_status(status):
    """Afficher le statut de la VM dans un format lisible"""
    print(f"\n{'='*60}")
    print(f"Rapport d'état de préparation VM: {status['name']}")
    print(f"Horodatage: {status['timestamp']}")
    print(f"{'='*60}")
    
    if status['ready']:
        print("✓ La VM est PRÊTE")
    else:
        print("✗ La VM n'est PAS PRÊTE")
    
    print(f"\nVérifications:")
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
    """Fonction principale pour vérifier l'état de préparation des VMs"""
    # Load configuration (support command line argument for config file)
    config_file = sys.argv[1] if len(sys.argv) > 1 else 'vm_config.json'
    config = load_vm_config(config_file)
    
    # Check if VMs are defined
    if 'vms' not in config or not config['vms']:
        print("Erreur: Aucune VM définie dans la configuration")
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
        print("Toutes les VMs sont prêtes! ✓")
        sys.exit(0)
    else:
        print("Certaines VMs ne sont pas prêtes. Veuillez vérifier le statut ci-dessus.")
        sys.exit(1)


if __name__ == '__main__':
    main()
