# UNIVERSAL RAG ENGINE

## Document 04 — Modèle conceptuel des données

**Version :** 1.0
**Statut :** VALIDATED
**Projet :** RAG-universal

---

# 1. Objectif

Ce document définit le modèle conceptuel des données de Universal RAG Engine.

Il identifie les concepts que le moteur doit représenter, leurs responsabilités, leurs relations et les cardinalités fondamentales entre eux. Il constitue la référence pour les futures spécifications du modèle logique et du modèle physique des données.

Ce document répond à quatre questions :

1. Quelles informations le moteur doit-il représenter ?
2. Quelles sont les entités et les associations nécessaires ?
3. Comment ces entités sont-elles reliées ?
4. Dans quelle mesure le modèle couvre-t-il les exigences du cahier des charges ?

Il ne définit pas les tables, colonnes, types SQL, clés physiques, index de base de données, technologies de stockage ou mécanismes d'implémentation.

# 2. Références et périmètre

Cette spécification s'appuie sur les documents suivants :

- `00_VISION_ET_OBJECTIFS.md`
- `DEPENDENCY_MAP.md`
- `DECISION_LOG.md`
- `01_CAHIER_DES_CHARGES.md`
- `02_ARCHITECTURE_GLOBALE.md`
- `03_ARCHITECTURE_MODULAIRE.md`

Le modèle couvre les données nécessaires à la gouvernance, aux espaces de connaissances, aux sources documentaires et structurées, aux représentations dérivées, à l'indexation, à la recherche, à la génération, aux opérations et à l'évaluation.

# 3. Principes de modélisation

## P1 — Indépendance métier

Le modèle représente des concepts génériques. Il ne doit pas imposer un domaine métier particulier ni reprendre le modèle interne d'une application cliente.

## P2 — Identité et cycle de vie

Un concept est modélisé comme entité lorsqu'il possède une identité, un rôle, des relations ou un cycle de vie qui doivent être distingués. La similitude des attributs entre deux objets ne supprime pas leur identité propre.

## P3 — Séparation des responsabilités

Les organisations, identités, bases de connaissances, sources, documents, versions, fragments, embeddings, index, requêtes et réponses sont des concepts distincts.

## P4 — Données originales et données dérivées

Le contenu original, les versions documentaires, les contenus extraits, les fragments, les embeddings et les entrées d'index sont des représentations distinctes. Une représentation dérivée doit conserver sa provenance.

## P5 — Gestion des versions

Les versions d'un document et les générations d'un index doivent pouvoir être distinguées et reliées à leur parent logique.

## P6 — Réutilisation sans confusion de propriété

Une source ou un élément de connaissance peut être utilisé dans plusieurs Knowledge Bases. Cette réutilisation ne confond ni l'identité de la source, ni l'association avec chaque base, ni les droits d'accès.

## P7 — Isolation et autorisation

Les données sont rattachées à un périmètre propriétaire et ne sont accessibles qu'aux acteurs autorisés. La propriété d'une ressource et l'autorisation d'y accéder sont deux notions distinctes.

## P8 — Indépendance des fournisseurs

Les fournisseurs et modèles externes sont représentés indépendamment de leurs configurations d'utilisation et des capacités du cœur du moteur.

## P9 — Distinction entre demande, recherche et réponse

Une Query, les résultats de Retrieval et une réponse générée ne sont pas le même objet. Une recherche peut ne produire aucune réponse LLM ; une réponse LLM peut être directe ou augmentée par Retrieval.

## P10 — Extensibilité maîtrisée

Le modèle doit permettre l'ajout de nouvelles sources, de nouveaux types de ressources et de nouveaux fournisseurs sans remettre en cause les concepts fondamentaux.

## P11 — Pas d'entité artificielle

Une opération, une étape de traitement ou une valeur descriptive ne devient pas automatiquement une entité. Elle le devient si elle possède une identité ou un cycle de vie qu'il est nécessaire de gérer indépendamment.

# 4. Familles de données

Le modèle est organisé en neuf familles conceptuelles :

| Famille | Contenu principal |
|---|---|
| Governance Data | Organisations, applications, identités, appartenances et autorisations |
| Knowledge Management Data | Knowledge Bases, sources et associations de connaissances |
| Documentary Data | Documents, versions, artefacts originaux et contenus extraits |
| Knowledge Representation Data | Ensembles de fragments, chunks et embeddings |
| Indexing Data | Index, configurations, générations et éléments indexés |
| Structured Data | Sources structurées et ressources structurées exposées |
| Query and Generation Data | Requêtes, résultats, réponses générées et citations |
| Provider Data | Fournisseurs, références de modèles et configurations |
| Operational and Evaluation Data | Tâches, événements d'audit, politiques de conservation et données d'évaluation |

Ces familles sont des regroupements conceptuels. Elles ne préjugent pas de leur séparation physique.

# 5. Gouvernance et sécurité

Cette famille représente les propriétaires des ressources, les applications qui consomment le moteur, les acteurs et les règles d'accès.

## 5.1 Organization

Représente une organisation utilisant Universal RAG Engine.

Elle constitue le propriétaire organisationnel des ressources qu'elle administre, notamment ses Knowledge Bases, ses applications clientes et ses sources enregistrées.

Une organisation peut posséder plusieurs Knowledge Bases et enregistrer plusieurs applications clientes.

## 5.2 Client Application

Représente une application externe qui consomme les services du moteur.

Elle est enregistrée sous une organisation propriétaire dans le modèle de base. Son identité et ses autorisations d'accès restent distinctes de celles des utilisateurs humains.

L'appartenance à une organisation ne lui accorde pas automatiquement l'accès à toutes les ressources de cette organisation.

## 5.3 Identity

Représente un acteur authentifié interagissant avec le moteur.

Deux catégories sont distinguées :

- **Human Identity :** identité d'une personne.
- **Service Identity :** identité utilisée par une application ou un service.

Une identité humaine est indépendante des organisations auxquelles la personne peut appartenir. Une Service Identity est associée à une application cliente ou à un service autorisé ; elle ne remplace pas l'entité Client Application.

## 5.4 Membership

Représente l'appartenance d'une Human Identity à une Organization.

Une même identité humaine peut posséder plusieurs Memberships, chacun correspondant à une organisation et à un contexte d'autorisation distinct.

Le Membership ne donne pas automatiquement accès à toutes les ressources de l'organisation.

## 5.5 Role

Représente un regroupement nommé de permissions pouvant être attribué à une identité ou à un contexte d'appartenance.

Un rôle facilite l'organisation des autorisations, mais ne remplace ni l'identité ni la décision d'autorisation.

## 5.6 Permission

Représente une capacité ou une action autorisable sur une catégorie de ressource : consulter, gérer, importer, supprimer ou interroger, par exemple.

Une Permission est un concept distinct d'un Role et d'une Authorization Policy.

## 5.7 Authorization Policy

Représente les règles utilisées pour déterminer si un acteur peut effectuer une action sur une ressource dans un contexte donné.

L'évaluation peut prendre en compte l'identité, l'organisation, l'application cliente, le Membership, le rôle, la ressource, l'action et le contexte de la demande.

Les règles détaillées et leur application relèvent de la spécification de sécurité.

## 5.8 Resource Access Grant

Représente l'octroi d'un accès à un acteur sur une ressource ou un périmètre déterminé. L'acteur peut être une identité humaine, une identité de service ou une application cliente selon le cas.

Le Grant représente un accès attribué. L'Authorization Policy détermine si cet accès permet effectivement l'opération demandée dans le contexte considéré.

## 5.9 Règles de gouvernance retenues

1. Une Organization est propriétaire de ses ressources organisationnelles.
2. Une Human Identity est indépendante d'une Organization.
3. Une Human Identity peut appartenir à plusieurs Organizations au moyen de Memberships distincts.
4. Une Client Application est distincte de sa Service Identity.
5. L'appartenance à une organisation ne vaut pas autorisation générale.
6. La propriété d'une ressource ne vaut pas autorisation d'accès.
7. Les permissions, rôles, politiques et accès accordés sont des concepts distincts.
8. L'accès est refusé lorsqu'une autorisation requise n'est pas démontrée.

**Périmètre d'isolation :** pour le modèle conceptuel initial, l'Organization constitue la racine logique de propriété et d'isolation des ressources. Le terme *tenant context* peut désigner le contexte d'isolation transmis lors d'une opération, mais un Tenant distinct n'est pas introduit comme entité indépendante à ce stade. Une séparation ultérieure entre Tenant et Organization nécessitera un besoin explicite et une décision documentée.

# 6. Gestion des Knowledge Bases et des sources

## 6.1 Knowledge Base

Représente un espace logique indépendant de connaissances.

Elle appartient à une Organization et possède son propre périmètre de connaissances, ses configurations et ses règles d'accès. Une organisation peut posséder plusieurs Knowledge Bases.

Une Knowledge Base ne correspond pas nécessairement à une infrastructure de stockage distincte.

## 6.2 Knowledge Base Configuration

Représente la configuration fonctionnelle d'une Knowledge Base : paramètres généraux, sources autorisées, stratégies applicables et options d'exploitation.

Elle est distincte de la Knowledge Base elle-même. Une Knowledge Base peut connaître plusieurs configurations successives, tandis qu'une configuration donnée se rapporte à une seule Knowledge Base.

Les configurations propres aux index et aux fournisseurs restent représentées par leurs concepts respectifs.

## 6.3 Knowledge Source

Représente une origine identifiable d'informations exploitées par le moteur.

Deux grandes catégories sont distinguées :

- **Documentary Source :** répertoire documentaire, stockage de fichiers, site web, API documentaire ou système de gestion de documents.
- **Structured Source :** base relationnelle, API métier, source tabulaire ou système fournissant des données structurées.

Une source représente l'origine des informations, et non son association à une Knowledge Base.

## 6.4 Source Connection

Représente une connexion configurée permettant d'accéder à une Knowledge Source.

Elle distingue l'identité logique de la source des modalités de connexion à celle-ci. Les informations secrètes ne sont pas définies ni exposées par ce modèle ; elles relèvent des règles de sécurité et de gestion des secrets.

Une source peut disposer de plusieurs connexions lorsque plusieurs accès ou environnements sont nécessaires.

## 6.5 Knowledge Base Source Association

Représente l'association entre une Knowledge Source et une Knowledge Base.

Une même source peut être associée à plusieurs Knowledge Bases et une Knowledge Base peut utiliser plusieurs sources. Cette relation est donc de type plusieurs-à-plusieurs.

L'association représente l'utilisation de la source dans une base ; elle ne signifie pas que toutes les connaissances fournies par la source sont automatiquement intégrées à cette base.

## 6.6 Knowledge Item

Représente le concept générique d'un élément de connaissance identifiable qui peut être rendu disponible dans une Knowledge Base.

Knowledge Item est un concept général spécialisé notamment par :

- **Document**, pour une connaissance documentaire.
- **Structured Resource**, pour une ressource structurée exposée par une source structurée.

Ce concept permet de représenter une connaissance indépendamment de la source qui l'expose et de la Knowledge Base qui l'utilise.

## 6.7 Knowledge Base Item Association

Représente l'intégration ou la mise à disposition d'un Knowledge Item dans une Knowledge Base.

Une Knowledge Base peut contenir plusieurs Knowledge Items et un Knowledge Item peut être associé à plusieurs Knowledge Bases. Cette relation est donc plusieurs-à-plusieurs.

Cette association est distincte de la Knowledge Base Source Association : la première concerne un élément de connaissance précis ; la seconde concerne l'utilisation d'une source dans son ensemble.

Chaque Knowledge Base conserve son propre périmètre d'accès, même lorsqu'un même Knowledge Item est réutilisé dans plusieurs bases.

## 6.8 Principes validés pour les sources et les bases

1. Une Knowledge Base peut utiliser plusieurs Knowledge Sources.
2. Une Knowledge Source peut alimenter plusieurs Knowledge Bases.
3. La relation source/base est représentée par Knowledge Base Source Association.
4. L'association d'une source à une base ne signifie pas l'importation automatique de tous ses éléments.
5. La mise à disposition d'un élément précis dans une base est représentée par Knowledge Base Item Association.
6. La suppression d'une association ne signifie pas automatiquement la suppression de la source ou de l'élément original.
7. La réutilisation d'une source ou d'un élément ne supprime pas l'isolation entre les Knowledge Bases.
8. Le partage entre organisations distinctes nécessite une autorisation explicite ; il n'est pas présumé par le modèle de base.

# 7. Données documentaires

## 7.1 Document

Représente l'identité logique et durable d'un élément documentaire. Document est une spécialisation de Knowledge Item.

Son identité reste stable lorsque son contenu évolue. Il peut représenter un manuel, un livre, un article, un rapport, une procédure ou une documentation technique.

## 7.2 Document Version

Représente un état précis du contenu d'un Document.

Un Document possède une ou plusieurs versions ; chaque Document Version appartient à un seul Document. Deux versions restent des instances distinctes même si leurs attributs ou leur contenu sont identiques.

Une modification documentaire identifiable peut produire une nouvelle version sans remplacer l'identité logique du Document. Chaque version conserve ses propres informations de provenance, de contenu et de traitement.

## 7.3 Original Artifact

Représente le fichier, le contenu binaire ou l'artefact original associé à une version documentaire.

Cette entité distingue le document logique de sa représentation originale. Une Document Version peut être associée à un ou plusieurs Original Artifacts ; un artefact original appartient à une version déterminée.

Ce concept permet notamment de représenter les documents composés de plusieurs pièces ou représentations originales sans confondre ces artefacts avec les versions logiques du document.

## 7.4 Extracted Content

Représente une représentation exploitable obtenue à partir d'une Document Version.

Elle conserve sa relation avec la version d'origine ainsi que les informations de structure et de provenance disponibles. Une version peut produire plusieurs représentations extraites lorsque plusieurs extractions ou formes de contenu doivent être distinguées.

Extracted Content est une donnée dérivée ; elle ne remplace pas le Document Version ni l'Original Artifact.

## 7.5 Principes documentaires retenus

1. Un Document possède une identité logique indépendante de son contenu.
2. Une Document Version est une entité distincte appartenant à un seul Document.
3. Les versions précédentes restent distinguables conformément aux règles de conservation.
4. Un Original Artifact représente une matérialisation originale d'une version.
5. Extracted Content est une représentation dérivée d'une version précise.
6. Les relations entre document, version, artefact original et contenu extrait conservent la provenance.

# 8. Représentations préparées pour la recherche

## 8.1 Chunk Set

Représente un ensemble cohérent de fragments produits à partir d'un Extracted Content selon une stratégie de découpage déterminée.

Un même contenu extrait peut donner lieu à plusieurs Chunk Sets, par exemple lorsque différentes stratégies de segmentation sont utilisées. Le Chunk Set permet de distinguer les résultats de ces découpages.

## 8.2 Chunk

Représente un fragment de contenu produit dans un Chunk Set.

Un Chunk appartient à un seul Chunk Set et conserve sa position, ses métadonnées et sa provenance. Un Chunk Set contient plusieurs Chunks.

Le Chunk est une unité de connaissance documentaire exploitable par les mécanismes de recherche. Il reste indépendant des représentations vectorielles qui peuvent être produites à partir de lui.

## 8.3 Provider

Représente un fournisseur ou un environnement d'exécution proposant une ou plusieurs capacités externes ou hébergées : embeddings, génération, reranking ou extraction spécialisée.

Le Provider est distinct des modèles qu'il propose et des configurations par lesquelles le moteur l'utilise.

## 8.4 Model Reference

Représente l'identification d'un modèle précis utilisable par le moteur.

Elle permet notamment d'identifier le fournisseur, le modèle et sa version ou variante pertinente. Les capacités du modèle — génération, embeddings, reranking ou autre — sont associées à cette référence.

Un Provider peut proposer plusieurs Model References. Un Model Reference appartient à un Provider identifié, y compris lorsque le Provider représente un environnement hébergé par l'organisation elle-même.

## 8.5 Embedding

Représente une représentation vectorielle produite à partir d'un Chunk ou d'un autre contenu explicitement pris en charge.

Chaque Embedding est associé au contenu représenté et au Model Reference utilisé pour le produire. Un même Chunk peut posséder plusieurs Embeddings issus de modèles ou de configurations différents.

Les représentations produites par des modèles différents ne sont pas automatiquement compatibles. Le changement de modèle ne modifie ni le Document original, ni sa version, ni le contenu extrait, ni l'identité du Chunk.

## 8.6 Embeddings documentaires et embeddings de requêtes

Le modèle distingue deux usages :

- **Embeddings documentaires :** produits lors de la préparation des connaissances, principalement à partir des Chunks.
- **Embeddings de requêtes :** produits lors d'une recherche pour représenter une Query.

Les deux usages peuvent faire appel à un Model Reference compatible, mais ils n'ont pas le même cycle de vie. Les embeddings de requêtes ne doivent pas être confondus avec des Embeddings documentaires persistants.

## 8.7 Principes validés

1. Un Extracted Content peut produire plusieurs Chunk Sets.
2. Un Chunk Set regroupe les Chunks issus d'une segmentation déterminée.
3. Chaque Chunk conserve sa provenance et sa position.
4. Un Chunk est indépendant de son Embedding.
5. Un Chunk peut avoir plusieurs Embeddings.
6. Chaque Embedding identifie le modèle utilisé pour le produire.
7. Les représentations incompatibles ne sont pas mélangées dans une même recherche.
8. Les embeddings documentaires et ceux des requêtes ont des cycles de vie distincts.

# 9. Indexation

## 9.1 Index

Représente une structure logique de recherche associée à une Knowledge Base.

Une Knowledge Base peut posséder plusieurs Index correspondant à différentes capacités ou stratégies de recherche, notamment vectorielle ou textuelle. La recherche hybride peut combiner plusieurs mécanismes et ne nécessite pas obligatoirement un index physique autonome.

## 9.2 Index Configuration

Représente les paramètres de construction ou d'utilisation d'un Index.

Une configuration peut évoluer au cours du temps. Une génération d'index doit pouvoir être reliée à la configuration qui a servi à la produire.

## 9.3 Index Generation

Représente un état déterminé d'un Index construit à partir d'un ensemble de connaissances et d'une configuration identifiables.

Un Index possède plusieurs générations successives. Chaque génération reste distinguable des autres et peut être dans un état conceptuel tel qu'en préparation, disponible, active, remplacée ou en erreur.

## 9.4 Index Entry

Représente l'inclusion d'un élément de connaissance ou d'une représentation de connaissance dans une Index Generation.

Une génération contient plusieurs Index Entries. Chaque entrée identifie l'élément représenté et sa relation avec la génération concernée.

Pour un index documentaire, une entrée peut référencer un Chunk et, lorsque la stratégie est vectorielle, l'Embedding compatible correspondant. Pour une recherche structurée, une entrée peut référencer une Structured Resource ou une représentation autorisée de celle-ci.

L'Index Entry distingue les connaissances existantes dans le moteur de celles effectivement présentes dans une génération particulière d'index.

## 9.5 Principes d'indexation retenus

1. Un Index possède une identité logique indépendante de ses générations.
2. Une Knowledge Base peut posséder plusieurs Index.
3. Un Index peut posséder plusieurs Index Generations.
4. Chaque génération est associée aux connaissances et à la configuration ayant servi à sa construction.
5. Une génération contient les Index Entries qui représentent les éléments effectivement indexés.
6. Les mécanismes de recherche utilisent une génération compatible avec leur stratégie.
7. Une modification de configuration peut nécessiter une nouvelle génération, sans l'imposer systématiquement.
8. Index, Index Configuration, Index Generation et Index Entry sont des concepts distincts.

# 10. Données structurées

## 10.1 Structured Source

Structured Source est une spécialisation de Knowledge Source. Elle représente une origine fournissant des données structurées, notamment une base relationnelle, une API métier, une source tabulaire ou un système externe.

## 10.2 Structured Resource

Structured Resource est une spécialisation de Knowledge Item. Elle représente une ressource identifiable exposée par une Structured Source, par exemple une table, une vue, une collection ou une ressource d'API.

Une Structured Source peut exposer plusieurs Structured Resources. Une Structured Resource conserve sa relation avec la source qui l'expose.

Une Structured Resource peut être rendue accessible dans une ou plusieurs Knowledge Bases par Knowledge Base Item Association, sous réserve des autorisations applicables.

## 10.3 Résultats structurés

Les données retournées par l'interrogation d'une Structured Resource sont représentées comme des résultats de recherche spécialisés. Elles conservent leur provenance vers la Structured Source et la Structured Resource concernées.

Un Structured Result n'est pas nécessairement une entité indépendante du Retrieval Result : il constitue un type de résultat de récupération lorsque le moteur restitue une donnée structurée.

## 10.4 Principes des données structurées

1. Les sources structurées restent distinctes des sources documentaires dans leur mode d'exploitation.
2. Une Structured Source peut exposer plusieurs Structured Resources.
3. Une Structured Resource peut être associée à une Knowledge Base selon les droits applicables.
4. Les résultats structurés conservent leur provenance.
5. Les ressources et données sensibles restent soumises aux mêmes exigences d'autorisation et d'isolation que les connaissances documentaires.
6. Les données structurées ne doivent pas être obligatoirement transformées en documents ou en Chunks pour être exploitées.

# 11. Requêtes, résultats et réponses

## 11.1 Query

Représente une demande adressée au moteur.

Elle est associée au contexte vérifié de l'opération : application cliente, identité à l'origine de la demande, organisation, mode de traitement et Knowledge Bases ou ressources autorisées concernées.

Une Query est distincte d'une conversation complète. Le modèle de conversation n'est pas imposé au cœur du moteur.

Une Query peut concerner une ou plusieurs Knowledge Bases, selon les permissions et le périmètre de la demande.

## 11.2 Retrieval Result

Représente un élément retourné par une opération de recherche associée à une Query.

Un résultat peut provenir d'une recherche vectorielle, textuelle, hybride ou d'une source structurée. Il conserve sa provenance et son lien avec la Query à laquelle il répond.

Une Query peut produire plusieurs Retrieval Results. Une recherche peut également ne retourner aucun résultat.

## 11.3 Generated Answer

Représente une réponse produite par un modèle de langage à la suite d'une Query.

Le modèle distingue deux modes de génération :

- **DIRECT_LLM :** le LLM répond sans Retrieval préalable dans les Knowledge Bases pour cette demande. La réponse ne doit pas être présentée comme fondée sur des connaissances récupérées dans le moteur.
- **RETRIEVAL_AUGMENTED :** le moteur récupère d'abord des connaissances autorisées, puis les fournit au LLM pour produire la réponse. La réponse conserve son lien avec les résultats et les sources effectivement utilisés.

Une Query peut également être traitée en mode **RETRIEVAL_ONLY** : le moteur retourne les Retrieval Results sans produire de Generated Answer.

Les trois modes sont distincts :

| Mode | Retrieval préalable | Génération LLM | Résultat principal |
|---|---|---|---|
| RETRIEVAL_ONLY | Oui | Non | Retrieval Results |
| DIRECT_LLM | Non | Oui | Generated Answer |
| RETRIEVAL_AUGMENTED | Oui | Oui | Generated Answer liée aux connaissances récupérées |

Une Query peut ne produire aucune Generated Answer, ou produire une réponse dans le cadre de son traitement. Les réponses alternatives ou les tentatives multiples relèvent des futures spécifications d'exécution si elles deviennent nécessaires.

## 11.4 Citation

Représente une référence reliant une Generated Answer à une information qui a effectivement contribué à cette réponse.

Une citation documentaire peut identifier le Document, la Document Version et le Chunk pertinents. Une citation structurée peut identifier la Structured Source, la Structured Resource et l'élément de données concerné lorsque celui-ci est localisable.

Les résultats simplement récupérés ne sont pas automatiquement des citations. Une réponse DIRECT_LLM ne reçoit pas artificiellement de citations issues des Knowledge Bases.

## 11.5 Principes d'exploitation retenus

1. Query, Retrieval Result et Generated Answer sont distincts.
2. Une Query peut retourner des résultats sans génération LLM.
3. Une génération directe est distinguée d'une génération augmentée par Retrieval.
4. Une réponse augmentée conserve le lien vers les connaissances effectivement utilisées.
5. Les résultats documentaires et structurés conservent leur provenance.
6. Une Citation référence une information ayant contribué à la réponse.
7. L'absence de connaissances suffisantes peut être représentée par l'état ou le résultat de la Query ou de la Generated Answer ; elle ne nécessite pas une entité autonome.

# 12. Fournisseurs et modèles

## 12.1 Provider

Représente un fournisseur ou un environnement d'exécution proposant des capacités utilisables par le moteur. Il peut s'agir d'un fournisseur externe ou d'un environnement hébergé par l'organisation.

Un Provider peut proposer plusieurs modèles et plusieurs capacités.

## 12.2 Model Reference

Représente un modèle précis proposé ou hébergé par un Provider.

Il permet d'identifier le modèle et les capacités qu'il expose, notamment génération, embeddings, reranking ou extraction spécialisée. Un même Provider peut proposer plusieurs Model References.

## 12.3 Provider Configuration

Représente la configuration par laquelle le moteur utilise un Provider et, lorsque nécessaire, un Model Reference particulier.

Elle est distincte du Provider et du modèle lui-même. Son périmètre d'application peut relever de la plateforme, d'une organisation ou d'une Knowledge Base ; les règles exactes seront définies dans les spécifications de configuration et de sécurité.

Les secrets ne sont pas représentés comme des valeurs lisibles dans le modèle conceptuel. Leur gestion relève d'un mécanisme sécurisé distinct.

## 12.4 Principes retenus

1. Provider, Model Reference et Provider Configuration sont distincts.
2. Un Provider peut proposer plusieurs Model References.
3. Une Provider Configuration identifie le fournisseur et, le cas échéant, le modèle sélectionné.
4. Le cœur du moteur ne dépend pas d'un fournisseur particulier.
5. Le modèle utilisé pour une représentation ou une génération doit pouvoir être identifié.

# 13. Données opérationnelles et gouvernance du cycle de vie

## 13.1 Job

Représente une opération nécessitant un suivi, notamment une importation, une ingestion, une extraction, une indexation, une réindexation ou une suppression.

Un Job identifie l'opération et son état général. Il ne devient pas propriétaire des données métier manipulées par l'opération.

## 13.2 Audit Event

Représente une trace historique d'un événement important concernant l'utilisation ou l'administration du moteur.

Un Audit Event peut être lié à un acteur, une organisation, une application et une ressource concernée. Il ne remplace pas l'état actuel de la ressource.

Un Audit Event est distinct d'un Job : le Job suit une opération ; l'Audit Event conserve la trace d'un événement.

## 13.3 Data Retention Policy

Représente une politique de conservation applicable à une organisation ou à une catégorie de données lorsque cette politique doit être gérée et vérifiée.

Elle permet de représenter les règles de conservation et de suppression sans définir ici leur exécution technique.

## 13.4 Principes opérationnels

1. Job représente une opération à suivre.
2. Audit Event représente une trace historique.
3. Data Retention Policy représente une règle de conservation.
4. Ces concepts ne remplacent pas les entités métier qu'ils concernent.
5. Les politiques de conservation et les événements d'audit doivent respecter les règles de confidentialité et d'accès.

# 14. Évaluation de la qualité

Cette famille représente les données nécessaires à des évaluations reproductibles de la qualité de la recherche et des réponses, conformément à NFR-019.

## 14.1 Evaluation Dataset

Représente un ensemble organisé de données destiné à l'évaluation du moteur.

## 14.2 Evaluation Case

Représente un cas individuel appartenant à un Evaluation Dataset : question, contexte attendu et éléments de référence nécessaires à l'évaluation.

## 14.3 Evaluation Metric

Représente une mesure définie permettant d'évaluer une dimension de qualité, par exemple la pertinence des résultats, la fidélité au contexte ou l'exactitude des références.

## 14.4 Evaluation Run

Représente l'exécution d'une évaluation sur un Evaluation Dataset avec une version ou configuration identifiable du moteur.

## 14.5 Evaluation Result

Représente le résultat obtenu pour un Evaluation Case lors d'un Evaluation Run, selon une ou plusieurs Evaluation Metrics.

Ces entités permettent de conserver des scénarios et résultats reproductibles. Les algorithmes, jeux de référence et seuils de qualité seront précisés dans le document consacré aux tests et à l'évaluation.

# 15. Relations conceptuelles et cardinalités

Les cardinalités ci-dessous décrivent le modèle conceptuel. Elles ne constituent pas des contraintes physiques de base de données.

## 15.1 Gouvernance

| Entité A | Relation | Entité B | Cardinalité conceptuelle |
|---|---|---|---|
| Organization | possède | Client Application | 1 Organization → 0..N Applications ; une Application → 1 Organization propriétaire |
| Organization | possède | Knowledge Base | 1 Organization → 0..N Knowledge Bases ; une Knowledge Base → 1 Organization propriétaire |
| Human Identity | possède | Membership | 1 Identity → 0..N Memberships |
| Organization | possède | Membership | 1 Organization → 0..N Memberships |
| Membership | concerne | Human Identity et Organization | chaque Membership → 1 Identity et 1 Organization |
| Client Application | utilise | Service Identity | 1 Application → 0..N Service Identities ; une Service Identity → 1 Application de référence |
| Role | regroupe | Permission | relation N:N |
| Membership ou Service Identity | reçoit | Role | relation N:N selon les règles d'autorisation |
| Authorization Policy | gouverne | ressource ou catégorie de ressources | relation 1:N ou N:N selon le périmètre de la politique |
| Resource Access Grant | accorde un accès à | acteur et ressource | chaque Grant → 1 acteur et 1 ressource ou périmètre |

## 15.2 Knowledge Bases et sources

| Entité A | Relation | Entité B | Cardinalité conceptuelle |
|---|---|---|---|
| Organization | possède | Knowledge Source | 1 Organization → 0..N Sources dans le modèle de base |
| Knowledge Base | possède | Knowledge Base Configuration | 1 Knowledge Base → 1..N configurations successives ; une configuration → 1 Knowledge Base |
| Knowledge Source | possède | Source Connection | 1 Source → 0..N Connections |
| Knowledge Base | utilise | Knowledge Source via Knowledge Base Source Association | relation N:N |
| Knowledge Base Source Association | relie | Knowledge Base et Knowledge Source | chaque association → 1 Base et 1 Source |
| Knowledge Base | contient ou expose | Knowledge Item via Knowledge Base Item Association | relation N:N |
| Knowledge Base Item Association | relie | Knowledge Base et Knowledge Item | chaque association → 1 Base et 1 Item |

## 15.3 Documents et représentations

| Entité A | Relation | Entité B | Cardinalité conceptuelle |
|---|---|---|---|
| Documentary Source | fournit | Document | 1 Source → 0..N Documents ; un Document possède une source d'origine principale dans le modèle de base |
| Document | possède | Document Version | 1 Document → 1..N Versions ; une Version → 1 Document |
| Document Version | est matérialisée par | Original Artifact | 1 Version → 0..N Artifacts ; un Artifact → 1 Version |
| Document Version | produit | Extracted Content | 1 Version → 0..N contenus extraits ; un contenu extrait → 1 Version |
| Extracted Content | produit | Chunk Set | 1 contenu → 0..N Chunk Sets ; un Chunk Set → 1 contenu |
| Chunk Set | regroupe | Chunk | 1 Chunk Set → 1..N Chunks ; un Chunk → 1 Chunk Set |
| Chunk | possède | Embedding | 1 Chunk → 0..N Embeddings ; un Embedding → 1 contenu source représenté |
| Embedding | est produit par | Model Reference | chaque Embedding → 1 Model Reference |

## 15.4 Indexation

| Entité A | Relation | Entité B | Cardinalité conceptuelle |
|---|---|---|---|
| Knowledge Base | possède | Index | 1 Knowledge Base → 0..N Indexes ; un Index → 1 Knowledge Base |
| Index | utilise | Index Configuration | 1 Index → 1..N configurations successives |
| Index | possède | Index Generation | 1 Index → 0..N Generations ; une Generation → 1 Index |
| Index Generation | est construite selon | Index Configuration | chaque Generation → 1 configuration de référence |
| Index Generation | contient | Index Entry | 1 Generation → 0..N Entries ; une Entry → 1 Generation |
| Index Entry | référence | Chunk/Embedding ou Structured Resource | chaque Entry → 1 représentation ou ressource cible compatible avec le type d'index |

## 15.5 Données structurées

| Entité A | Relation | Entité B | Cardinalité conceptuelle |
|---|---|---|---|
| Structured Source | expose | Structured Resource | 1 Source → 0..N Resources ; une Resource → 1 Source de référence |
| Structured Resource | est rendue disponible dans | Knowledge Base via Knowledge Base Item Association | relation N:N |
| Structured Result | provient de | Structured Resource | chaque résultat structuré → 1 ressource d'origine identifiable |

## 15.6 Requêtes, résultats et réponses

| Entité A | Relation | Entité B | Cardinalité conceptuelle |
|---|---|---|---|
| Client Application | émet | Query | 1 Application → 0..N Queries ; une Query → 1 Application d'origine |
| Identity | est à l'origine de | Query | une Query → 1 identité ou principal d'exécution identifié |
| Query | concerne | Knowledge Base | relation N:N lorsque plusieurs bases sont interrogées |
| Query | produit | Retrieval Result | 1 Query → 0..N Results ; un Result → 1 Query |
| Retrieval Result | référence | Knowledge Item ou ressource structurée | chaque Result conserve une provenance identifiable |
| Query | peut produire | Generated Answer | 1 Query → 0..N Answers ; une Answer → 1 Query |
| Generated Answer | est produite par | Model Reference | chaque réponse LLM → 1 Model Reference identifié |
| Generated Answer | possède | Citation | 1 Answer → 0..N Citations ; une Citation → 1 Answer |
| Citation | référence | Document Version/Chunk ou Structured Resource/élément identifiable | chaque Citation → 1 cible probante identifiable |

## 15.7 Fournisseurs, opérations et évaluation

| Entité A | Relation | Entité B | Cardinalité conceptuelle |
|---|---|---|---|
| Provider | propose | Model Reference | 1 Provider → 0..N Models ; un Model Reference → 1 Provider |
| Provider | fait l'objet de | Provider Configuration | 1 Provider → 0..N Configurations |
| Provider Configuration | sélectionne éventuellement | Model Reference | une Configuration → 0..N modèles selon sa portée fonctionnelle |
| Job | concerne | ressource ou opération | chaque Job identifie au moins une opération ou cible suivie |
| Audit Event | identifie | acteur et ressource concernée | l'acteur ou la ressource peuvent être absents pour certains événements système |
| Data Retention Policy | s'applique à | organisation ou catégorie de données | une politique peut couvrir plusieurs ressources d'un périmètre défini |
| Evaluation Dataset | regroupe | Evaluation Case | 1 Dataset → 1..N Cases |
| Evaluation Run | utilise | Evaluation Dataset | chaque Run → 1 Dataset |
| Evaluation Run | produit | Evaluation Result | 1 Run → 0..N Results |
| Evaluation Result | concerne | Evaluation Case et Evaluation Metric | chaque Result → 1 Case et 1..N Metrics |

# 16. Parcours conceptuel des connaissances

Le parcours documentaire principal est le suivant :

```text
ORGANIZATION
    |
    v
KNOWLEDGE BASE
    |
    +---- KNOWLEDGE BASE SOURCE ASSOCIATION ---- KNOWLEDGE SOURCE
    |
    +---- KNOWLEDGE BASE ITEM ASSOCIATION ------- KNOWLEDGE ITEM
                                                    |
                                                    v
                                                 DOCUMENT
                                                    |
                                                    v
                                             DOCUMENT VERSION
                                                    |
                                  +-----------------+----------------+
                                  |                                  |
                                  v                                  v
                           ORIGINAL ARTIFACT                  EXTRACTED CONTENT
                                                                     |
                                                                     v
                                                                 CHUNK SET
                                                                     |
                                                                     v
                                                                   CHUNKS
                                                                     |
                                                                     v
                                                                 EMBEDDINGS
                                                                     |
                                                                     v
                                                                   INDEX
                                                                     |
                                                                     v
                                                              INDEX GENERATION
                                                                     |
                                                                     v
                                                                 INDEX ENTRY
```

Ce parcours est conceptuel. Les sources structurées suivent une branche adaptée : Structured Source → Structured Resource → Knowledge Base Item Association → exploitation structurée.

# 17. Couverture des exigences fonctionnelles

La matrice suivante relie chaque exigence FR du cahier des charges aux entités et relations qui permettent de la représenter. Certaines exigences sont aussi satisfaites par des règles ou des comportements ; elles ne nécessitent donc pas systématiquement une entité supplémentaire.

| Exigence | Besoin | Entités et relations principales | Couverture conceptuelle |
|---|---|---|---|
| FR-001 | Gestion des organisations | Organization et ses relations avec les ressources | Couvert |
| FR-002 | Applications clientes | Client Application, Organization, Service Identity | Couvert |
| FR-003 | Utilisateurs et permissions | Identity, Membership, Role, Permission, Authorization Policy, Resource Access Grant | Couvert |
| FR-004 | Gestion des Knowledge Bases | Organization, Knowledge Base | Couvert |
| FR-005 | Configuration des Knowledge Bases | Knowledge Base Configuration, Provider Configuration, Index Configuration | Couvert |
| FR-006 | Isolation des Knowledge Bases | Organization, Knowledge Base, Membership, Authorization Policy, Resource Access Grant | Couvert conceptuellement ; règles détaillées dans la sécurité |
| FR-007 | Gestion des sources | Knowledge Source, Source Connection, Knowledge Base Source Association | Couvert |
| FR-008 | Importation documentaire | Document, Document Version, Original Artifact, Job | Couvert |
| FR-009 | Extraction et normalisation | Document Version, Extracted Content, Job | Couvert au niveau des données produites et suivies |
| FR-010 | Cycle de vie documentaire | Document, Document Version, Knowledge Base Item Association, Chunk, Embedding, Index Entry | Couvert conceptuellement |
| FR-011 | Découpage documentaire | Extracted Content, Chunk Set, Chunk | Couvert |
| FR-012 | Gestion des embeddings | Chunk, Embedding, Provider, Model Reference | Couvert |
| FR-013 | Indexation et réindexation | Index, Index Configuration, Index Generation, Index Entry, Job | Couvert conceptuellement |
| FR-014 | Recherche vectorielle | Query, Index, Index Generation, Embedding, Retrieval Result | Couvert |
| FR-015 | Recherche textuelle | Query, Index, Index Generation, Chunk, Retrieval Result | Couvert |
| FR-016 | Recherche hybride | Query, plusieurs Index ou stratégies, Retrieval Result | Couvert |
| FR-017 | Filtrage et classement | Query, Knowledge Base, Knowledge Base Item Association, autorisations, Retrieval Result | Couvert ; règles de recherche détaillées ailleurs |
| FR-018 | Génération augmentée | Query, Retrieval Result, Generated Answer, Citation | Couvert |
| FR-019 | Fournisseurs LLM | Provider, Model Reference, Provider Configuration | Couvert |
| FR-020 | Références documentaires | Generated Answer, Citation, Document Version, Chunk, Structured Resource | Couvert |
| FR-021 | Informations insuffisantes | Query et état/résultat de Generated Answer ou Retrieval Result | Couvert sans entité autonome nécessaire |
| FR-022 | Connexion aux données structurées | Structured Source, Source Connection, Structured Resource | Couvert |
| FR-023 | Interrogation contrôlée | Identity, Client Application, Permission, Authorization Policy, Resource Access Grant, Structured Resource | Couvert conceptuellement ; contrôles détaillés dans la sécurité |
| FR-024 | Combinaison des connaissances | Query, Retrieval Result, Structured Resource, Generated Answer, Citation | Couvert |
| FR-025 | Interface publique | Client Application, Identity, Query | Données d'identité couvertes ; contrats API définis dans le document API |
| FR-026 | Gestion des requêtes | Query, Client Application, Identity, Job lorsque le suivi différé est nécessaire | Couvert |
| FR-027 | Administration | Organization, Client Application, Identity, Knowledge Base, Knowledge Source, Job, Provider Configuration | Couvert |
| FR-028 | Journalisation et supervision | Audit Event, Job | Données de traçabilité couvertes ; métriques techniques dans l'observabilité |

# 18. Couverture des exigences non fonctionnelles

Les exigences non fonctionnelles ne correspondent pas toutes à des entités. Plusieurs sont satisfaites par des relations, des contraintes, des comportements ou des propriétés de l'architecture. La matrice distingue la contribution du modèle de données de ce qui sera défini ailleurs.

| Exigence | Besoin | Contribution du modèle conceptuel | Spécification complémentaire |
|---|---|---|---|
| NFR-001 | Isolation des organisations | Organization, Knowledge Base, Membership, Authorization Policy, Resource Access Grant | Sécurité et isolation |
| NFR-002 | Contrôle des accès | Identity, Service Identity, Role, Permission, Authorization Policy, Resource Access Grant | Sécurité et authentification |
| NFR-003 | Protection des données sensibles | Propriété, périmètres d'accès, Provider Configuration, Source Connection, Data Retention Policy | Sécurité, chiffrement et gestion des secrets |
| NFR-004 | Protection contre les injections | Provenance des sources et distinction des contenus externes | Sécurité des traitements et génération |
| NFR-005 | Gestion des secrets | Références de configuration des fournisseurs et connexions | Gestion sécurisée des secrets |
| NFR-006 | Intégrité des connaissances | Relations Document/Version/Content/Chunk/Embedding/Index Generation | Contraintes et transactions |
| NFR-007 | Résilience | Job, Index Generation et états des ressources | Reprise et gestion des erreurs |
| NFR-008 | Traçabilité | Audit Event, provenance, Citation et versions | Audit et observabilité |
| NFR-009 | Cohérence après modification | Versions documentaires, associations et générations d'index | Gestion du cycle de vie et synchronisation |
| NFR-010 | Performance | Index et Index Generation identifient les structures de recherche | Mesures et objectifs de performance |
| NFR-011 | Évolutivité | Séparation des domaines et associations indépendantes | Architecture et déploiement |
| NFR-012 | Traitements volumineux | Job | Exécution asynchrone et capacité de traitement |
| NFR-013 | Modularité | Entités regroupées par domaines cohérents | Architecture modulaire |
| NFR-014 | Extensibilité | Provider, Model Reference, Source, Structured Resource et configurations | Contrats d'extension |
| NFR-015 | Maintenabilité | Concepts et relations documentés | Qualité du code et documentation |
| NFR-016 | Interopérabilité | Client Application, Knowledge Source et Provider | Contrats API et connecteurs |
| NFR-017 | Portabilité | Absence de dépendance aux structures physiques dans le modèle conceptuel | Déploiement |
| NFR-018 | Observabilité | Job et Audit Event | Journaux, métriques et traces techniques |
| NFR-019 | Évaluation de la qualité | Evaluation Dataset, Case, Metric, Run et Result | Méthodes et seuils d'évaluation |
| NFR-020 | Vérifiabilité | Liens entre exigences, données, provenance et évaluations | Stratégie de tests |

# 19. Décisions conceptuelles retenues et sujets reportés

## 19.1 Principes retenus dans ce modèle

- Document et Document Version sont deux entités distinctes.
- Une même source peut être associée à plusieurs Knowledge Bases.
- L'association d'une source à une base est distincte de l'association des éléments individuels de connaissance à cette base.
- Une Knowledge Base peut contenir plusieurs Knowledge Items ; un même Knowledge Item peut être associé à plusieurs bases sous réserve des autorisations.
- Un Chunk est distinct de son Embedding.
- Un Chunk peut posséder plusieurs Embeddings.
- Provider, Model Reference et Provider Configuration sont distincts.
- Index et Index Generation sont distincts ; Index Entry représente les éléments présents dans une génération.
- Structured Source et Structured Resource sont représentés sans imposer la conversion des données structurées en documents.
- Retrieval Only, Direct LLM Generation et Retrieval-Augmented Generation sont trois modes distincts.
- Organization constitue la racine logique de propriété et d'isolation du modèle initial ; Tenant n'est pas une entité indépendante dans cette version.
- Les scénarios d'évaluation reproductibles sont représentés dans le modèle.

## 19.2 Sujets explicitement reportés

Les questions suivantes ne bloquent pas le modèle conceptuel, mais devront être résolues dans les spécifications correspondantes :

1. Le partage de sources ou d'éléments de connaissance entre organisations différentes.
2. Une éventuelle séparation future entre Tenant et Organization.
3. Le périmètre exact des Provider Configurations : plateforme, organisation ou Knowledge Base.
4. Les politiques détaillées de sélection et de conservation des versions documentaires.
5. Les mécanismes de synchronisation des sources et de propagation de leurs modifications.
6. Les règles précises de sélection des Knowledge Items au sein d'une source.
7. La description détaillée des structures accessibles dans les sources structurées.
8. Le niveau de conservation des requêtes, résultats et réponses.
9. La gestion des conversations et de la mémoire conversationnelle, qui n'est pas obligatoire dans le cœur du moteur.
10. Les règles détaillées de conservation, d'archivage et de suppression des données.

Ces sujets sont reportés vers les spécifications spécialisées ; ils ne doivent pas être transformés en décisions techniques implicites.

# 20. Éléments qui ne constituent pas des entités autonomes à ce niveau

Pour éviter une prolifération artificielle, les concepts suivants sont traités à ce stade comme des opérations, des états, des attributs ou des notions relevant de spécifications ultérieures, et non comme des entités fondamentales supplémentaires :

- Extraction, normalisation, découpage, génération d'embeddings et indexation : opérations de traitement.
- Embedding de requête : représentation temporaire d'une Query, distincte des Embeddings documentaires persistants.
- Retrieval Execution et Generation Execution : exécutions détaillées ; leur modélisation persistante sera décidée si les besoins de suivi l'exigent.
- Context Package : représentation construite pour une génération ; son existence conceptuelle est couverte par les liens entre Query, Retrieval Results, Generated Answer et Citations, sans imposer une entité persistante à ce stade.
- Score, position, format, taille, langue, date et autres propriétés descriptives : attributs ou valeurs associés aux entités concernées.
- Conversation et Message : capacités conversationnelles optionnelles, hors du cœur conceptuel obligatoire.
- Groupe d'utilisateurs : extension possible du modèle de gouvernance, non nécessaire pour couvrir les exigences actuelles.

Une future spécification pourra promouvoir l'un de ces concepts au rang d'entité si un cycle de vie ou un besoin de traçabilité autonome est établi.

# 21. Conditions de validation

Le modèle conceptuel pourra être validé lorsque :

1. Les familles de données et leurs principales entités seront approuvées.
2. Les responsabilités de chaque entité seront compréhensibles et non redondantes.
3. Les associations nécessaires seront identifiées.
4. Les cardinalités conceptuelles seront examinées.
5. Les données originales et dérivées seront distinguées.
6. Les sources documentaires et structurées seront représentées.
7. Les trois modes de traitement des requêtes seront distingués.
8. La provenance des résultats et des citations sera conservée.
9. Les 28 exigences fonctionnelles auront une couverture identifiée.
10. Les 20 exigences non fonctionnelles auront une contribution du modèle ou une spécification complémentaire identifiée.
11. Les questions reportées seront explicitement documentées.
12. La cohérence avec les documents 00 à 03 sera vérifiée.

# 22. Conclusion

Le modèle conceptuel de Universal RAG Engine représente les organisations, les applications, les identités, les espaces de connaissances, les sources, les documents et leurs versions, les représentations dérivées, les index, les données structurées, les requêtes, les réponses, les fournisseurs et les données opérationnelles et d'évaluation.

Il distingue les informations originales de leurs représentations dérivées, les sources de leur utilisation dans les Knowledge Bases, les demandes de leurs résultats, et les réponses directes des réponses augmentées par Retrieval.

La matrice de traçabilité relie les exigences fonctionnelles et non fonctionnelles aux entités, relations et spécifications complémentaires nécessaires.

**Le modèle conceptuel doit représenter le cycle de vie des connaissances et leur exploitation, indépendamment des applications clientes et des technologies qui seront choisies ultérieurement.**
