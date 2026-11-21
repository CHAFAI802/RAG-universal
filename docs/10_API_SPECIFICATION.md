# UNIVERSAL RAG ENGINE

## Document 10 — API Specification

**Version :** 1.0
**Statut :** VALIDATED
**Projet :** RAG-universal

---

# 1. Objectif

Ce document définit le rôle, le périmètre et les principes fonctionnels de l'API de Universal RAG Engine.

Il précise comment les applications clientes et les acteurs autorisés peuvent accéder aux capacités du moteur sans dépendre de son organisation interne.

Il décrit notamment :

- Les catégories d'utilisateurs de l'API.
- Les grandes capacités exposées.
- Les frontières entre API publique et interfaces internes.
- Le contexte d'identité, d'organisation et d'autorisation.
- Les principaux parcours d'utilisation.
- Les principes de requête et de réponse.
- La gestion des erreurs, des opérations longues et de la compatibilité.
- Les exigences de sécurité, de traçabilité et de disponibilité.

Ce document reste au niveau fonctionnel et contractuel. Il ne fixe pas encore les routes, les méthodes HTTP, les schémas détaillés des messages, le protocole, le framework ou la technologie d'implémentation.

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

L'API doit respecter les décisions validées dans ces documents. Elle ne doit pas introduire de responsabilités métier qui appartiennent aux modules du moteur.

# 3. Objectifs de l'API

L'API doit :

1. Permettre à plusieurs applications indépendantes d'utiliser le même moteur.
2. Exposer les capacités du moteur à travers des contrats documentés et stables.
3. Permettre la gestion autorisée des organisations, applications et Knowledge Bases.
4. Permettre la gestion des sources et des opérations d'ingestion.
5. Exposer les capacités de recherche et de génération.
6. Permettre l'exploitation contrôlée des données structurées.
7. Fournir des résultats compréhensibles et traçables.
8. Masquer les détails internes de l'architecture et du stockage.
9. Maintenir l'isolation des organisations, applications et Knowledge Bases.
10. Permettre l'évolution du moteur sans imposer une refonte des applications clientes.

# 4. Principes de conception

## P1 — Indépendance des applications clientes

Une application cliente utilise l'API sans accéder directement aux modules internes, aux stockages ou aux fournisseurs du moteur.

## P2 — Contrats explicites

Chaque capacité exposée doit définir clairement son objectif, ses conditions d'accès, ses entrées conceptuelles, ses résultats et ses erreurs possibles.

## P3 — Stabilité

Les changements internes du moteur ne doivent pas entraîner inutilement des changements dans les applications clientes.

## P4 — Sécurité côté moteur

L'API ne considère jamais une information déclarée par le client comme une preuve d'identité ou d'autorisation. L'accès est déterminé à partir d'une identité authentifiée et de règles vérifiées par le moteur.

## P5 — Séparation des responsabilités

L'API reçoit, valide et transmet les demandes. Les règles métier restent la responsabilité des modules concernés.

## P6 — Neutralité technologique

La spécification ne dépend d'aucun protocole, framework ou fournisseur particulier.

## P7 — Traçabilité

Les opérations importantes et les réponses doivent pouvoir être reliées à leur demande d'origine et à leur contexte d'exécution.

## P8 — Évolution contrôlée

Les contrats peuvent évoluer, mais les changements incompatibles doivent être identifiés et gérés explicitement.

# 5. Consommateurs de l'API

L'API peut être utilisée par plusieurs catégories d'acteurs :

## 5.1 Applications clientes

Applications métier ou plateformes externes qui intègrent les capacités de Universal RAG Engine.

Exemples :

- Applications de santé.
- Applications juridiques.
- Plateformes éducatives.
- Applications d'entreprise.
- Assistants spécialisés.

Ces applications restent propriétaires de leur interface utilisateur et de leurs processus métier.

## 5.2 Interfaces d'administration

Interfaces autorisées à gérer les organisations, les applications, les Knowledge Bases, les sources et les configurations relevant de leur périmètre.

Une interface d'administration est un consommateur de l'API ; elle ne doit pas accéder directement aux données internes.

## 5.3 Services et agents externes

Des services ou agents peuvent utiliser les capacités de recherche et de génération, dans les limites des permissions qui leur sont accordées.

L'accès d'un agent ne lui confère pas de privilèges supplémentaires par rapport à son identité et à son contexte d'autorisation.

# 6. Frontières de l'API

L'API constitue la frontière publique entre les applications clientes et Universal RAG Engine.

Elle expose des capacités fonctionnelles, et non les modules internes un par un.

Trois catégories d'interfaces sont distinguées conceptuellement :

## 6.1 API d'utilisation

Expose les capacités destinées à être consommées par les applications :

- Recherche de connaissances.
- Récupération de résultats.
- Génération directe par LLM, lorsque cette capacité est autorisée.
- Génération augmentée par récupération.
- Exploitation contrôlée des données structurées.
- Consultation des résultats et références associés à une demande.

## 6.2 API de gestion

Expose les capacités administratives autorisées :

- Gestion des organisations et applications.
- Gestion des identités et des autorisations, dans le périmètre défini.
- Création et gestion des Knowledge Bases.
- Gestion des sources et de leurs associations.
- Gestion des configurations accessibles à l'acteur.
- Consultation de l'état des opérations.

## 6.3 Interfaces internes entre modules

Les contrats internes qui permettent aux modules de collaborer ne constituent pas automatiquement des interfaces publiques.

Ils restent distincts des contrats destinés aux applications clientes et peuvent évoluer selon la gouvernance architecturale interne.

# 7. Capacités fonctionnelles exposées

## 7.1 Gestion des Knowledge Bases

L'API de gestion doit permettre aux acteurs autorisés de :

- Créer une Knowledge Base.
- Consulter ses informations accessibles.
- Modifier sa configuration autorisée.
- Activer ou désactiver son utilisation.
- Supprimer une Knowledge Base, selon les règles de cycle de vie.
- Gérer les associations avec les sources.
- Gérer les connaissances intégrées dans son périmètre.

L'API ne doit pas exposer une Knowledge Base à un acteur qui n'y est pas autorisé.

## 7.2 Gestion des sources

L'API doit permettre de gérer les sources accessibles et leurs associations avec les Knowledge Bases.

Elle doit préserver la distinction entre :

- L'identité d'une source.
- La connexion à cette source.
- L'association de cette source à une Knowledge Base.
- Les connaissances effectivement retenues dans une Knowledge Base.

L'association d'une source à une base ne signifie pas que toutes les données de la source sont automatiquement intégrées.

## 7.3 Ingestion et cycle de vie documentaire

L'API doit permettre de déclencher les opérations documentaires autorisées, notamment :

- Importer ou enregistrer un document.
- Demander le traitement d'un document ou d'une source.
- Consulter l'état d'une opération.
- Déclencher une actualisation ou une réindexation lorsque cette capacité est autorisée.
- Demander la suppression d'une connaissance.

L'API doit distinguer l'acceptation d'une demande de traitement de son achèvement effectif.

Les opérations longues doivent pouvoir être suivies à travers les concepts opérationnels définis dans le modèle de données.

## 7.4 Recherche seule — Retrieval Only

L'API doit permettre d'effectuer une recherche et de retourner les résultats récupérés sans appeler nécessairement un LLM.

Les résultats doivent conserver leur provenance et les informations de pertinence disponibles.

Une réponse de recherche seule ne doit pas être présentée comme une réponse générée par un LLM.

## 7.5 Génération directe — Direct LLM Generation

Lorsque cette capacité est autorisée, l'API peut permettre de demander une génération directe par LLM sans récupération préalable dans les Knowledge Bases pour cette requête.

Le résultat doit être identifiable comme une génération directe.

Il ne doit pas être présenté comme fondé sur des connaissances récupérées dans les Knowledge Bases.

## 7.6 Génération augmentée — Retrieval-Augmented Generation

L'API doit permettre de demander une réponse générée après récupération de connaissances autorisées.

La réponse doit préserver les relations avec :

- La demande d'origine.
- Les Knowledge Bases concernées.
- Les résultats récupérés.
- Les éléments effectivement transmis au modèle.
- Les sources utilisées pour produire la réponse.
- Les citations retournées.

Les résultats récupérés ne doivent pas être assimilés automatiquement aux citations de la réponse.

## 7.7 Accès aux données structurées

L'API doit permettre l'exploitation contrôlée des sources structurées lorsque cette capacité est configurée et autorisée.

Elle ne doit pas fournir aux applications clientes ou aux modèles un accès libre aux systèmes de données sous-jacents.

Les résultats structurés doivent conserver leur provenance et leur contexte de récupération.

## 7.8 Consultation des opérations

L'API doit permettre de consulter les informations accessibles concernant les opérations suivies, notamment leur état et leur résultat.

La consultation d'une opération est soumise aux mêmes règles d'identité, de périmètre et d'autorisation que son déclenchement.

# 8. Contexte d'une requête

Toute demande protégée doit être traitée dans un contexte de sécurité vérifié.

Ce contexte peut inclure :

- L'identité authentifiée.
- L'application cliente à l'origine de l'appel.
- L'organisation dans laquelle l'opération est réalisée.
- Les Knowledge Bases visées.
- Les permissions applicables.
- Un identifiant permettant de relier les événements d'une même demande.

Les valeurs indiquées par le client ne constituent pas, à elles seules, une preuve d'autorisation.

Le moteur doit vérifier que l'identité, l'application, l'organisation et les ressources demandées sont compatibles entre elles.

Une requête sans périmètre Knowledge Base, telle qu'une génération directe autorisée, ne doit pas être artificiellement associée à une Knowledge Base.

# 9. Principes de réponse

Les réponses de l'API doivent être suffisamment explicites pour que l'application cliente puisse comprendre le résultat obtenu.

Selon la capacité appelée, une réponse peut contenir conceptuellement :

- L'identification de la demande.
- Le type de traitement réalisé.
- Le résultat obtenu.
- Les références de provenance disponibles.
- Les informations de pertinence disponibles.
- L'état d'une opération lorsque le traitement se poursuit.
- Les avertissements nécessaires à une interprétation correcte.

Le format définitif des messages sera spécifié ultérieurement.

## 9.1 Distinction des résultats

L'API doit distinguer clairement :

| Mode | Nature du résultat | Génération LLM |
|---|---|---|
| Retrieval Only | Résultats récupérés | Non |
| Direct LLM Generation | Réponse générée sans Retrieval dans les Knowledge Bases | Oui |
| Retrieval-Augmented Generation | Réponse générée à partir de connaissances récupérées | Oui |

Une réponse directe ne doit pas recevoir artificiellement des citations issues des Knowledge Bases.

Une réponse augmentée doit retourner les citations correspondant aux sources effectivement utilisées, dans la mesure où elles peuvent être établies.

# 10. Gestion des erreurs

L'API doit retourner des erreurs compréhensibles, cohérentes et exploitables par les applications clientes.

Les catégories conceptuelles comprennent notamment :

- Demande invalide ou incomplète.
- Identité absente ou non valide.
- Accès non autorisé.
- Ressource inexistante ou inaccessible.
- Ressource indisponible ou dans un état incompatible avec l'opération.
- Capacité non configurée ou non supportée.
- Conflit avec l'état actuel d'une ressource.
- Échec d'un traitement ou d'un fournisseur externe.
- Erreur interne du moteur.

Les réponses d'erreur ne doivent pas révéler de secrets, de détails internes sensibles ou des informations sur des ressources auxquelles l'appelant n'a pas accès.

# 11. Opérations longues et suivi

Certaines opérations peuvent nécessiter un traitement différé, notamment l'ingestion, l'extraction, l'indexation, la réindexation ou la suppression de volumes importants.

L'API doit distinguer :

- La réception d'une demande.
- Son acceptation ou son rejet.
- Son exécution.
- Son achèvement ou son échec.

Lorsqu'une opération est acceptée pour traitement différé, l'application cliente doit disposer d'une référence permettant d'en consulter l'état si elle est autorisée.

Les détails du mécanisme d'exécution, des files de traitement et des tentatives de reprise ne sont pas définis dans ce document.

# 12. Compatibilité et évolution des contrats

Les contrats publics doivent évoluer de manière contrôlée.

Les principes suivants s'appliquent :

1. Les changements incompatibles doivent être identifiés.
2. Les applications clientes doivent disposer d'une période ou d'une stratégie de transition lorsque cela est nécessaire.
3. Les capacités et options disponibles doivent être documentées.
4. Les comportements non supportés ne doivent pas être simulés silencieusement.
5. Les contrats publics ne doivent pas exposer les structures internes de stockage.
6. Les évolutions internes ne doivent pas imposer de changement aux clients lorsqu'elles restent compatibles avec les contrats publics.

La stratégie précise de versionnement sera définie dans la conception détaillée de l'API.

# 13. Sécurité et isolation

L'API constitue une frontière de confiance majeure.

Elle doit garantir les principes suivants :

- Toute opération protégée repose sur une identité authentifiée.
- Les permissions sont évaluées côté moteur.
- Les périmètres organisationnels et les accès aux Knowledge Bases sont vérifiés.
- L'identité de l'application est distinguée de l'identité humaine éventuellement représentée.
- Les accès aux données structurées sont contrôlés séparément des accès documentaires.
- Les erreurs ne divulguent pas les ressources non accessibles.
- Les secrets ne sont jamais retournés dans les réponses ordinaires.
- Les opérations sensibles sont traçables.

L'API ne doit pas permettre de contourner les contrôles de sécurité des modules internes.

# 14. Traçabilité et observabilité

Les opérations importantes doivent pouvoir être reliées à leur demande d'origine.

La traçabilité doit permettre, selon les règles de conservation applicables, de retrouver :

- L'acteur et l'application à l'origine de la demande.
- Le périmètre organisationnel concerné.
- La capacité invoquée.
- Le résultat ou l'état de l'opération.
- Les erreurs pertinentes.
- Les références de provenance associées à une réponse.

Les données sensibles ne doivent pas être copiées sans nécessité dans les journaux ou les informations de diagnostic.

# 15. Limites et responsabilités

L'API ne doit pas :

- Exposer directement les tables ou structures internes du moteur.
- Permettre aux applications clientes de contourner les autorisations.
- Donner un accès libre aux fournisseurs ou stockages sous-jacents.
- Imposer une interface utilisateur aux applications clientes.
- Transformer les règles métier des applications clientes en règles du cœur RAG.
- Confondre gestion des Knowledge Bases, ingestion, recherche et génération.
- Garantir qu'une réponse générée est vraie simplement parce qu'elle a été produite par un LLM.

# 16. Correspondance avec les exigences

| Exigence | Couverture apportée par l'API |
|---|---|
| FR-001 | Exposition autorisée de la gestion des organisations |
| FR-002 | Enregistrement et gestion des applications clientes |
| FR-003 | Application des identités et permissions aux opérations |
| FR-004 | Gestion des Knowledge Bases |
| FR-005 | Gestion des configurations autorisées des Knowledge Bases |
| FR-006 | Contrôle des accès aux Knowledge Bases |
| FR-007 | Gestion des sources et de leurs associations |
| FR-008 | Demande d'importation documentaire |
| FR-010 | Demandes de modification et suppression documentaire |
| FR-013 | Déclenchement et suivi des opérations d'indexation |
| FR-014 à FR-017 | Exposition des capacités de recherche et de classement |
| FR-018 à FR-021 | Exposition des modes de génération et de leurs résultats |
| FR-022 à FR-024 | Accès contrôlé aux données structurées et combinaison des résultats |
| FR-025 | Interface publique documentée pour les applications clientes |
| FR-026 | Réception, traitement et suivi des requêtes |
| FR-027 | Capacités d'administration autorisées |
| FR-028 | Traçabilité des opérations et supervision |

Les exigences non fonctionnelles relatives à la sécurité, à l'isolation, à la fiabilité, à la compatibilité, à la traçabilité et à l'observabilité s'appliquent transversalement à l'API.

# 17. Éléments non décidés

Les sujets suivants restent volontairement ouverts :

- Protocole et style d'API.
- Routes et méthodes détaillées.
- Schémas définitifs des requêtes et réponses.
- Mécanisme et protocole d'authentification.
- Stratégie de versionnement technique.
- Pagination et limites précises.
- Limites de débit et quotas.
- Format exact des erreurs.
- Mécanisme de traitement asynchrone.
- Mécanisme de diffusion de progression ou de notifications.
- Politique de compatibilité et de dépréciation détaillée.

Ces choix seront étudiés dans les spécifications techniques et de sécurité correspondantes.

# 18. Conditions de validation

Le document pourra être validé lorsque :

1. Les consommateurs et frontières de l'API seront clairement définis.
2. Les capacités d'utilisation et de gestion seront identifiées.
3. La séparation entre API publique et interfaces internes sera confirmée.
4. Le contexte d'identité et d'autorisation sera cohérent avec le modèle de gouvernance.
5. Les trois modes Retrieval Only, Direct LLM Generation et Retrieval-Augmented Generation seront distingués.
6. Les données structurées conserveront leur mécanisme d'accès contrôlé.
7. Les opérations longues pourront être suivies sans confondre acceptation et achèvement.
8. Les principes de réponse, d'erreur et de compatibilité seront définis.
9. La traçabilité et l'isolation seront prises en compte.
10. La cohérence avec les documents 00 à 09 sera vérifiée.
11. Aucun choix technologique prématuré ne sera imposé.

# 19. Conclusion

L'API constitue la frontière contractuelle entre Universal RAG Engine et les applications qui l'utilisent.

Elle expose les capacités du moteur sans révéler son implémentation interne et sans transférer aux applications clientes la responsabilité des règles de sécurité ou de cohérence des connaissances.

Elle doit permettre l'utilisation indépendante des capacités de gestion, d'ingestion, de recherche, de génération et d'accès aux données structurées.

**Une API stable, des contrats explicites et des applications clientes indépendantes : le moteur doit pouvoir évoluer sans imposer son évolution interne à ses utilisateurs.**
