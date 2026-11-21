# UNIVERSAL RAG ENGINE

## Document 05 — Knowledge Bases

**Version :** 1.0
**Statut :** VALIDATED
**Projet :** RAG-universal

---

# 1. Objectif

Ce document définit le rôle, le périmètre et les principes de gestion des Knowledge Bases dans Universal RAG Engine.

Il précise notamment :

- Ce qu'est une Knowledge Base et ce qu'elle représente dans le moteur.
- Son lien avec l'organisation propriétaire.
- Ses relations avec les sources et les éléments de connaissance.
- La distinction entre l'association d'une source et l'intégration d'un élément individuel.
- Le rôle de sa configuration.
- Son périmètre d'accès et d'utilisation.
- Ses relations avec l'indexation et les requêtes.
- Les principes généraux de son cycle de vie.

Ce document approfondit le concept de Knowledge Base déjà défini dans les documents 00 à 04. Il ne remplace pas ces documents et ne redéfinit pas les entités du modèle conceptuel.

# 2. Références et dépendances

Cette spécification s'appuie sur les documents suivants :

- `00_VISION_ET_OBJECTIFS.md` — vision, indépendance métier et organisation des connaissances.
- `DEPENDENCY_MAP.md` — dépendances entre les spécifications.
- `DECISION_LOG.md` — décisions fondatrices validées.
- `01_CAHIER_DES_CHARGES.md` — exigences fonctionnelles et non fonctionnelles.
- `02_ARCHITECTURE_GLOBALE.md` — organisation générale du moteur.
- `03_ARCHITECTURE_MODULAIRE.md` — responsabilités des modules.
- `04_MODELE_DE_DONNEES.md` — entités et relations conceptuelles.

Les concepts employés dans ce document doivent rester cohérents avec le modèle de données validé, notamment :

- Organization.
- Knowledge Base.
- Knowledge Base Configuration.
- Knowledge Source.
- Source Connection.
- Knowledge Base Source Association.
- Knowledge Item.
- Knowledge Base Item Association.
- Index et ses concepts associés.
- Identity, Client Application, Membership et mécanismes d'autorisation.

# 3. Définition et rôle d'une Knowledge Base

## 3.1 Définition

Une Knowledge Base est un espace logique indépendant dans lequel Universal RAG Engine organise les éléments de connaissance qu'une application ou une identité autorisée peut exploiter.

Elle constitue un périmètre identifiable de connaissances. Elle permet de regrouper des éléments provenant d'une ou plusieurs sources, de leur appliquer un contexte de gestion propre et de les rendre accessibles selon des règles d'autorisation déterminées.

Une Knowledge Base n'est :

- Ni une simple liste de fichiers.
- Ni une source documentaire.
- Ni un index vectoriel.
- Ni une application cliente.
- Ni nécessairement une base de données ou une infrastructure de stockage distincte.

Elle représente un espace logique de connaissances et d'utilisation.

## 3.2 Responsabilités principales

Une Knowledge Base permet de :

1. Définir un espace logique de connaissances.
2. Être rattachée à une organisation propriétaire.
3. Référencer une ou plusieurs sources.
4. Déterminer quels éléments de connaissance sont associés à cet espace.
5. Disposer de sa propre configuration fonctionnelle.
6. Être soumise à des règles d'accès et d'utilisation.
7. Disposer des index nécessaires à ses capacités de recherche.
8. Être ciblée par les requêtes des applications autorisées.
9. Être activée, désactivée, archivée ou supprimée selon les règles de cycle de vie applicables.

# 4. Organisation et propriété

## 4.1 Propriété organisationnelle

Dans le modèle de base, une Knowledge Base appartient à une seule Organization propriétaire.

Une Organization peut posséder plusieurs Knowledge Bases indépendantes.

La propriété détermine le périmètre administratif de la Knowledge Base. Elle ne signifie pas que tous les utilisateurs ou toutes les applications de l'organisation disposent automatiquement d'un accès à cette base.

## 4.2 Indépendance des Knowledge Bases

Deux Knowledge Bases appartenant à une même organisation restent deux espaces logiques distincts.

Elles peuvent avoir :

- Des éléments de connaissance différents.
- Des associations de sources différentes.
- Des configurations fonctionnelles différentes.
- Des règles d'accès différentes.
- Des index et générations d'index différents.
- Des applications utilisatrices différentes.

L'appartenance à une même organisation ne doit pas conduire à mélanger automatiquement leurs connaissances.

## 4.3 Accès entre organisations

Le modèle initial ne présume pas qu'une Knowledge Base est partagée entre plusieurs organisations.

Un accès externe au périmètre de l'organisation propriétaire ne peut être envisagé qu'au moyen d'une autorisation explicite et contrôlée. La propriété de la base reste attachée à son organisation d'origine.

Les modalités de partage interorganisationnel, si elles sont retenues, relèvent des spécifications de sécurité et d'isolation.

# 5. Sources et Knowledge Bases

## 5.1 Association d'une source à une Knowledge Base

Une Knowledge Source représente l'origine identifiable des informations. Une Knowledge Base Source Association représente l'utilisation de cette source dans une Knowledge Base déterminée.

Une Knowledge Base peut être associée à plusieurs Knowledge Sources.

Une Knowledge Source peut être associée à plusieurs Knowledge Bases.

La relation entre Knowledge Base et Knowledge Source est donc de type plusieurs-à-plusieurs, matérialisée conceptuellement par Knowledge Base Source Association.

## 5.2 Une association de source ne signifie pas une intégration complète

L'association d'une source à une Knowledge Base signifie que cette base peut utiliser cette origine selon les autorisations et paramètres applicables.

Elle ne signifie pas que chaque document, ressource ou élément exposé par la source est automatiquement intégré dans la Knowledge Base.

Une source peut exposer de nombreux éléments alors qu'une Knowledge Base n'en utilise qu'une partie.

## 5.3 Réutilisation d'une même source

Une même source documentaire peut être utilisée dans plusieurs Knowledge Bases sans que son identité logique soit dupliquée pour chaque association.

Exemple conceptuel :

```text
                  KNOWLEDGE SOURCE
                 Documentation RH
                         |
             +-----------+-----------+
             |                       |
             v                       v
     SOURCE ASSOCIATION      SOURCE ASSOCIATION
             |                       |
             v                       v
       KNOWLEDGE BASE A        KNOWLEDGE BASE B
       RH Administration       RH Formation
```

Chaque association représente l'utilisation de la source dans une base déterminée.

La réutilisation de la source ne signifie pas que les deux bases doivent avoir les mêmes éléments, les mêmes configurations, les mêmes index ou les mêmes autorisations.

## 5.4 Source Connection

Source Connection représente une modalité de connexion à une Knowledge Source. Elle est distincte de l'association entre cette source et une Knowledge Base.

La Source Connection décrit comment le moteur peut accéder à la source. La Knowledge Base Source Association décrit dans quel espace logique cette source est utilisée.

Les règles déterminant quelle connexion est utilisée pour une association donnée seront précisées dans les spécifications relatives aux sources et à l'ingestion.

# 6. Éléments de connaissance associés à une Knowledge Base

## 6.1 Knowledge Item

Knowledge Item représente un élément de connaissance identifiable pouvant être rendu disponible dans une Knowledge Base.

Dans le modèle conceptuel validé, les spécialisations principales comprennent :

- Document, pour une connaissance documentaire.
- Structured Resource, pour une ressource structurée exposée par une Structured Source.

Knowledge Item permet de parler de ces éléments de manière générique sans confondre leurs structures ni leurs modes d'exploitation.

## 6.2 Knowledge Base Item Association

Knowledge Base Item Association représente le lien entre une Knowledge Base et un Knowledge Item déterminé.

Une Knowledge Base peut être associée à plusieurs Knowledge Items. Un même Knowledge Item peut être associé à plusieurs Knowledge Bases, sous réserve des règles de propriété et d'autorisation applicables.

Cette association représente la mise à disposition de l'élément dans un espace de connaissances déterminé.

## 6.3 Distinction entre les deux associations

Les deux associations ont des rôles différents :

| Association | Ce qu'elle relie | Ce qu'elle signifie |
|---|---|---|
| Knowledge Base Source Association | Knowledge Base et Knowledge Source | La base utilise ou peut utiliser cette origine. |
| Knowledge Base Item Association | Knowledge Base et Knowledge Item | Cet élément précis est associé ou rendu disponible dans la base. |

L'une ne remplace pas l'autre.

```text
KNOWLEDGE SOURCE
       |
       +------ DOCUMENT A
       +------ DOCUMENT B
       +------ DOCUMENT C

       |
       v
KNOWLEDGE BASE SOURCE ASSOCIATION
       |
       v
KNOWLEDGE BASE A
       |
       +------ ITEM ASSOCIATION ------ DOCUMENT A
       |
       +------ ITEM ASSOCIATION ------ DOCUMENT C
```

La Knowledge Base peut ainsi utiliser une source sans intégrer automatiquement tous les éléments qu'elle expose.

## 6.4 Indépendance des associations

L'association d'un Knowledge Item à une Knowledge Base est propre à cette base.

Si un même Document est associé à deux Knowledge Bases, chacune conserve son propre contexte d'utilisation et son propre périmètre d'accès.

Le retrait d'un Knowledge Item d'une Knowledge Base ne signifie pas automatiquement :

- La suppression du Document original.
- La suppression de ses versions.
- La suppression de la Knowledge Source.
- Le retrait du même élément d'une autre Knowledge Base.

Les conséquences sur les représentations dérivées et les index concernés seront définies dans les spécifications du cycle de vie, de l'ingestion et de l'indexation.

# 7. Configuration d'une Knowledge Base

## 7.1 Knowledge Base Configuration

Knowledge Base Configuration représente la configuration fonctionnelle propre à une Knowledge Base.

Elle est distincte de l'identité de la Knowledge Base. Une Knowledge Base peut connaître plusieurs configurations successives ; chaque configuration se rapporte à une seule Knowledge Base.

La configuration exprime les paramètres de fonctionnement propres à l'espace de connaissances, sans devenir une copie des configurations spécialisées d'index ou de fournisseurs.

## 7.2 Portée de la configuration

Au niveau conceptuel, une configuration de Knowledge Base peut couvrir des catégories de paramètres telles que :

- Les caractéristiques générales de l'espace de connaissances.
- Les options d'utilisation des sources associées.
- Les règles générales d'admission des éléments de connaissance.
- Les paramètres fonctionnels de mise à disposition et d'utilisation des connaissances.
- Les préférences générales de recherche applicables à la base.
- Les références vers des configurations spécialisées lorsque nécessaire.

Cette liste indique des catégories fonctionnelles et ne constitue pas la définition des attributs définitifs de la configuration.

## 7.3 Distinction avec les autres configurations

Knowledge Base Configuration ne doit pas être confondue avec :

- **Source Connection :** décrit une modalité d'accès à une source.
- **Index Configuration :** décrit les paramètres propres à la construction ou à l'utilisation d'un index.
- **Provider Configuration :** décrit l'utilisation d'un fournisseur ou d'un modèle externe.

La configuration de la Knowledge Base peut référencer ou sélectionner des configurations spécialisées, mais ne doit pas absorber leurs responsabilités.

## 7.4 Évolution des configurations

Les changements de configuration doivent pouvoir être distingués dans le temps.

Le modèle conceptuel prévoit plusieurs configurations successives pour une même Knowledge Base. La configuration applicable à une opération doit pouvoir être identifiée lorsque cela est nécessaire à la traçabilité.

Les règles de versionnement, d'activation et de compatibilité des configurations seront définies dans les spécifications spécialisées.

# 8. Accès et utilisation d'une Knowledge Base

## 8.1 Accès explicite

L'accès à une Knowledge Base est soumis aux mécanismes de gouvernance et d'autorisation définis dans le modèle de données et dans la spécification de sécurité.

La décision d'accès peut tenir compte notamment :

- De l'identité humaine ou de service.
- De l'appartenance à l'organisation.
- De l'application cliente à l'origine de la demande.
- De la Knowledge Base ciblée.
- De l'opération demandée.
- Des politiques et accès accordés applicables.

## 8.2 L'application cliente n'hérite pas de tous les accès

Une application cliente enregistrée auprès d'une organisation ne doit pas recevoir automatiquement l'accès à toutes les Knowledge Bases de cette organisation.

L'accès doit être accordé selon les règles applicables à l'application et au périmètre demandé.

## 8.3 L'identité humaine conserve son contexte

Une identité humaine peut appartenir à plusieurs organisations au moyen de Memberships distincts.

Lorsqu'elle utilise une application pour interroger une Knowledge Base, le contexte organisationnel et les autorisations applicables doivent être pris en compte.

## 8.4 Recherche sur une ou plusieurs Knowledge Bases

Une requête peut cibler une ou plusieurs Knowledge Bases auxquelles l'acteur dispose d'un accès autorisé.

La sélection de plusieurs bases ne doit pas supprimer leur distinction. Les résultats doivent conserver l'information permettant d'identifier la Knowledge Base et le contexte dans lequel chaque élément a été récupéré.

Une requête en mode DIRECT_LLM peut ne cibler aucune Knowledge Base, conformément au modèle de données validé.

Les stratégies de recherche multi-bases, de fusion et de classement relèvent du document consacré au moteur de recherche.

# 9. Relation avec les index

Une Knowledge Base peut posséder plusieurs Index correspondant à différentes capacités ou stratégies de recherche.

Les Index et leurs générations sont des concepts distincts de la Knowledge Base :

- La Knowledge Base représente l'espace logique des connaissances.
- L'Index représente une structure logique de recherche associée à cet espace.
- L'Index Generation représente un état déterminé de cette structure.
- L'Index Entry représente un élément présent dans une génération donnée.

La présence d'un Knowledge Item dans une Knowledge Base ne signifie pas nécessairement que toutes ses représentations sont déjà disponibles dans tous les index de cette base.

La préparation, l'indexation, l'activation des générations et la disponibilité effective des éléments seront définies dans les spécifications d'ingestion, d'embeddings et de recherche.

# 10. Cycle de vie conceptuel d'une Knowledge Base

Le cycle de vie général d'une Knowledge Base comprend les étapes conceptuelles suivantes :

1. **Création :** une Knowledge Base est créée sous la propriété d'une Organization.
2. **Configuration :** une configuration fonctionnelle lui est associée.
3. **Association des sources :** une ou plusieurs Knowledge Sources peuvent être associées.
4. **Sélection des connaissances :** les Knowledge Items destinés à cet espace sont associés à la base.
5. **Préparation et indexation :** les connaissances sont préparées et rendues exploitables selon les capacités requises.
6. **Disponibilité :** les éléments dont la préparation est terminée peuvent être utilisés conformément aux règles d'accès.
7. **Évolution :** les sources, éléments de connaissance et configurations peuvent évoluer.
8. **Désactivation ou archivage :** l'utilisation de la base peut être suspendue ou limitée sans impliquer immédiatement la suppression de ses ressources.
9. **Suppression :** la base et les associations qui lui sont propres sont supprimées conformément aux politiques applicables.

Cet enchaînement décrit un cycle de vie fonctionnel. Il ne fixe pas une liste définitive d'états techniques ni les mécanismes de transition.

## 10.1 État de la Knowledge Base et disponibilité des connaissances

L'état général d'une Knowledge Base doit être distingué de l'état de préparation de ses éléments et de ses index.

Une base peut être active alors que certains éléments sont encore en cours de préparation. Ces éléments ne doivent pas être considérés comme disponibles pour la recherche tant que les conditions de disponibilité correspondantes ne sont pas satisfaites.

Inversement, désactiver une Knowledge Base ne signifie pas nécessairement que ses documents, ses sources ou ses index doivent être immédiatement supprimés.

Les états précis et leurs règles seront définis dans les spécifications de cycle de vie et d'indexation.

# 11. Suppression et conséquences conceptuelles

La suppression d'une Knowledge Base doit être distinguée de la suppression de ses sources et des Knowledge Items qu'elle utilise.

Les principes suivants s'appliquent :

1. Le retrait d'une Knowledge Base Source Association ne supprime pas automatiquement la Knowledge Source.
2. Le retrait d'une Knowledge Base Item Association ne supprime pas automatiquement le Knowledge Item original.
3. La suppression d'une Knowledge Base ne doit pas supprimer un élément qui reste utilisé ou référencé dans une autre Knowledge Base.
4. Les représentations et index propres à la base supprimée doivent être traités selon les règles de cycle de vie et de conservation.
5. La suppression ne doit pas contourner les obligations de conservation, d'audit ou de protection des données.

Les mécanismes détaillés de suppression, de propagation et de vérification relèvent des spécifications d'ingestion, de sécurité et de gestion du cycle de vie.

# 12. Exigences fonctionnelles couvertes

Cette spécification approfondit principalement les exigences suivantes du cahier des charges :

| Exigence | Besoin | Contribution de la spécification |
|---|---|---|
| FR-001 | Gestion des organisations | Définit la propriété organisationnelle des Knowledge Bases. |
| FR-002 | Gestion des applications clientes | Précise que l'accès d'une application à une base doit être explicite. |
| FR-003 | Utilisateurs et permissions | Précise l'application du contexte d'identité et d'autorisation. |
| FR-004 | Gestion des Knowledge Bases | Définit l'espace logique, sa propriété et son cycle de vie. |
| FR-005 | Configuration des Knowledge Bases | Distingue Knowledge Base Configuration des configurations spécialisées. |
| FR-006 | Isolation des Knowledge Bases | Définit l'indépendance des bases et la séparation de leurs périmètres d'accès. |
| FR-007 | Gestion des sources | Définit Source, Source Connection et Knowledge Base Source Association. |
| FR-010 | Cycle de vie documentaire | Distingue l'association d'un document à une base de sa source d'origine. |
| FR-014 | Recherche vectorielle | Définit la Knowledge Base comme périmètre des index et des connaissances ciblées. |
| FR-015 | Recherche textuelle | Même contribution pour les index textuels. |
| FR-016 | Recherche hybride | Permet à une base de disposer de plusieurs capacités de recherche. |
| FR-017 | Filtrage et classement | Rappelle le périmètre de base et les règles d'accès à respecter. |
| FR-022 | Connexion aux données structurées | Permet d'associer des Structured Resources à une base. |
| FR-023 | Interrogation contrôlée | Rappelle que l'accès aux ressources structurées dépend des autorisations. |
| FR-024 | Combinaison des connaissances | Permet de réunir des connaissances documentaires et structurées dans une même base ou requête autorisée. |
| FR-026 | Gestion des requêtes | Précise la sélection d'une ou plusieurs bases dans le contexte d'une requête. |
| FR-027 | Administration | Définit les principales opérations de gestion d'une Knowledge Base. |

Cette table présente les exigences principalement approfondies ici. Elle ne remplace pas la matrice de traçabilité globale du document 04.

# 13. Frontières avec les autres spécifications

Ce document définit le rôle et le périmètre fonctionnel des Knowledge Bases. Il ne remplace pas les spécifications suivantes :

| Sujet | Document responsable |
|---|---|
| Entités et relations conceptuelles | 04 — Modèle de données |
| Architecture des modules et responsabilités | 03 — Architecture modulaire |
| Connexion, extraction et synchronisation des sources | 06 — Pipeline d'ingestion |
| Découpage et embeddings | 07 — Chunking et embeddings |
| Index, recherche et récupération | 08 — Moteur de recherche |
| Contrats d'accès publics | 10 — API |
| Authentification, autorisation et isolation détaillées | 11 — Sécurité et isolation |
| Sources et interrogation structurées | 12 — Données structurées |
| Déploiement et capacité opérationnelle | 14 — Déploiement et scalabilité |

# 14. Éléments non décidés

Les sujets suivants sont volontairement reportés :

1. Les modalités précises de partage d'une Knowledge Base ou d'un Knowledge Item entre organisations distinctes.
2. Les règles détaillées de propriété et de partage interorganisationnel des Knowledge Sources.
3. Les critères exacts de sélection des éléments d'une source pour une Knowledge Base.
4. Les paramètres exacts de Knowledge Base Configuration.
5. La relation détaillée entre une Knowledge Base Source Association et une ou plusieurs Source Connections.
6. Les états précis de cycle de vie et leurs transitions.
7. Les règles détaillées de disponibilité des connaissances pendant les traitements et réindexations.
8. Les mécanismes de suppression et de conservation des représentations dérivées.
9. Les stratégies de recherche simultanée sur plusieurs Knowledge Bases.
10. Les règles détaillées d'accès aux Knowledge Bases par les applications et les identités.

Ces sujets seront traités dans les spécifications appropriées. Leur report ne doit pas être interprété comme une décision implicite.

# 15. Éléments exclus de cette spécification

Ce document ne définit pas :

- Les tables, colonnes ou contraintes physiques.
- Les technologies de stockage.
- Les endpoints API.
- Les protocoles de connexion aux sources.
- Les formats de configuration définitifs.
- Les stratégies de chunking et de génération d'embeddings.
- Les algorithmes d'indexation, de recherche ou de classement.
- Les mécanismes détaillés d'authentification et d'autorisation.
- Les mécanismes d'exécution asynchrone.
- Les stratégies de déploiement.

Ces éléments appartiennent aux spécifications spécialisées.

# 16. Conditions de validation

Cette spécification pourra être validée lorsque :

1. La définition et le rôle d'une Knowledge Base seront approuvés.
2. Sa relation avec Organization et son périmètre de propriété seront cohérents avec le modèle de données.
3. La distinction entre Knowledge Source et Knowledge Item sera claire.
4. La distinction entre Knowledge Base Source Association et Knowledge Base Item Association sera confirmée.
5. La réutilisation d'une source dans plusieurs Knowledge Bases sera correctement représentée.
6. L'indépendance des configurations et des périmètres d'accès sera préservée.
7. La relation avec les index et les requêtes sera cohérente avec les documents 02 à 04.
8. Le cycle de vie conceptuel et les principes de suppression seront compris.
9. Les exigences fonctionnelles concernées seront couvertes.
10. Les détails relevant des autres spécifications ne seront pas anticipés.

# 17. Conclusion

Une Knowledge Base est un espace logique indépendant de connaissances, possédé par une organisation et exploité par des applications et des identités autorisées.

Elle peut utiliser plusieurs sources et contenir plusieurs éléments de connaissance. Une source peut être réutilisée dans plusieurs bases, et un même élément peut être associé à plusieurs bases, sans confondre l'identité de la source, l'identité de l'élément et chacune de leurs associations.

La Knowledge Base possède son propre contexte fonctionnel, ses configurations et ses règles d'accès. Ses connaissances restent traçables jusqu'à leur origine et leurs représentations dérivées.

**La Knowledge Base est le périmètre logique dans lequel Universal RAG Engine organise, contrôle et expose des connaissances réutilisables, sans confondre leur origine, leur propriété et leurs usages.**
