# Universal RAG Engine
## Registre des décisions architecturales

**Version :** 1.0
**Statut :** VALIDATED

---

# 1. Objectif

Ce registre centralise les décisions architecturales et techniques prises durant la conception et le développement de Universal RAG Engine.

Il permet de conserver :

- Les décisions approuvées.
- Leur justification.
- Les alternatives envisagées.
- Les conséquences.
- Les dépendances concernées.
- Les décisions reportées ou remplacées.

Il constitue une référence pour éviter les contradictions architecturales.

# 2. Statuts des décisions

| Statut | Signification |
|---|---|
| PROPOSED | Proposition non validée |
| ACCEPTED | Décision validée |
| REJECTED | Décision rejetée |
| DEFERRED | Décision reportée |
| SUPERSEDED | Décision remplacée |

Une décision ne peut être considérée comme ACCEPTED qu'après validation explicite.

# 3. Décisions fondatrices

## DEC-001 — Indépendance métier

**Statut : ACCEPTED**

**Décision :**

Universal RAG Engine doit être indépendant de tout domaine métier.

**Justification :**

Le moteur doit pouvoir être utilisé dans plusieurs secteurs sans modification de son cœur fonctionnel.

**Conséquences :**

- Aucune logique spécifique à Dental Clinic dans le cœur.
- Les applications clientes restent indépendantes.
- Les fonctionnalités métier appartiennent aux applications clientes.

**Source :** 00_VISION_ET_OBJECTIFS.md

---

## DEC-002 — Indépendance des applications clientes

**Statut : ACCEPTED**

**Décision :**

Les applications clientes doivent pouvoir communiquer avec le moteur sans dépendre de son implémentation interne.

**Justification :**

Permettre la réutilisation du moteur dans différents environnements.

**Conséquences :**

- Interfaces publiques documentées.
- Séparation des responsabilités.
- Contrats d'intégration stables.

**Source :** 00_VISION_ET_OBJECTIFS.md

---

## DEC-003 — Gestion de plusieurs organisations et bases de connaissances

**Statut : ACCEPTED**

**Décision :**

Le moteur doit prévoir la gestion de plusieurs organisations et de plusieurs bases de connaissances indépendantes.

**Justification :**

Permettre à plusieurs clients d'utiliser une infrastructure commune sans mélanger leurs connaissances.

**Conséquences :**

- Gestion des organisations.
- Gestion des Knowledge Bases.
- Isolation des données.
- Gestion des permissions.

Les mécanismes techniques d'isolation restent à définir.

**Source :** 00_VISION_ET_OBJECTIFS.md

---

## DEC-004 — Indépendance des fournisseurs d'intelligence artificielle

**Statut : ACCEPTED**

**Décision :**

Le moteur doit pouvoir utiliser différents fournisseurs de LLM et d'embeddings.

**Justification :**

Éviter une dépendance permanente à un fournisseur particulier.

**Conséquences :**

- Interfaces de fournisseurs interchangeables.
- Configuration des modèles.
- Gestion des différences entre fournisseurs.

Les technologies et fournisseurs ne sont pas encore sélectionnés.

**Source :** 00_VISION_ET_OBJECTIFS.md

---

## DEC-005 — Traçabilité des réponses

**Statut : ACCEPTED**

**Décision :**

Les réponses doivent pouvoir être reliées aux documents et passages qui les justifient.

**Justification :**

Permettre de vérifier l'origine des informations utilisées.

**Conséquences :**

- Conservation des références documentaires.
- Identification des passages récupérés.
- Traçabilité du processus de génération.

**Source :** 00_VISION_ET_OBJECTIFS.md

---

## DEC-006 — Prise en charge des données structurées et non structurées

**Statut : ACCEPTED**

**Décision :**

Le moteur doit pouvoir exploiter les documents non structurés et les données structurées.

Ces deux catégories doivent disposer de mécanismes d'accès adaptés.

**Justification :**

Ne pas limiter Universal RAG Engine à la recherche documentaire classique.

**Conséquences :**

- Pipeline documentaire.
- Accès aux données structurées.
- Possibilité de combiner les résultats.

Les architectures détaillées restent à définir.

**Source :** 00_VISION_ET_OBJECTIFS.md

---

## DEC-007 — Documentation avant développement

**Statut : ACCEPTED**

**Décision :**

Les spécifications et les dépendances doivent être étudiées et validées avant le développement des composants concernés.

**Justification :**

Éviter les incohérences architecturales et les réécritures inutiles.

**Conséquences :**

- Validation progressive des documents.
- Identification des dépendances.
- Traçabilité des modifications.
- Développement fondé sur des spécifications approuvées.

**Sources :**
- 00_VISION_ET_OBJECTIFS.md
- DEPENDENCY_MAP.md

# 4. Décisions techniques en attente

Aucune technologie majeure n'est encore définitivement sélectionnée.

Les sujets suivants nécessitent une étude :

| ID | Sujet | Statut |
|---|---|---|
| TD-001 | Langage et environnement | DEFERRED |
| TD-002 | Framework API | DEFERRED |
| TD-003 | Base de données principale | DEFERRED |
| TD-004 | Stockage vectoriel | DEFERRED |
| TD-005 | Fournisseurs d'embeddings | DEFERRED |
| TD-006 | Fournisseurs LLM | DEFERRED |
| TD-007 | Stratégies de chunking | DEFERRED |
| TD-008 | Recherche hybride | DEFERRED |
| TD-009 | Architecture multi-tenant | DEFERRED |
| TD-010 | Stockage documentaire | DEFERRED |
| TD-011 | Authentification et autorisation | DEFERRED |
| TD-012 | Infrastructure de déploiement | DEFERRED |

Ces sujets ne sont pas des décisions rejetées. Ils sont volontairement reportés jusqu'à ce que les exigences et dépendances soient suffisamment définies.

# 5. Modèle de décision

Toute nouvelle décision devra respecter le modèle suivant :

**Identifiant :** DEC-XXX

**Titre :**

**Date :**

**Statut :**

**Contexte :**

Quel problème ou besoin nécessite une décision ?

**Décision :**

Quel choix est retenu ?

**Alternatives étudiées :**

Quelles autres solutions ont été examinées ?

**Justification :**

Pourquoi cette décision est-elle préférable ?

**Conséquences :**

Quels sont les avantages, limites et impacts ?

**Dépendances :**

Quels documents ou composants sont concernés ?

**Sources :**

Quels documents ou éléments justifient cette décision ?

# 6. Gestion des ADR

Les décisions architecturales complexes pourront être détaillées dans des fichiers individuels :

docs/adr/

Exemples futurs :

- ADR-001 : Architecture multi-tenant.
- ADR-002 : Stratégie de stockage vectoriel.
- ADR-003 : Architecture des fournisseurs LLM.
- ADR-004 : Stratégie de recherche hybride.

Ces exemples ne constituent pas des décisions déjà prises.

# 7. Règles de gouvernance

1. Aucune décision proposée ne doit être présentée comme validée.
2. Toute décision importante doit avoir un identifiant unique.
3. Les justifications doivent être conservées.
4. Les alternatives pertinentes doivent être documentées.
5. Les conséquences doivent être identifiées.
6. Une décision validée ne doit pas être modifiée silencieusement.
7. Une décision remplacée doit conserver son historique.
8. Les documents dépendants doivent être mis à jour lorsqu'une décision les concerne.
9. Les choix techniques doivent être précédés d'une analyse adaptée.
10. Le registre doit rester cohérent avec les spécifications validées.

# 8. Conclusion

Le Decision Log constitue la mémoire architecturale de Universal RAG Engine.

Il permet de comprendre non seulement ce qui a été décidé, mais également pourquoi cela a été décidé.

**Aucune décision architecturale importante ne doit rester implicite.**
