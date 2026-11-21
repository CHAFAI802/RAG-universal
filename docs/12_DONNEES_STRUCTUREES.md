# UNIVERSAL RAG ENGINE

## Document 12 — Données structurées

**Version :** 1.0
**Statut :** VALIDATED
**Projet :** RAG-universal
**Date :** 2026-11-21

---

# 1. Objectif

Ce document définit le rôle, le périmètre et les principes fonctionnels d'accès, de découverte et d'exploitation des données structurées dans Universal RAG Engine.

Il précise notamment :

- La distinction entre une source structurée et les ressources qu'elle expose.
- La manière dont les ressources structurées sont découvertes, décrites et rendues accessibles dans une Knowledge Base.
- Les principes de compréhension du schéma et de description des données.
- Les conditions d'interrogation contrôlée des ressources.
- La séparation entre interprétation d'une demande, validation d'une requête et exécution sur une source.
- La restitution de résultats structurés, leur provenance et leur fraîcheur.
- La combinaison de résultats structurés avec des connaissances documentaires.
- Les frontières avec les autres modules et spécifications.

Cette spécification reste fonctionnelle et conceptuelle. Elle ne choisit ni technologie de connexion, ni langage de requête, ni moteur de stockage, ni protocole, ni fournisseur.

# 2. Références et dépendances

Cette spécification s'appuie sur les documents suivants :

- `00_VISION_ET_OBJECTIFS.md` — vision, indépendance métier et principes fondateurs.
- `DEPENDENCY_MAP.md` — dépendances entre les spécifications.
- `DECISION_LOG.md` — décisions architecturales et conceptuelles retenues.
- `01_CAHIER_DES_CHARGES.md` — exigences fonctionnelles et non fonctionnelles.
- `02_ARCHITECTURE_GLOBALE.md` — organisation générale du moteur.
- `03_ARCHITECTURE_MODULAIRE.md` — responsabilités des modules.
- `04_MODELE_DE_DONNEES.md` — entités et relations conceptuelles.
- `05_KNOWLEDGE_BASES.md` — gestion des Knowledge Bases et des associations.
- `06_PIPELINE_INGESTION.md` — parcours documentaire et séparation des données structurées.
- `07_CHUNKING_ET_EMBEDDINGS.md` — périmètre du chunking et des embeddings.
- `08_MOTEUR_DE_RECHERCHE.md` — orchestration de la recherche et des résultats.
- `09_GENERATION_ET_LLM.md` — utilisation des résultats dans la génération.
- `10_API_SPECIFICATION.md` — contrats d'intégration avec les applications clientes.
- `11_SECURITE_ET_ISOLATION.md` — identité, autorisation, isolation et protection des données.

Les concepts structurants de référence sont notamment `Knowledge Source`, `Structured Source`, `Source Connection`, `Structured Resource`, `Knowledge Base`, `Knowledge Base Source Association`, `Knowledge Base Item Association`, `Query`, `Retrieval Result`, `Structured Result`, `Generated Answer` et `Citation`.

Ce document approfondit l'exploitation des données structurées sans redéfinir ces entités ni modifier implicitement le modèle de données validé.

# 3. Positionnement des données structurées

## 3.1 Deux grandes familles de connaissances

Universal RAG Engine doit pouvoir exploiter au moins deux grandes familles de connaissances :

1. **Connaissances documentaires**, issues de contenus tels que des fichiers, pages, textes ou documents métiers. Elles suivent le parcours documentaire décrit dans les documents 06 et 07.
2. **Données structurées**, exposées par des sources telles que des bases relationnelles, des API métier, des ressources tabulaires ou des systèmes d'information structurés.

Ces deux familles peuvent contribuer à une même Query et à une même Generated Answer. Elles ne doivent toutefois pas être forcées dans un parcours technique identique.

## 3.2 Une branche d'exploitation distincte

Les données structurées suivent une branche adaptée :

```text
STRUCTURED SOURCE
       |
       v
SOURCE CONNECTION
       |
       v
STRUCTURED RESOURCE
       |
       v
KNOWLEDGE BASE ITEM ASSOCIATION
       |
       v
STRUCTURED ACCESS AND QUERY
       |
       v
STRUCTURED RESULT
       |
       v
RETRIEVAL RESULT
```

Ce parcours est conceptuel. Il ne prescrit pas l'ordre physique des composants ni une technologie d'exécution.

## 3.3 Pas de conversion documentaire automatique

Une Structured Resource n'est pas automatiquement transformée en `Document`, `Extracted Content`, `Chunk`, `Embedding` ou `Original Artifact`.

Une représentation dérivée peut être produite pour un besoin particulier, par exemple pour indexer certains attributs ou permettre une recherche sémantique. Cette représentation reste une projection dérivée de la donnée structurée et doit conserver son lien avec la ressource et les éléments d'origine.

Cette possibilité ne signifie pas que toutes les ressources structurées doivent être découpées ou vectorisées. La recherche structurée doit pouvoir fonctionner sans imposer le chunking ni les embeddings.

# 4. Principes fondamentaux

Les principes suivants gouvernent cette spécification :

1. Une source structurée conserve son identité propre et reste distincte de ses connexions.
2. Une ressource structurée est identifiée et décrite indépendamment de son utilisation dans une Knowledge Base.
3. L'association d'une source à une Knowledge Base ne rend pas automatiquement toutes ses ressources ou toutes ses données accessibles.
4. Seules les ressources explicitement découvertes, sélectionnées, autorisées et rendues disponibles peuvent être interrogées.
5. L'accès aux données se fait par des capacités contrôlées du moteur, jamais par un accès libre accordé à un LLM ou à une application cliente.
6. Une demande exprimée en langage naturel ne constitue pas à elle seule une autorisation d'exécuter une opération sur une source.
7. Toute requête d'accès doit être validée avant son exécution et limitée aux ressources, champs, opérations et volumes autorisés.
8. Les données retournées conservent leur provenance et leur contexte de fraîcheur.
9. Les résultats structurés sont typés et ne sont pas traités comme de simples chaînes de texte.
10. Les données sensibles restent soumises aux règles de sécurité et d'isolation, y compris lorsqu'elles sont utilisées dans un contexte de génération LLM.
11. Les opérations de lecture constituent le périmètre initial. Toute opération modifiant les données d'une source est exclue de cette spécification.
12. Les modalités de connexion et d'exécution restent indépendantes des applications clientes et des technologies sous-jacentes.

# 5. Sources structurées et connexions

## 5.1 Structured Source

`Structured Source` est une spécialisation de `Knowledge Source`. Elle représente une origine identifiable qui fournit des données organisées selon une structure exploitable.

Les catégories de sources peuvent notamment comprendre :

- Bases de données relationnelles.
- API métier exposant des ressources structurées.
- Sources tabulaires.
- Systèmes de gestion ou d'information exposant des objets structurés.
- Services externes fournissant des données structurées.

Cette liste décrit des catégories fonctionnelles et ne constitue pas une liste fermée de technologies prises en charge.

## 5.2 Source Connection

`Source Connection` représente une modalité configurée d'accès à une `Knowledge Source`.

L'identité de la source, la connexion utilisée et les autorisations associées doivent rester distinctes :

- La source identifie l'origine des données.
- La connexion décrit une modalité d'accès à cette origine.
- Les informations d'authentification et secrets nécessaires à la connexion sont gérés par les mécanismes sécurisés prévus à cet effet.
- Les droits d'utilisation de la source et de ses ressources sont évalués séparément.

Une source peut disposer de plusieurs connexions lorsque plusieurs environnements, accès ou contextes sont nécessaires. Le choix de la connexion utilisable dépend de la configuration et des autorisations applicables.

## 5.3 Principe du moindre privilège

Une connexion utilisée par le moteur doit disposer uniquement des droits nécessaires aux opérations explicitement permises.

Le fait qu'une connexion puisse techniquement accéder à une base ou à un service ne signifie pas que toutes les ressources de cette source peuvent être exposées au moteur.

L'administration de la connexion doit donc être distincte de la sélection des ressources accessibles dans Universal RAG Engine.

# 6. Découverte et sélection des ressources

## 6.1 Structured Resource

`Structured Resource` est une spécialisation de `Knowledge Item`. Elle représente une ressource identifiable exposée par une `Structured Source`, par exemple une table, une vue, une collection ou une ressource d'API.

Une `Structured Source` peut exposer plusieurs `Structured Resources`. Chaque ressource conserve sa relation avec sa source d'origine.

## 6.2 Découverte des ressources

Le moteur doit pouvoir découvrir les ressources structurées que la connexion et les droits techniques permettent d'identifier.

La découverte peut fournir, selon les capacités de la source :

- Les ressources disponibles.
- Leur nom logique et leur description lorsqu'ils existent.
- Les champs ou attributs exposés.
- Les types de données déclarés ou observés.
- Les identifiants et clés permettant de localiser les éléments.
- Les relations explicitement connues entre ressources.
- Les informations utiles à la compréhension métier des champs.

La découverte est une opération de connaissance du catalogue de la source. Elle ne rend pas automatiquement les ressources accessibles aux utilisateurs ou aux applications clientes.

## 6.3 Sélection explicite

La découverte, l'autorisation d'utilisation et la mise à disposition dans une Knowledge Base sont trois notions distinctes.

Une ressource ne peut être exploitée dans une Knowledge Base que si les conditions nécessaires sont réunies :

1. La source est identifiée et une connexion utilisable est configurée.
2. La ressource a été découverte ou déclarée de manière contrôlée.
3. La ressource est sélectionnée pour l'utilisation prévue.
4. Une `Knowledge Base Item Association` la rend disponible dans la Knowledge Base concernée.
5. Les autorisations requises permettent l'opération demandée.

La présence d'une `Knowledge Base Source Association` indique que la Knowledge Base peut utiliser cette origine. Elle ne remplace pas l'association de chaque `Structured Resource` retenue.

## 6.4 Séparation des périmètres

Une même Structured Resource peut être associée à plusieurs Knowledge Bases, sous réserve des règles de propriété, de partage et d'autorisation.

Chaque association conserve son propre contexte d'utilisation. La présence d'une ressource dans une Knowledge Base ne doit pas la rendre automatiquement accessible dans une autre.

Le retrait d'une association d'une Knowledge Base ne signifie pas la suppression de la ressource dans sa source d'origine ni le retrait de ses autres associations.

# 7. Description et compréhension du schéma

## 7.1 Rôle de la description

Pour interroger correctement une ressource structurée, le moteur doit disposer d'une description suffisamment précise de sa structure et de sa signification.

Cette description permet notamment de distinguer les noms techniques des significations fonctionnelles, les champs filtrables des champs simplement restituables et les relations valides des rapprochements supposés.

## 7.2 Informations descriptives utiles

La description d'une Structured Resource peut inclure, selon les informations disponibles :

- Son identifiant logique, son nom et sa description.
- Les noms des champs ou attributs exposés.
- Le type de données de chaque champ.
- Le caractère obligatoire, facultatif ou nullable d'une valeur lorsqu'il est connu.
- Les identifiants stables permettant de retrouver un élément.
- Les relations déclarées vers d'autres ressources.
- Les libellés et descriptions métier des champs.
- Les unités, devises, fuseaux horaires ou conventions pertinentes.
- Les champs sensibles ou soumis à restriction.
- Les opérations autorisées sur la ressource et sur ses champs.
- Les capacités de filtrage, de tri, de regroupement ou d'agrégation autorisées.

Ces informations décrivent le schéma et les capacités d'une ressource. Leur présence ne crée pas automatiquement de nouvelles entités centrales dans le modèle de données.

## 7.3 Description technique et interprétation métier

La description technique d'un champ ne suffit pas toujours à déterminer sa signification.

Par exemple, un champ nommé `status`, `date`, `amount` ou `code` peut avoir une signification différente selon la ressource et le contexte métier.

Le moteur doit éviter d'inventer la signification des champs à partir de leur seul nom. Lorsque la description disponible est insuffisante ou ambiguë, il doit limiter l'interprétation, demander une précision ou signaler qu'une requête fiable ne peut pas être construite.

## 7.4 Types et sémantique des valeurs

Les valeurs doivent conserver leur nature et leur sémantique. Le moteur ne doit pas convertir arbitrairement toutes les données en texte.

Les catégories de valeurs à prendre en compte comprennent notamment :

- Texte et identifiants.
- Nombres entiers et décimaux.
- Valeurs booléennes.
- Dates, heures et horodatages.
- Valeurs monétaires et unités de mesure.
- Valeurs nulles ou absentes.
- Collections et structures imbriquées lorsqu'elles sont exposées par la source.

Les règles de comparaison et de restitution doivent respecter les types, les précisions et les conventions de la source. Les conversions nécessaires doivent être explicites et cohérentes.

## 7.5 Évolution du schéma

Le schéma d'une source peut évoluer indépendamment du moteur.

Le moteur doit pouvoir identifier qu'une description connue n'est plus à jour ou qu'une ressource a changé. Une requête ne doit pas continuer à utiliser silencieusement une interprétation devenue invalide.

Lorsqu'un changement empêche de garantir la validité d'une requête, la capacité concernée doit être suspendue ou limitée jusqu'à ce que la description soit actualisée et vérifiée.

Les mécanismes de versionnement détaillé des descriptions, de détection des changements et de validation relèvent des spécifications techniques ultérieures. Ils ne sont pas fixés ici.

# 8. Modes d'accès aux données

## 8.1 Accès direct contrôlé

Dans ce mode, la demande validée est exécutée sur la source au moment de la requête, au moyen d'une connexion autorisée.

Ce mode permet de consulter les données présentes dans la source au moment de l'exécution, sous réserve de la disponibilité de celle-ci et des garanties qu'elle fournit.

Une consultation directe ne doit toutefois pas être qualifiée de temps réel sans garantie explicite de la source et du chemin d'accès.

## 8.2 Représentation synchronisée ou matérialisée

Une ressource peut faire l'objet d'une copie ou d'une représentation synchronisée afin de limiter les accès répétés à la source ou de répondre à des besoins de disponibilité et de performance.

Cette représentation reste dérivée de la source d'origine. Le moteur doit pouvoir distinguer la date de synchronisation, l'état de la copie et la fraîcheur des données retournées.

La synchronisation ne doit pas être présentée comme instantanée si un délai de propagation existe.

## 8.3 Représentation préparée pour la recherche

Une sélection de données ou d'attributs structurés peut être convertie en une représentation adaptée à une capacité de recherche particulière, notamment une indexation textuelle ou sémantique.

Cette représentation est dérivée et ne remplace pas la source d'origine. Elle doit conserver une provenance permettant de retrouver la ressource et l'élément d'origine.

Elle n'impose pas que le système transforme toutes les données structurées en documents ou en chunks.

## 8.4 Absence de choix technologique prématuré

Les trois modes précédents décrivent des possibilités fonctionnelles qui peuvent être utilisées selon les besoins et les contraintes d'une ressource.

Cette spécification ne décide pas :

- Qu'un mode unique doit être imposé à toutes les sources.
- Que toutes les sources doivent être copiées dans le moteur.
- Que toutes les requêtes doivent être exécutées directement sur leur système d'origine.
- Qu'une ressource doit obligatoirement être indexée ou vectorisée.
- Qu'un fournisseur ou un moteur de stockage particulier doit être utilisé.

Le choix du mode applicable doit tenir compte de la fraîcheur attendue, du volume, des performances, des autorisations, des contraintes de la source et des politiques de conservation.

# 9. Interrogation contrôlée

## 9.1 Principe général

L'interrogation des ressources structurées doit être effectuée par une capacité dédiée du moteur, à partir d'une demande et d'un contexte autorisés.

L'application cliente transmet une Query au moteur. Le sous-système structuré identifie les ressources pertinentes, prépare une représentation contrôlée de la demande, la valide puis l'exécute au moyen d'une connexion autorisée.

Aucun accès direct et général au système sous-jacent ne doit être exposé à l'application cliente ou au modèle LLM.

## 9.2 Interprétation de la demande

La demande peut être fournie en langage naturel ou sous une forme structurée par une application cliente.

Lorsque le langage naturel est utilisé, un modèle LLM ou un autre mécanisme d'interprétation peut contribuer à identifier :

- L'objectif de recherche.
- Les ressources susceptibles de répondre à la demande.
- Les champs nécessaires.
- Les filtres et critères de comparaison.
- Les regroupements ou agrégations éventuels.
- Le tri et le volume de résultats souhaités.

Cette interprétation produit une proposition de requête. Elle ne constitue ni une validation de sécurité ni une autorisation d'accès.

## 9.3 Plan de requête contrôlé

Avant toute exécution, la demande interprétée doit être représentée sous une forme contrôlable par le moteur.

Cette représentation doit rendre identifiables les ressources ciblées, les champs utilisés, les opérations demandées, les relations nécessaires, les paramètres, les limites et le contexte d'autorisation.

Le moteur doit pouvoir vérifier cette représentation indépendamment du modèle qui l'a proposée.

Le plan de requête ne doit pas être assimilé à une instruction libre fournie par le LLM.

## 9.4 Validation avant exécution

Le moteur doit vérifier au minimum :

1. Que l'acteur et l'application disposent d'un contexte d'identité valide.
2. Que la Knowledge Base ciblée est accessible.
3. Que la Structured Resource est associée à cette Knowledge Base et autorisée pour cet usage.
4. Que la connexion utilisée est autorisée et disponible.
5. Que chaque champ demandé est connu et accessible.
6. Que les opérations et relations utilisées sont permises.
7. Que les filtres, paramètres, tris, regroupements et limites respectent les règles définies.
8. Que la requête ne tente pas de contourner les restrictions d'accès ou d'exposer des données non autorisées.
9. Que les limites d'exécution et de restitution sont respectées.
10. Que la description du schéma utilisée est suffisamment actuelle pour garantir une interprétation correcte.

Une requête invalide ou non autorisée ne doit pas être exécutée.

## 9.5 Opérations de lecture

Le périmètre initial couvre les opérations de consultation nécessaires à la récupération de connaissances, telles que :

- Sélection d'éléments ou de champs autorisés.
- Filtrage par critères autorisés.
- Comparaison de valeurs typées.
- Tri et pagination.
- Regroupement et agrégation lorsque la ressource et les droits le permettent.
- Relations ou rapprochements déclarés et autorisés.

Ces capacités ne signifient pas que chaque ressource doit prendre en charge toutes les opérations.

## 9.6 Relations et rapprochements

Les rapprochements entre ressources doivent s'appuyer sur des relations connues, déclarées et autorisées.

Le moteur ne doit pas inventer une relation entre deux champs simplement parce que leurs noms ou leurs valeurs semblent proches.

Les opérations multi-ressources doivent rester dans le périmètre explicitement permis par les sources, les descriptions disponibles et les autorisations.

Les rapprochements entre plusieurs sources indépendantes ne constituent pas une capacité universelle garantie par cette version ; ils nécessitent une définition et des garanties spécifiques.

## 9.7 Aucune écriture implicite

La génération d'une requête de lecture ne doit jamais être convertie en opération d'écriture.

La création, la modification ou la suppression de données dans les systèmes sources ne fait pas partie du périmètre de ce document. Une éventuelle capacité d'action devra faire l'objet d'une spécification distincte, d'autorisations spécifiques et d'une validation explicite.

# 10. Sécurité et isolation pendant l'interrogation

## 10.1 Autorisation à plusieurs niveaux

L'accès aux données structurées doit respecter les contrôles applicables à plusieurs niveaux :

- Organisation propriétaire de la source et de la Knowledge Base.
- Application cliente et identité à l'origine de la Query.
- Knowledge Base ciblée.
- Source et connexion utilisées.
- Structured Resource concernée.
- Champs ou catégories de données accessibles.
- Opération demandée.
- Éléments ou lignes pouvant être restitués lorsque la source ou la politique permet un contrôle à ce niveau.

L'accès à la source ne remplace pas l'autorisation appliquée par Universal RAG Engine. De même, l'autorisation d'utiliser une Knowledge Base ne confère pas automatiquement un accès à toutes les ressources et à tous les champs qui lui sont techniquement associés.

## 10.2 Filtrage des données

Les contrôles d'accès doivent être appliqués avant la restitution des résultats et, lorsque cela est possible, au plus près de l'exécution sur la source.

Les restrictions de lignes et de champs doivent être conservées dans toute représentation synchronisée, matérialisée ou indexée. Une copie locale ne doit pas devenir un moyen de contourner les règles appliquées à la source.

## 10.3 Prévention des injections et des requêtes détournées

Les contenus de la source, les descriptions de champs et les demandes en langage naturel doivent être considérés comme des données non fiables.

Le moteur doit séparer les instructions de contrôle des valeurs fournies par l'utilisateur ou produites par un modèle. Les valeurs doivent être transmises comme paramètres typés ; les noms de ressources, de champs et les opérations doivent provenir de définitions autorisées et validées.

Un LLM ne doit jamais recevoir la responsabilité d'exécuter directement une instruction libre sur une source. La validation du plan et les contrôles d'autorisation restent déterministes et indépendants de la génération du modèle.

## 10.4 Protection des données sensibles

Les champs sensibles ou confidentiels doivent être identifiés et soumis à des règles adaptées.

Le moteur doit limiter les données transmises au modèle LLM au strict nécessaire pour la réponse demandée. Une donnée qui ne peut pas être consultée par l'acteur ne doit pas être incluse dans le contexte de génération, même si elle est techniquement accessible à une connexion interne.

## 10.5 Secrets et connexions

Les secrets de connexion ne doivent pas apparaître dans les Query, plans de requête, résultats, citations, messages d'erreur ou journaux accessibles aux utilisateurs.

La gestion, la rotation, le stockage et la révocation des secrets relèvent des mécanismes de sécurité et de configuration prévus par les documents 10 et 11 et par les spécifications techniques ultérieures.

## 10.6 Refus par défaut

Lorsqu'une autorisation, une relation, une description de schéma ou une restriction nécessaire ne peut pas être vérifiée, le moteur doit refuser ou limiter l'opération concernée.

Il ne doit pas considérer l'absence d'une règle comme une autorisation implicite.

# 11. Exécution, limites et maîtrise des résultats

## 11.1 Exécution contrôlée

Une requête validée est exécutée uniquement par le mécanisme adapté à la source et à la connexion autorisée.

Le moteur doit conserver le lien entre la Query initiale, le plan validé, la source et la ressource interrogées, ainsi que le résultat obtenu.

La traduction vers le langage ou le protocole spécifique à la source relève de l'adaptateur correspondant. Elle ne doit pas être exposée comme une dépendance du contrat fonctionnel universel.

## 11.2 Limites d'exécution et de restitution

Les requêtes doivent être soumises à des limites configurables portant notamment sur :

- Le temps d'exécution.
- Le nombre d'éléments retournés.
- La taille totale des données restituées.
- Le nombre de ressources consultées.
- La complexité des opérations autorisées.
- Les volumes transférés depuis une source externe.

Les valeurs numériques et mécanismes d'application seront définis dans les spécifications techniques et de déploiement.

## 11.3 Pagination et cohérence

Lorsque les résultats sont paginés, le moteur doit préserver une navigation cohérente et éviter de présenter une pagination instable comme un ensemble complet et déterministe.

Les garanties dépendent des capacités de la source et du mode d'accès. Les limites éventuelles doivent être identifiables.

## 11.4 Résultat partiel

Si une requête multi-ressources ou multi-sources ne peut être exécutée que partiellement, le moteur doit distinguer les résultats disponibles des parties en échec.

Un résultat partiel ne doit pas être présenté comme complet. Les sources indisponibles et les limites rencontrées doivent être signalées sans divulguer d'informations protégées.

# 12. Résultats structurés et provenance

## 12.1 Structured Result

Un `Structured Result` représente les données obtenues par l'interrogation d'une Structured Resource.

Il constitue une forme spécialisée de `Retrieval Result` et ne nécessite pas automatiquement une entité indépendante supplémentaire dans le modèle de données.

Le résultat doit conserver les informations permettant de comprendre ce qui a été consulté, dans quel contexte et à partir de quelle ressource.

## 12.2 Informations de provenance

Selon le mode d'accès et les capacités de la source, la provenance d'un résultat structuré doit permettre d'identifier :

- La Structured Source d'origine.
- La Structured Resource consultée.
- La Knowledge Base dans le contexte de laquelle le résultat a été obtenu.
- La Query à l'origine de la récupération.
- L'identifiant stable de l'élément concerné lorsqu'il existe et peut être exposé.
- Les champs ou informations effectivement restitués.
- Le moment de consultation ou d'exécution.
- La date de synchronisation ou la référence de la représentation utilisée, le cas échéant.
- Les éventuelles transformations fonctionnelles appliquées au résultat.

Ces informations doivent être conservées à un niveau suffisant pour permettre la vérification, la traçabilité et la citation, sans imposer l'exposition de données techniques sensibles.

## 12.3 Fraîcheur des résultats

Le moteur doit distinguer :

- Une donnée consultée directement sur la source.
- Une donnée issue d'une représentation synchronisée.
- Une donnée issue d'une représentation préparée ou indexée.

Lorsqu'une date de consultation, de synchronisation ou une information de fraîcheur est disponible, elle doit être préservée.

Le moteur ne doit pas affirmer qu'une valeur est actuelle ou à jour si cette garantie ne peut pas être démontrée.

## 12.4 Types et valeurs

Les résultats doivent préserver autant que possible les types, la précision et le sens des valeurs de la source.

Les valeurs nulles, absentes, inconnues ou non applicables ne doivent pas être transformées silencieusement en valeurs par défaut susceptibles de modifier le sens du résultat.

Les unités, devises, fuseaux horaires et conventions doivent être conservés ou explicités lorsqu'ils influencent l'interprétation.

## 12.5 Minimisation

Le moteur ne doit restituer que les données nécessaires à l'objectif de la Query et autorisées dans son contexte.

La capacité d'accéder à une ressource contenant de nombreux champs ne justifie pas de retourner l'ensemble de ces champs lorsque seuls quelques éléments sont requis.

# 13. Intégration au moteur de recherche et à la génération

## 13.1 Rôle du sous-système structuré

Le sous-système structuré assure la découverte, la description, la validation, l'accès contrôlé et la normalisation des résultats issus des Structured Resources.

Il ne remplace pas le Retrieval Engine défini dans le document 08. Il lui fournit des résultats structurés pouvant être intégrés au traitement d'une Query.

## 13.2 Combinaison avec les connaissances documentaires

Une même Query peut nécessiter :

- Des résultats documentaires issus de la recherche dans les Chunks.
- Des résultats structurés issus de l'interrogation de Structured Resources.
- Une combinaison des deux catégories lorsque la demande, les autorisations et les capacités disponibles le permettent.

Les deux catégories doivent rester identifiables dans les résultats. Leur combinaison ne doit pas effacer leur provenance, leur nature ou leurs différences de fraîcheur.

Le Retrieval Engine demeure responsable de la coordination globale des résultats, de leur fusion éventuelle et de leur restitution selon les règles du document 08.

## 13.3 Modes de traitement des Query

L'exploitation structurée doit rester cohérente avec les trois modes définis dans le modèle de données et les spécifications de recherche et de génération :

| Mode | Accès aux données structurées | Génération LLM |
|---|---|---|
| `RETRIEVAL_ONLY` | Possible si la Query le demande et si l'accès est autorisé | Non |
| `DIRECT_LLM` | Aucun Retrieval structuré pour cette Query | Oui |
| `RETRIEVAL_AUGMENTED` | Possible avant la génération, selon le besoin et les autorisations | Oui |

Une génération `DIRECT_LLM` ne doit pas être présentée comme fondée sur une consultation structurée qui n'a pas eu lieu.

## 13.4 Utilisation dans le contexte LLM

Lorsqu'un résultat structuré est transmis à un LLM, seules les données nécessaires et autorisées doivent être incluses.

Les résultats sont des éléments de contexte et non des instructions à suivre par le modèle. Leur contenu doit être traité comme une donnée externe non fiable.

Le modèle ne doit pas obtenir de connexion directe à la source ni de capacité d'élargir lui-même le périmètre de consultation.

## 13.5 Citations

Une réponse générée à partir de données structurées doit pouvoir référencer les informations qui ont effectivement contribué à cette réponse.

Une citation structurée doit permettre, selon les capacités disponibles, de retrouver la source, la Structured Resource et l'élément ou l'ensemble de données concerné. Elle peut également indiquer le moment de consultation ou la référence de synchronisation pertinente.

Une citation ne doit pas être créée simplement parce qu'une ressource a été consultée. Elle doit correspondre à une information réellement utilisée dans la réponse.

# 14. Cycle de vie des ressources structurées

## 14.1 Évolution et actualisation

Une ressource structurée peut évoluer dans sa source : ajout ou retrait de champs, changement de type, modification des relations, changement de disponibilité ou de signification.

Le moteur doit pouvoir identifier les changements qui affectent sa description ou les requêtes autorisées.

## 14.2 Désactivation et indisponibilité

Une ressource ou une connexion peut devenir indisponible, être désactivée ou perdre les autorisations nécessaires.

Dans ces situations, le moteur ne doit pas utiliser une connexion ou une description invalide comme si la ressource était toujours accessible.

Une représentation synchronisée ou indexée peut rester présente techniquement, mais son utilisation doit respecter la politique de fraîcheur, de révocation et de suppression applicable.

## 14.3 Suppression et retrait d'association

Le retrait d'une Structured Resource d'une Knowledge Base doit rendre cette ressource indisponible dans le périmètre concerné conformément aux règles de propagation définies.

Ce retrait ne doit pas supprimer automatiquement la source d'origine ni les associations de cette ressource avec d'autres Knowledge Bases.

Les copies, caches, représentations indexées et résultats persistés doivent être traités conformément aux règles de sécurité, de conservation et de suppression applicables.

## 14.4 Révocation des accès

Une révocation d'autorisation ou de connexion doit empêcher les nouvelles opérations qui ne sont plus permises.

Les données déjà récupérées, mises en cache ou transmises à un modèle doivent être prises en compte selon les politiques de sécurité et de conservation. Aucun mécanisme de cache ne doit permettre de contourner une révocation.

# 15. Gestion des erreurs et résilience

Les erreurs peuvent notamment provenir :

- D'une connexion indisponible ou refusée.
- D'une source temporairement inaccessible.
- D'une ressource supprimée ou renommée.
- D'une description de schéma obsolète.
- D'un champ ou d'une relation inconnus.
- D'une requête invalide ou non autorisée.
- D'une limite d'exécution atteinte.
- D'un résultat incomplet ou impossible à interpréter de manière fiable.

Le moteur doit distinguer les erreurs de validation, les refus d'autorisation, les erreurs de source et les résultats partiels.

Une erreur ne doit pas provoquer un élargissement implicite des droits ou un accès de remplacement moins sécurisé.

Les reprises doivent respecter les limites d'exécution et ne pas produire de doublons ou de résultats contradictoires présentés comme équivalents.

Les erreurs restituées aux applications clientes doivent éviter de révéler des détails techniques ou des informations protégées sur les sources.

# 16. Traçabilité et audit

Les opérations d'administration, de découverte, de connexion, de sélection et d'interrogation doivent pouvoir être tracées selon les règles d'audit applicables.

La traçabilité doit permettre, selon le niveau de détail requis :

- D'identifier l'acteur ou l'application à l'origine de l'opération.
- D'identifier la Knowledge Base, la source et la ressource concernées.
- De connaître la nature de l'opération et son résultat.
- De distinguer une exécution complète d'une exécution partielle ou en échec.
- De retrouver les informations de provenance nécessaires à une vérification.

Les journaux ne doivent pas enregistrer inutilement les secrets de connexion, les valeurs sensibles complètes, ni le contenu confidentiel des résultats. Les exigences de minimisation et de conservation restent applicables.

# 17. Frontières avec les autres spécifications

| Sujet | Document responsable | Frontière de responsabilité |
|---|---|---|
| Vision et indépendance applicative | 00 — Vision et objectifs | Principes fondateurs et périmètre universel |
| Exigences fonctionnelles et non fonctionnelles | 01 — Cahier des charges | Besoins auxquels cette spécification contribue |
| Architecture générale | 02 — Architecture globale | Positionnement du sous-système structuré |
| Responsabilités modulaires | 03 — Architecture modulaire | Répartition des responsabilités entre modules |
| Entités et relations | 04 — Modèle de données | Structured Source, Structured Resource, Structured Result et relations |
| Knowledge Bases et associations | 05 — Knowledge Bases | Association des sources et des éléments aux bases |
| Connexions et parcours documentaires | 06 — Pipeline ingestion | Connectivité générale des sources ; l'ingestion documentaire reste distincte |
| Chunking et embeddings | 07 — Chunking et embeddings | Représentations documentaires ; éventuelles projections structurées spécialisées |
| Recherche et fusion des résultats | 08 — Moteur de recherche | Coordination du Retrieval et des résultats documentaires et structurés |
| Génération et LLM | 09 — Génération et LLM | Utilisation contrôlée du contexte et production de réponses |
| Contrats d'intégration externes | 10 — API | Exposition des capacités autorisées aux applications clientes |
| Authentification, autorisation et isolation | 11 — Sécurité et isolation | Règles de contrôle d'accès, de protection et de gestion des secrets |
| Tests et évaluation | 13 — Tests et évaluation | Vérification de la qualité, de la sécurité et de la fiabilité des résultats |
| Déploiement et scalabilité | 14 — Déploiement et scalabilité | Capacité, disponibilité et exécution opérationnelle |

# 18. Correspondance avec les exigences fonctionnelles

Cette spécification approfondit principalement les exigences FR-022 à FR-024. Elle contribue également à plusieurs exigences transversales.

| Exigence | Besoin | Contribution de cette spécification |
|---|---|---|
| FR-007 | Gestion des sources | Distingue la source, la connexion, la découverte et les ressources structurées disponibles. |
| FR-017 | Filtrage et classement | Définit les limites de sélection, les champs, les filtres et les résultats structurés autorisés ; le classement global reste dans le document 08. |
| FR-018 | Génération augmentée | Définit les conditions d'utilisation des résultats structurés dans le contexte transmis au LLM. |
| FR-020 | Références documentaires et sources | Précise la provenance et la citation d'un élément structuré ayant contribué à une réponse. |
| FR-021 | Gestion des connaissances insuffisantes | Empêche de présenter comme fiable une requête structurée invalide, incomplète ou insuffisamment documentée. |
| FR-022 | Connexion aux données structurées | Définit la découverte, la description, la sélection et les modes d'accès aux Structured Resources. |
| FR-023 | Interrogation contrôlée | Définit la validation préalable, les opérations permises, les limites et les contrôles appliqués aux requêtes structurées. |
| FR-024 | Combinaison des connaissances | Définit l'intégration des résultats structurés et documentaires dans une même Query autorisée. |
| FR-026 | Gestion des requêtes | Précise le traitement des Query qui nécessitent une interrogation structurée. |
| FR-028 | Journalisation et supervision | Définit les informations de traçabilité attendues pour les opérations structurées. |

Cette matrice présente la contribution spécifique du document 12. Elle ne remplace pas la matrice globale de traçabilité du cahier des charges et du modèle de données.

# 19. Contribution aux exigences non fonctionnelles

Les exigences non fonctionnelles sont satisfaites par des règles, des contrôles et des propriétés d'architecture ; elles ne nécessitent pas toutes une entité supplémentaire.

| Exigence | Besoin | Contribution de cette spécification | Spécification complémentaire |
|---|---|---|---|
| NFR-001 | Isolation des organisations | Séparation des sources, ressources, Knowledge Bases et contextes d'utilisation | 11 — Sécurité et isolation |
| NFR-002 | Contrôle des accès | Validation de l'identité, des ressources, des champs et des opérations | 11 — Sécurité et isolation |
| NFR-003 | Protection des données sensibles | Minimisation des champs et contrôle de la transmission au LLM | 11 — Sécurité et isolation |
| NFR-004 | Protection contre les injections | Séparation entre instructions, paramètres et données non fiables ; validation du plan | 11 — Sécurité et isolation ; 09 — Génération et LLM |
| NFR-005 | Gestion des secrets | Séparation entre source, connexion et secrets | 11 — Sécurité et isolation |
| NFR-006 | Intégrité des connaissances | Préservation de la provenance, des types et de la relation à la source | 04 — Modèle de données |
| NFR-007 | Résilience | Gestion des indisponibilités, échecs partiels et reprises contrôlées | 14 — Déploiement et scalabilité |
| NFR-008 | Traçabilité | Provenance des résultats et suivi des opérations | 11 — Sécurité et isolation |
| NFR-009 | Cohérence après modification | Prise en compte des évolutions de schéma, retraits et révocations | 11 — Sécurité et isolation ; 14 — Déploiement et scalabilité |
| NFR-010 | Performance | Limites de requête, de restitution et choix de mode d'accès | 14 — Déploiement et scalabilité |
| NFR-011 | Évolutivité | Séparation des sources, connexions, ressources et adaptateurs | 03 — Architecture modulaire ; 14 — Déploiement et scalabilité |
| NFR-012 | Traitements volumineux | Maîtrise des volumes, limites et possibilité de suivi des opérations longues | 14 — Déploiement et scalabilité |
| NFR-014 | Extensibilité | Modèle indépendant des types de sources et contrats d'adaptation | 03 — Architecture modulaire |
| NFR-016 | Interopérabilité | Description commune des ressources et séparation des formats propres aux sources | 10 — API |
| NFR-018 | Observabilité | Informations de suivi et d'audit des opérations structurées | 14 — Déploiement et scalabilité |
| NFR-020 | Vérifiabilité | Provenance, contexte d'exécution, fraîcheur et résultats identifiables | 13 — Tests et évaluation |

Cette contribution est spécifique aux données structurées. Elle ne remplace pas la couverture globale des exigences non fonctionnelles.

# 20. Éléments explicitement non décidés

Les sujets suivants sont volontairement reportés et ne doivent pas être interprétés comme des décisions implicites :

1. Les protocoles, pilotes, bibliothèques et technologies de connexion.
2. Les fournisseurs de bases de données, de services ou de connecteurs à prendre en charge dans une version donnée.
3. Le langage interne exact de représentation des requêtes et sa traduction vers chaque source.
4. Les structures physiques du catalogue et des descriptions de schéma.
5. Le mécanisme détaillé de détection et de versionnement des changements de schéma.
6. Le choix d'un accès direct, d'une synchronisation, d'une matérialisation ou d'une combinaison pour chaque source.
7. Les mécanismes de cache, les stratégies de cohérence et les durées de conservation.
8. Les seuils chiffrés de temps, de volume, de pagination et de concurrence.
9. Les algorithmes de découverte, d'interprétation, de planification et d'optimisation des requêtes.
10. Les mécanismes détaillés de gestion des politiques au niveau des lignes et des champs.
11. Les stratégies de rapprochement entre ressources de sources différentes.
12. Les modalités précises de création de représentations textuelles ou vectorielles dérivées de données structurées.
13. Les contrats API détaillés et les formats de réponse publics.
14. Les modalités de chiffrement, de rotation des secrets et de gestion des connexions.
15. Les mécanismes détaillés d'exécution asynchrone, de reprise et de supervision.

Ces sujets devront être traités dans les spécifications spécialisées, les décisions d'architecture ou les ADR appropriés avant leur implémentation.

# 21. Conditions de validation

Le document pourra être validé lorsque :

1. La distinction entre sources structurées, connexions et ressources structurées sera claire.
2. La distinction entre découverte d'une ressource, association à une Knowledge Base et autorisation d'utilisation sera respectée.
3. La séparation entre le parcours documentaire et le parcours des données structurées sera explicite.
4. Le rôle de la description du schéma et des informations métier sera compréhensible.
5. Les modes d'accès direct, synchronisé et préparé pour la recherche seront distingués sans imposer prématurément une technologie.
6. Le principe d'une requête contrôlée et validée avant exécution sera approuvé.
7. La séparation entre interprétation par un LLM et décision d'autorisation sera sans ambiguïté.
8. Les limites sur les opérations de lecture et l'exclusion des écritures implicites seront approuvées.
9. Les principes de sécurité, d'isolation, de minimisation et de gestion des secrets seront cohérents avec le document 11.
10. Les résultats structurés conserveront leur typage, leur provenance et leur fraîcheur.
11. La combinaison avec les connaissances documentaires restera cohérente avec le document 08.
12. L'utilisation des résultats structurés dans les réponses et citations restera cohérente avec les documents 04 et 09.
13. Les exigences fonctionnelles et non fonctionnelles concernées auront une couverture identifiée.
14. Les sujets non décidés seront explicitement reportés.
15. Les détails techniques prématurés seront évités.
16. La cohérence avec les documents 00 à 11 sera vérifiée.

# 22. Conclusion

Les données structurées constituent une famille de connaissances de première classe dans Universal RAG Engine. Elles permettent au moteur d'exploiter des informations provenant de bases, d'API et d'autres systèmes structurés sans les assimiler artificiellement à des documents.

Leur exploitation repose sur la distinction entre la source, la connexion, la ressource exposée, son association à une Knowledge Base, l'autorisation d'accès et la requête effectivement exécutée.

Les demandes doivent être interprétées puis validées avant toute exécution. Les résultats doivent préserver les types, la provenance et les informations de fraîcheur nécessaires à leur vérification. Leur utilisation par un LLM reste limitée au contexte autorisé et aux données nécessaires.

**Universal RAG Engine doit pouvoir interroger des données structurées de manière contrôlée, traçable et indépendante des technologies sources, puis combiner ces résultats avec les connaissances documentaires sans confondre leurs modèles ni leurs cycles de vie.**
