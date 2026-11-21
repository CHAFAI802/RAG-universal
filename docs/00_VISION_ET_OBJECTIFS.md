# Universal RAG Engine
## Document 00 — Vision et objectifs

**Version :** 1.0
**Statut :** Validated
**Projet :** RAG-universal

---

# 1. Présentation du projet

Universal RAG Engine est un moteur autonome de recherche augmentée par génération (Retrieval-Augmented Generation).

Il a pour mission de permettre à différentes applications, organisations et domaines métier d'exploiter leurs propres connaissances à travers une interface commune.

Le moteur doit pouvoir importer, organiser, indexer, rechercher et exploiter des connaissances provenant de différentes sources.

Il ne doit contenir aucune dépendance fonctionnelle à un domaine métier particulier.

Dental Clinic pourra constituer une première application cliente, mais ne déterminera ni l'architecture ni les limites fonctionnelles du moteur.

# 2. Vision à long terme

Construire un moteur RAG universel, durable, extensible et indépendant des applications qui l'utilisent.

À terme, Universal RAG Engine devra pouvoir être utilisé :

- Comme service autonome.
- Comme backend d'une application SaaS.
- Comme composant d'une application locale.
- Comme service interne d'une entreprise.
- Comme moteur de connaissances pour des agents IA.
- Comme infrastructure de recherche documentaire.

L'objectif est de construire un véritable produit logiciel réutilisable.

# 3. Problématique

Les applications utilisant l'intelligence artificielle rencontrent plusieurs difficultés :

- Les modèles de langage ne connaissent pas nécessairement les informations propres à chaque organisation.
- Les connaissances sont dispersées dans différents formats et systèmes.
- Les réponses peuvent contenir des informations inventées.
- Les données évoluent et nécessitent une actualisation des index.
- Les applications développent souvent leurs propres mécanismes de recherche documentaire.
- Le changement de fournisseur d'IA peut entraîner une dépendance technique.

Universal RAG Engine doit apporter une infrastructure commune pour résoudre ces problèmes.

# 4. Objectifs principaux

## 4.1 Centralisation des connaissances

Permettre l'importation de connaissances depuis différentes sources :

- PDF.
- DOCX.
- TXT.
- Markdown.
- HTML.
- Bases de données.
- API externes.
- Documentation technique.
- Autres sources intégrables.

## 4.2 Gestion indépendante des connaissances

Permettre de créer plusieurs bases de connaissances indépendantes.

Chaque base doit disposer de ses propres configurations, documents, index et règles d'accès.

## 4.3 Recherche intelligente

Développer plusieurs mécanismes de recherche :

- Recherche vectorielle.
- Recherche textuelle.
- Recherche hybride.
- Filtrage par métadonnées.
- Classement des résultats.
- Reranking.

## 4.4 Génération augmentée

Permettre à différents modèles de langage de produire des réponses à partir des informations récupérées.

Les réponses doivent être accompagnées de références permettant de retrouver les documents et passages utilisés.

## 4.5 Gestion des données structurées

Ne pas limiter le moteur aux documents.

Prévoir des mécanismes permettant d'exploiter des données provenant de bases relationnelles et d'autres systèmes structurés.

## 4.6 Interopérabilité

Permettre à différentes applications de communiquer avec le moteur à travers des interfaces documentées et stables.

# 5. Principes architecturaux fondamentaux

Les principes suivants constituent les règles fondamentales du projet.

### P1 — Indépendance métier

Le moteur ne doit contenir aucune logique spécifique à Dental Clinic ou à une autre application métier.

### P2 — Indépendance des applications clientes

Les applications clientes doivent pouvoir utiliser le moteur sans connaître son implémentation interne.

### P3 — Indépendance des fournisseurs

Les fournisseurs de LLM et d'embeddings doivent pouvoir être remplacés sans réécrire le cœur du moteur.

### P4 — Modularité

Les composants doivent avoir des responsabilités clairement définies et des interfaces indépendantes.

### P5 — Extensibilité

L'ajout d'un nouveau connecteur, extracteur, fournisseur ou mécanisme de recherche ne doit pas nécessiter une refonte générale.

### P6 — Isolation des connaissances

Les données de différentes organisations et applications doivent être protégées contre tout accès non autorisé.

### P7 — Traçabilité

Les réponses doivent pouvoir être reliées aux documents et passages qui les justifient.

### P8 — Fiabilité

Le moteur doit pouvoir reconnaître les situations dans lesquelles les connaissances disponibles sont insuffisantes.

### P9 — Maintenabilité

Le code doit être organisé, documenté, testé et évolutif.

### P10 — Évolutivité

L'architecture doit permettre une augmentation progressive du volume de documents, du nombre d'utilisateurs et des requêtes simultanées.

# 6. Gestion des bases de connaissances

Le concept central du système sera la Knowledge Base.

Une Knowledge Base représente un espace organisé de connaissances.

Elle possède notamment :

- Un identifiant unique.
- Un nom.
- Une description.
- Une organisation propriétaire.
- Des paramètres d'indexation.
- Une configuration d'embeddings.
- Une stratégie de recherche.
- Des règles d'accès.
- Un état opérationnel.
- Des dates de création et de modification.

Une organisation pourra posséder plusieurs bases de connaissances.

Exemple :

Organisation A :
- Documentation technique.
- Procédures internes.
- Documentation commerciale.

Organisation B :
- Documentation médicale.
- Protocoles.
- Documentation administrative.

Les connaissances doivent rester isolées selon les règles d'accès définies.

# 7. Types de connaissances

Le moteur devra progressivement prendre en charge deux grandes catégories.

## 7.1 Données non structurées

Documents, fichiers et contenus textuels.

Exemples :
- PDF.
- DOCX.
- HTML.
- Documentation.
- Manuels.
- Articles.

## 7.2 Données structurées

Informations organisées dans des structures exploitables directement.

Exemples :
- Tables relationnelles.
- Enregistrements.
- Données provenant d'API.
- Données métier.
- Données tabulaires.

Le système devra pouvoir combiner les résultats provenant de ces deux catégories.

# 8. Utilisateurs et applications clientes

Universal RAG Engine doit répondre aux besoins de plusieurs catégories d'utilisateurs.

### Administrateurs de plateforme

Gestion globale du moteur, des organisations, des ressources et des configurations.

### Administrateurs d'organisation

Gestion des bases de connaissances et des utilisateurs de leur organisation.

### Développeurs

Intégration du moteur dans leurs applications à travers les interfaces publiques.

### Utilisateurs finaux

Interrogation des connaissances auxquelles ils ont accès.

### Agents IA

Utilisation du moteur comme source externe de connaissances.

# 9. Périmètre fonctionnel

Le produit devra progressivement couvrir :

1. Gestion des organisations.
2. Gestion des utilisateurs et permissions.
3. Gestion des bases de connaissances.
4. Gestion des sources de données.
5. Ingestion documentaire.
6. Extraction et normalisation.
7. Découpage intelligent des contenus.
8. Calcul des embeddings.
9. Indexation.
10. Recherche vectorielle.
11. Recherche textuelle.
12. Recherche hybride.
13. Classement des résultats.
14. Génération augmentée.
15. Gestion des fournisseurs LLM.
16. Gestion des données structurées.
17. Traçabilité des réponses.
18. Évaluation des performances.
19. Journalisation et supervision.

# 10. Hors périmètre initial

Les fonctionnalités suivantes ne constituent pas le cœur du produit :

- Développement d'une application métier complète.
- Développement d'un assistant médical spécifique.
- Remplacement des applications clientes.
- Création d'un modèle de langage propriétaire.
- Entraînement initial d'un LLM généraliste.
- Automatisation complète des processus métier.
- Développement d'une interface conversationnelle obligatoire.

Ces fonctionnalités pourront éventuellement être développées séparément ou intégrées par des applications clientes.

# 11. Critères de réussite

Le projet sera considéré comme ayant atteint ses objectifs fondamentaux lorsque :

1. Une application externe pourra utiliser le moteur sans dépendre de son code interne.
2. Plusieurs organisations pourront exploiter une même infrastructure avec isolation effective.
3. Plusieurs bases de connaissances pourront fonctionner indépendamment.
4. Le système pourra importer plusieurs formats documentaires.
5. Le moteur pourra effectuer des recherches vectorielles et textuelles.
6. Un mécanisme de recherche hybride pourra combiner leurs résultats.
7. Plusieurs fournisseurs d'embeddings pourront être intégrés.
8. Plusieurs fournisseurs LLM pourront être utilisés.
9. Les réponses pourront présenter leurs sources.
10. Les données structurées pourront être exploitées sans les transformer artificiellement en documents.
11. Les composants pourront évoluer sans imposer une refonte globale.
12. Les tests pourront démontrer le respect des exigences de sécurité et d'isolation.

# 12. Gouvernance technique

Les décisions architecturales devront respecter les principes définis dans ce document.

Toute décision importante devra être documentée.

Les modifications de conception devront être justifiées et accompagnées de leurs conséquences.

Les spécifications techniques constitueront la référence avant le développement.

Aucune application cliente ne devra imposer une dépendance métier dans le cœur du moteur.

# 13. Conclusion

Universal RAG Engine est conçu comme une infrastructure autonome de gestion et d'exploitation des connaissances.

Sa valeur ne réside pas dans son utilisation pour un domaine particulier, mais dans sa capacité à s'adapter à différents domaines sans modifier son cœur architectural.

**Un seul moteur. Plusieurs organisations. Plusieurs bases de connaissances. Plusieurs applications.**

C'est le principe fondateur du projet.
