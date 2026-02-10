# VMs - Vérificateur d'état de préparation des machines virtuelles

Un outil simple pour vérifier si vos machines virtuelles sont prêtes et opérationnelles.

## Description

Ce dépôt fournit un vérificateur d'état de préparation des VMs qui valide si vos machines virtuelles sont correctement configurées et en cours d'exécution. Il vérifie divers aspects de la configuration des VMs, notamment le statut, le CPU, la mémoire et l'allocation du disque.

## Démarrage rapide

### Prérequis

- Python 3.6 ou supérieur

### Utilisation

1. Configurez vos VMs dans `vm_config.json`:

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

2. Exécutez la vérification d'état:

```bash
python3 check_vm_status.py
```

### Champs de configuration

- **status**: Statut de la VM (running, stopped, etc.)
- **cpu**: Allocation CPU (ex: "4 cores")
- **memory**: Allocation mémoire (ex: "8GB")
- **disk**: Allocation disque (ex: "100GB")
- **ip**: (Optionnel) Adresse IP de la VM
- **os**: (Optionnel) Système d'exploitation

## Sortie

Le script vérifie chaque VM et rapporte:
- ✓ La VM est PRÊTE - Toutes les vérifications sont réussies
- ✗ La VM n'est PAS PRÊTE - Certaines vérifications ont échoué

Exemple de sortie:
```
============================================================
Rapport d'état de préparation VM: vm-01
Horodatage: 2025-11-01T12:00:00.000000
============================================================
✓ La VM est PRÊTE

Vérifications:
  ✓ cpu: OK (4 cores)
  ✓ memory: OK (8GB)
  ✓ disk: OK (100GB)
  ✓ Statut VM: OK - La VM est en cours d'exécution
============================================================
```

## Codes de sortie

- `0`: Toutes les VMs sont prêtes
- `1`: Une ou plusieurs VMs ne sont pas prêtes ou une erreur s'est produite

## Licence

MIT