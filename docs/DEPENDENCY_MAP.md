# Universal RAG Engine
## Cartographie des dépendances

**Version :** 1.0
**Statut :** VALIDATED
**Document :** DEPENDENCY_MAP.md

---

# 1. Objectif

Ce document définit les relations de dépendance entre les spécifications, les composants fonctionnels et les infrastructures de Universal RAG Engine.

Son objectif est d'établir un ordre cohérent de conception et d'éviter les décisions techniques prématurées.

Aucun composant ne doit être conçu indépendamment des contraintes et interfaces avec lesquelles il devra fonctionner.

# 2. Types de dépendances

## 2.1 Dépendances documentaires

Relations entre les documents de spécification.

Exemple : l'architecture globale dépend du cahier des charges.

## 2.2 Dépendances fonctionnelles

Relations entre les composants logiciels.

Exemple : le moteur de recherche dépend du système d'indexation.

## 2.3 Dépendances techniques

Relations entre les composants et les infrastructures nécessaires à leur fonctionnement.

Exemple : le stockage vectoriel nécessite un moteur de stockage compatible.

Ces dépendances ne seront précisées qu'après les études techniques correspondantes.

# 3. Dépendances documentaires

| Document | Dépendances principales |
|---|---|
| 00 — Vision | Aucune |
| 01 — Cahier des charges | 00 |
| 02 — Architecture globale | 00, 01 |
| 03 — Architecture modulaire | 02 |
| 04 — Modèle de données | 01, 02, 03 |
| 05 — Knowledge Bases | 01, 02, 03, 04 |
| 06 — Pipeline ingestion | 02, 03, 04, 05 |
| 07 — Chunking et embeddings | 03, 06 |
| 08 — Moteur de recherche | 03, 04, 05, 07 |
| 09 — Génération et LLM | 03, 08 |
| 10 — API | 01, 02, 03, 05, 08, 09 |
| 11 — Sécurité et isolation | 01, 02, 03, 04, 05, 10 |
| 12 — Données structurées | 01, 02, 03, 04, 05, 08 |
| 13 — Tests et évaluation | 01 à 12 |
| 14 — Déploiement et scalabilité | 02, 03, 04, 11, 13 |
| 15 — Roadmap technique | Ensemble des spécifications validées |

Ces dépendances constituent une première proposition. Elles devront être affinées lorsque les responsabilités de chaque document seront définies.

# 4. Dépendances fonctionnelles

## 4.1 Gestion des connaissances

Composants concernés :

- Organisations.
- Utilisateurs.
- Permissions.
- Knowledge Bases.
- Sources de données.
- Métadonnées.

La gestion des connaissances constitue une fondation du système.

## 4.2 Ingestion documentaire

Relations :

Sources de données → Connecteurs → Extracteurs → Normalisation → Chunking → Embeddings → Indexation.

Chaque étape doit avoir une interface définie.

## 4.3 Recherche

Relations :

Question utilisateur → Analyse → Recherche vectorielle et textuelle → Fusion → Reranking → Résultats.

Le système doit pouvoir effectuer des recherches indépendamment de la génération LLM.

## 4.4 Génération

Relations :

Question → Retrieval → Construction du contexte → Fournisseur LLM → Réponse → Références.

La génération ne doit pas être responsable de la recherche documentaire.

## 4.5 Données structurées

Relations :

Application cliente → Connecteur structuré → Validation des permissions → Exécution contrôlée → Résultats.

Les données structurées ne doivent pas être artificiellement transformées en documents pour pouvoir être exploitées.

# 5. Dépendances transversales

Certaines exigences concernent plusieurs composants.

| Exigence | Composants concernés |
|---|---|
| Sécurité | Tous les composants |
| Isolation multi-tenant | Stockage, recherche, API, génération |
| Traçabilité | Ingestion, indexation, retrieval, génération |
| Journalisation | API, ingestion, recherche, génération |
| Gestion des erreurs | Tous les composants |
| Configuration | Fournisseurs, indexation, recherche |
| Observabilité | API, traitements et infrastructure |
| Évaluation | Ingestion, retrieval et génération |

Ces exigences doivent être prises en compte dès la conception des interfaces.

# 6. Principes de gestion des dépendances

1. Une dépendance doit être identifiée avant l'implémentation du composant concerné.
2. Les interfaces entre composants doivent être documentées.
3. Aucun module ne doit dépendre directement de l'implémentation interne d'un autre module lorsque cela peut être évité.
4. Les dépendances circulaires doivent être évitées.
5. Les fournisseurs externes doivent être isolés derrière des interfaces.
6. Les décisions techniques doivent être documentées.
7. Toute modification d'une interface doit entraîner une analyse de ses impacts.
8. Les exigences de sécurité doivent être intégrées transversalement.

# 7. Phases de conception proposées (D0 à D13)

| Phase | Travail | Prérequis |
|---|---|---|
| D0 | Vision et objectifs | Aucun |
| D1 | Cahier des charges | D0 |
| D2 | Architecture globale | D1 |
| D3 | Architecture modulaire | D2 |
| D4 | Modèle de données et sécurité | D2, D3 |
| D5 | Knowledge Bases et API | D3, D4 |
| D6 | Ingestion documentaire | D4, D5 |
| D7 | Chunking et embeddings | D6 |
| D8 | Recherche hybride | D5, D7 |
| D9 | Génération LLM | D8 |
| D10 | Données structurées | D4, D5, D8 |
| D11 | Tests et évaluation | Selon composants concernés |
| D12 | Déploiement et scalabilité | Architecture et validation |
| D13 | Roadmap définitive | Ensemble des phases |

Cet ordre est un ordre de conception proposé, pas une obligation de développer les composants dans le même ordre.

# 8. Gestion des changements

Toute modification importante d'une dépendance devra être accompagnée de :

- L'identification de la dépendance modifiée.
- La justification du changement.
- L'identification des composants impactés.
- L'analyse des conséquences.
- La mise à jour des documents concernés.
- Une validation explicite.

# 9. Conclusion

La cartographie des dépendances constitue un instrument de gouvernance technique.

Elle permet de construire Universal RAG Engine progressivement, en maintenant la cohérence entre les besoins, l'architecture, les modules et les infrastructures.

Elle devra évoluer avec le projet.

**Aucune dépendance importante ne doit être ignorée ou laissée implicite.**
