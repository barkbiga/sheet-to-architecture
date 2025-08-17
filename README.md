# Sheet to Architecture

Générateur de diagrammes d'architecture et de documentation à partir de fichiers Excel.

## 🆕 Nouveautés

### Version 3.0 - Janvier 2025 🎉

**Évolutions majeures :**
- ✅ **Glossaire intégré** : Onglet Excel et section documentation pour définir les termes techniques
- ✅ **Documents de référence** : Onglet Excel et section pour tracer les standards et réglementations
- ✅ **Historique des révisions** : Onglet Excel et section pour le versioning complet du projet
- ✅ **Templates enrichis** : Nouvelles sections dans l'architecture avec table des matières mise à jour

**Fichiers ajoutés :**
- `templates_multi/chapters/09_glossaire.md.j2` - Template glossaire
- `templates_multi/chapters/10_references.md.j2` - Template références  
- `templates_multi/chapters/11_revisions.md.j2` - Template révisions
- Scripts d'ajout des nouveaux onglets Excel

**Impact utilisateur :**
- 📚 Documentation plus complète et professionnelle
- 🔍 Traçabilité des standards appliqués
- 📝 Suivi des évolutions du projet
- 🎯 Meilleure compréhension des termes techniques

### Version 2.2 - Septembre 2024

**Optimisations :**
- 🔧 Correction des incohérences dans les flux de données
- 📊 Mise à jour de la matrice de traçabilité
- 🎨 Amélioration de la lisibilité des diagrammes

### Version 2.1 - Juillet 2024

**Performance :**
- ⚡ Optimisation des performances des diagrammes
- 📈 Ajout des métriques de monitoring
- 🔍 Amélioration de l'observabilité

### Version 2.0 - Juin 2024

**Refonte majeure :**
- 🏗️ Nouvelle architecture microservices
- 📡 Approche event-driven
- 🔄 Refonte complète des vues applicatives

### Version 1.2 - Mars 2024

**Sécurité :**
- 🛡️ Renforcement de la section sécurité
- 🔒 Analyse des risques détaillée
- 💳 Conformité PCI-DSS

### Version 1.1 - Février 2024

**Enrichissement métier :**
- 📋 Ajout des diagrammes de capacités
- 💼 Flux de valeur métier
- 🎯 Vue métier enrichie

### Version 1.0 - Janvier 2024

**Création initiale :**
- 🎯 Première version avec vues métier et technique de base
- 📊 Générateur de diagrammes C4
- 📁 Structure de projet modulaire

## 📦 Installation et Démarrage rapide

### Option 1 : Installation locale

**Prérequis** : Python ≥ 3.9

```bash
# Clone et installation
git clone <repository-url>
cd sheet-to-architecture

# Environnement virtuel
python3 -m venv .venv
source .venv/bin/activate   # Windows : .venv\Scripts\activate

# Dépendances
pip install -r requirements.txt

# Génération complète
python generate.py --all
```

### Option 2 : Docker (Recommandé)

```bash
# Construction de l'image
docker build -t sheet-to-architecture .

# Génération complète (fichier inclus dans le projet)
docker run --rm -v $(pwd):/app sheet-to-architecture

# Génération avec paramètres (fichier inclus)
docker run --rm -v $(pwd):/app sheet-to-architecture --diagrams context
docker run --rm -v $(pwd):/app sheet-to-architecture --docs architecture security

# Windows PowerShell (fichier inclus)
docker run --rm -v ${PWD}:/app sheet-to-architecture
```

> 💡 **Pour utiliser des fichiers Excel externes**, voir la section "Utilisation avec fichiers Excel externes" ci-dessous.

## 🚀 Utilisation

### Commandes principales

```bash
# Tout générer
python generate.py --all

# Diagrammes spécifiques
python generate.py --diagrams context infrastructure security

# Fichier Excel personnalisé
python generate.py --input mon_architecture.xlsx --all

# Répertoire de sortie personnalisé
python generate.py --all --output-dir /custom/path

# Exclure certains types de composants
python generate.py --diagrams context --exclude topic database

# Filtrage des clients
python generate.py --diagrams context --client-types EndUser Partner

# Nettoyage puis génération
python generate.py --all --clean
```

### Types de contenu disponibles

| Type | Options | Description |
|------|---------|-------------|
| **Diagrammes** | `context` | Diagrammes C4 Context par zones réseau |
| | `overview` | Vue d'ensemble des applications |
| | `infrastructure` | Diagrammes d'infrastructure technique |
| | `security` | Vues et tables de sécurité |
| | `process` | Diagrammes de processus métier |
| | `capabilities` | Cartographie des capacités et value streams |
| | `all` | Tous les diagrammes |
| **Documentation** | `architecture` | Documents d'architecture complets |
| | `infrastructure` | Vue infrastructure détaillée |
| | `security` | Documentation sécurité |
| | `technology` | Vue technologique |
| | `traceability` | Matrice de traçabilité |
| | `all` | Toute la documentation |

### Utilisation avec fichiers Excel externes et répertoires personnalisés

Docker permet de traiter des fichiers Excel situés **en dehors** du projet et de spécifier des répertoires de sortie :

#### Méthode 1 : Montage de répertoire avec sortie personnalisée

```bash
# Linux/MacOS - Fichier Excel externe et sortie personnalisée
docker run --rm \
  -v $(pwd):/app \
  -v /chemin/vers/mes/excels:/data \
  -v /chemin/sortie:/output \
  sheet-to-architecture \
  --input /data/mon_architecture.xlsx \
  --output-dir /output \
  --all

# Windows PowerShell
docker run --rm \
  -v ${PWD}:/app \
  -v C:\chemin\vers\mes\excels:/data \
  -v C:\chemin\sortie:/output \
  sheet-to-architecture \
  --input /data/mon_architecture.xlsx \
  --output-dir /output \
  --all

# Windows CMD
docker run --rm ^
  -v %CD%:/app ^
  -v C:\chemin\vers\mes\excels:/data ^
  -v C:\chemin\sortie:/output ^
  sheet-to-architecture ^
  --input /data/mon_architecture.xlsx ^
  --output-dir /output ^
  --all
```

#### Méthode 2 : Fichier Excel unique

```bash
# Linux/MacOS - Monter un fichier Excel spécifique
docker run --rm \
  -v $(pwd):/app \
  -v /chemin/vers/mon_fichier.xlsx:/app/input.xlsx \
  sheet-to-architecture --input input.xlsx --diagrams context

# Windows PowerShell  
docker run --rm \
  -v ${PWD}:/app \
  -v C:\chemin\vers\mon_fichier.xlsx:/app/input.xlsx \
  sheet-to-architecture --input input.xlsx --diagrams context
```

#### Méthode 3 : Copie temporaire

```bash
# Copier le fichier dans le projet puis lancer
cp /chemin/vers/mon_fichier.xlsx ./
docker run --rm -v $(pwd):/app sheet-to-architecture --input mon_fichier.xlsx --all
rm mon_fichier.xlsx  # Nettoyage après traitement
```

### Exemples d'utilisation complets

```bash
# 1. Génération contexte uniquement (fichier projet)
docker run --rm -v $(pwd):/app sheet-to-architecture --diagrams context

# 2. Contexte sans topics ni bases de données
docker run --rm -v $(pwd):/app \
  sheet-to-architecture --diagrams context --exclude topic database

# 3. Documentation avec fichier externe et sortie personnalisée
docker run --rm \
  -v $(pwd):/app \
  -v /mes/architectures:/data \
  -v /mes/resultats:/output \
  sheet-to-architecture \
  --input /data/architecture_client.xlsx \
  --output-dir /output \
  --docs architecture security

# 4. Tout générer avec filtrage clients (Windows)
docker run --rm \
  -v ${PWD}:/app \
  -v C:\Projets\Architectures:/data \
  -v C:\Resultats:/output \
  sheet-to-architecture \
  --input /data/projet_xyz.xlsx \
  --output-dir /output \
  --client-types EndUser \
  --all --clean

# 5. Diagrammes avec flux asynchrones agrégés
docker run --rm -v $(pwd):/app \
  sheet-to-architecture --diagrams context --exclude topic

# 6. Génération complète avec capacités métier
docker run --rm -v $(pwd):/app \
  sheet-to-architecture --input petstore_archi_enhanced.xlsx \
  --diagrams capabilities context --all
```

## 📊 Format des données Excel

### Onglets essentiels (optimisés)

Le fichier Excel utilise **2 onglets principaux** pour les diagrammes C4 :

| Onglet | Colonnes essentielles | Colonnes optionnelles | Usage |
|--------|--------------------|----------------------|-------|
| **Applications** | ID, Name, Domain, Network_Zone, Status | Type, ClientType, ShowInDiagram | Composants et leur organisation |
| **Flows** | ID, Outbound, Inbound, Name, BusinessProcess | FlowType, AsyncMessage | Flux métier entre composants |

### Colonnes optionnelles pour fonctionnalités avancées

**Applications :**
- `Type` : CLIENT, APPLICATION, TOPIC, DATABASE (défaut: APPLICATION)  
- `ClientType` : EndUser, Partner, System (pour Type=CLIENT)
- `ShowInDiagram` : true/false (contrôle d'affichage)

**Flows :**
- `FlowType` : SYNC, ASYNC (défaut: SYNC)
- `AsyncMessage` : Description du message asynchrone

### Nouveaux onglets pour capacités (optionnels)

**Capabilities :**
- `ID, Name, Description, Domain, Level, Applications`
- `Level` : Core, Supporting, Infrastructure
- `Applications` : Liste d'IDs séparés par virgule

**ValueStreams :**
- `ID, Name, Description, StartEvent, EndEvent, Steps, Capabilities`
- `Steps` : Liste de processus métier séparés par virgule
- `Capabilities` : Liste d'IDs de capacités séparés par virgule

### Fichiers d'exemple

**`petstore_archi_enhanced.xlsx`** - Version complète avec toutes les fonctionnalités :
- ✅ 15 applications (CLIENT, APPLICATION, TOPIC, DATABASE)
- ✅ 11 flux (SYNC et ASYNC avec topics)
- ✅ 5 capacités métier avec applications liées
- ✅ 3 value streams bout-en-bout
- ✅ Support de tous les filtres et types

**`petstore_archi_optimized.xlsx`** - Version basique compatible :
- ✅ Applications par domaines métier
- ✅ Flux métier simples
- ✅ Zones réseau (DMZ, INTERNE, PCI)

## 📁 Structure du projet

```
sheet-to-architecture/
├── generate.py                     # 🎯 Script principal paramétrable
├── Dockerfile                      # 🐳 Container Docker
├── requirements.txt                # 📦 Dépendances Python
│
├── scripts/                        # 🛠️  Utilitaires
│   ├── build_docs.py               # Documentation Markdown
│   └── optimize_excel.py           # Optimisation fichiers Excel
│
├── generators/                     # 📊 Générateurs de diagrammes
│   ├── generate_context_diagram.py # C4 Context (zones réseau)
│   ├── generate_diagrams.py        # Aperçu et processus  
│   └── generate_infrastructure_diagrams.py # Infrastructure/sécurité
│
├── templates_multi/                # 📄 Templates Jinja2
│   ├── architecture_*.md.j2        # Templates documentation
│   └── chapters/                   # Chapitres modulaires
│
├── generated/                      # 📁 Sortie générée
│   ├── diagrams/                   # Tous les diagrammes (.puml, .md)
│   └── *.md                        # Documentation générée
│
└── petstore_archi_optimized.xlsx   # 📋 Données d'exemple optimisées
```

## 🎨 Fonctionnalités

### Diagrammes C4 Context
- ✅ **Agrégation par domaines** métier (Customer Experience, Supply Chain, Finance, Support)
- ✅ **Zones réseau visuelles** avec conteneurs (DMZ, INTERNE, PCI)
- ✅ **Sous-domaines automatiques** quand un domaine traverse plusieurs zones
- ✅ **Flux métier lisibles** sans numérotation technique
- ✅ **PlantUML optimisé** avec styles C4 intégrés

### Vues Infrastructure & Sécurité
- ✅ **Composants techniques** par zones réseau
- ✅ **Tables de flux** avec protocoles et sécurité
- ✅ **Diagrammes de sécurité** avec niveaux de risque
- ✅ **Matrices de traçabilité** exigences→composants

### Documentation multi-audience
- ✅ **Architecture complète** technique détaillée
- ✅ **Résumé exécutif** vision stratégique
- ✅ **Vues spécialisées** infrastructure, sécurité, technologie
- ✅ **Templates modulaires** Jinja2 personnalisables

## 📁 Structure des Répertoires de Sortie

### Avec `--output-dir` (recommandé)

Quand vous utilisez `--output-dir`, tous les fichiers sont organisés dans une structure claire :

```
mon-output/
├── diagrams/          # Tous les diagrammes PlantUML
│   ├── c4_context.puml
│   ├── overview.puml
│   ├── infrastructure_view.puml
│   ├── security_view.puml
│   ├── capabilities_map.puml
│   └── process_*.puml
└── docs/              # Toute la documentation
    ├── architecture.md
    ├── executive_summary.md
    ├── infrastructure_view.md
    ├── security_view.md
    └── technology_view.md
```

### Exemples d'utilisation

```bash
# Local - structure organisée
python generate.py -i mon_fichier.xlsx --output-dir /mes/resultats --all

# Docker - avec volumes séparés
docker run --rm \
  -v $(pwd):/app \
  -v /mes/donnees:/input \
  -v /mes/resultats:/output \
  sheet-to-architecture \
  --input /input/architecture.xlsx \
  --output-dir /output \
  --all

# Résultat dans /mes/resultats/diagrams/ et /mes/resultats/docs/
```

### Sans `--output-dir` (legacy)

```bash
# Ancienne méthode - compatibilité
python generate.py -i fichier.xlsx -o generated/diagrams -d generated
```

## 📋 Points d'attention Docker

### Chemins et montage de volumes

| Méthode | Avantages | Inconvénients | Usage recommandé |
|---------|-----------|---------------|------------------|
| **Montage répertoire** | Accès à plusieurs fichiers, organisation claire | Volume plus large | Traitement de multiple projets |
| **Montage fichier unique** | Minimal, sécurisé | Un seul fichier accessible | Traitement ponctuel |
| **Copie temporaire** | Simple, pas de configuration Docker | Duplication fichier | Tests rapides |

### Exemples de chemins par OS

```bash
# Linux/MacOS
-v /home/user/architectures:/data              # Répertoire home
-v /opt/projets/excel_files:/data              # Répertoire système
-v ~/Documents/Architectures:/data             # Répertoire utilisateur

# Windows
-v C:\Users\username\Documents\Architectures:/data    # Répertoire utilisateur
-v D:\Projets\Excel:/data                              # Autre disque
-v \\server\shared\architectures:/data                 # Partage réseau
```

## 💡 Avantages de cette approche

| Aspect | Bénéfice |
|--------|----------|
| **Paramétrable** | Génération sélective selon les besoins |
| **Containerisé** | Environnement reproductible, évite les conflits |
| **Modulaire** | Scripts spécialisés par fonction |
| **Optimisé** | Excel allégé (22→17 onglets), focus sur l'essentiel |
| **Maintenable** | Structure claire, documentation complète |
| **Flexible** | Support fichiers Excel externes via montage Docker |

## 🔧 Scripts individuels (usage avancé)

```bash
# Génération C4 Context uniquement
python generators/generate_context_diagram.py -i mon_fichier.xlsx

# Documentation sans diagrammes
python scripts/build_docs.py -i mon_fichier.xlsx

# Optimisation d'un fichier Excel existant  
python scripts/optimize_excel.py mon_fichier.xlsx optimized_output.xlsx
```