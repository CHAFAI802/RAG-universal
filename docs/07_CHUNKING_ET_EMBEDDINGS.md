# UNIVERSAL RAG ENGINE

## Document 07 — Chunking et embeddings

**Version :** 1.0
**Statut :** VALIDATED
**Projet :** RAG-universal

---

# 1. Objectif

Ce document définit le rôle et les principes fonctionnels des capacités de découpage (Chunking) et de vectorisation (Embeddings) dans Universal RAG Engine.

Il précise :

- La place du Chunking et des Embeddings dans le cycle de préparation des connaissances.
- Les relations entre Extracted Content, Chunk Set, Chunk, Provider, Model Reference et Embedding.
- Les principes de production et de traçabilité des fragments et représentations vectorielles.
- La distinction entre embeddings documentaires et embeddings de requêtes.
- Les conditions générales de compatibilité nécessaires à la recherche vectorielle.
- Les frontières avec le pipeline d'ingestion, l'indexation et le moteur de recherche.

Ce document reste au niveau conceptuel et fonctionnel. Il ne définit pas les algorithmes, bibliothèques, modèles, dimensions vectorielles, paramètres numériques, structures physiques ou technologies de stockage.

# 2. Références et dépendances

Cette spécification s'appuie sur les documents suivants :

- `00_VISION_ET_OBJECTIFS.md` — vision, indépendance métier et principes fondateurs.
- `DEPENDENCY_MAP.md` — dépendances entre les spécifications.
- `DECISION_LOG.md` — décisions architecturales validées.
- `01_CAHIER_DES_CHARGES.md` — exigences fonctionnelles et non fonctionnelles.
- `02_ARCHITECTURE_GLOBALE.md` — organisation générale du moteur.
- `03_ARCHITECTURE_MODULAIRE.md` — responsabilités des modules.
- `04_MODELE_DE_DONNEES.md` — modèle conceptuel et relations des entités.
- `05_KNOWLEDGE_BASES.md` — gestion des espaces de connaissances, sources et associations.
- `06_PIPELINE_INGESTION.md` — parcours documentaire jusqu'à la préparation et à l'indexation.

Les concepts de référence sont notamment :

- `Document Version` et `Extracted Content`.
- `Chunk Set` et `Chunk`.
- `Provider` et `Model Reference`.
- `Embedding`.
- `Knowledge Base` et `Knowledge Base Item Association`.
- `Index`, `Index Configuration`, `Index Generation` et `Index Entry`.
- `Query` et `Retrieval Result`.

# 3. Définition et distinction des deux capacités

## 3.1 Chunking

Le Chunking est la capacité qui transforme un contenu extrait en unités de contenu plus petites, cohérentes et exploitables par les mécanismes de recherche.

Il produit un `Chunk Set` composé d'un ou plusieurs `Chunks`.

Le Chunking organise le contenu ; il ne produit pas lui-même une représentation vectorielle et ne décide pas de l'index dans lequel les fragments seront utilisés.

## 3.2 Embeddings

L'Embedding est la capacité qui produit une représentation vectorielle à partir d'un contenu pris en charge, principalement un `Chunk` pour les connaissances documentaires.

Chaque représentation doit pouvoir être reliée au contenu qu'elle représente et au `Model Reference` utilisé pour la produire.

La vectorisation ne modifie ni le contenu original, ni sa version documentaire, ni le `Chunk` source.

## 3.3 Séparation des responsabilités

Chunking et Embeddings sont deux capacités complémentaires mais distinctes :

- Chunking détermine les unités de contenu.
- Embeddings représente un contenu sous forme vectorielle.
- Index Management détermine comment les représentations sont prises en compte dans un index.
- Retrieval exploite les index compatibles pour rechercher des connaissances.

Aucune de ces capacités ne doit absorber les responsabilités des autres.

# 4. Principes fondamentaux

Les principes suivants encadrent cette spécification :

1. Le contenu extrait reste associé à une `Document Version` précise.
2. Un `Extracted Content` peut produire plusieurs `Chunk Sets`.
3. Un `Chunk Set` regroupe les `Chunks` issus d'une segmentation déterminée.
4. Chaque `Chunk` conserve sa provenance et sa position dans le contenu d'origine.
5. Un `Chunk` est indépendant de la représentation vectorielle qui peut en être produite.
6. Un même `Chunk` peut posséder plusieurs `Embeddings` issus de modèles ou configurations différents.
7. Chaque `Embedding` identifie le `Model Reference` utilisé pour sa production.
8. Les représentations incompatibles ne sont pas mélangées dans une même recherche vectorielle.
9. Les embeddings documentaires et les embeddings de requêtes ont des cycles de vie distincts.
10. Les contenus originaux et les contenus dérivés restent identifiables séparément.
11. Les capacités de Chunking et d'Embeddings restent indépendantes des applications clientes et des domaines métier.
12. Les stratégies et modèles peuvent évoluer sans modifier l'identité du document ni celle de son contenu source.

# 5. Périmètre

## 5.1 Dans le périmètre

Cette spécification couvre :

- La préparation conceptuelle d'un contenu extrait pour le découpage.
- La production et la distinction des `Chunk Sets`.
- La production et la provenance des `Chunks`.
- La production des embeddings documentaires.
- L'identification des fournisseurs et modèles utilisés.
- La distinction entre embeddings documentaires et embeddings de requêtes.
- Les principes généraux de compatibilité des embeddings.
- Les relations avec l'indexation et la recherche.
- Les exigences de qualité, de traçabilité et de sécurité propres à ces capacités.

## 5.2 Hors du périmètre détaillé

Cette spécification ne définit pas :

- Les algorithmes précis de découpage.
- Les tailles de fragments ou valeurs de chevauchement.
- Les règles numériques ou heuristiques de segmentation.
- Les modèles d'embeddings à sélectionner.
- Les fournisseurs à retenir.
- Les dimensions vectorielles ou fonctions de distance.
- Les formats physiques de stockage des vecteurs.
- Les structures des index.
- Les stratégies détaillées de fusion ou de classement des résultats.
- Les contrats techniques des fournisseurs.

Ces sujets relèvent des études techniques spécialisées et des décisions ultérieures.

# 6. Position dans le cycle de préparation des connaissances

Le Chunking et les embeddings documentaires interviennent après l'extraction et la normalisation du contenu, et avant sa prise en compte dans les index concernés.

Le parcours conceptuel est le suivant :

```text
DOCUMENT VERSION
       |
       v
EXTRACTED CONTENT
       |
       v
CHUNKING
       |
       v
CHUNK SET
       |
       +------ CHUNK 1
       +------ CHUNK 2
       +------ CHUNK 3
                  |
                  v
             EMBEDDINGS
                  |
                  v
          INDEX MANAGEMENT
                  |
                  v
           INDEX GENERATION
```

Ce schéma représente le parcours documentaire général. Une stratégie de recherche textuelle peut exploiter des `Chunks` sans nécessiter d'embeddings. La production d'embeddings est nécessaire lorsque la capacité vectorielle concernée l'exige.

Les embeddings de requêtes sont produits au moment de la recherche et relèvent du parcours du moteur de requête. Ils peuvent utiliser la même capacité générale de vectorisation, mais ne sont pas une étape d'ingestion documentaire.

# 7. Entrées et résultats conceptuels

## 7.1 Entrées du Chunking

La capacité de Chunking reçoit principalement :

- Un `Extracted Content` associé à une `Document Version`.
- Les informations structurelles disponibles et utiles à la segmentation.
- Le contexte de la connaissance et de la `Knowledge Base` concernées.
- La stratégie ou configuration de découpage applicable.

Le contenu reçu doit être suffisamment identifié pour préserver sa provenance.

## 7.2 Résultats du Chunking

Le Chunking produit :

- Un `Chunk Set` associé au contenu extrait d'origine.
- Un ou plusieurs `Chunks` appartenant à ce `Chunk Set`.
- Les informations de position, d'ordre et de provenance nécessaires à l'exploitation ultérieure.

Un même `Extracted Content` peut produire plusieurs `Chunk Sets`, notamment lorsque plusieurs stratégies ou configurations de segmentation sont utilisées.

## 7.3 Entrées des Embeddings documentaires

La capacité d'Embeddings reçoit principalement :

- Un ou plusieurs `Chunks` identifiés.
- Le `Model Reference` sélectionné pour la capacité d'embeddings.
- La `Provider Configuration` applicable, lorsque nécessaire.
- Les informations de compatibilité requises pour le contexte d'utilisation.

## 7.4 Résultats des Embeddings documentaires

La capacité produit un ou plusieurs `Embeddings` associés :

- Au contenu représenté.
- Au `Model Reference` utilisé.
- À la configuration de production pertinente.

Un échec de vectorisation doit être identifiable sans transformer le `Chunk` source en donnée invalide ou le faire disparaître.

# 8. Chunking : principes de segmentation

## 8.1 Objectif de la segmentation

La segmentation vise à produire des unités de contenu suffisamment cohérentes pour être retrouvées et exploitées dans le cadre d'une requête.

Un `Chunk` ne doit pas être considéré uniquement comme une portion de texte de longueur arbitraire. Il représente une unité issue d'un contenu et d'une stratégie de segmentation identifiables.

## 8.2 Préservation de la structure

Lorsque le contenu source le permet, la segmentation doit préserver les informations structurelles utiles, par exemple :

- Les titres et niveaux de section.
- Les paragraphes et leur ordre.
- Les références de page ou de position.
- Les listes et éléments associés.
- Les structures tabulaires lorsqu'elles sont prises en charge.
- Les relations entre un passage et son contexte documentaire.

Le degré de préservation dépend du contenu extrait et des capacités applicables. Le détail du traitement de chaque format n'est pas défini ici.

## 8.3 Cohérence des fragments

Les fragments doivent conserver une cohérence suffisante pour pouvoir être interprétés dans leur contexte.

La segmentation doit éviter, autant que possible, de séparer des éléments dont la compréhension dépend directement les uns des autres.

Les règles précises de cohérence, de granularité, de taille et de chevauchement seront évaluées dans les spécifications et travaux techniques ultérieurs.

## 8.4 Provenance et position

Chaque `Chunk` doit rester relié :

- Au `Chunk Set` auquel il appartient.
- À l'`Extracted Content` à partir duquel il a été produit, par l'intermédiaire de son `Chunk Set`.
- À la `Document Version` d'origine, par la chaîne de provenance.
- À sa position ou à ses références structurelles dans le contenu d'origine, lorsque disponibles.

L'ordre des fragments doit pouvoir être retrouvé.

## 8.5 Plusieurs stratégies de segmentation

Un même `Extracted Content` peut produire plusieurs `Chunk Sets` distincts.

Chaque `Chunk Set` représente le résultat d'une segmentation déterminée. Les fragments de deux `Chunk Sets` différents ne doivent pas être confondus, même lorsqu'ils proviennent du même contenu extrait.

Cette distinction permet de comparer ou de faire évoluer des stratégies de segmentation sans modifier le contenu original.

## 8.6 Indépendance vis-à-vis des Knowledge Bases

Le `Chunk` et le `Chunk Set` décrivent des représentations dérivées du contenu ; ils ne remplacent pas le `Knowledge Item` ni son association à une `Knowledge Base`.

Le même élément documentaire peut être associé à plusieurs Knowledge Bases. Les représentations préparées peuvent être réutilisées lorsque leurs caractéristiques et les règles applicables le permettent. Une base peut également nécessiter une préparation distincte lorsque sa configuration ou ses besoins le justifient.

Les règles de sélection et de réutilisation entre bases sont définies au niveau des Knowledge Bases et du pipeline d'ingestion ; cette spécification ne présume pas que toutes les bases partagent automatiquement les mêmes fragments.

# 9. Embeddings : principes de représentation

## 9.1 Nature de l'Embedding

Un `Embedding` est une représentation vectorielle associée à un contenu précis et produite par un modèle identifié.

Il s'agit d'une représentation dérivée. Elle ne remplace ni le contenu source ni le `Chunk` qu'elle représente.

## 9.2 Identification du modèle

Chaque `Embedding` doit pouvoir être relié au `Model Reference` utilisé pour sa production.

Cette référence permet d'identifier le fournisseur, le modèle et la version ou variante pertinente, conformément au modèle de données validé.

La `Provider Configuration` utilisée peut également être identifiée lorsque cela est nécessaire à la traçabilité et à la reproductibilité.

## 9.3 Plusieurs embeddings pour un même contenu

Un même `Chunk` peut posséder plusieurs `Embeddings`, par exemple lorsque plusieurs modèles ou configurations sont évalués ou utilisés.

Ces représentations restent distinctes. Elles ne doivent pas être fusionnées ni considérées comme équivalentes uniquement parce qu'elles représentent le même contenu.

## 9.4 Indépendance du contenu source

Le remplacement ou l'évolution d'un modèle d'embeddings ne modifie pas :

- Le `Document`.
- La `Document Version`.
- L'`Original Artifact`.
- L'`Extracted Content`.
- Le `Chunk Set`.
- Le `Chunk`.

Une nouvelle représentation vectorielle peut être produite à partir du même contenu lorsque cela est nécessaire.

## 9.5 Compatibilité des représentations

Les embeddings ne sont pas automatiquement compatibles entre eux.

Une recherche vectorielle doit utiliser des représentations compatibles entre les embeddings documentaires indexés et l'embedding de la requête.

La compatibilité dépend du modèle et de ses caractéristiques pertinentes, ainsi que des configurations qui affectent la représentation. L'identité du fournisseur ou une dimension identique ne suffit pas, à elle seule, à démontrer la compatibilité.

Les modalités de vérification de compatibilité seront précisées dans les spécifications du moteur de recherche et dans les études techniques des modèles.

# 10. Embeddings documentaires et embeddings de requêtes

Le moteur distingue deux usages de la capacité d'embeddings.

## 10.1 Embeddings documentaires

Les embeddings documentaires sont produits pendant la préparation des connaissances, principalement à partir des `Chunks`.

Ils peuvent être associés aux représentations indexées et être réutilisés pour les recherches compatibles, selon leur état et les règles applicables.

Ils appartiennent au cycle de vie des connaissances préparées.

## 10.2 Embeddings de requêtes

Les embeddings de requêtes sont produits lorsqu'une recherche vectorielle doit représenter une `Query`.

Ils représentent la demande de recherche et non un document ou un `Chunk` documentaire.

Ils ne doivent pas être confondus avec les embeddings documentaires persistants du modèle conceptuel.

## 10.3 Compatibilité entre requête et index

Pour qu'une recherche vectorielle soit valide, l'embedding de la requête doit être compatible avec les représentations documentaires de la génération d'index interrogée.

Si la compatibilité n'est pas établie, le moteur ne doit pas présenter le résultat comme une recherche vectorielle valide. Les stratégies alternatives ou les réponses d'erreur relèvent du document 08 — Moteur de recherche.

# 11. Relations avec les Knowledge Bases et les Index

Le Chunking et les Embeddings interviennent dans la préparation des éléments de connaissance associés aux Knowledge Bases.

Les relations conceptuelles principales sont les suivantes :

- Un `Extracted Content` peut produire plusieurs `Chunk Sets`.
- Un `Chunk Set` appartient à un `Extracted Content` déterminé.
- Un `Chunk Set` contient un ou plusieurs `Chunks`.
- Un `Chunk` appartient à un seul `Chunk Set`.
- Un `Chunk` peut être associé à plusieurs `Embeddings`.
- Chaque `Embedding` identifie le contenu représenté et le `Model Reference` utilisé.
- Un `Index Entry` peut référencer un `Chunk` et, pour une stratégie vectorielle, l'`Embedding` compatible correspondant.
- L'`Index Generation` identifie la génération dans laquelle l'`Index Entry` est présente.

Le fait qu'un `Chunk` ou un `Embedding` existe ne signifie pas automatiquement qu'il est disponible dans un index ou interrogeable dans une Knowledge Base. La disponibilité dépend des associations, des index concernés et de leurs générations.

# 12. Qualité et cohérence des représentations

Les représentations produites doivent permettre de préserver la qualité et l'intégrité des connaissances.

Au niveau conceptuel, les attentes sont les suivantes :

1. Chaque `Chunk` doit pouvoir être interprété et relié à son contexte d'origine.
2. Les fragments doivent conserver un ordre et une provenance exploitables.
3. Chaque `Embedding` doit être associé au contenu et au modèle qui l'ont produit.
4. Les représentations issues de configurations ou de modèles différents doivent rester distinguables.
5. Une représentation incomplète ou produite en échec ne doit pas être considérée comme disponible pour l'indexation concernée.
6. La modification d'une stratégie de segmentation doit pouvoir être distinguée des résultats de segmentation antérieurs.
7. La modification d'un modèle d'embeddings doit pouvoir être distinguée des représentations antérieures.
8. Les contenus originaux et les représentations dérivées ne doivent pas être confondus.

Les critères mesurables de qualité du découpage et des embeddings seront définis dans le document 13 — Tests et évaluation.

# 13. Traçabilité

Le moteur doit préserver une chaîne de provenance permettant de remonter depuis une représentation préparée jusqu'au contenu d'origine.

La traçabilité conceptuelle doit permettre d'identifier :

- La `Document Version` concernée.
- L'`Extracted Content` utilisé.
- Le `Chunk Set` produit.
- La stratégie ou configuration de segmentation applicable, lorsque cette information est conservée.
- Le ou les `Chunks` produits.
- Le `Provider` et le `Model Reference` utilisés pour les embeddings.
- La `Provider Configuration` pertinente, lorsque nécessaire.
- Les `Index Entries` et `Index Generations` qui utilisent ces représentations.

Cette traçabilité permet de comprendre l'origine des éléments retrouvés et de distinguer les représentations produites à des moments ou selon des configurations différentes.

# 14. Sécurité et isolation

Le Chunking et les Embeddings doivent respecter le contexte de sécurité établi pour les connaissances concernées.

Les principes suivants s'appliquent :

1. Le contenu traité doit provenir d'une source et d'un élément auxquels l'opération est autorisée à accéder.
2. Les représentations dérivées doivent conserver leur lien avec le périmètre de connaissance et les règles d'accès applicables.
3. La production d'un Chunk ou d'un Embedding ne doit pas élargir les droits d'accès au contenu source.
4. Les données envoyées à un fournisseur externe doivent respecter les autorisations et politiques applicables à la source et à la Knowledge Base.
5. Les informations sensibles ne doivent pas être exposées dans les journaux ou les résultats de traitement.
6. Une représentation dérivée ne doit pas rester accessible lorsque le contenu correspondant a été retiré ou rendu indisponible, conformément aux politiques de cycle de vie applicables.

Les mécanismes détaillés d'autorisation, de protection des données et de gestion des fournisseurs relèvent du document 11 — Sécurité et isolation.

# 15. Échecs et disponibilité

Les opérations de Chunking et d'Embeddings peuvent échouer indépendamment.

Les principes suivants doivent être respectés :

- Un échec de Chunking doit être identifiable pour le contenu concerné.
- Un échec de vectorisation ne doit pas supprimer ni invalider le `Chunk` source.
- Un `Embedding` incomplet ou invalide ne doit pas être présenté comme prêt pour une génération d'index.
- Les échecs doivent être traçables et reliés à l'opération concernée.
- Les reprises ne doivent pas créer de doublons incontrôlés ou mélanger des représentations incompatibles.
- Un contenu peut rester exploitable par une recherche textuelle même si la production d'un embedding a échoué, lorsque la capacité d'indexation concernée le permet.

Les mécanismes opérationnels de reprise et de suivi sont traités dans les spécifications d'ingestion, de recherche et de déploiement.

# 16. Responsabilités et frontières avec les autres composants

| Composant | Responsabilité liée à cette spécification |
|---|---|
| Extraction et Normalization | Fournir un contenu extrait exploitable et identifié. |
| Chunking | Produire les Chunk Sets et les Chunks à partir des contenus extraits. |
| Embedding | Produire les représentations vectorielles à partir des contenus pris en charge. |
| Provider / Model Integration | Rendre accessibles les capacités des fournisseurs et modèles identifiés. |
| Index Management | Intégrer les représentations pertinentes dans les Index Generations concernées. |
| Retrieval | Utiliser les index et représentations compatibles pour effectuer les recherches. |
| Job Management | Suivre les opérations de préparation lorsqu'un suivi d'exécution est nécessaire. |
| Audit et Observability | Assurer la traçabilité et l'observation des opérations pertinentes. |

Cette séparation ne prescrit pas un découpage physique en services ou en processus indépendants.

# 17. Couverture des exigences

## 17.1 Exigences fonctionnelles principalement couvertes

| Exigence | Besoin | Contribution de cette spécification |
|---|---|---|
| FR-011 | Découpage documentaire | Définit le rôle du Chunking, des Chunk Sets et des Chunks, ainsi que leur provenance. |
| FR-012 | Gestion des embeddings | Définit les représentations, leur lien avec les modèles et les principes de compatibilité. |
| FR-013 | Indexation et réindexation | Définit les relations entre Chunks, Embeddings et Index Entries, sans remplacer la spécification d'indexation. |
| FR-014 | Recherche vectorielle | Établit la nécessité d'une compatibilité entre embeddings documentaires et embeddings de requêtes. |

Les FR-014 à FR-017 seront détaillées dans le document 08 — Moteur de recherche. Cette spécification ne définit pas les algorithmes de retrieval ni le classement des résultats.

## 17.2 Exigences non fonctionnelles concernées

| Exigence | Besoin | Contribution de cette spécification |
|---|---|---|
| NFR-003 à NFR-005 | Protection des données et des secrets | Encadre la prise en compte des autorisations et l'utilisation des fournisseurs externes. |
| NFR-006 | Intégrité des connaissances | Préserve les relations entre contenus extraits, fragments et embeddings. |
| NFR-007 | Résilience | Distingue les échecs de découpage et de vectorisation et préserve les données sources. |
| NFR-008 | Traçabilité | Préserve la provenance des représentations produites. |
| NFR-009 | Cohérence après modification | Permet de distinguer les représentations dérivées de contenus et versions différents. |
| NFR-014 | Extensibilité | Sépare les stratégies de découpage et les fournisseurs de modèles. |
| NFR-019 | Évaluation de la qualité | Identifie les dimensions de qualité à mesurer ultérieurement. |
| NFR-020 | Vérifiabilité | Rend les représentations et leurs origines identifiables pour les tests. |

Cette couverture est limitée au périmètre du Chunking et des Embeddings. Elle ne remplace pas la matrice globale des exigences.

# 18. Sujets reportés aux spécifications spécialisées

| Sujet | Document responsable |
|---|---|
| Entités et relations conceptuelles | 04 — Modèle de données |
| Gestion fonctionnelle des Knowledge Bases et associations | 05 — Knowledge Bases |
| Parcours d'ingestion et préparation documentaire | 06 — Pipeline d'ingestion |
| Choix et étude des stratégies de segmentation | Étude technique dédiée, après validation des exigences |
| Modèles, fournisseurs et compatibilité détaillée | Étude technique et contrats fournisseurs |
| Index, générations et entrées d'index | 08 — Moteur de recherche et indexation |
| Recherche vectorielle, textuelle et hybride | 08 — Moteur de recherche |
| Contrats d'intégration des fournisseurs | 10 — API et interfaces d'intégration, selon périmètre |
| Sécurité, autorisations et transfert vers les fournisseurs | 11 — Sécurité et isolation |
| Évaluation de la qualité du découpage et des embeddings | 13 — Tests et évaluation |
| Exécution, ressources et montée en charge | 14 — Déploiement et scalabilité |

# 19. Éléments explicitement non décidés

Cette spécification ne sélectionne pas :

- Une stratégie de découpage particulière.
- Des tailles de Chunk ou valeurs de chevauchement.
- Un format documentaire ou multimodal supplémentaire.
- Un fournisseur d'embeddings.
- Un modèle d'embeddings.
- Une dimension vectorielle.
- Une fonction de distance ou de similarité.
- Une méthode de normalisation des vecteurs.
- Une technologie ou structure de stockage vectoriel.
- Une politique définitive de mise en cache des embeddings de requêtes.
- Une stratégie de réutilisation physique des représentations entre Knowledge Bases.

Ces décisions nécessitent des études et des critères d'évaluation adaptés. Elles ne doivent pas être déduites du seul modèle conceptuel.

# 20. Conditions de validation

Le document pourra être validé lorsque :

1. Le rôle et la frontière du Chunking seront clairement définis.
2. La distinction entre Extracted Content, Chunk Set et Chunk sera cohérente avec le document 04.
3. La relation entre Chunk et Embedding sera clairement établie.
4. Le rôle du Provider et du Model Reference sera respecté.
5. Les embeddings documentaires seront distingués des embeddings de requêtes.
6. Les principes de compatibilité entre embeddings seront suffisamment clairs sans imposer de modèle ou de technologie.
7. Les relations avec Knowledge Base, Index, Index Generation et Index Entry seront cohérentes.
8. La provenance et la traçabilité des représentations seront préservées.
9. Les exigences FR et NFR concernées seront couvertes.
10. Les choix techniques prématurés seront exclus.
11. Le document restera cohérent avec les documents 00 à 06.

# 21. Conclusion

Le Chunking transforme un contenu extrait en unités de connaissance identifiables, cohérentes et traçables. Les Embeddings produisent des représentations vectorielles liées à ces unités et à des modèles précisément identifiés.

Ces deux capacités sont complémentaires mais distinctes. Elles permettent de préparer les connaissances pour les mécanismes de recherche sans confondre le contenu original, les fragments, les représentations vectorielles et les structures d'indexation.

Les embeddings documentaires et ceux des requêtes conservent des cycles de vie distincts, et leur compatibilité est une condition nécessaire à la validité d'une recherche vectorielle.

**Le Chunking définit les unités de connaissance ; l'Embedding représente ces unités dans un espace vectoriel identifié ; l'indexation et la recherche exploitent ensuite ces représentations selon leurs propres responsabilités.**
