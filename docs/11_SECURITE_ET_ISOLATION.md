# UNIVERSAL RAG ENGINE

## Document 11 — Sécurité et isolation

**Version :** 1.0
**Statut :** VALIDATED
**Projet :** RAG-universal

---

# 1. Objectif

Ce document définit les exigences et principes de sécurité et d'isolation applicables à Universal RAG Engine.

Il précise les acteurs, les périmètres de confiance, les règles générales d'accès, la protection des connaissances et les responsabilités de sécurité dans les différents parcours du moteur.

Il constitue la référence de sécurité pour les futures spécifications détaillées et pour la conception des mécanismes techniques.

Ce document reste au niveau fonctionnel et architectural. Il ne choisit pas de protocole d'authentification, d'algorithme cryptographique, de produit de gestion des secrets, de technologie de stockage ou de mécanisme réseau particulier.

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
- `08_MOTEUR_DE_RECHERCHE.md`
- `09_GENERATION_ET_LLM.md`
- `10_API_SPECIFICATION.md`

# 3. Périmètre de sécurité

La sécurité couvre l'ensemble du cycle de vie et des interactions du moteur :

- organisations, applications et identités ;
- Knowledge Bases, sources et associations ;
- documents, versions et contenus dérivés ;
- fragments, embeddings et index ;
- données structurées et ressources exposées ;
- requêtes, résultats, contextes, réponses et citations ;
- fournisseurs externes et configurations ;
- opérations administratives, traitements et événements d'audit ;
- interfaces publiques et communications entre composants.

La sécurité n'est pas une fonction isolée. Elle doit être prise en compte à chaque frontière où une identité, une donnée, une ressource ou un traitement change de périmètre de confiance.

# 4. Principes fondamentaux

## 4.1 Refus par défaut

Toute opération protégée doit être refusée tant qu'une autorisation applicable n'a pas été établie.

## 4.2 Moindre privilège

Une identité ou une application ne reçoit que les droits nécessaires à ses usages autorisés.

## 4.3 Séparation entre identité, propriété et accès

L'identité d'un acteur, la propriété organisationnelle d'une ressource et l'autorisation d'y accéder sont trois notions distinctes.

## 4.4 Isolation par périmètre

Les données et opérations doivent respecter les périmètres organisationnels, applicatifs et de Knowledge Base applicables.

## 4.5 Sécurité de bout en bout

Les contrôles doivent rester applicables pendant l'ingestion, l'indexation, la recherche, l'accès structuré, la génération, l'administration et la suppression.

## 4.6 Défense en profondeur

La sécurité ne doit pas dépendre d'un contrôle unique. Les différentes frontières doivent appliquer les vérifications qui relèvent de leur responsabilité.

## 4.7 Données externes non fiables

Les documents, contenus extraits, résultats externes et réponses de fournisseurs doivent être considérés comme des données non fiables jusqu'à leur traitement approprié.

## 4.8 Traçabilité maîtrisée

Les opérations sensibles et décisions d'accès doivent pouvoir être auditées, sans exposer inutilement les contenus confidentiels ou les secrets.

# 5. Acteurs et identités

Le modèle de sécurité distingue les catégories d'acteurs suivantes :

### 5.1 Identité humaine

Représente une personne qui utilise le moteur directement ou par l'intermédiaire d'une application cliente.

Une identité humaine est indépendante d'une organisation. Son appartenance et ses droits dans une organisation sont établis dans le contexte correspondant.

### 5.2 Identité de service

Représente une application, un service ou un processus autorisé à agir auprès du moteur.

Elle est distincte de l'identité humaine éventuellement à l'origine d'une action. Lorsque cela est pertinent, le contexte doit permettre de distinguer l'acteur humain, l'application cliente et l'identité technique ayant exécuté l'opération.

### 5.3 Application cliente

L'application cliente possède une identité propre et un périmètre d'accès défini. Son association à une organisation ne lui accorde pas automatiquement tous les droits de cette organisation.

### 5.4 Acteur effectif

Pour chaque opération protégée, le moteur doit pouvoir déterminer l'identité sous laquelle l'opération est exécutée et, lorsque disponible, l'identité humaine ou applicative qui l'a initiée.

# 6. Authentification et autorisation

## 6.1 Authentification

L'authentification établit l'identité d'un utilisateur ou d'un service.

Le moteur doit distinguer les mécanismes d'authentification des utilisateurs humains et ceux des applications ou services. Les mécanismes précis, les protocoles et les fournisseurs d'identité seront définis dans une spécification technique dédiée ou une décision architecturale ultérieure.

## 6.2 Autorisation

L'autorisation détermine si une identité peut effectuer une action sur une ressource dans un contexte donné.

L'évaluation doit pouvoir prendre en compte :

- l'identité et sa catégorie ;
- l'organisation et l'appartenance applicable ;
- l'application cliente ;
- la ressource ciblée ;
- l'action demandée ;
- le contexte de la requête ;
- les politiques et droits explicitement accordés.

## 6.3 Distinction des concepts d'autorisation

Le modèle conserve les distinctions suivantes :

- `Identity` : qui agit ;
- `Membership` : dans quelle organisation une identité humaine intervient ;
- `Permission` : quelle action peut être autorisée ;
- `Role` ou groupe, lorsqu'ils sont utilisés : moyen de regrouper des droits ou des acteurs ;
- `Authorization Policy` : règles d'évaluation d'un accès ;
- `Resource Access Grant` : droit accordé sur une ressource ou un périmètre.

La présence d'un grant ne dispense pas de l'évaluation des autres contraintes applicables, telles que l'état de la ressource, le périmètre organisationnel ou une politique de sécurité.

## 6.4 Contrôle côté moteur

Les autorisations doivent être vérifiées côté moteur. Une application cliente ne peut pas déclarer elle-même qu'un accès est autorisé.

Les identifiants d'organisation, d'application ou de Knowledge Base transmis dans une requête doivent être vérifiés par rapport à l'identité authentifiée et aux droits applicables.

# 7. Isolation organisationnelle et multi-tenant

## 7.1 Principe général

Les ressources d'une organisation ne doivent pas être accessibles à une autre organisation sans mécanisme de partage explicitement autorisé.

L'organisation propriétaire d'une ressource et les acteurs autorisés à l'utiliser doivent rester identifiables séparément.

## 7.2 Organisation et contexte d'isolation

Pour le modèle conceptuel initial, `Organization` constitue la racine logique de propriété et d'isolation des ressources.

L'expression `tenant context` peut désigner le contexte d'isolation transmis lors d'une opération. Elle ne désigne pas une entité `Tenant` indépendante dans le modèle initial. Une séparation future entre `Tenant` et `Organization` nécessitera un besoin explicite, une analyse d'impact et une décision architecturale documentée.

Les mécanismes techniques et le niveau physique d'isolation restent à définir dans les décisions techniques correspondantes. Cette définition conceptuelle ne préjuge donc pas d'une stratégie de déploiement ou de stockage.

## 7.3 Périmètres à protéger

L'isolation doit être prise en compte pour :

- les applications et identités ;
- les Knowledge Bases et leurs associations ;
- les sources et documents ;
- les versions, contenus extraits et fragments ;
- les embeddings et index ;
- les ressources et résultats structurés ;
- les requêtes, résultats, réponses et citations ;
- les configurations, tâches, journaux et historiques ;
- les résultats intermédiaires et éventuels caches.

## 7.4 Isolation des Knowledge Bases

L'accès à une Knowledge Base doit être vérifié indépendamment de l'appartenance générale à son organisation.

Une application ou une identité ne doit recevoir que les Knowledge Bases explicitement accessibles dans son contexte.

## 7.5 Partage de sources

Une source peut être associée à plusieurs Knowledge Bases conformément aux principes validés dans le document 04.

Cette réutilisation ne transfère pas la propriété de la source et ne donne pas automatiquement accès à son contenu à toutes les organisations concernées. Tout partage interorganisationnel nécessite une autorisation explicite et traçable.

# 8. Protection des connaissances et des données

Le moteur doit protéger la confidentialité, l'intégrité et la disponibilité des informations qu'il gère.

La protection concerne les contenus originaux ainsi que toutes leurs représentations dérivées : contenus extraits, chunks, embeddings, index, résultats de recherche et contextes de génération.

Les données dérivées ne doivent pas être considérées comme moins sensibles que leur source. Un embedding, un extrait ou un résultat de recherche peut révéler des informations confidentielles.

Les politiques de classification, de conservation, de localisation, de chiffrement et de sauvegarde seront précisées selon les besoins du produit et les contextes réglementaires des déploiements.

# 9. Sécurité du pipeline d'ingestion

Les sources externes et leurs contenus doivent être considérés comme non fiables.

Le pipeline d'ingestion doit respecter les principes suivants :

1. Vérifier que l'acteur est autorisé à connecter ou utiliser la source.
2. Vérifier que la source est autorisée pour la Knowledge Base concernée.
3. Contrôler les types de contenus et les limites d'importation définis par la politique applicable.
4. Traiter les contenus extraits comme des données, et non comme des instructions de contrôle du moteur.
5. Préserver la provenance et le périmètre d'accès des données dérivées.
6. Empêcher qu'une ingestion ou une réindexation rende accessibles des connaissances dans une base non autorisée.
7. Appliquer les règles de suppression et de conservation aux représentations dérivées.

Les contrôles spécialisés propres aux formats et aux connecteurs seront définis dans les spécifications d'ingestion.

# 10. Sécurité des données structurées

L'accès aux sources structurées doit être contrôlé indépendamment de l'accès aux documents.

Le moteur doit pouvoir déterminer quelles ressources structurées sont exposées et quelles opérations sont autorisées sur celles-ci.

Les principes suivants s'appliquent :

- seules les ressources autorisées peuvent être découvertes ou interrogées ;
- les permissions doivent être vérifiées pour chaque opération ;
- les résultats ne doivent pas révéler des enregistrements ou attributs non autorisés ;
- les opérations doivent être limitées au périmètre explicitement approuvé ;
- la provenance des résultats doit être conservée ;
- les erreurs ne doivent pas révéler la structure ou les données auxquelles l'acteur n'a pas accès.

Un LLM ne doit pas disposer d'un accès direct et libre aux sources structurées. Toute interrogation doit passer par une capacité contrôlée qui applique les autorisations et limites définies.

Les modèles d'interrogation, les opérations autorisées et les contrôles détaillés seront définis dans le document 12.

# 11. Sécurité de la recherche et de la récupération

Toute opération de recherche doit être limitée aux connaissances accessibles à l'acteur et à l'application concernés.

Les contrôles d'accès doivent s'appliquer avant qu'un résultat soit communiqué à l'appelant ou transmis à une étape ultérieure du traitement.

Les mécanismes de recherche, de fusion et de classement ne doivent pas pouvoir supprimer ou contourner les contraintes d'autorisation.

Les résultats récupérés doivent conserver leur provenance et leur contexte d'accès.

# 12. Sécurité de la génération et des fournisseurs externes

## 12.1 Contenus récupérés non fiables

Les documents, fragments et résultats externes transmis à un LLM constituent des données non fiables. Ils ne doivent pas être interprétés comme des instructions capables de remplacer les instructions de contrôle du moteur.

Le moteur doit maintenir une séparation claire entre les instructions de contrôle, la demande de l'utilisateur et les contenus récupérés.

## 12.2 Injection de prompt

Le moteur doit prendre en compte les tentatives d'injection directe ou indirecte provenant des demandes utilisateur, des documents, des pages web, des résultats structurés ou des réponses de fournisseurs.

La simple présence d'instructions dans un document ne leur confère aucune autorité sur le moteur.

## 12.3 Limitation des données transmises

Seules les informations nécessaires à la génération doivent être transmises au fournisseur externe, conformément aux autorisations et politiques de traitement applicables.

Le moteur doit pouvoir tenir compte des contraintes de confidentialité et des règles de transfert définies pour les organisations et les Knowledge Bases.

## 12.4 Absence d'autorité du LLM

Un LLM ne constitue pas une autorité d'authentification ou d'autorisation. Il ne peut ni accorder des droits, ni modifier le périmètre d'accès, ni contourner les contrôles du moteur.

Ses propositions d'actions ou d'interrogations doivent être validées par les composants responsables avant toute exécution.

# 13. Protection des fournisseurs et des secrets

Les configurations de fournisseurs peuvent nécessiter des informations d'authentification ou des secrets.

Les principes suivants s'appliquent :

- les secrets sont distincts des paramètres ordinaires de configuration ;
- ils ne doivent pas être exposés dans les réponses API, les journaux ou les interfaces d'administration ;
- leur accès doit être limité aux composants et opérations qui en ont besoin ;
- leur utilisation doit pouvoir être auditée sans enregistrer leur valeur ;
- leur remplacement ou leur révocation doit être possible sans exposer les autres configurations.

Les mécanismes de stockage, de rotation et de gestion des secrets seront définis ultérieurement.

# 14. Sécurité des interfaces et des opérations administratives

Les interfaces publiques et administratives doivent appliquer l'authentification, l'autorisation et les contrôles de périmètre pertinents.

Les opérations sensibles — notamment la gestion des identités, des permissions, des sources, des Knowledge Bases et des configurations — doivent être réservées aux acteurs habilités.

Une opération administrative ne doit pas bénéficier d'une confiance implicite simplement parce qu'elle provient d'une interface d'administration.

Les contrôles doivent aussi s'appliquer aux opérations déclenchées par des tâches ou des traitements internes.

# 15. Audit, traçabilité et confidentialité des journaux

Les événements importants de sécurité et d'administration doivent être traçables.

La traçabilité doit permettre, selon le cas, d'identifier :

- l'acteur humain ou applicatif ;
- l'organisation et l'application concernées ;
- la ressource visée ;
- l'action demandée ;
- le résultat de l'opération ;
- le moment de l'événement.

Les décisions d'accès importantes, les changements de permissions, les opérations de partage et les suppressions doivent pouvoir être audités.

Les journaux ne doivent pas contenir de secrets ni reproduire inutilement des contenus documentaires, des données personnelles ou des réponses confidentielles.

# 16. Cycle de vie, révocation et suppression

La sécurité doit rester applicable pendant tout le cycle de vie d'une ressource.

La révocation d'un accès doit empêcher les accès ultérieurs selon les règles de cohérence définies.

La suppression d'une source, d'un document, d'une association ou d'une Knowledge Base doit tenir compte des données dérivées, index, résultats persistés et copies éventuelles.

La suppression d'une association ne doit pas entraîner automatiquement la suppression d'une ressource partagée ou de son original, sauf si la politique et les droits applicables le prévoient.

Les politiques de conservation, les délais de propagation et le traitement des sauvegardes seront définis dans les spécifications spécialisées.

# 17. Gestion des erreurs et des incidents

Les erreurs de sécurité doivent être traitées sans divulguer d'informations auxquelles l'acteur n'a pas droit.

Le moteur doit distinguer les refus d'accès, les ressources inexistantes ou non visibles, les erreurs de validation et les indisponibilités externes, tout en évitant les réponses qui faciliteraient l'énumération de ressources protégées.

Les incidents importants doivent pouvoir être enregistrés et suivis conformément aux règles d'audit et de supervision.

# 18. Exigences de sécurité transversales

Les principes de sécurité doivent s'appliquer à tous les domaines :

| Domaine | Contrôle attendu |
|---|---|
| Gouvernance | Identités vérifiées et droits explicites |
| Applications clientes | Identité applicative et périmètre d'accès distincts |
| Knowledge Bases | Isolation et autorisation par base |
| Sources | Autorisation de connexion et d'utilisation |
| Documents et versions | Protection du contenu original et de ses versions |
| Chunks et embeddings | Conservation de la provenance et du périmètre d'accès |
| Index | Recherche limitée aux connaissances autorisées |
| Données structurées | Accès contrôlé aux ressources et opérations |
| Retrieval | Filtrage de sécurité avant restitution des résultats |
| Generation | Contexte limité, contenu non fiable et citations traçables |
| Fournisseurs | Protection des secrets et contrôle des transferts |
| Administration | Privilèges limités et opérations auditées |
| Journaux | Traçabilité sans divulgation excessive |
| Suppression | Prise en compte des représentations dérivées |

# 19. Correspondance avec les exigences du cahier des charges

Cette spécification contribue principalement aux exigences suivantes :

| Exigence | Couverture dans cette spécification |
|---|---|
| FR-001 à FR-006 | Organisations, applications, identités, permissions et isolation des Knowledge Bases |
| FR-007 | Contrôle des sources et de leurs associations |
| FR-010 | Protection du cycle de vie et suppression des données documentaires |
| FR-018 à FR-021 | Protection du contexte de génération, des contenus récupérés et des citations |
| FR-022 et FR-023 | Accès contrôlé aux sources et ressources structurées |
| FR-025 et FR-026 | Sécurité des interfaces et des requêtes |
| FR-027 et FR-028 | Sécurité des opérations administratives et audit |
| NFR-001 | Isolation des organisations |
| NFR-002 | Contrôle des accès |
| NFR-003 | Protection des données sensibles |
| NFR-004 | Protection contre les injections |
| NFR-005 | Gestion des secrets |
| NFR-006 à NFR-009 | Intégrité, résilience, traçabilité et cohérence après modification |
| NFR-018 | Observabilité des événements et incidents |
| NFR-020 | Vérifiabilité des exigences de sécurité |

Cette correspondance ne signifie pas que la sécurité est limitée à ces exigences. Elle est transversale à l'ensemble du cahier des charges.

# 20. Décisions et sujets reportés

Les sujets suivants nécessitent des décisions ou spécifications ultérieures :

1. Évaluer, si un besoin concret apparaît, l'opportunité de distinguer un Tenant ou un Isolation Scope de l'Organization. Le modèle initial retient Organization comme racine logique de propriété et d'isolation.
2. Modèle précis de rôles, groupes, permissions et politiques.
3. Mécanismes et protocoles d'authentification des identités humaines et applicatives.
4. Gestion, stockage, rotation et révocation des secrets.
5. Classification des données et politiques de conservation.
6. Exigences de chiffrement et gestion des clés.
7. Conditions de partage interorganisationnel des sources et connaissances.
8. Contrôles précis sur les ressources structurées.
9. Politiques de transfert des données vers les fournisseurs externes.
10. Traitement des sauvegardes et des suppressions différées.
11. Exigences réglementaires applicables selon les juridictions et les déploiements.

Ces sujets restent ouverts et ne doivent pas être considérés comme des décisions techniques déjà approuvées.

# 21. Conditions de validation

Le document pourra être validé lorsque :

1. Les acteurs et identités sont clairement distingués.
2. La séparation entre authentification, propriété et autorisation est confirmée.
3. Les principes d'isolation des organisations et des Knowledge Bases sont cohérents avec les documents précédents.
4. Les sources partagées ne contournent pas les règles de propriété et d'accès.
5. La protection des données documentaires et structurées est couverte.
6. Les contenus externes et récupérés sont considérés comme non fiables.
7. Les fournisseurs externes et leurs secrets sont couverts.
8. L'audit et la confidentialité des journaux sont pris en compte.
9. Le cycle de vie et la suppression des données dérivées sont couverts.
10. Les exigences du cahier des charges sont correctement reliées à cette spécification.
11. Les décisions techniques non prises sont clairement identifiées.
12. La cohérence avec les documents 00 à 10 est vérifiée.

# 22. Conclusion

La sécurité et l'isolation constituent des propriétés fondamentales de Universal RAG Engine.

Elles s'appliquent aux organisations, aux applications, aux identités, aux Knowledge Bases, aux sources, aux documents, aux données structurées, aux recherches, aux générations et aux opérations administratives.

Le moteur doit garantir que chaque acteur n'accède qu'aux ressources et capacités explicitement autorisées, sans permettre aux applications clientes, aux contenus externes ou aux fournisseurs d'outrepasser les règles de contrôle du système.

**La sécurité est une responsabilité architecturale transversale et une condition de confiance du moteur, pas une fonction ajoutée après sa construction.**
