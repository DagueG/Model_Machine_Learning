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
│   ├── schemas/
│   │   └── p3_request.py       # Modèles Pydantic pour la validation des requêtes
│   ├── services/
│   │   └── p3_model.py         # Classe de service pour charger et utiliser le modèle ML
│   └── __pycache__/
├── models/
│   └── model_p3.joblib         # Modèle ML sérialisé (Random Forest)
├── tests/
│   ├── unit/
│   │   └── test_health.py      # Tests unitaires pour l'endpoint /health
│   ├── integration/
│   │   └── test_p3_predict.py  # Tests d'intégration pour l'endpoint /predict
│   └── __pycache__/
├── pyproject.toml              # Configuration du projet et dépendances
└── README.md                   # Documentation du projet
```

---

## 🛠️ Installation

### Prérequis
- Python >= 3.11
- [uv](https://docs.astral.sh/uv/) (gestionnaire de paquets Python)

### Étapes d'installation

```bash
# Initialiser l'environnement virtuel avec Python 3.11
uv init --python 3.11

# Installer toutes les dépendances du projet
uv sync
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

## 🔧 Architecture et Composants

### `app/main.py`
- **Rôle**: Point d'entrée principal de l'application
- **Contient**: 
  - Configuration de l'application FastAPI
  - Tous les endpoints de l'API
  - Logique de traitement des requêtes

### `app/schemas/p3_request.py`
- **Rôle**: Définition des modèles de données
- **Contient**: 
  - `EnergyRequest`: Modèle Pydantic pour valider les requêtes de prédiction
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
Requête HTTP POST
    ↓
Validation Pydantic (EnergyRequest)
    ↓
Renommage du champ PropertyGFABuildings
    ↓
Conversion en DataFrame pandas
    ↓
Chargement du modèle (singleton)
    ↓
Prédiction
    ↓
Réponse JSON
```

---

## 🚀 Déploiement

Pour déployer cette API en production, considérez :

1. **Conteneurisation**: Docker
2. **Orchestration**: Kubernetes
3. **CI/CD**: GitHub Actions (configuré dans `.github/workflows/`)
4. **Monitoring**: Application Performance Monitoring (APM)

---

## 📄 Licence

Projet réalisé dans le cadre d'OpenClassroom.

---

## 👤 Auteur

**DagueG** - [GitHub Profile](https://github.com/DagueG)
