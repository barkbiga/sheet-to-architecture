<!-- architecture_full.md.j2 : template complet -->
# Dossier d’architecture – Développement d'une plateforme PetStore en ligne pour la vente et l'adoption d'animaux domestiques.

---

## 1 · Contexte & périmètre

### 1.1 Contexte
Développement d'une plateforme PetStore en ligne pour la vente et l'adoption d'animaux domestiques.

### 1.2 Périmètre fonctionnel
- Gestion des animaux
- Commandes
- Paiement

### 1.3 Hors périmètre
- Services vétérinaires
- Gestion RH

### 1.4 · Objectifs métier & indicateurs

#### 1.4.1 Objectifs
- **Réduire le délai de mise sur le marché**
- **Augmenter le taux de conversion**

#### 1.4.2 KPI
| KPI | Cible | Unité |
|-----|-------|-------|
| Lead Time (jours) | 7 | jours |
| Conversion (%) | 5 | % |

---


## 2 · Contraintes

### 2.1 Budget
150000 €

### 2.2 Planning
| Jalon | Date |
|-------|------|
| MVP | 2025-11-15 |
| Go‑Live | 2026-02-01 |

### 2.3 Dépendances
*(Aucune dépendance renseignée)*

---

## 3 · Processus métier & exigences fonctionnelles

### 3.1 Processus couverts
| ID | Nom | Description | Acteurs |
|----|-----|-------------|---------|
| BP‑01 | Navigation catalogue | Parcours de navigation dans le catalogue d'animaux | Client |
| BP‑02 | Passage commande | Processus de passage de commande et de paiement | Client;Payment Gateway |

### 3.2 Exigences fonctionnelles
| ID | Description | Priorité |
|----|-------------|----------|
| FR‑01 | Afficher le catalogue d'animaux en temps réel | High |
| FR‑02 | Gérer le panier et le checkout | High |

---

## 4 · Données manipulées

### 4.1 Dictionnaire de données
| Entity | Description | CRUD | Source |
|--------|-------------|------|--------|

### 4.2 Classification & sensibilité
| Entity | Classification | Sensibilité |
|--------|---------------|-------------|

### 4.3 Volumes & rétention
| Entity | Période | Base légale |
|--------|---------|-------------|

### 4.4 Gouvernance & qualité
| Entity | Owner | Steward | Quality Metric |
|--------|-------|---------|----------------|

---


## 5 · Positionnement dans le SI

### 5.1 Cartographie applicative
| ID | Nom | Département | Statut |
|----|-----|-------------|--------|
| APP‑WEB | PetStore‑Web | Digital | New |
| APP‑INV | Inventory‑Service | Supply | Existing |
| APP‑PAY | Payment‑Gateway | Finance | SaaS |

```mermaid
flowchart LR
    APP‑WEB["PetStore‑Web"]
    APP‑INV["Inventory‑Service"]
    APP‑PAY["Payment‑Gateway"]
```
---

## 6 · Exigences 

### 6.1 Exigences non fonctionnelles 

| ID | Catégorie | Description | SLI/SLO |
|----|-----------|-------------|---------|
| NFR‑PERF‑01 | Performance | Temps de réponse < 500 ms | p95 |
| NFR‑SCAL‑01 | Scalabilité | Auto‑scaling horizontal jusqu'à 10 nœuds | nan |


### 6.2 Exigences de sécurité

| ID | Pilier | Description |
|----|--------|-------------|
| SEC‑CONF‑01 | Confidentialité | Chiffrement TLS 1.3 obligatoire |
| SEC‑INT‑01 | Intégrité | Signature des messages API |

---
## 6 · Exigences 

### 6.1 Exigences non fonctionnelles 

| ID | Catégorie | Description | SLI/SLO |
|----|-----------|-------------|---------|
| NFR‑PERF‑01 | Performance | Temps de réponse < 500 ms | p95 |
| NFR‑SCAL‑01 | Scalabilité | Auto‑scaling horizontal jusqu'à 10 nœuds | nan |


### 6.2 Exigences de sécurité

| ID | Pilier | Description |
|----|--------|-------------|
| SEC‑CONF‑01 | Confidentialité | Chiffrement TLS 1.3 obligatoire |
| SEC‑INT‑01 | Intégrité | Signature des messages API |

## 7 · Solution applicative – Vue d’ensemble
---
```plantuml
!include diagrams/overview.puml
```

---

## 8 · Solution détaillée – Composants, intégrations & vues processus

### 8.1 Composants
| ID | Nom | Techno | Repo |
|----|-----|--------|------|
| CMP‑WEB | Web Frontend | Next.js | https://git/petstore/web |
| CMP‑API | API Backend | Spring Boot | https://git/petstore/api |

### 8.2 Intégrations
| Source | Cible | Pattern |
|--------|-------|---------|
| CMP‑API | APP‑PAY | Synchronous‑REST |

### 8.3 Vues par processus métier
#### BP‑01 – Navigation catalogue
```plantuml
!include diagrams/process_BP‑01.puml
```
#### BP‑02 – Passage commande
```plantuml
!include diagrams/process_BP‑02.puml
```

---

## 9 · Matrice de flux / échanges

| ID | Source | Cible | Protocole | Format | Processus |
|----|--------|-------|-----------|--------|-----------|
| FL‑01 | APP‑WEB | APP‑INV | REST/HTTPS | JSON | BP‑01 |
| FL‑02 | APP‑WEB | APP‑PAY | REST/HTTPS | JSON | BP‑02 |

```mermaid
flowchart LR
    APP‑WEB -->|REST/HTTPS| APP‑INV
    APP‑WEB -->|REST/HTTPS| APP‑PAY
```

---

## 10 · Architecture technique / Infrastructure

### 10.1 Vue infra (diagramme)
```plantuml
!include diagrams/infrastructure.puml
```

### 10.2 Détails des ressources
| Layer | Service | SLA |
|-------|---------|-----|
| Compute | Kubernetes | 99.9% |
| Database | PostgreSQL‑Cloud | 99.95% |

---

## 11 · Vue sécurité

```plantuml
!include diagrams/security.puml
```

### 11.1 Contrôles & zones
| Zone | Contrôle | Outil |
|------|----------|-------|
| Public | WAF | CloudArmor |
| Private | IAM | Kubernetes RBAC |

---

## 12 · Gouvernance, exploitation & plan de migration

### 12.1 RACI
| Rôle | Responsable |
|------|-------------|
| Production Owner | IT Ops |

### 12.2 Processus d’exploitation
- https://wiki/runbook‑petstore

### 12.3 Plan de migration
*(À compléter)*

---

## 13 · Annexes

### 13.1 Glossaire
Animal : Être vivant ...

### 13.2 Références

### 13.3 Hypothèses / Décisions / Risques
