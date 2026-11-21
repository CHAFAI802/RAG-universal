# UNIVERSAL RAG ENGINE

## Document 08 — Moteur de recherche (Retrieval Engine)

**Version :** 1.0
**Statut :** VALIDATED
**Projet :** RAG-universal

---

# 1. Objectif

Ce document définit le rôle et le périmètre fonctionnel du moteur de recherche de Universal RAG Engine.

Il décrit les capacités permettant de retrouver des connaissances pertinentes à partir d'une requête, dans les Knowledge Bases auxquelles l'acteur demandeur est autorisé à accéder.

Il précise notamment :

- les modes de recherche pris en charge ;
- les connaissances pouvant être recherchées ;
- les principes de filtrage et de classement ;
- la provenance des résultats ;
- les relations avec les Knowledge Bases, les index et les données structurées ;
- la séparation entre recherche et génération.

Ce document reste au niveau conceptuel et fonctionnel. Il ne définit pas les algorithmes, les formules de score, les structures physiques, les technologies de stockage ou les contrats API détaillés.

# 2. Références

Cette spécification s'appuie sur les documents suivants :

- `00_VISION_ET_OBJECTIFS.md`
- `DEPENDENCY_MAP.md`
- `DECISION_LOG.md`
- `01_CAHIER_DES_CHARGES.md`
- `02_ARCHITECTURE_GLOBALE.md`
- `03_ARCHITECTURE_MODULAIRE.md`
- `04_MODELE_DE_DONNEES.md`
- `05_KNOWLEDGE_BASES.md`
- `06_PIPELINE_INGESTION.md`
- `07_CHUNKING_ET_EMBEDDINGS.md`

Les exigences fonctionnelles principalement concernées sont FR-014 à FR-017. Le document contribue également à FR-018, FR-020, FR-021 et FR-024.

# 3. Position dans l'architecture

Le Retrieval Engine appartient à l'ensemble fonctionnel Knowledge Query défini dans l'architecture globale et l'architecture modulaire.

Il reçoit une demande de recherche dans un contexte déjà établi par les composants responsables de l'accès et de l'orchestration. Il exploite les connaissances accessibles, récupère les éléments pertinents et retourne des résultats traçables.

Le Retrieval Engine ne remplace pas :

- le contrôle d'identité et d'autorisation ;
- la gestion des Knowledge Bases ;
- le pipeline d'ingestion et de préparation des connaissances ;
- le sous-système d'accès aux données structurées ;
- le moteur de génération LLM.

Il collabore avec ces composants dans les limites de leurs responsabilités respectives.

# 4. Responsabilité principale

La responsabilité principale du Retrieval Engine est de retrouver et de classer les connaissances pertinentes pour une requête, dans le périmètre autorisé.

Il doit pouvoir fournir des résultats de recherche sans déclencher de génération LLM.

Les résultats doivent conserver leur origine et permettre de retrouver les connaissances dont ils proviennent.

# 5. Concepts utilisés

Le Retrieval Engine s'appuie sur les concepts déjà définis dans le modèle de données.

## 5.1 Query

Représente la demande adressée au moteur. Elle fournit le contenu à rechercher et le contexte nécessaire pour déterminer le périmètre de recherche.

Une Query peut viser une Knowledge Base ou plusieurs Knowledge Bases, à condition que l'accès à chacune soit autorisé.

## 5.2 Knowledge Base

Représente un espace logique de connaissances dans lequel la recherche peut être effectuée.

La sélection d'une Knowledge Base ne confère pas, à elle seule, une autorisation d'accès. Le périmètre doit être établi et vérifié par les mécanismes de sécurité.

## 5.3 Index et Index Generation

L'Index représente une capacité logique de recherche. Une Index Generation représente un état déterminé de cette capacité.

La recherche doit s'appuyer sur des index et des générations disponibles et compatibles avec la stratégie de recherche demandée.

## 5.4 Chunk et Embedding

Pour la recherche documentaire, le Chunk représente l'unité de contenu récupérable. L'Embedding représente une représentation vectorielle associée à un contenu et produite par un modèle déterminé.

La recherche vectorielle doit respecter la compatibilité entre les représentations documentaires indexées et la représentation de la requête.

## 5.5 Structured Resource et Structured Result

Les données structurées sont exploitées par le sous-système Structured Data Access. Le Retrieval Engine peut coordonner leur prise en compte dans une recherche combinée, mais ne remplace pas les responsabilités de ce sous-système.

## 5.6 Retrieval Result

Représente un élément récupéré par une opération de recherche. Il conserve sa provenance afin que l'application cliente et, le cas échéant, le processus de génération puissent identifier son origine.

# 6. Périmètre des connaissances recherchées

Le moteur doit pouvoir rechercher dans deux grandes catégories de connaissances.

## 6.1 Connaissances documentaires

Elles proviennent des documents intégrés dans les Knowledge Bases et préparés par le pipeline d'ingestion.

Le Retrieval Engine exploite les représentations disponibles pour retrouver les passages pertinents, notamment les Chunks et leurs informations associées.

## 6.2 Connaissances structurées

Elles proviennent de sources structurées et de ressources accessibles dans le périmètre autorisé.

Leur interrogation relève du sous-système Structured Data Access, qui applique ses propres règles de contrôle. Le Retrieval Engine peut intégrer les résultats structurés à une recherche combinée sans les transformer artificiellement en Chunks ou en documents.

## 6.3 Recherche combinée

Une même Query peut nécessiter des connaissances documentaires et structurées.

Les résultats des deux catégories peuvent être réunis pour constituer un ensemble de résultats cohérent. Leur nature et leur provenance doivent néanmoins rester distinguables.

# 7. Modes de recherche

Le moteur doit prendre en charge trois modes principaux pour la recherche documentaire.

## 7.1 Recherche vectorielle

La recherche vectorielle retrouve des contenus à partir de la proximité sémantique entre la requête et les représentations vectorielles des connaissances indexées.

Principes :

- les connaissances recherchées doivent disposer de représentations compatibles ;
- le modèle utilisé pour représenter la requête doit être compatible avec celui de l'index ciblé ;
- les résultats doivent rester associés aux Chunks et à leurs sources ;
- les limites du modèle et de la recherche doivent être prises en compte dans l'interprétation des résultats.

## 7.2 Recherche textuelle

La recherche textuelle retrouve des contenus à partir de leurs termes et de leurs correspondances textuelles.

Elle doit pouvoir fonctionner indépendamment de la recherche vectorielle.

Elle est notamment utile lorsque la requête contient des termes exacts, des noms, des références, des identifiants ou des expressions dont la forme précise importe.

## 7.3 Recherche hybride

La recherche hybride combine les résultats de la recherche vectorielle et de la recherche textuelle.

Elle vise à exploiter leurs complémentarités tout en produisant un ensemble de résultats consolidé.

La recherche hybride est une stratégie de recherche. Elle n'impose pas nécessairement l'existence d'un troisième type d'index physique distinct.

Les méthodes de fusion et leurs paramètres seront définis dans une spécification ultérieure.

# 8. Périmètre et filtrage des recherches

La recherche doit respecter le périmètre établi pour la requête.

Ce périmètre peut notamment dépendre :

- de l'identité authentifiée ;
- de l'organisation concernée ;
- de l'application cliente ;
- des Knowledge Bases autorisées ;
- des sources et connaissances accessibles ;
- des filtres fonctionnels demandés.

Les contrôles d'autorisation constituent une contrainte obligatoire. Ils ne doivent pas dépendre uniquement de filtres librement fournis par l'application cliente ou par la requête.

Les filtres fonctionnels peuvent préciser le périmètre de recherche, mais ne peuvent jamais élargir les droits accordés.

Les règles détaillées d'autorisation et d'isolation relèvent de la spécification de sécurité.

# 9. Pertinence et classement des résultats

Le moteur doit classer les résultats selon leur pertinence par rapport à la requête et à la stratégie de recherche utilisée.

Le classement peut prendre en compte différentes informations pertinentes, sans que leurs méthodes de calcul soient définies dans ce document.

Les résultats issus de modes de recherche différents doivent pouvoir être rapprochés dans une recherche hybride.

Le moteur peut également faire appel à une capacité de reranking lorsque le scénario le justifie. Le reranking constitue une capacité complémentaire et ne doit pas être considéré comme obligatoire pour toutes les recherches.

Un score de pertinence indique une estimation relative de correspondance. Il ne constitue pas, à lui seul, une preuve de vérité ou de fiabilité du contenu.

# 10. Résultats et provenance

Chaque Retrieval Result doit conserver les informations nécessaires pour comprendre ce qui a été retrouvé et d'où provient l'information.

Pour un résultat documentaire, la provenance doit permettre de retrouver au minimum :

- la Knowledge Base concernée ;
- la source d'origine ;
- le Document ;
- la Document Version ;
- le Chunk récupéré, lorsque le résultat correspond à un passage documentaire.

Pour un résultat structuré, la provenance doit permettre d'identifier :

- la Knowledge Base ou le périmètre autorisé concerné, lorsqu'applicable ;
- la Structured Source ;
- la Structured Resource ;
- le résultat structuré retourné.

Les résultats documentaires et structurés doivent conserver leur nature propre, même lorsqu'ils sont réunis dans une même réponse de recherche.

Les formes détaillées des résultats seront définies dans les spécifications du modèle de données logique et de l'API.

# 11. Recherche dans plusieurs Knowledge Bases

Le moteur peut prendre en charge une recherche portant sur plusieurs Knowledge Bases lorsque la requête et les autorisations le permettent.

Chaque résultat doit conserver l'identification de la Knowledge Base dont il provient.

La recherche multi-bases ne doit pas supprimer les frontières d'accès entre les bases ni créer un partage implicite de leurs connaissances.

Les règles de sélection, de combinaison et de présentation des résultats multi-bases seront précisées dans les spécifications concernées.

# 12. Relation entre recherche et génération

Le Retrieval Engine est distinct du Generation Engine.

Il peut fournir des résultats pour une utilisation directe par l'application cliente ou transmettre des résultats sélectionnés au processus de génération.

Les trois modes d'utilisation suivants doivent rester distincts :

| Mode | Recherche dans les Knowledge Bases | Génération LLM | Responsabilité principale |
|---|---|---|---|
| Retrieval Only | Oui | Non | Retourner les résultats de recherche |
| Direct LLM Generation | Non, pour cette requête | Oui | Générer une réponse sans Retrieval dans les Knowledge Bases |
| Retrieval-Augmented Generation | Oui | Oui | Générer une réponse à partir des connaissances récupérées |

Le mode Direct LLM Generation ne relève pas du Retrieval Engine. Il est mentionné ici uniquement pour préserver la distinction établie dans le modèle de données.

La construction du contexte transmis au LLM, la génération et les citations finales seront détaillées dans le document consacré à la génération.

# 13. Informations insuffisantes ou résultats absents

Le moteur doit pouvoir retourner un résultat de recherche vide ou signaler que les connaissances accessibles ne permettent pas de retrouver des éléments suffisamment pertinents.

L'absence de résultats ne doit pas être masquée par l'invention de connaissances.

Le Retrieval Engine retourne l'état et les résultats de la recherche. La décision de répondre, de demander une précision ou de déclarer les connaissances insuffisantes dans une réponse générée relève du processus de génération et de ses règles.

# 14. Fraîcheur et disponibilité des connaissances

La recherche doit tenir compte de l'état de disponibilité des connaissances et des index.

Une connaissance qui n'est pas encore disponible pour la recherche ne doit pas être présentée comme si elle était correctement indexée.

Les résultats doivent pouvoir être reliés à la génération d'index utilisée. Cette relation contribue à comprendre l'état des connaissances exploitées au moment de la recherche.

Les règles précises d'activation, de remplacement et de synchronisation des générations d'index relèvent des spécifications d'indexation et du cycle de vie des connaissances.

# 15. Relations avec les autres composants

| Composant | Relation avec le Retrieval Engine |
|---|---|
| Access Layer et services de sécurité | Fournissent le contexte d'identité et le périmètre autorisé |
| Knowledge Base Management | Fournit les références et configurations des bases concernées |
| Index Management | Rend disponibles les index et générations utilisables |
| Chunking et Embedding | Fournissent les représentations documentaires préparées et leurs informations de compatibilité |
| Structured Data Access | Exécute les recherches structurées autorisées et retourne leur provenance |
| Query Orchestration | Coordonne la demande et les capacités de recherche nécessaires |
| Reranking | Peut réordonner les résultats lorsque cette capacité est sollicitée |
| Generation Engine | Consomme les résultats sélectionnés lorsqu'une génération augmentée est demandée |
| Citation et Provenance | Exploitent les références conservées avec les résultats pour établir les sources utilisées |

# 16. Exigences non fonctionnelles concernées

Le Retrieval Engine contribue notamment aux exigences suivantes :

- **NFR-001 à NFR-005 :** respect de l'isolation, des autorisations et de la protection des données ;
- **NFR-006 à NFR-009 :** intégrité, résilience, traçabilité et cohérence des connaissances ;
- **NFR-010 à NFR-012 :** performance et évolutivité des recherches ;
- **NFR-013 à NFR-017 :** modularité, extensibilité, maintenabilité et interopérabilité ;
- **NFR-018 à NFR-020 :** observabilité, évaluation et vérifiabilité.

Les objectifs mesurables et les moyens de vérification seront définis dans les spécifications de tests, d'évaluation et de déploiement.

# 17. Traçabilité avec les exigences fonctionnelles

| Exigence | Besoin | Couverture conceptuelle dans ce document |
|---|---|---|
| FR-014 | Recherche vectorielle | Sections 5, 7.1, 8, 10 et 14 |
| FR-015 | Recherche textuelle | Sections 7.2, 8 et 10 |
| FR-016 | Recherche hybride | Sections 7.3, 9 et 10 |
| FR-017 | Filtrage et classement | Sections 8 et 9 |
| FR-018 | Génération à partir des connaissances récupérées | Section 12 et relation avec le document 09 |
| FR-020 | Références documentaires | Sections 10 et 12 et relation avec le document 09 |
| FR-021 | Gestion des connaissances insuffisantes | Section 13 et relation avec le document 09 |
| FR-022 | Connexion aux données structurées | Sections 6.2, 6.3 et 15, en complément du document 12 |
| FR-023 | Interrogation contrôlée des données | Sections 6.2 et 8, en complément du document 12 |
| FR-024 | Combinaison des connaissances | Sections 6.3, 10 et 12 |

Cette matrice indique la contribution du Retrieval Engine. Elle ne signifie pas que ce document remplace les spécifications spécialisées auxquelles il fait référence.

# 18. Éléments reportés

Les sujets suivants ne sont pas définis dans cette spécification :

- les algorithmes précis de recherche vectorielle et textuelle ;
- les formules de fusion des résultats ;
- les métriques et seuils de pertinence ;
- les algorithmes de reranking ;
- les dimensions et formats des vecteurs ;
- les structures détaillées des résultats ;
- les contrats API ;
- les mécanismes techniques d'autorisation ;
- les technologies de stockage et d'indexation ;
- les objectifs chiffrés de latence et de charge.

Ces sujets seront examinés dans les documents spécialisés correspondants.

# 19. Conditions de validation

Le document pourra être validé lorsque :

1. Le rôle et les limites du Retrieval Engine seront approuvés.
2. Les recherches vectorielle, textuelle et hybride seront clairement distinguées.
3. La séparation entre recherche documentaire et accès aux données structurées sera respectée.
4. Les principes de filtrage et d'autorisation seront cohérents avec les documents précédents.
5. La provenance des résultats sera préservée.
6. La distinction entre Retrieval Only, Direct LLM Generation et Retrieval-Augmented Generation sera claire.
7. Les relations avec les Knowledge Bases, les index, les Chunks et les résultats structurés seront cohérentes avec le modèle de données.
8. Les exigences fonctionnelles concernées seront couvertes.
9. Les détails techniques prématurés seront évités.
10. La cohérence avec les documents 00 à 07 sera vérifiée.

# 20. Conclusion

Le Retrieval Engine constitue la capacité de recherche et de récupération des connaissances de Universal RAG Engine.

Il doit permettre de retrouver des informations pertinentes dans les Knowledge Bases autorisées, en utilisant des mécanismes vectoriels, textuels ou hybrides, tout en préservant la provenance des résultats.

Il doit également pouvoir collaborer avec le sous-système d'accès aux données structurées sans confondre les deux catégories de connaissances.

La recherche reste indépendante de la génération : elle peut être utilisée seule ou servir de fondation à une réponse augmentée par un LLM.

**Le Retrieval Engine retrouve et structure les connaissances pertinentes ; le Generation Engine décide comment les exploiter pour produire une réponse.**
