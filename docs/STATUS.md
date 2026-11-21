# Universal RAG Engine — Suivi documentaire

## Vision du projet

Construire un moteur RAG universel, durable, extensible
et indépendant des applications clientes.

## Documents fondateurs

| ID | Document | Version | Statut |
|---|---|---|---|
| 00 | Vision et objectifs | 1.0 | VALIDATED |
| DM | Cartographie des dépendances | 1.0 | VALIDATED |
| DL | Registre des décisions architecturales | 1.0 | VALIDATED |

## Spécifications techniques

| ID | Document | Version | Statut |
|---|---|---|---|
| 01 | Cahier des charges | 1.0 | VALIDATED |
| 02 | Architecture globale | 1.0 | VALIDATED |
| 03 | Architecture modulaire | 1.0 | VALIDATED |
| 04 | Modèle de données | 1.0 | VALIDATED |
| 05 | Knowledge Bases | 1.0 | VALIDATED |
| 06 | Pipeline ingestion | 1.0 | VALIDATED |
| 07 | Chunking et embeddings | 1.0 | VALIDATED |
| 08 | Moteur de recherche | 1.0 | VALIDATED |
| 09 | Génération et LLM | 1.0 | VALIDATED |
| 10 | API | 1.0 | VALIDATED |
| 11 | Sécurité et isolation | 1.0 | VALIDATED |
| 12 | Données structurées | 1.0 | VALIDATED |
| 13 | Tests et évaluation | 1.0 | VALIDATED |
| 14 | Déploiement et scalabilité | 1.0 | VALIDATED |
| 15 | Roadmap technique | 1.0 | VALIDATED |

## Règles de gouvernance

1. Aucun document validé ne peut être modifié sans nouvelle validation.
2. Les dépendances doivent être identifiées avant toute conception détaillée.
3. Les décisions architecturales doivent être documentées.
4. Aucune décision proposée ne doit être considérée comme validée.
5. Aucun développement avant validation des spécifications nécessaires.
6. Toute modification architecturale doit être justifiée.
7. Les documents dépendants doivent être actualisés après une décision ayant un impact sur leur contenu.

## Audit du dépôt distant — 2026-11-21

- Dépôt public : `CHAFAI802/RAG-universal`.
- Branche de référence : `main`.
- Commit audité : `e9e4b37d20e2520c3430e3a6bbeea8a2e6273663`.
- Historique distant visible : un commit initial, sans parent.
- Périmètre actuel : dépôt au stade documentaire, sans code applicatif
  ni configuration d'exécution recensée. Les fichiers présents sont
  principalement des spécifications Markdown et les fichiers auxiliaires
  du dépôt. Aucun secret applicatif n'est attendu dans ce périmètre.
- Points documentaires relevés : nomenclature des phases de conception clarifiée ;
  définition de `Tenant` alignée sur le modèle conceptuel ; licence du dépôt encore
  à décider explicitement.

## Prochaine étape

Préparer la phase P0 de réalisation décrite dans `15_ROADMAP_TECHNIQUE.md` :
matrice de traçabilité exigences/capacités/tests, registre des décisions à instruire,
étude comparative des options techniques, backlog initial et critères de Definition
of Done. Aucun choix technologique ne doit être considéré comme validé avant décision
explicite.
