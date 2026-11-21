# UNIVERSAL RAG ENGINE

## Document 02 — Architecture globale

**Version :** 1.0
**Statut :** Validated
**Projet :** RAG-universal

---

# 1. Objectif du document

Ce document définit l'architecture logique globale de Universal RAG Engine.

Il décrit :

- Les grands ensembles architecturaux.
- Les responsabilités de chaque ensemble.
- Les frontières fonctionnelles.
- Les interactions entre composants.
- Les principaux flux de données.
- Les mécanismes transversaux.
- Les dépendances entre les différentes parties du système.

L'objectif est de définir une architecture cohérente avant de préciser les modules internes et leurs implémentations.

Ce document ne sélectionne aucune technologie particulière.

# 2. Références architecturales

Cette spécification dépend des documents suivants :

| Document | Rôle |
|---|---|
| 00_VISION_ET_OBJECTIFS.md | Vision et principes fondateurs |
| DEPENDENCY_MAP.md | Dépendances documentaires et fonctionnelles |
| DECISION_LOG.md | Décisions architecturales validées |
| 01_CAHIER_DES_CHARGES.md | Exigences fonctionnelles et non fonctionnelles |

L'architecture devra respecter les exigences FR-001 à FR-028 et NFR-001 à NFR-020.

# 3. Principes architecturaux

L'architecture doit respecter les principes suivants.

## 3.1 Indépendance métier

Le cœur du moteur ne doit contenir aucune logique spécifique à une application métier.

## 3.2 Indépendance des applications clientes

Les applications communiquent avec le moteur par des interfaces publiques documentées.

Elles ne doivent pas accéder directement à ses composants internes.

## 3.3 Séparation des responsabilités

Chaque ensemble possède des responsabilités clairement définies.

Un composant ne doit pas prendre en charge les responsabilités propres à un autre ensemble.

## 3.4 Modularité logique

Les composants communiquent à travers des contrats définis.

Les dépendances directes vers les implémentations internes doivent être limitées.

## 3.5 Séparation du contrôle et du traitement

La gestion des organisations, des utilisateurs, des configurations et des permissions doit être distinguée des traitements documentaires et des opérations de recherche.

## 3.6 Indépendance des fournisseurs

Les services externes doivent être accessibles à travers des interfaces permettant leur remplacement.

## 3.7 Sécurité transversale

La sécurité ne doit pas être considérée comme un module isolé.

Elle doit accompagner les opérations de gestion, d'ingestion, de recherche et de génération.

## 3.8 Évolutivité

L'architecture doit permettre l'évolution indépendante des composants sans imposer une refonte générale.

# 4. Vue architecturale globale

L'architecture logique est organisée autour de quatre grands ensembles :

1. Control Plane.
2. Knowledge Processing.
3. Query Engine.
4. Cross-cutting Services.

Des mécanismes de stockage et des adaptateurs externes assurent leur fonctionnement.

## 4.1 Représentation globale

```text
                 APPLICATIONS CLIENTES
                          |
                          |
                  INTERFACE PUBLIQUE
                          |
                          v
              +------------------------+
              |     ACCESS LAYER       |
              |                        |
              | Authentication         |
              | Authorization          |
              | Request Context        |
              +------------------------+
                          |
                          v
              +------------------------+
              |  CENTRAL ORCHESTRATION |
              +------------------------+
                          |
             +------------+------------+
             |            |            |
             v            v            v
        CONTROL       KNOWLEDGE      QUERY
        PLANE         PROCESSING     ENGINE
             |            |            |
             |            |            |
             +------------+------------+
                          |
                          v
               PERSISTENCE LAYER
                          |
             +------------+------------+
             |            |            |
             v            v            v
         Metadata      Documents     Indexes
         Storage       Storage       Storage
             |
             v
       EXTERNAL PROVIDERS
       ------------------
       Embedding Providers
       LLM Providers
       Reranking Providers
       Extraction Providers
       External Data Sources
```

Cette représentation est logique. Elle ne préjuge pas du nombre de processus ou de serveurs qui seront nécessaires.

# 5. Control Plane

## 5.1 Responsabilité générale

Le Control Plane gère les ressources, les identités, les configurations et les règles d'organisation du moteur.

Il définit qui peut utiliser le système, quelles ressources existent et dans quelles conditions elles peuvent être exploitées.

Il ne doit pas prendre en charge directement les traitements lourds d'ingestion ou de génération.

## 5.2 Composants conceptuels

### A. Organization Management

Responsabilités :

- Création des organisations.
- Gestion de leur cycle de vie.
- Identification des propriétaires.
- Gestion des ressources organisationnelles.

### B. Application Management

Responsabilités :

- Enregistrement des applications clientes.
- Attribution d'une identité aux applications.
- Configuration des accès.
- Activation et désactivation des applications.

### C. Identity and Access Management

Responsabilités :

- Identification des utilisateurs.
- Gestion des identités applicatives.
- Gestion des autorisations.
- Application des politiques d'accès.

### D. Knowledge Base Management

Responsabilités :

- Création des Knowledge Bases.
- Gestion de leurs configurations.
- Gestion de leurs états.
- Association des sources.
- Gestion de leurs règles d'accès.

### E. Configuration Management

Responsabilités :

- Gestion des paramètres du moteur.
- Gestion des configurations des fournisseurs.
- Gestion des stratégies applicables aux Knowledge Bases.
- Gestion des versions des configurations.

### F. Source Registry

Responsabilités :

- Enregistrement des sources.
- Identification de leur origine.
- Gestion de leurs configurations.
- Suivi de leur état.

## 5.3 Frontière du Control Plane

Le Control Plane possède les métadonnées de gestion et les règles d'accès.

Il ne doit pas devenir le moteur d'exécution des recherches documentaires.

Les traitements sont délégués aux composants concernés.

# 6. Knowledge Processing

## 6.1 Responsabilité générale

Knowledge Processing est responsable de la transformation des sources externes en connaissances exploitables par le moteur.

Il constitue le pipeline de préparation et d'indexation.

## 6.2 Composants conceptuels

### A. Source Connectors

Responsabilités :

- Connexion aux sources.
- Récupération des contenus.
- Identification de leur origine.
- Gestion des erreurs de connexion.

### B. Document Ingestion

Responsabilités :

- Réception des documents.
- Validation des entrées.
- Identification des documents.
- Gestion des opérations d'importation.

### C. Extraction Engine

Responsabilités :

- Extraction des contenus.
- Extraction des métadonnées.
- Préservation des informations de structure.
- Signalement des erreurs d'extraction.

### D. Normalization Engine

Responsabilités :

- Normalisation des contenus.
- Harmonisation des représentations.
- Préparation des données pour les traitements suivants.

### E. Chunking Engine

Responsabilités :

- Découpage des contenus.
- Gestion des stratégies de découpage.
- Conservation de la relation entre fragments et documents.
- Préservation des métadonnées nécessaires.

### F. Embedding Engine

Responsabilités :

- Production des représentations vectorielles.
- Gestion des fournisseurs d'embeddings.
- Identification des modèles utilisés.
- Vérification de la compatibilité des représentations.

### G. Indexing Engine

Responsabilités :

- Préparation des données pour la recherche.
- Gestion des index.
- Synchronisation des différentes représentations.
- Réindexation après modification des connaissances.

## 6.3 Résultat de Knowledge Processing

À l'issue du pipeline, les connaissances doivent être disponibles pour les mécanismes de recherche avec leurs références d'origine.

Le pipeline doit permettre de retrouver :

- Le document source.
- Sa version.
- Ses fragments.
- Le modèle d'embeddings utilisé.
- Les informations d'indexation.
- L'état du traitement.

# 7. Query Engine

## 7.1 Responsabilité générale

Query Engine est responsable du traitement des requêtes envoyées par les applications clientes.

Il coordonne la recherche, la récupération des informations, leur classement et, lorsque cela est demandé, la génération de réponses.

La recherche et la génération doivent rester deux capacités distinctes.

Le moteur doit pouvoir fournir des résultats de recherche sans obligatoirement appeler un LLM.

## 7.2 Composants conceptuels

### A. Query Reception

Responsabilités :

- Réception des requêtes.
- Validation des paramètres.
- Association avec le contexte d'exécution.
- Transmission à l'orchestrateur.

### B. Query Orchestration

Responsabilités :

- Coordination des mécanismes de recherche.
- Sélection des stratégies applicables.
- Coordination des sources documentaires et structurées.
- Gestion du déroulement d'une requête.

### C. Vector Retrieval

Responsabilités :

- Recherche sémantique.
- Récupération des fragments pertinents.
- Respect des filtres et autorisations.

### D. Keyword Retrieval

Responsabilités :

- Recherche textuelle.
- Identification des correspondances lexicales.
- Récupération des résultats pertinents.

### E. Hybrid Retrieval

Responsabilités :

- Combinaison des résultats vectoriels et textuels.
- Fusion des classements.
- Production d'une liste consolidée.

### F. Reranking

Responsabilités :

- Réévaluation de la pertinence.
- Classement des résultats.
- Sélection des informations les plus adaptées à la requête.

### G. Context Assembly

Responsabilités :

- Construction du contexte documentaire.
- Sélection des passages.
- Gestion des limites de contexte.
- Conservation des références.

### H. Generation Engine

Responsabilités :

- Construction des entrées de génération.
- Transmission du contexte au fournisseur LLM.
- Réception des réponses.
- Gestion des situations d'insuffisance documentaire.

### I. Citation and Provenance

Responsabilités :

- Association des réponses avec leurs sources.
- Identification des documents et fragments utilisés.
- Conservation des références exploitables par les applications clientes.

# 8. Structured Data Access

Les données structurées constituent un sous-système distinct de l'ingestion documentaire.

Elles ne doivent pas être obligatoirement transformées en documents et fragments pour être exploitées.

## 8.1 Responsabilités

- Connexion aux sources structurées.
- Découverte ou configuration des structures accessibles.
- Application des autorisations.
- Exécution contrôlée des opérations.
- Normalisation des résultats.
- Conservation de la provenance.

## 8.2 Frontière de sécurité

Les fournisseurs LLM ne doivent pas disposer d'un accès direct et libre aux bases de données externes.

Toute opération doit passer par une couche contrôlée qui vérifie les autorisations et la nature de l'opération demandée.

Les stratégies précises d'interrogation seront définies dans le document consacré aux données structurées.

## 8.3 Interaction avec Query Engine

Query Engine peut solliciter :

- Le moteur documentaire.
- Le sous-système Structured Data Access.
- Les deux simultanément lorsque le besoin le justifie.

Les résultats doivent conserver leur origine respective.

# 9. Cross-cutting Services

Ces services accompagnent les différents ensembles architecturaux.

## 9.1 Security Services

Responsabilités :

- Authentification.
- Autorisation.
- Isolation organisationnelle.
- Contrôle des accès aux Knowledge Bases.
- Protection des données sensibles.
- Gestion des secrets.

## 9.2 Tenant Context Management

Responsabilités :

- Identification du périmètre organisationnel.
- Association des requêtes à leur organisation.
- Vérification des applications autorisées.
- Propagation du contexte de sécurité.

Le contexte organisationnel doit être établi à partir d'une identité authentifiée et de permissions vérifiées.

Il ne doit pas être accepté aveuglément à partir d'un identifiant transmis par une application cliente.

## 9.3 Audit and Traceability

Responsabilités :

- Identification des opérations.
- Suivi des traitements.
- Conservation des événements importants.
- Traçabilité des accès.
- Traçabilité des réponses et de leurs sources.

## 9.4 Observability

Responsabilités :

- Suivi des performances.
- Suivi des erreurs.
- Surveillance des traitements.
- Identification des problèmes.
- Mesure de l'utilisation des ressources.

## 9.5 Lifecycle Management

Responsabilités :

- Gestion des états des ressources.
- Propagation des modifications.
- Suppression des connaissances.
- Gestion des versions.
- Synchronisation des index.

## 9.6 Reliability Services

Responsabilités :

- Gestion des erreurs.
- Reprise des traitements.
- Contrôle des opérations répétées.
- Gestion des indisponibilités externes.
- Protection contre les incohérences.

# 10. Persistence Layer

Cette couche représente les différentes catégories de stockage nécessaires au fonctionnement du moteur.

Il s'agit de responsabilités logiques et non d'une sélection de technologies.

## 10.1 Metadata Storage

Contient notamment :

- Organisations.
- Applications.
- Utilisateurs.
- Permissions.
- Knowledge Bases.
- Sources.
- Documents.
- Versions.
- Configurations.
- États des traitements.

## 10.2 Document Storage

Conserve les contenus documentaires originaux ou leurs représentations nécessaires.

Les règles de conservation et de suppression doivent être respectées.

## 10.3 Index Storage

Conserve les représentations nécessaires à la recherche.

Il peut notamment contenir :

- Les représentations vectorielles.
- Les index textuels.
- Les métadonnées d'indexation.
- Les références vers les documents.

## 10.4 Execution State Storage

Conserve les informations nécessaires au suivi des opérations :

- Importations.
- Extraction.
- Indexation.
- Réindexation.
- Suppression.
- Traitement des requêtes lorsque leur suivi est nécessaire.

Les responsabilités de ces catégories de stockage seront précisées dans le modèle de données et les spécifications techniques.

# 11. External Provider Layer

Le moteur devra pouvoir communiquer avec différents fournisseurs externes.

Les catégories envisagées sont :

| Catégorie | Responsabilité |
|---|---|
| Embedding Providers | Production des embeddings |
| LLM Providers | Génération des réponses |
| Reranking Providers | Classement des résultats |
| Extraction Providers | Extraction spécialisée |
| Source Connectors | Connexion aux sources de connaissances |

Chaque catégorie devra disposer d'un contrat d'intégration adapté.

Les fournisseurs ne doivent pas imposer leurs propres modèles de données au cœur du moteur.

Les différences de capacités et les incompatibilités doivent être identifiables.

# 12. Flux architecturaux principaux

## 12.1 Initialisation d'une organisation

```text
Administrateur
      |
      v
Access Layer
      |
      v
Control Plane
      |
      v
Organization Management
      |
      v
Application Management
      |
      v
Identity and Access
      |
      v
Knowledge Base Management
      |
      v
Configuration
```

Résultat : une organisation dispose de ressources configurées et d'identités autorisées à utiliser le moteur.

## 12.2 Ingestion documentaire

```text
Source
  |
  v
Source Connector
  |
  v
Document Ingestion
  |
  v
Extraction
  |
  v
Normalization
  |
  v
Chunking
  |
  v
Embeddings
  |
  v
Indexing
  |
  v
Knowledge Storage
  |
  v
Knowledge Available
```

Chaque opération doit pouvoir être suivie.

Les erreurs doivent être identifiables et les traitements pouvant être repris doivent disposer de mécanismes de reprise contrôlés.

## 12.3 Recherche documentaire

```text
Application Client
       |
       v
Public API
       |
       v
Authentication
       |
       v
Authorization
       |
       v
Request Context
       |
       v
Query Orchestration
       |
       +-----------------+
       |                 |
       v                 v
Vector Retrieval   Keyword Retrieval
       |                 |
       +--------+--------+
                |
                v
           Hybrid Fusion
                |
                v
             Reranking
                |
                v
          Result Selection
                |
                v
          Response Assembly
```

Cette opération peut retourner directement les résultats sans génération LLM.

## 12.4 Recherche avec génération

```text
User Question
      |
      v
Query Engine
      |
      v
Retrieval
      |
      v
Reranking
      |
      v
Context Assembly
      |
      v
Generation Engine
      |
      v
LLM Provider
      |
      v
Citation Verification
      |
      v
Response
```

La réponse doit conserver la relation avec les informations récupérées.

## 12.5 Recherche combinant plusieurs sources

```text
                User Question
                      |
                      v
               Query Orchestration
                      |
             +--------+--------+
             |                 |
             v                 v
       Document Retrieval   Structured Access
             |                 |
             v                 v
       Document Results    Structured Results
             |                 |
             +--------+--------+
                      |
                      v
               Result Integration
                      |
                      v
               Context Assembly
                      |
                      v
                   Optional
                  Generation
                      |
                      v
                   Response
```

La combinaison ne doit jamais supprimer les informations de provenance.

## 12.6 Suppression documentaire

```text
Deletion Request
       |
       v
Authorization Check
       |
       v
Document Lifecycle
       |
       +------------------+
       |                  |
       v                  v
Document Storage     Index Storage
       |                  |
       v                  v
Content Deletion     Index Removal
       |                  |
       +---------+--------+
                 |
                 v
          Deletion Verification
                 |
                 v
             Audit Event
```

Une suppression ne sera considérée comme terminée que lorsque toutes les représentations concernées auront été traitées conformément à la politique de conservation.

# 13. Isolation multi-tenant

L'isolation organisationnelle constitue une propriété fondamentale de l'architecture.

Elle doit être appliquée à tous les niveaux concernés.

## 13.1 Contexte organisationnel

Chaque opération protégée doit être associée à un contexte d'accès vérifié.

Ce contexte doit permettre d'identifier :

- L'organisation.
- L'application cliente.
- L'utilisateur ou l'identité de service.
- Les permissions applicables.
- Les Knowledge Bases accessibles.

## 13.2 Application de l'isolation

L'isolation doit concerner :

- Les métadonnées.
- Les documents.
- Les fragments.
- Les embeddings.
- Les index.
- Les recherches.
- Les sources structurées.
- Les caches éventuels.
- Les journaux et historiques.

## 13.3 Principe de refus par défaut

Lorsqu'une autorisation n'est pas démontrée, l'accès doit être refusé.

Les mécanismes précis d'isolation seront définis dans le document 11.

# 14. Gestion du cycle de vie des connaissances

L'architecture doit prendre en charge les différentes opérations affectant une connaissance.

## 14.1 Création

Une nouvelle source ou un nouveau document est enregistré.

## 14.2 Traitement

Le contenu est extrait, normalisé et préparé.

## 14.3 Indexation

Les différentes représentations nécessaires sont produites et enregistrées.

## 14.4 Activation

La nouvelle version devient disponible pour la recherche uniquement lorsque les conditions de cohérence définies sont satisfaites.

## 14.5 Modification

Une modification doit pouvoir déclencher un nouveau traitement sans laisser des représentations obsolètes accessibles.

## 14.6 Réindexation

Un changement de modèle ou de stratégie doit permettre de reconstruire les index concernés.

## 14.7 Suppression

Les données et représentations dérivées doivent être supprimées conformément aux règles définies.

La gestion des versions et les transitions d'état seront détaillées dans les spécifications spécialisées.

# 15. Frontières de responsabilité

Les responsabilités suivantes doivent rester séparées.

| Responsabilité | Ensemble propriétaire |
|---|---|
| Gestion des organisations | Control Plane |
| Gestion des applications | Control Plane |
| Gestion des utilisateurs et permissions | Control Plane |
| Gestion des Knowledge Bases | Control Plane |
| Gestion des sources | Control Plane |
| Importation documentaire | Knowledge Processing |
| Extraction documentaire | Knowledge Processing |
| Normalisation | Knowledge Processing |
| Chunking | Knowledge Processing |
| Embeddings | Knowledge Processing |
| Indexation | Knowledge Processing |
| Recherche vectorielle | Query Engine |
| Recherche textuelle | Query Engine |
| Recherche hybride | Query Engine |
| Reranking | Query Engine |
| Construction du contexte | Query Engine |
| Génération | Query Engine |
| Interrogation structurée | Structured Data Access |
| Isolation et autorisation | Cross-cutting Services |
| Audit | Cross-cutting Services |
| Observabilité | Cross-cutting Services |
| Gestion du cycle de vie | Services concernés, avec coordination transversale |

# 16. Exigences architecturales de cohérence

L'architecture doit garantir les propriétés suivantes :

1. Une application cliente ne peut pas contourner les mécanismes d'autorisation.
2. Une Knowledge Base ne peut pas exposer des informations d'une autre base sans permission.
3. L'ingestion et la recherche sont indépendantes dans leurs responsabilités.
4. La recherche documentaire peut fonctionner sans génération.
5. Les données structurées conservent leur propre mécanisme d'accès.
6. Les résultats provenant de sources différentes conservent leur provenance.
7. Les fournisseurs externes peuvent être remplacés à travers des contrats définis.
8. La suppression d'une connaissance est répercutée sur ses représentations dérivées.
9. Les opérations importantes peuvent être tracées.
10. Les changements de configuration susceptibles d'invalider les index sont maîtrisés.

# 17. Principes de déploiement

Les ensembles architecturaux définis dans ce document constituent des frontières logiques.

Ils ne représentent pas obligatoirement des services physiques indépendants.

L'architecture ne présuppose donc pas :

- Un déploiement en microservices.
- Un déploiement en application unique.
- Un nombre fixe de bases de données.
- Un nombre fixe de serveurs.
- Une infrastructure cloud particulière.

Le nombre de processus, les mécanismes de communication et la topologie de déploiement seront étudiés dans les spécifications correspondantes.

La séparation logique doit rester valable indépendamment du mode de déploiement retenu.

# 18. Points à approfondir

Les sujets suivants ne sont pas encore définitivement résolus.

| Sujet | Spécification concernée |
|---|---|
| Organisation interne des modules | 03 — Architecture modulaire |
| Entités et relations persistées | 04 — Modèle de données |
| Structure détaillée des Knowledge Bases | 05 |
| Pipeline et traitement des documents | 06 |
| Stratégies de découpage et embeddings | 07 |
| Fusion et classement des résultats | 08 |
| Génération et interfaces LLM | 09 |
| Contrats de communication publics | 10 |
| Authentification et isolation | 11 |
| Interrogation des données structurées | 12 |
| Tests et évaluation | 13 |
| Infrastructure et scalabilité | 14 |

# 19. Décisions non prises

Ce document ne valide pas les choix suivants :

- Langage de programmation.
- Framework backend.
- Architecture physique.
- Base de données.
- Moteur vectoriel.
- Système de stockage documentaire.
- Fournisseur LLM.
- Fournisseur d'embeddings.
- Système de traitement asynchrone.
- Protocole d'authentification.
- Topologie de déploiement.
- Stratégie physique d'isolation multi-tenant.

Ces sujets nécessitent des études spécifiques et, lorsque nécessaire, des décisions documentées dans le Decision Log ou dans des ADR.

# 20. Conditions de validation

Le document sera considéré comme validé lorsque :

1. Les quatre ensembles architecturaux seront clairement définis.
2. Les frontières de responsabilité seront approuvées.
3. Les principaux flux seront cohérents.
4. La séparation entre données structurées et non structurées sera confirmée.
5. Les règles générales d'isolation seront approuvées.
6. Les principes d'indépendance des applications clientes seront respectés.
7. Les dépendances avec les autres spécifications seront identifiées.
8. Les ambiguïtés architecturales importantes seront résolues ou explicitement reportées.

# 21. Conclusion

L'architecture globale de Universal RAG Engine repose sur la séparation des responsabilités, l'indépendance des applications clientes et la gestion autonome des connaissances.

Elle distingue le contrôle des ressources, le traitement des connaissances, l'exploitation des connaissances et les services transversaux.

Cette organisation doit permettre de faire évoluer le moteur sans imposer une dépendance à un domaine métier, à un fournisseur ou à une application cliente.

**Un moteur central, des responsabilités séparées, des interfaces maîtrisées et des connaissances indépendantes des applications qui les exploitent.**
