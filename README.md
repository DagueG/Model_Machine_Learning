![CI](https://github.com/DagueG/Model_Machine_Learning/actions/workflows/ci.yml/badge.svg)
# Futurisys ML Deploy🚀

## 👇 Objectif
Déployer un modèle de ML derrière une API FastAPI.

## Conventions de commit
- ADD: ajout de fonctionnalité/fichier
- FIX: correction de bug/problème
- DOCS: documentation
- DEL: suppression volontaire

### Installation

```bash
# Créer l'environnement
uv init --python 3.11

# Installer les dépendances
uv sync
```
## 🚀 Lancer le projet localement

### Démarrer le serveur FastAPI
```bash
uv run uvicorn app.main:app --reload
```