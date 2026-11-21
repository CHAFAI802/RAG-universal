# Universal RAG Engine

Moteur de recherche augmentée par génération (RAG), conçu pour être
autonome, durable, extensible et indépendant des applications clientes.

Le projet vise à fournir une infrastructure réutilisable pour ingérer,
organiser, indexer, rechercher et exploiter des connaissances documentaires
et structurées, tout en préservant les contrôles d'accès, l'isolation et
la traçabilité.

## Principes directeurs

- Indépendance vis-à-vis des domaines métier et des applications clientes.
- Séparation entre ingestion, recherche, génération et accès aux données structurées.
- Contrôle des autorisations côté moteur et isolation des organisations.
- Traçabilité des sources, résultats, réponses et décisions.
- Neutralité vis-à-vis des fournisseurs et technologies tant que les études
  et décisions correspondantes ne sont pas validées.
- Documentation et décisions explicites avant toute implémentation structurante.

## État du projet

Le dépôt contient actuellement les spécifications et documents de gouvernance.
Il ne constitue pas encore une version logicielle implémentée. Les choix
technologiques majeurs restent à instruire et à enregistrer dans le registre
des décisions.

## Documentation

| Document | Contenu |
|---|---|
| [Vision et objectifs](docs/00_VISION_ET_OBJECTIFS.md) | Finalité et principes fondateurs |
| [Cahier des charges](docs/01_CAHIER_DES_CHARGES.md) | Exigences fonctionnelles et non fonctionnelles |
| [Architecture globale](docs/02_ARCHITECTURE_GLOBALE.md) | Vue d'ensemble du système |
| [Architecture modulaire](docs/03_ARCHITECTURE_MODULAIRE.md) | Responsabilités et frontières des modules |
| [Modèle de données](docs/04_MODELE_DE_DONNEES.md) | Modèle conceptuel des données |
| [Knowledge Bases](docs/05_KNOWLEDGE_BASES.md) | Organisation des bases de connaissances |
| [Pipeline d'ingestion](docs/06_PIPELINE_INGESTION.md) | Acquisition et cycle de vie des contenus |
| [Chunking et embeddings](docs/07_CHUNKING_ET_EMBEDDINGS.md) | Préparation des contenus |
| [Moteur de recherche](docs/08_MOTEUR_DE_RECHERCHE.md) | Stratégies de retrieval |
| [Génération et LLM](docs/09_GENERATION_ET_LLM.md) | Génération et orchestration |
| [API](docs/10_API_SPECIFICATION.md) | Contrats d'intégration |
| [Sécurité et isolation](docs/11_SECURITE_ET_ISOLATION.md) | Autorisations et protection des périmètres |
| [Données structurées](docs/12_DONNEES_STRUCTUREES.md) | Accès contrôlé aux ressources structurées |
| [Tests et évaluation](docs/13_TESTS_ET_EVALUATION.md) | Vérification fonctionnelle et qualité RAG |
| [Déploiement et scalabilité](docs/14_DEPLOIEMENT_ET_SCALABILITE.md) | Exigences opérationnelles |
| [Roadmap technique](docs/15_ROADMAP_TECHNIQUE.md) | Phases de réalisation |
| [Registre des décisions](docs/DECISION_LOG.md) | Décisions acceptées et sujets reportés |
| [Cartographie des dépendances](docs/DEPENDENCY_MAP.md) | Ordre de conception et dépendances |
| [Suivi documentaire](docs/STATUS.md) | Statut des documents et prochaines étapes |

## Gouvernance

Les documents marqués `VALIDATED` constituent les références approuvées.
Toute évolution de leur contenu doit être justifiée, tracée et validée.
Une proposition ou une étude ne vaut pas décision tant qu'elle n'a pas été
explicitement acceptée et enregistrée.

## Licence

Aucune licence n'est actuellement déclarée dans le dépôt. Les conditions
de réutilisation et de distribution restent donc à décider explicitement.
