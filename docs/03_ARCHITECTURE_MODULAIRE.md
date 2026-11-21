# UNIVERSAL RAG ENGINE

## Document 03 — Architecture modulaire

**Version :** 1.0
**Statut :** Validated
**Projet :** RAG-universal

---

# 1. Objectif

Ce document définit la décomposition modulaire de Universal RAG Engine.

Il précise :

- Les modules constitutifs du moteur.
- Leurs responsabilités.
- Leurs frontières fonctionnelles.
- Leurs données de référence.
- Leurs interfaces.
- Leurs dépendances.
- Les règles de communication.
- Les mécanismes d'extension.
- Les principes de remplacement des implémentations.

L'objectif est de garantir une architecture modulaire, cohérente, extensible et maintenable.

Ce document décrit les frontières logiques. Il ne définit pas encore la structure des fichiers, les classes, les tables SQL ou les endpoints API.

# 2. Principes fondamentaux de conception

## P1 — Responsabilité unique

Chaque module doit posséder une responsabilité fonctionnelle identifiable.

## P2 — Encapsulation

Un module contrôle ses règles métier et ses données de référence.

Les autres modules ne doivent pas modifier directement son état interne.

## P3 — Faible couplage

Un module doit dépendre des contrats des autres modules, et non de leurs implémentations internes.

## P4 — Cohésion forte

Les responsabilités appartenant au même domaine fonctionnel doivent être regroupées.

## P5 — Dépendances orientées

Les dépendances doivent suivre une direction définie.

Les dépendances circulaires sont interdites.

## P6 — Indépendance des fournisseurs

Les fournisseurs externes doivent être accessibles à travers des contrats abstraits.

## P7 — Isolation

Les frontières organisationnelles et les règles d'autorisation doivent être respectées par tous les modules concernés.

## P8 — Remplaçabilité

Le remplacement d'une implémentation ne doit pas imposer une modification générale du moteur.

## P9 — Testabilité

Chaque module doit pouvoir être testé indépendamment à travers ses contrats.

## P10 — Évolution contrôlée

Toute modification d'un contrat partagé doit faire l'objet d'une analyse de compatibilité.

# 3. Architecture modulaire en couches

L'architecture repose sur cinq couches logiques.

## 3.1 Interface Layer

Responsabilité :

Permettre aux applications clientes et aux systèmes externes de communiquer avec le moteur.

Composants conceptuels :

- Public API.
- Administration Interfaces.
- External Integration Adapters.

Cette couche ne doit pas contenir les règles métier principales.

## 3.2 Application Layer

Responsabilité :

Coordonner l'exécution des cas d'utilisation.

Composants conceptuels :

- Application Services.
- Query Orchestrator.
- Ingestion Orchestrator.
- Knowledge Lifecycle Coordinator.
- Administration Use Cases.

Cette couche coordonne les modules métier sans absorber leurs responsabilités.

## 3.3 Domain Layer

Responsabilité :

Contenir les capacités fonctionnelles du moteur et ses règles métier.

Elle comprend :

- Identity and Access.
- Organization Management.
- Application Management.
- Knowledge Base Management.
- Source Management.
- Document Management.
- Ingestion Processing.
- Retrieval.
- Structured Data Access.
- Generation.
- Provenance.

## 3.4 Abstraction Layer

Responsabilité :

Définir les contrats permettant au domaine d'accéder aux ressources externes.

Exemples :

- Embedding Provider Contract.
- LLM Provider Contract.
- Reranking Provider Contract.
- Storage Contracts.
- Document Connector Contract.
- Structured Data Connector Contract.

## 3.5 Infrastructure Layer

Responsabilité :

Fournir les implémentations concrètes des contrats.

Elle contient les adaptateurs et mécanismes techniques nécessaires aux communications externes et à la persistance.

Elle ne doit pas imposer ses détails internes au domaine.

# 4. Cartographie des modules

Les modules sont regroupés en cinq ensembles fonctionnels.

```text
UNIVERSAL RAG ENGINE
|
+-- 1. ACCESS AND GOVERNANCE
|   |
|   +-- Organization Management
|   +-- Application Management
|   +-- Identity Management
|   +-- Authorization & Policy
|   +-- Knowledge Base Management
|   +-- Source Management
|   +-- Configuration Management
|
+-- 2. KNOWLEDGE LIFECYCLE
|   |
|   +-- Document Management
|   +-- Ingestion Orchestration
|   +-- Source Connectors
|   +-- Extraction & Normalization
|   +-- Chunking
|   +-- Embedding
|   +-- Index Management
|
+-- 3. KNOWLEDGE QUERY
|   |
|   +-- Query Orchestration
|   +-- Retrieval
|   +-- Reranking
|   +-- Structured Data Access
|   +-- Context Assembly
|   +-- Generation
|   +-- Citation & Provenance
|
+-- 4. CROSS-CUTTING SERVICES
|   |
|   +-- Audit
|   +-- Observability
|   +-- Job Management
|   +-- Error Management
|   +-- Lifecycle Coordination
|
+-- 5. EXTERNAL PROVIDER ADAPTERS
    |
    +-- Storage Adapters
    +-- Embedding Adapters
    +-- LLM Adapters
    +-- Reranking Adapters
    +-- Extraction Adapters
    +-- Source Adapters
```

Cette décomposition représente les responsabilités logiques.

Elle ne prescrit pas le nombre de services, de processus ou de déploiements physiques.

# 5. Modules de gestion et de gouvernance

## 5.1 Organization Management

Responsabilité :

Gérer les organisations utilisatrices du moteur.

Fonctions :

- Création.
- Modification.
- Activation.
- Désactivation.
- Suppression.
- Gestion du cycle de vie organisationnel.

Données de référence :

Identité et état des organisations.

Dépendances :

- Identity and Access.
- Configuration Management.

Ce module ne doit pas gérer directement les documents ou les index.

## 5.2 Application Management

Responsabilité :

Gérer les applications clientes utilisant le moteur.

Fonctions :

- Enregistrement des applications.
- Identification.
- Configuration.
- Activation et désactivation.
- Association avec les organisations.
- Gestion des autorisations applicatives.

Ce module ne doit pas connaître l'implémentation interne des applications clientes.

## 5.3 Identity Management

Responsabilité :

Gérer les identités des acteurs autorisés à utiliser le moteur.

Acteurs concernés :

- Utilisateurs humains.
- Applications clientes.
- Identités de service.

Il doit permettre d'établir l'identité authentifiée à l'origine d'une opération.

Les mécanismes de connexion et les protocoles seront définis dans le document de sécurité.

## 5.4 Authorization & Policy

Responsabilité :

Décider si une identité peut effectuer une opération sur une ressource donnée.

Les contrôles doivent prendre en compte :

- L'identité.
- L'organisation.
- L'application.
- La ressource.
- L'action demandée.
- Les permissions applicables.

Principe obligatoire :

L'absence de permission démontrée entraîne un refus.

Les autres modules ne doivent pas contourner les décisions d'autorisation.

## 5.5 Knowledge Base Management

Responsabilité :

Gérer les bases de connaissances.

Fonctions :

- Création.
- Modification.
- Activation.
- Désactivation.
- Suppression.
- Configuration.
- Association des sources.
- Gestion des politiques d'accès.

Chaque Knowledge Base doit appartenir à un périmètre organisationnel identifiable.

Ce module possède les règles de gestion des Knowledge Bases, mais ne réalise pas lui-même les recherches vectorielles.

## 5.6 Source Management

Responsabilité :

Gérer les sources de connaissances enregistrées.

Fonctions :

- Enregistrement.
- Configuration.
- Association à une Knowledge Base.
- Gestion des autorisations d'accès.
- Suivi de l'état.
- Désactivation.

Il délègue la récupération effective des données aux connecteurs.

## 5.7 Configuration Management

Responsabilité :

Gérer les configurations nécessaires au fonctionnement du moteur.

Les configurations peuvent concerner :

- Les Knowledge Bases.
- Les stratégies d'ingestion.
- Les embeddings.
- Les fournisseurs.
- La recherche.
- La génération.
- Les limites d'utilisation.

Les secrets et informations sensibles doivent être protégés et ne doivent pas être exposés par les interfaces de configuration.

# 6. Modules de gestion et de préparation des connaissances

## 6.1 Document Management

Responsabilité :

Gérer l'identité et le cycle de vie des documents.

Il est responsable de :

- L'enregistrement des documents.
- L'identification de leur origine.
- La gestion des versions.
- Leur association avec les Knowledge Bases.
- Leur état de traitement.
- Leur modification.
- Leur suppression.

Il doit maintenir la relation entre un document et toutes ses représentations dérivées.

## 6.2 Ingestion Orchestration

Responsabilité :

Coordonner le pipeline d'ingestion.

Il organise les opérations suivantes :

1. Récupération.
2. Validation.
3. Extraction.
4. Normalisation.
5. Découpage.
6. Embeddings.
7. Indexation.
8. Vérification.
9. Activation.

Il ne doit pas implémenter lui-même les algorithmes spécialisés de chaque étape.

Il coordonne les modules responsables.

## 6.3 Source Connectors

Responsabilité :

Récupérer les données depuis les systèmes externes.

Exemples :

- Importation de fichiers.
- Stockages documentaires.
- API externes.
- Répertoires.
- Sources web.
- Systèmes documentaires.

Chaque connecteur doit respecter un contrat commun adapté à sa catégorie.

Les particularités d'un fournisseur ne doivent pas contaminer le cœur du moteur.

## 6.4 Extraction & Normalization

Responsabilité :

Transformer le contenu source en une représentation exploitable.

Extraction :

- Lecture du contenu.
- Récupération des métadonnées.
- Identification de la structure.
- Signalement des erreurs.

Normalisation :

- Harmonisation.
- Nettoyage contrôlé.
- Préservation des informations utiles.
- Production d'un contenu normalisé.

L'extraction doit préserver autant que possible les informations permettant de retrouver le contenu original.

## 6.5 Chunking Engine

Responsabilité :

Découper les contenus en fragments adaptés aux mécanismes de recherche.

Il doit prendre en charge différentes stratégies.

Chaque fragment doit conserver :

- Son document d'origine.
- Sa version.
- Sa position ou ses références structurelles.
- Ses métadonnées.
- Sa relation avec la Knowledge Base.

Le choix des stratégies est défini dans le document 07.

## 6.6 Embedding Engine

Responsabilité :

Transformer les contenus en représentations vectorielles.

Il doit :

- Utiliser des fournisseurs interchangeables.
- Identifier le modèle utilisé.
- Vérifier la compatibilité des représentations.
- Gérer les erreurs.
- Conserver les informations nécessaires à la réindexation.

Le moteur ne doit pas supposer que tous les modèles d'embeddings sont interchangeables sur un même index.

## 6.7 Index Management

Responsabilité :

Gérer la cohérence et le cycle de vie des index.

Il doit :

- Enregistrer les informations d'indexation.
- Détecter les index incomplets ou obsolètes.
- Gérer les générations d'index.
- Organiser les réindexations.
- Retirer les représentations supprimées.
- Contrôler la disponibilité des nouvelles versions.

Il ne doit pas décider des règles métier de gestion des documents.

# 7. Modules de recherche et d'exploitation

## 7.1 Query Orchestration

Responsabilité :

Coordonner le traitement d'une requête.

Il reçoit une requête autorisée et détermine les capacités nécessaires à son traitement.

Il peut solliciter :

- Retrieval.
- Structured Data Access.
- Reranking.
- Context Assembly.
- Generation.

Il ne doit pas contenir les algorithmes de recherche eux-mêmes.

## 7.2 Retrieval Engine

Responsabilité :

Récupérer les connaissances pertinentes.

Il comprend plusieurs capacités :

### Vector Retrieval

Recherche basée sur la similarité vectorielle.

### Keyword Retrieval

Recherche basée sur les correspondances textuelles.

### Hybrid Retrieval

Combinaison des résultats précédents.

Les stratégies doivent pouvoir évoluer indépendamment du reste du moteur.

## 7.3 Reranking Engine

Responsabilité :

Réévaluer et classer les résultats récupérés.

Il peut utiliser différentes stratégies.

Il ne doit pas être obligatoire pour tous les scénarios.

Le remplacement d'un fournisseur de reranking ne doit pas imposer une modification du module de récupération.

## 7.4 Structured Data Access

Responsabilité :

Exploiter directement les données structurées.

Il constitue une capacité distincte du Retrieval documentaire.

Il gère :

- Les connecteurs structurés.
- La définition des accès autorisés.
- La validation des opérations.
- L'exécution contrôlée.
- La normalisation des résultats.
- La provenance des données.

Les modèles de langage ne doivent jamais disposer d'un accès libre aux bases externes.

## 7.5 Context Assembly

Responsabilité :

Construire un ensemble cohérent d'informations pouvant être exploité par le mécanisme de génération.

Il doit :

- Recevoir les résultats documentaires.
- Recevoir les résultats structurés lorsque nécessaire.
- Conserver leur provenance.
- Éliminer les doublons selon des règles définies.
- Respecter les limites de contexte.
- Préparer une représentation cohérente des éléments disponibles.

Ce module ne doit pas inventer ou compléter les informations manquantes.

## 7.6 Generation Engine

Responsabilité :

Produire une réponse à partir du contexte fourni.

Il doit :

- Construire les entrées destinées au modèle.
- Respecter les instructions système.
- Appeler le fournisseur approprié.
- Gérer les erreurs.
- Identifier le modèle utilisé.
- Retourner le résultat avec les métadonnées nécessaires.

La génération doit rester facultative.

Une recherche peut être exécutée sans génération.

## 7.7 Citation & Provenance

Responsabilité :

Maintenir la relation entre les informations exploitées et leurs sources.

Il doit permettre d'identifier :

- Le document d'origine.
- Sa version.
- Le fragment utilisé.
- La position du passage.
- La source structurée éventuelle.
- Les éléments récupérés ayant contribué à la réponse.

Il doit distinguer les sources récupérées des sources effectivement utilisées dans la réponse.

La vérification de la fidélité sémantique des citations sera approfondie dans les spécifications de génération et d'évaluation.

# 8. Services transversaux

Ces services peuvent être utilisés par plusieurs modules.

Ils ne doivent pas absorber les responsabilités métier de ces modules.

## 8.1 Audit Service

Enregistre les opérations importantes :

- Accès.
- Modifications.
- Suppressions.
- Opérations administratives.
- Changements de configuration.
- Opérations sensibles.

## 8.2 Observability Service

Permet de suivre :

- Les performances.
- Les erreurs.
- Les traitements.
- L'utilisation des ressources.
- Les appels externes.

## 8.3 Job Management

Gère le suivi des traitements pouvant dépasser la durée d'une requête normale.

Exemples :

- Ingestion.
- Réindexation.
- Importations volumineuses.
- Suppression de grandes quantités de données.

Il doit permettre le suivi des états, les tentatives de reprise et l'identification des échecs.

La technologie d'exécution reste à définir.

## 8.4 Error Management

Définit les catégories d'erreurs communes et leur traitement.

Les erreurs internes ne doivent pas être exposées directement aux applications clientes.

## 8.5 Lifecycle Coordination

Coordonne les opérations qui affectent plusieurs modules.

Exemples :

- Suppression d'un document et de ses index.
- Réindexation.
- Activation d'une nouvelle version.
- Suppression d'une Knowledge Base.

Ce service coordonne les opérations mais ne remplace pas les règles de gestion des modules propriétaires.

# 9. Contrats entre modules

Les communications doivent reposer sur des contrats explicites.

Un contrat définit :

- L'opération disponible.
- Les données d'entrée.
- Les données de sortie.
- Les erreurs possibles.
- Les conditions d'exécution.
- Les garanties attendues.
- Les règles de sécurité.

Les contrats détaillés seront spécifiés ultérieurement.

## 9.1 Contrats principaux

| Contrat | Fournisseur | Consommateur |
|---|---|---|
| Identity Resolution | Identity Management | Access Layer, Application Services |
| Authorization Decision | Authorization & Policy | Modules protégés |
| Knowledge Base Resolution | KB Management | Ingestion, Query |
| Source Read | Source Connectors | Ingestion |
| Document Registration | Document Management | Ingestion |
| Extraction Result | Extraction | Normalization, Ingestion |
| Normalized Content | Normalization | Chunking |
| Chunk Result | Chunking | Embedding |
| Embedding Result | Embedding | Index Management |
| Index Operation | Index Management | Ingestion, Lifecycle |
| Retrieval Result | Retrieval | Query Orchestration |
| Structured Result | Structured Data Access | Query Orchestration |
| Reranking Result | Reranking | Context Assembly |
| Context Package | Context Assembly | Generation |
| Generation Result | Generation | Citation, API |
| Provenance Result | Citation & Provenance | API |
| Audit Event | Audit Service | Modules concernés |
| Job Status | Job Management | Ingestion, Administration |

# 10. Contrats de données conceptuels

Les contrats devront manipuler des représentations explicites et indépendantes des technologies.

Les concepts suivants devront être définis :

### Identity Context

Contient l'identité authentifiée et les informations de sécurité vérifiées.

### Tenant Context

Identifie le périmètre organisationnel autorisé.

### Knowledge Base Reference

Identifie une base de connaissances et ses informations de configuration nécessaires.

### Source Reference

Identifie l'origine d'une connaissance.

### Document Reference

Identifie un document et sa version.

### Content Representation

Représente le contenu extrait et normalisé.

### Chunk Representation

Représente un fragment associé à son document.

### Embedding Representation

Contient le vecteur et les informations relatives à son modèle de production.

### Retrieval Result

Contient les éléments retrouvés et leurs scores.

### Structured Result

Contient les données récupérées depuis une source structurée et leur provenance.

### Context Package

Contient les éléments retenus pour la génération.

### Generation Result

Contient la réponse, les métadonnées de génération et les informations nécessaires à la traçabilité.

Les structures formelles seront définies dans les documents spécialisés et les contrats API.

# 11. Règles de dépendance

Les règles suivantes sont obligatoires.

## R1 — Aucun accès direct aux données internes d'un autre module

Un module ne peut pas modifier directement les données dont un autre module est propriétaire.

## R2 — Pas de dépendances circulaires

Aucun cycle de dépendances n'est autorisé entre les modules.

## R3 — Pas de dépendance directe aux fournisseurs

Le domaine dépend de contrats, jamais d'une implémentation spécifique de fournisseur.

## R4 — Pas de logique métier dans les adaptateurs

Les adaptateurs convertissent les contrats vers les mécanismes externes.

Ils ne doivent pas devenir propriétaires des règles métier.

## R5 — Autorisation obligatoire

Toute opération protégée doit vérifier les autorisations applicables.

## R6 — Pas de dépendance entre applications clientes

Une application cliente ne doit jamais dépendre du code interne d'une autre application.

## R7 — Pas de dépendance directe entre modules de persistance

Un module ne doit pas contourner un autre module en accédant directement à son stockage.

## R8 — Orchestration sans appropriation

Un orchestrateur coordonne les modules mais ne prend pas possession de leurs règles métier.

## R9 — Interfaces explicites

Les communications intermodules doivent passer par des contrats identifiés.

## R10 — Évolution compatible

Un changement de contrat doit être évalué sur ses conséquences pour les consommateurs.

# 12. Direction des dépendances

Le principe général est le suivant :

```text
APPLICATION CLIENTE
        |
        v
INTERFACE / API
        |
        v
APPLICATION SERVICES
        |
        v
DOMAIN CAPABILITIES
        |
        v
ABSTRACTION CONTRACTS
        |
        v
INFRASTRUCTURE ADAPTERS
        |
        v
EXTERNAL SYSTEMS
```

Les contrats et les abstractions ne doivent pas dépendre des implémentations concrètes.

Les implémentations concrètes doivent respecter les contrats définis par le moteur.

Les services transversaux peuvent être sollicités par plusieurs couches dans le respect de leurs contrats.

# 13. Flux intermodules

## 13.1 Flux d'ingestion

```text
Source Management
       |
       v
Source Connector
       |
       v
Ingestion Orchestration
       |
       v
Document Management
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
Embedding
       |
       v
Index Management
       |
       v
Document Activation
```

Les erreurs et états doivent être transmis à Job Management et Audit.

## 13.2 Flux de recherche

```text
Application Client
       |
       v
API / Access
       |
       v
Identity Resolution
       |
       v
Authorization
       |
       v
Query Orchestration
       |
       +-------------------+
       |                   |
       v                   v
Retrieval          Structured Data Access
       |                   |
       +---------+---------+
                 |
                 v
              Reranking
                 |
                 v
          Context Assembly
                 |
                 v
              Generation
                 |
                 v
       Citation & Provenance
                 |
                 v
               Response
```

La génération peut être ignorée lorsqu'une recherche seule est demandée.

Les résultats provenant de sources structurées et documentaires doivent rester identifiables.

## 13.3 Flux de remplacement d'un fournisseur

```text
DOMAIN MODULE
      |
      v
PROVIDER CONTRACT
      |
      +-------------------+
      |                   |
      v                   v
ADAPTER A             ADAPTER B
      |                   |
      v                   v
PROVIDER A            PROVIDER B
```

Le remplacement ne doit pas modifier les règles métier du module consommateur.

Il peut toutefois nécessiter une migration de données ou une réindexation lorsque les représentations produites ne sont pas compatibles.

# 14. Gestion des communications

Les communications doivent être adaptées à la nature des opérations.

## 14.1 Communications synchrones

À privilégier pour :

- Vérification des permissions.
- Résolution des configurations.
- Lecture de ressources.
- Recherche interactive.
- Opérations nécessitant un résultat immédiat.

## 14.2 Communications asynchrones

À prévoir pour :

- Ingestion volumineuse.
- Extraction longue.
- Calcul d'embeddings en masse.
- Réindexation.
- Suppression de grandes quantités de représentations.

Le mécanisme technique sera défini dans les spécifications de déploiement et d'exécution.

## 14.3 Événements fonctionnels

Les modules peuvent signaler des événements tels que :

- DocumentRegistered.
- DocumentUpdated.
- DocumentProcessingCompleted.
- IndexActivated.
- DocumentDeleted.
- KnowledgeBaseDisabled.

Ces événements doivent représenter des faits métier vérifiables.

Ils ne doivent pas constituer un mécanisme permettant de contourner les contrats des modules propriétaires.

# 15. Fiabilité des interactions

Les communications entre modules doivent respecter les garanties suivantes :

1. Une opération répétée ne doit pas provoquer de doublons non maîtrisés.
2. Les traitements interrompus doivent pouvoir être identifiés.
3. Les échecs doivent être classifiés.
4. Les reprises doivent être contrôlées.
5. Les états intermédiaires doivent être consultables.
6. Les données partiellement traitées ne doivent pas être exposées comme des connaissances actives.
7. Les suppressions doivent atteindre toutes les représentations concernées.
8. Les opérations qui traversent plusieurs modules doivent disposer d'une stratégie de cohérence.

Le système ne doit pas supposer qu'une opération distribuée est automatiquement atomique.

# 16. Gestion de la sécurité entre modules

Chaque opération doit conserver le contexte de sécurité vérifié.

Ce contexte comprend notamment :

- L'identité.
- L'organisation.
- L'application.
- Les permissions.
- Le périmètre des ressources accessibles.

Les modules ne doivent pas accepter aveuglément un identifiant d'organisation ou de Knowledge Base transmis par une application cliente.

Les contrôles doivent être effectués aux frontières de confiance et au niveau des ressources concernées.

Une autorisation accordée pour une recherche documentaire ne donne pas automatiquement le droit d'interroger une source structurée.

Les permissions doivent être adaptées à chaque opération.

# 17. Extensibilité

L'architecture doit permettre l'ajout de nouvelles capacités sans modification générale du moteur.

Les extensions possibles comprennent :

| Extension | Frontière concernée |
|---|---|
| Nouveau format documentaire | Extraction |
| Nouveau connecteur | Source Connectors |
| Nouvelle stratégie de découpage | Chunking |
| Nouveau fournisseur d'embeddings | Embedding |
| Nouveau moteur de stockage | Storage Adapters |
| Nouveau fournisseur LLM | Generation |
| Nouveau fournisseur de reranking | Reranking |
| Nouvelle stratégie de recherche | Retrieval |
| Nouvelle source structurée | Structured Data Access |
| Nouveau mécanisme de traçabilité | Provenance |

Chaque extension doit respecter le contrat de sa catégorie.

Elle doit également déclarer les capacités, limites et incompatibilités pertinentes.

# 18. Testabilité des modules

Chaque module doit posséder des tests adaptés à sa responsabilité.

## Tests unitaires

Vérification de la logique interne du module sans dépendance réelle aux fournisseurs externes.

## Tests de contrat

Vérification du respect des interfaces entre modules et adaptateurs.

## Tests d'intégration

Vérification de plusieurs modules fonctionnant ensemble.

## Tests de sécurité

Vérification des permissions et de l'isolation.

## Tests de résilience

Vérification du comportement en cas d'échec ou d'indisponibilité d'un composant externe.

## Tests end-to-end

Vérification des parcours complets depuis une application cliente jusqu'au résultat final.

# 19. Traçabilité avec les exigences

| Domaine modulaire | Exigences principales |
|---|---|
| Access and Governance | FR-001 à FR-006 |
| Source Management | FR-007 |
| Knowledge Lifecycle | FR-008 à FR-013 |
| Retrieval | FR-014 à FR-017 |
| Generation | FR-018 à FR-021 |
| Structured Data Access | FR-022 à FR-024 |
| Interfaces et orchestration | FR-025 et FR-026 |
| Administration et supervision | FR-027 et FR-028 |
| Services transversaux | NFR-001 à NFR-020 |

Cette correspondance doit être affinée dans les spécifications détaillées et les tests.

# 20. Éléments explicitement non décidés

Ce document ne fixe pas :

- Le langage de programmation.
- La structure physique des fichiers.
- Le nombre de packages.
- Le nombre de services déployables.
- Le framework API.
- La technologie de stockage.
- Le système de traitement asynchrone.
- Les protocoles de communication.
- Les structures SQL.
- Les schémas JSON définitifs.
- Les fournisseurs externes.

Ces choix doivent faire l'objet d'études dédiées.

# 21. Conditions de validation

La validation de cette spécification nécessite :

1. L'approbation des couches logiques.
2. L'approbation des frontières entre modules.
3. La validation des responsabilités.
4. La validation des règles de dépendance.
5. L'examen des contrats intermodules.
6. La validation des flux d'ingestion et de recherche.
7. La confirmation de l'indépendance des fournisseurs.
8. L'examen de la gestion des opérations distribuées.
9. La cohérence avec l'architecture globale.
10. La cohérence avec les exigences fonctionnelles et non fonctionnelles.

# 22. Conclusion

L'architecture modulaire de Universal RAG Engine repose sur des frontières fonctionnelles explicites, des responsabilités maîtrisées et des contrats indépendants des implémentations.

Elle doit permettre de remplacer, étendre ou faire évoluer un composant sans remettre en cause l'ensemble du moteur.

Les modules constituent des unités de conception et de responsabilité. Leur transformation éventuelle en packages, processus ou services physiques reste une décision ultérieure.

**Le moteur doit évoluer par remplacement et extension de composants, et non par réécriture permanente de son cœur.**
