# 🏢 Futurisys ML Deploy - Prédiction de Consommation Énergétique

![CI](https://github.com/DagueG/Model_Machine_Learning/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.119.1-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Une **API FastAPI** pour le déploiement et la prédiction d'un modèle de Machine Learning capable de prédire la consommation énergétique des bâtiments en temps réel.

**🌐 API Déployée:** https://huggingface.co/spaces/DagueGG/model-machine-learning

---

## 📋 Table des Matières

- [Objectif du Projet](#objectif-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure du Projet](#structure-du-projet)
- [Tests et Couverture](#tests-et-couverture)
- [API Documentation](#api-documentation)
- [Déploiement](#déploiement)
- [CI/CD Pipeline](#cicd-pipeline)
- [Contribution](#contribution)
- [Livrables](#livrables)

---

## 🎯 Objectif du Projet

Déployer un modèle de Machine Learning (**Random Forest Regressor**) entraîné pour prédire la consommation énergétique des bâtiments. Le projet démontre :

✅ Une **API REST** moderne et documentée  
✅ Une **base de données PostgreSQL** pour stocker prédictions et historique  
✅ Une **couverture de tests** complète avec pytest  
✅ Un **pipeline CI/CD** avec GitHub Actions  
✅ Un **déploiement automatisé** sur Hugging Face Spaces  
✅ Une gestion des versions et des branches structurée  

---

## ⚡ Fonctionnalités

### 🔌 Endpoints API

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Endpoint racine avec infos de l'API |
| `/health` | GET | Vérification de santé de l'API et du modèle |
| `/docs` | GET | Documentation Swagger interactive |
| `/redoc` | GET | Documentation ReDoc interactive |
| `/api/p3/predict` | POST | Prédiction de consommation énergétique |
| `/api/p3/prediction/{id}` | GET | Récupération d'une prédiction spécifique |
| `/api/p3/predictions` | GET | Historique des prédictions |
| `/api/p3/dataset` | GET | Accès à l'historique des données |

### 🤖 Modèle ML

- **Type:** Random Forest Regressor
- **Features:** 12 variables incluant type de bâtiment, zone géographique, latitude/longitude
- **Performance:** Entraîné et validé sur données réelles

### 💾 Persistance

- **Base de données:** PostgreSQL 16
- **Tables:** `energy_dataset`, `energy_prediction`
- **ORM:** SQLAlchemy
- **Migrations:** Schéma créé automatiquement

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│         Hugging Face Spaces (Production)         │
│         https://huggingface.co/spaces/...        │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │   FastAPI App      │
        │  (Uvicorn Server)  │
        └────────┬───────────┘
                 │
      ┌──────────┴──────────┐
      ▼                     ▼
  ┌────────┐         ┌──────────────┐
  │ Model  │         │ PostgreSQL   │
  │ (.pkl) │         │   (Database) │
  └────────┘         └──────────────┘
      │                     │
      └──────────┬──────────┘
                 ▼
      ┌──────────────────────┐
      │  GitHub (Versioning) │
      │  & GitHub Actions    │
      └──────────────────────┘
```

---

## 📦 Installation

### 1. Prérequis

- **Python** ≥ 3.11
- **[uv](https://docs.astral.sh/uv/)** - Gestionnaire de paquets moderne
- **Docker & Docker Compose** - Pour PostgreSQL local
- **Git** - Contrôle de version

### 2. Cloner le Dépôt

```bash
git clone https://github.com/DagueG/Model_Machine_Learning.git
cd Model_Machine_Learning
```

### 3. Installer les Dépendances

```bash
# Initialiser l'environnement virtuel
uv sync

# Activer l'environnement (optionnel, uv run le fait automatiquement)
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

### 4. Configurer la Base de Données

```bash
# Démarrer PostgreSQL avec Docker
docker-compose up -d

# Initialiser le schéma
uv run python create_db.py

# Vérifier le statut
docker-compose ps
```

### 5. Télécharger le Modèle

Le modèle ML est stocké dans `models/model_p3.joblib`. 

- **En local:** Le fichier doit être présent dans le répertoire `models/`
- **En production (HF Spaces):** Téléchargé automatiquement depuis GitHub Releases

---

## ⚙️ Configuration

### Variables d'Environnement

Créez un fichier `.env` à la racine du projet (template : `.env.example`) :

```env
# Base de Données
DATABASE_URL=postgresql://futurisys_user:futurisys_password@localhost:5432/futurisys_db

# API Configuration
API_TITLE=Futurisys ML API
API_VERSION=0.1.0
LOG_LEVEL=INFO
```

### Structure de Configuration

| Variable | Description | Valeur par Défaut |
|----------|-------------|-------------------|
| `DATABASE_URL` | Connexion PostgreSQL | `postgresql://...@localhost:5432/...` |
| `API_TITLE` | Titre de l'API | `Futurisys ML API` |
| `API_VERSION` | Version API | `0.1.0` |
| `LOG_LEVEL` | Niveau de log | `INFO` |

---

## 🚀 Utilisation

### Démarrer Localement

```bash
# Terminal 1 : PostgreSQL
docker-compose up -d

# Terminal 2 : Serveur FastAPI
uv run uvicorn app.main:app --reload --port 8000
```

### Accès à l'API

- **API Root:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Exemple de Requête Predict

```bash
curl -X POST "http://localhost:8000/api/p3/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "BuildingType": "Office",
    "PrimaryPropertyType": "Office",
    "ZipCode": 75001,
    "CouncilDistrictCode": 1,
    "Neighborhood": "Marais",
    "Latitude": 48.8624,
    "Longitude": 2.3522,
    "YearBuilt": 1990,
    "NumberofFloors": 5,
    "PropertyGFABuildings": 5000,
    "SiteEnergyUseIntensity": 150.5,
    "SourceEnergyUseIntensity": 250.3
  }'
```

### Exemple de Réponse

```json
{
  "prediction_id": 1,
  "predicted_energy_consumption": 1245.75,
  "building_type": "Office",
  "created_at": "2025-01-12T15:30:45.123456"
}
```

---

## 📁 Structure du Projet

```
Model_Machine_Learning/
├── 📁 app/
│   ├── main.py                      # Application FastAPI + endpoints
│   ├── models.py                    # Modèles SQLAlchemy (DB)
│   ├── 📁 core/
│   │   ├── __init__.py
│   │   └── database.py              # Configuration SQLAlchemy
│   ├── 📁 schemas/
│   │   └── p3_request.py            # Schémas Pydantic (validation)
│   └── 📁 services/
│       └── p3_model.py              # Service ML (chargement/prédiction)
│
├── 📁 tests/
│   ├── conftest.py                  # Fixtures pytest
│   ├── 📁 unit/
│   │   └── test_health.py           # Tests unitaires
│   └── 📁 integration/
│       ├── test_p3_dataset.py       # Tests dataset
│       └── test_p3_predict.py       # Tests prédiction + DB
│
├── 📁 models/
│   └── model_p3.joblib              # Modèle ML sérialisé
│
├── 📁 data/
│   ├── X_test.csv                   # Features test
│   └── y_test.csv                   # Labels test
│
├── 📁 .github/
│   └── 📁 workflows/
│       └── ci.yml                   # Pipeline CI/CD GitHub Actions
│
├── 📄 pyproject.toml                # Dépendances + config projet
├── 📄 uv.lock                       # Lock file (dépendances figées)
├── 📄 docker-compose.yml            # Config PostgreSQL
├── 📄 Dockerfile                    # Image Docker pour déploiement
├── 📄 create_db.py                  # Initialisation base de données
├── 📄 .env.example                  # Template variables d'env
├── 📄 .gitignore                    # Fichiers ignorés Git
└── 📄 README.md                     # Ce fichier
```

---

## 🧪 Tests et Couverture

### Exécuter les Tests

```bash
# Tous les tests avec rapport de couverture
uv run pytest -v --cov=app --cov-report=term-missing

# Tests spécifiques
uv run pytest tests/unit/ -v                    # Unitaires
uv run pytest tests/integration/ -v             # Intégration

# Avec rapport HTML
uv run pytest --cov=app --cov-report=html
# Ouvrir htmlcov/index.html
```

### Résumé des Tests

| Type | Fichier | Tests | Coverage |
|------|---------|-------|----------|
| **Unitaires** | `test_health.py` | Health check, model loading | ✅ |
| **Intégration** | `test_p3_dataset.py` | Dataset CRUD, validation | ✅ |
| **Intégration** | `test_p3_predict.py` | Prédiction, DB persistence | ✅ |

### Configuration Pytest

Via `pyproject.toml`:
```toml
[tool.pytest.ini_options]
addopts = "-v --cov=app --cov-report=term-missing"
testpaths = ["tests"]
pythonpath = ["."]
```

---

## 📚 API Documentation

### Swagger UI Interactif

Accédez à **http://localhost:8000/docs** pour :
- Tester les endpoints directement
- Voir les schémas de requête/réponse
- Consulter les codes de réponse HTTP

### Schémas Principaux

#### `EnergyRequest` (POST /api/p3/predict)

```json
{
  "BuildingType": "string (enum)",
  "PrimaryPropertyType": "string",
  "ZipCode": "integer",
  "CouncilDistrictCode": "integer",
  "Neighborhood": "string",
  "Latitude": "float",
  "Longitude": "float",
  "YearBuilt": "integer",
  "NumberofFloors": "integer",
  "PropertyGFABuildings": "float",
  "SiteEnergyUseIntensity": "float",
  "SourceEnergyUseIntensity": "float"
}
```

#### `PredictionResponse`

```json
{
  "prediction_id": "integer",
  "predicted_energy_consumption": "float",
  "building_type": "string",
  "created_at": "datetime"
}
```

---

## 🌐 Déploiement

### Déploiement sur Hugging Face Spaces

Le projet est **automatiquement déployé** sur [Hugging Face Spaces](https://huggingface.co/spaces/DagueGG/model-machine-learning) à chaque push sur `main`.

#### Configuration HF Spaces

1. **Dockerfile:** Spécifie l'image et les commandes de démarrage
2. **Port:** L'API écoute sur le port `7860` (standard HF Spaces)
3. **Modèle:** Téléchargé depuis GitHub Releases au démarrage
4. **Base de données:** SQLite local (persistant via volumes HF)

#### Logs de Déploiement

Consultables directement dans HF Spaces console.

---

## 🔄 CI/CD Pipeline

### GitHub Actions (`.github/workflows/ci.yml`)

Le pipeline automatise :

```yaml
name: CI - Tests & Deployment

on:
  push:
    branches: [main, "feature/**"]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - Checkout du code
      - Installation de uv
      - Synchronisation des dépendances (uv sync --frozen)
      - Exécution des tests avec couverture (pytest)
      - Upload du modèle vers HF (si main et succès)
```

### Secrets Requis

Configure dans **Settings > Secrets and variables > Actions** :

| Secret | Description | Où l'obtenir |
|--------|-------------|--------------|
| `HF_TOKEN` | Token Hugging Face | [HF Settings](https://huggingface.co/settings/tokens) |

### Environnements

- **feature/\*:** Tests seulement
- **main:** Tests + Déploiement HF

---

## 📊 Versioning & Git

### Convention des Branches

```
main                           # Production
├── feature/project-structure   # Nouvelles features
├── feature/ci-setup            # Configuration CI/CD
├── feature/env-setup           # Configuration env
├── feature/test-protection     # Tests & validation
└── feature/hf-spaces-deployment # Déploiement HF
```

### Convention des Commits

```
TYPE: description détaillée

Types:
  ADD:    Nouvelle fonctionnalité
  FIX:    Correction de bug
  UPD:    Mise à jour existante
  MERGE:  Merge / Résolution de conflit
  DOCS:   Documentation
  PERF:   Performance
  REFACTOR: Restructuration de code
```

### Tags

- `v0.0.0` - Initiale
- `v0.1.0` - Version alpha
- `v1.0.0-model` - Modèle ML v1.0

---

## 🔧 Maintenance et Troubleshooting

### Problèmes Courants

#### ❌ `InconsistentVersionWarning` avec scikit-learn

**Cause:** Mismatch entre version de scikit-learn d'entraînement et de déploiement

**Solution:**
```bash
# Assurez-vous que pyproject.toml spécifie:
scikit-learn>=1.5.2,<1.6  # Version d'entraînement
```

#### ❌ Connexion PostgreSQL échoue

```bash
# Vérifier le conteneur
docker-compose ps

# Redémarrer
docker-compose down && docker-compose up -d

# Logs
docker-compose logs postgres
```

#### ❌ Tests échouent localement

```bash
# Vider cache pytest
rm -rf .pytest_cache/

# Réinstaller dépendances
uv sync

# Réexécuter
uv run pytest -v
```

---

## 📋 Livrables du Projet

Selon les critères OpenClassrooms, ce projet livre :

### ✅ Dépôt Git Structuré
- ✔️ Code source complet en contrôle de version
- ✔️ Historique de commits claire (`git log`)
- ✔️ Branches feature avec convention
- ✔️ Tags de versioning (v0.0.0, v0.1.0, v1.0.0-model)

### ✅ Dépendances & Configuration
- ✔️ `pyproject.toml` avec dépendances complètes
- ✔️ `uv.lock` pour reproductibilité
- ✔️ `.env.example` avec variables requises
- ✔️ Dockerfile pour containerisation

### ✅ API Fonctionnelle & Documentée
- ✔️ Endpoints REST documentés
- ✔️ Swagger UI interactive
- ✔️ Déployée sur [HF Spaces](https://huggingface.co/spaces/DagueGG/model-machine-learning)
- ✔️ Health check & monitoring

### ✅ Tests & Couverture
- ✔️ Tests unitaires & intégration (Pytest)
- ✔️ `conftest.py` avec fixtures
- ✔️ Rapport de couverture (`--cov-report`)
- ✔️ CI automatisé dans GitHub Actions

### ✅ Base de Données PostgreSQL
- ✔️ Schéma SQLAlchemy (models.py)
- ✔️ Tables: `energy_dataset`, `energy_prediction`
- ✔️ Configuration `docker-compose.yml`
- ✔️ Script `create_db.py` d'initialisation

### ✅ Pipeline CI/CD
- ✔️ GitHub Actions (`.github/workflows/ci.yml`)
- ✔️ Tests automatisés à chaque push
- ✔️ Déploiement automatisé sur HF Spaces
- ✔️ Secrets management (HF_TOKEN)

### ✅ Documentation Complète
- ✔️ README détaillé (ce fichier)
- ✔️ Instructions d'installation
- ✔️ Exemples d'utilisation
- ✔️ Architecture et structure expliquées

---

## 🤝 Contribution

Les contributions sont bienvenues ! Merci de :

1. **Fork** le projet
2. **Créer une branche feature** : `git checkout -b feature/ma-feature`
3. **Committer** avec convention : `git commit -m "ADD: description"`
4. **Pusher** : `git push origin feature/ma-feature`
5. **Créer une Pull Request** sur `main`

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir [LICENSE](LICENSE) pour les détails.

---

## 📞 Support & Contact

- **Issues GitHub:** [DagueG/Model_Machine_Learning/issues](https://github.com/DagueG/Model_Machine_Learning/issues)
- **HF Space:** [DagueGG/model-machine-learning](https://huggingface.co/spaces/DagueGG/model-machine-learning)

---

## 📈 Roadmap Futur

- [ ] Dashboard de monitoring des prédictions
- [ ] Versioning du modèle ML
- [ ] Webhooks pour notifications
- [ ] Rate limiting & authentication
- [ ] Cache Redis pour optimisation
- [ ] Logs centralisés (ELK/Grafana)

---

**Dernière mise à jour:** Février 2026  
**Statut:** ✅ Production  
**Maintenance:** Active
