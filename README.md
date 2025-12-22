![CI](https://github.com/DagueG/Model_Machine_Learning/actions/workflows/ci.yml/badge.svg)

# Futurisys ML Deploy 🚀

Une API FastAPI pour le déploiement et la prédiction d'un modèle de Machine Learning capable de prédire la consommation énergétique des bâtiments.

## 📋 Objectif
Déployer un modèle de ML (Random Forest) derrière une API FastAPI pour fournir des prédictions en temps réel sur la consommation énergétique des propriétés.
---

## 📁 Structure du Projet

```
Model_Machine_Learning/
├── app/
│   ├── main.py                 # Application FastAPI principale avec tous les endpoints
│   ├── models.py               # Modèles SQLAlchemy pour la base de données
│   ├── schemas/
│   │   └── p3_request.py       # Modèles Pydantic pour la validation des requêtes
│   ├── services/
│   │   └── p3_model.py         # Classe de service pour charger et utiliser le modèle ML
│   ├── core/
│   │   ├── database.py         # Configuration SQLAlchemy et session management
│   │   └── __init__.py
│   └── __pycache__/
├── models/
│   └── model_p3.joblib         # Modèle ML sérialisé (Random Forest)
├── tests/
│   ├── unit/
│   │   └── test_health.py      # Tests unitaires pour l'endpoint /health
│   ├── integration/
│   │   └── test_p3_predict.py  # Tests d'intégration pour l'endpoint /predict et DB
│   └── __pycache__/
├── docker-compose.yml          # Configuration PostgreSQL avec Docker
├── create_db.py                # Script d'initialisation de la base de données
├── .env                        # Variables d'environnement (local)
├── .env.example                # Template des variables d'environnement
├── pyproject.toml              # Configuration du projet et dépendances
└── README.md                   # Documentation du projet
```

---

## 🛠️ Installation

### Prérequis
- Python >= 3.11
- [uv](https://docs.astral.sh/uv/) (gestionnaire de paquets Python)
- Docker & Docker Compose (pour PostgreSQL)

### Étapes d'installation

```bash
# 1. Initialiser l'environnement virtuel avec Python 3.11
uv init --python 3.11

# 2. Installer toutes les dépendances du projet
uv sync

# 3. Copier le fichier .env
cp .env.example .env

# 4. Démarrer PostgreSQL avec Docker
docker-compose up -d

# 5. Initialiser la base de données
uv run python create_db.py
```

### Vérification du statut PostgreSQL
```bash
docker-compose ps
```

### Arrêter PostgreSQL
```bash
docker-compose down
```

---

## 🚀 Lancer le Projet Localement

### Démarrer le serveur FastAPI
```bash
uv run uvicorn app.main:app --reload
```

Le serveur sera accessible sur `http://localhost:8000`

### Accès à la documentation interactive
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 Endpoints disponibles

### 1. **Vérification de santé**
```http
GET /health
```

**Réponse réussie (200)**:
```json
{
  "status": "ok",
  "message": "API en ligne 🚀"
}
```

---

### 2. **Prédiction de consommation énergétique**
```http
POST /api/p3/predict
```

**Payload (application/json)**:
```json
{
  "BuildingType": "Commercial",
  "PrimaryPropertyType": "Office",
  "ZipCode": 98101,
  "CouncilDistrictCode": 1,
  "Neighborhood": "Downtown",
  "Latitude": 47.6062,
  "Longitude": -122.3321,
  "YearBuilt": 2005,
  "NumberofBuildings": 1,
  "NumberofFloors": 10,
  "PropertyGFATotal": 50000.0,
  "PropertyGFAParking": 5000.0,
  "PropertyGFABuildings": 45000.0,
  "ListOfAllPropertyUseTypes": "Office",
  "LargestPropertyUseType": "Office",
  "LargestPropertyUseTypeGFA": 45000.0,
  "SecondLargestPropertyUseType": null,
  "SecondLargestPropertyUseTypeGFA": null,
  "ThirdLargestPropertyUseType": null,
  "ThirdLargestPropertyUseTypeGFA": null,
  "YearsENERGYSTARCertified": 5,
  "Outlier": "No",
  "BuildingAge": 19.0,
  "SurfacePerFloor": 4500.0,
  "IsMultiUse": false,
  "LatZone": 47,
  "LonZone": 122
}
```

**Réponse réussie (200)**:
```json
{
  "prediction": 1250.5
}
```

---

### 3. **Récupérer l'historique des prédictions**
```http
GET /api/p3/history?skip=0&limit=100
```

**Paramètres de query**:
- `skip` (optional): Nombre d'enregistrements à ignorer (défaut: 0)
- `limit` (optional): Nombre maximal d'enregistrements à retourner (défaut: 100)

**Réponse réussie (200)**:
```json
{
  "total": 42,
  "predictions": [
    {
      "id": 1,
      "prediction": 1250.5,
      "building_type": "Commercial",
      "created_at": "2025-12-10T12:30:45.123456"
    },
    ...
  ]
}
```

---

### 4. **Récupérer une prédiction spécifique**
```http
GET /api/p3/prediction/{prediction_id}
```

**Réponse réussie (200)**:
```json
{
  "id": 1,
  "prediction": 1250.5,
  "building_type": "Commercial",
  "created_at": "2025-12-10T12:30:45.123456"
}
```

---

## 🗄️ Base de Données

### Architecture

La base de données PostgreSQL enregistre **automatiquement** toutes les entrées et sorties du modèle ML.

#### Table: `energy_predictions`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER | Clé primaire auto-incrémentée |
| `building_type` | VARCHAR | Type de bâtiment |
| `primary_property_type` | VARCHAR | Type de propriété principal |
| `zip_code` | INTEGER | Code postal |
| `council_district_code` | INTEGER | Code district conseil |
| `neighborhood` | VARCHAR | Quartier |
| `latitude` | FLOAT | Latitude GPS |
| `longitude` | FLOAT | Longitude GPS |
| `year_built` | INTEGER | Année de construction |
| `number_of_buildings` | INTEGER | Nombre de bâtiments |
| `number_of_floors` | INTEGER | Nombre d'étages |
| `property_gfa_total` | FLOAT | Surface GFA totale |
| `property_gfa_parking` | FLOAT | Surface parking GFA |
| `property_gfa_buildings` | FLOAT | Surface bâtiments GFA |
| ... | ... | *25+ champs d'entrée* |
| `prediction` | FLOAT | **Résultat de la prédiction** |
| `created_at` | TIMESTAMP | Date/heure de création |

### Schéma UML Simplifié

```
┌─────────────────────────┐
│   EnergyPrediction      │
├─────────────────────────┤
│ id (PK)                 │
│ building_type           │
│ primary_property_type   │
│ zip_code                │
│ council_district_code   │
│ neighborhood            │
│ latitude                │
│ longitude               │
│ ... (25+ input fields)  │
│ prediction (OUTPUT) ⭐   │
│ created_at (TIMESTAMP)  │
└─────────────────────────┘
```

### Gestion de la base de données

**Créer les tables** (automatique au premier démarrage):
```bash
uv run python create_db.py
```

**Réinitialiser la base de données** (⚠️ supprime toutes les données):
```bash
uv run python create_db.py drop
```

**Interroger les données directement**:
```python
from app.core.database import SessionLocal
from app.models import EnergyPrediction

db = SessionLocal()
predictions = db.query(EnergyPrediction).all()
for pred in predictions:
    print(f"ID: {pred.id}, Prédiction: {pred.prediction}, Date: {pred.created_at}")
db.close()
```

---

## 🔧 Architecture et Composants

### `app/main.py`
- **Rôle**: Point d'entrée principal de l'application
- **Contient**: 
  - Configuration de l'application FastAPI
  - Tous les endpoints de l'API
  - Logique de prédiction et enregistrement en DB
  - Endpoints de consultation de l'historique

### `app/models.py`
- **Rôle**: Modèles SQLAlchemy pour la persistance
- **Contient**: 
  - `EnergyPrediction`: Modèle ORM représentant la table `energy_predictions`
  - Tous les champs d'entrée du ML + résultat de prédiction

### `app/core/database.py`
- **Rôle**: Configuration de la base de données
- **Contient**: 
  - Configuration SQLAlchemy + psycopg3
  - SessionLocal factory
  - Dépendance `get_db()` pour l'injection dans les endpoints

### `app/schemas/p3_request.py`
- **Rôle**: Définition des modèles de données
- **Contient**: 
  - `EnergyRequest`: Modèle Pydantic pour valider les requêtes de prédiction
  - `PredictionResponse`: Modèle de réponse pour une prédiction unique
  - `PredictionHistoryResponse`: Modèle de réponse pour l'historique
  - 25+ champs pour décrire les caractéristiques d'un bâtiment

### `app/services/p3_model.py`
- **Rôle**: Service de gestion du modèle ML
- **Contient**: 
  - `EnergyModel`: Classe singleton pour charger et utiliser le modèle
  - Gestion du cache du modèle (chargé une seule fois en mémoire)
  - Méthode `predict()` pour générer des prédictions

### `models/model_p3.joblib`
- **Format**: Fichier binaire sérialisé (joblib)
- **Contenu**: Modèle Random Forest entraîné
- **Utilisation**: Chargé au moment de la première requête

### `docker-compose.yml`
- **Rôle**: Configuration de PostgreSQL en conteneur
- **Contient**: 
  - Service PostgreSQL 16 Alpine
  - Configuration des credentials
  - Volumes persistants pour les données
  - Health check automatique

### `create_db.py`
- **Rôle**: Script d'initialisation de la base de données
- **Utilisation**: 
  - `uv run python create_db.py` → Crée les tables
  - `uv run python create_db.py drop` → Supprime les tables

---

## 🧪 Tests

### Exécuter tous les tests
```bash
uv run pytest
```

### Tests unitaires
```bash
uv run pytest tests/unit/
```

### Tests d'intégration
```bash
uv run pytest tests/integration/
```

### Tests avec couverture de code
```bash
uv run pytest --cov=app --cov-report=html
```

---

## 📦 Dépendances principales

| Paquet | Version | Utilité |
|--------|---------|---------|
| `fastapi` | >=0.119.1 | Framework API web |
| `uvicorn` | >=0.38.0 | Serveur ASGI |
| `pydantic` | >=2.12.3 | Validation des données |
| `pandas` | >=2.3.3 | Manipulation des données |
| `scikit-learn` | >=1.7.2 | Modèle ML et utilitaires |
| `joblib` | >=1.5.2 | Sérialisation du modèle |
| `pytest` | >=8.4.2 | Framework de test |
| `pytest-cov` | >=7.0.0 | Couverture de tests |
| `sqlalchemy` | >=2.0.44 | ORM pour la base de données |
| `psycopg[binary]` | >=3.2.11 | Driver PostgreSQL Python |
| `python-dotenv` | >=1.1.1 | Gestion des variables d'environnement |

---

## 📝 Conventions de Commit

Pour maintenir un historique de commits clair et cohérent :

| Type | Description | Exemple |
|------|-------------|---------|
| **ADD** | Ajout de fonctionnalité/fichier | `ADD: endpoint de prédiction` |
| **FIX** | Correction de bug/problème | `FIX: erreur de validation` |
| **DOCS** | Documentation | `DOCS: mise à jour du README` |
| **DEL** | Suppression volontaire | `DEL: route obsolète` |

---

## 🔐 Variables d'environnement

Si nécessaire, créez un fichier `.env` à la racine du projet :

```bash
# Exemple de configuration
API_TITLE=Futurisys ML API
API_VERSION=0.1.0
LOG_LEVEL=INFO
```

---

## 📊 Flux de Prédiction

```
Requête HTTP POST /api/p3/predict
    ↓
Validation Pydantic (EnergyRequest)
    ↓
Renommage du champ PropertyGFABuildings
    ↓
Conversion en DataFrame pandas
    ↓
Chargement du modèle (singleton)
    ↓
Prédiction ML
    ↓
Enregistrement en base de données PostgreSQL ⭐
    ↓
Réponse JSON {"prediction": value}
```

### Enregistrement des données

Chaque prédiction est automatiquement enregistrée dans la table `energy_predictions` avec:
- ✅ Tous les champs d'entrée
- ✅ Le résultat de la prédiction
- ✅ L'horodatage exact (UTC)

---

## 🚀 Déploiement

### Déploiement sur Hugging Face Spaces

Cette application est prête à être déployée sur [Hugging Face Spaces](https://huggingface.co/spaces).

#### Étapes:

1. **Créer un nouvel Space sur Hugging Face**
   - Aller sur https://huggingface.co/new-space
   - Sélectionner **Docker** comme runtime
   - Nommer l'espace: `model-machine-learning`
   - Rendre public ou privé selon vos besoins

2. **Connecter votre dépôt GitHub**
   - Dans les paramètres du Space, activer la synchronisation GitHub
   - Sélectionner votre dépôt `Model_Machine_Learning`
   - Sélectionner la branche `main`

3. **Configuration automatique**
   - HF Spaces détectera automatiquement le `Dockerfile`
   - Construira et déploiera l'image Docker
   - L'API sera accessible via `https://huggingface.co/spaces/[username]/model-machine-learning`

#### Variables d'environnement

Laissez `DATABASE_URL` vide pour utiliser SQLite automatiquement sur HF Spaces:

```
# Database: Auto-switch
# - Si DATABASE_URL vide → SQLite (HF Spaces)
# - Si DATABASE_URL défini → PostgreSQL (local)
```

#### Points importants:

- ✅ **Base de données**: SQLite (`/tmp/predictions.db`) - pas besoin de PostgreSQL sur HF
- ✅ **Port**: 7860 (standard HF Spaces)
- ✅ **Documentation**: Swagger UI accessible à `/docs`
- ⚠️ **Données persistantes**: Les prédictions sont sauvegardées tant que le Space tourne

### Déploiement local avec Docker

```bash
# Builder l'image Docker
docker build -t model-api .

# Lancer le conteneur
docker run -p 8000:7860 model-api
```

### Autres options de déploiement

Pour un déploiement en production:

1. **Conteneurisation**: Docker ✅ (configuré)
2. **Orchestration**: Kubernetes
3. **CI/CD**: GitHub Actions (configuré dans `.github/workflows/`)
4. **Monitoring**: Application Performance Monitoring (APM)
5. **Base de données persistante**: PostgreSQL (remplacer DATABASE_URL)

---

## 📄 Licence

Projet réalisé dans le cadre d'OpenClassroom.

---

## 👤 Auteur

**DagueG** - [GitHub Profile](https://github.com/DagueG)
