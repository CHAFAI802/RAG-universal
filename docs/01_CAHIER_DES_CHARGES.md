# UNIVERSAL RAG ENGINE

## Document 01 — Cahier des charges

**Version :** 1.0
**Statut :** VALIDATED
**Date :** 21 novembre 2026
**Projet :** RAG-universal

---

1. Introduction

1.1 Objet du document

Ce document définit les exigences fonctionnelles et non fonctionnelles de Universal RAG Engine.

Il précise ce que le système devra être capable de faire, les contraintes qu'il devra respecter et les conditions permettant de vérifier que les exigences sont satisfaites.

Il constitue la référence fonctionnelle pour les futures spécifications architecturales et techniques.

1.2 Références

Ce cahier des charges s'appuie sur les documents suivants :

00_VISION_ET_OBJECTIFS.md

DEPENDENCY_MAP.md

DECISION_LOG.md

En cas de contradiction, les documents fondateurs et les décisions architecturales validées devront être examinés avant toute modification.

1.3 Périmètre

Le cahier des charges couvre :

La gestion des organisations.

La gestion des applications clientes.

La gestion des utilisateurs et des permissions.

La gestion des bases de connaissances.

L'importation des connaissances.

Le traitement documentaire.

L'indexation.

La recherche.

La génération augmentée.

L'exploitation des données structurées.

La traçabilité.

La sécurité.

L'administration et la supervision.

L'évaluation de la qualité.

2. Terminologie

Terme

Définition

Universal RAG Engine

Moteur central de gestion et d'exploitation des connaissances

Organisation

Entité propriétaire d'un ensemble de ressources

Application cliente

Application externe utilisant les services du moteur

Knowledge Base

Espace organisé de connaissances

Source

Origine des informations importées

Document

Élément documentaire intégré au système

Chunk

Fragment de contenu issu du découpage d'un document

Embedding

Représentation vectorielle d'un contenu

Retrieval

Processus de recherche et de récupération des informations

Reranking

Réorganisation des résultats selon leur pertinence

LLM

Modèle de langage utilisé pour produire les réponses

Citation

Référence permettant de retrouver une source utilisée

Tenant

Contexte d'isolation associé à une opération et déterminé à partir de l'Organization et des autorisations applicables. Il ne constitue pas une entité indépendante dans le modèle conceptuel initial.

3. Classification des priorités

Les exigences seront classées selon trois niveaux.

Priorité

Signification

MUST

Indispensable au fonctionnement attendu du produit

SHOULD

Important, mais peut être planifié après les fonctions fondamentales

COULD

Fonctionnalité complémentaire ou amélioration future

Une exigence MUST ne pourra pas être considérée comme satisfaite sans preuve et test appropriés.

4. Exigences fonctionnelles (FR)

4.1 Gestion des organisations et des applications

FR-001 — Gestion des organisations

Priorité : MUST

Le système doit permettre de créer, consulter, modifier, désactiver et supprimer des organisations.

Critères d'acceptation :

Chaque organisation possède un identifiant unique.

Les ressources sont associées à leur organisation propriétaire.

Une organisation ne peut pas accéder aux ressources d'une autre organisation sans autorisation explicite.

FR-002 — Gestion des applications clientes

Priorité : MUST

Le système doit permettre d'enregistrer plusieurs applications clientes.

Critères d'acceptation :

Chaque application possède une identité distincte.

Une application est associée à une organisation ou à un périmètre autorisé.

Les droits d'accès sont vérifiables.

Une application peut être désactivée sans supprimer les données de son organisation.

FR-003 — Gestion des utilisateurs et permissions

Priorité : MUST

Le système doit gérer les utilisateurs, leurs identités et leurs autorisations.

Critères d'acceptation :

Les accès sont soumis à une authentification.

Les autorisations sont contrôlées côté moteur.

Les permissions peuvent être associées aux organisations, applications et bases de connaissances.

Un utilisateur ne peut pas dépasser les droits qui lui sont attribués.

Les mécanismes précis d'authentification et d'autorisation seront définis dans les spécifications de sécurité.

4.2 Gestion des Knowledge Bases

FR-004 — Création et gestion des Knowledge Bases

Priorité : MUST

Le système doit permettre de créer et de gérer plusieurs bases de connaissances indépendantes.

Critères d'acceptation :

Chaque base possède un identifiant unique.

Chaque base appartient à un périmètre organisationnel.

Une organisation peut posséder plusieurs bases.

Chaque base possède ses propres paramètres.

Une base peut être activée, désactivée et supprimée.

FR-005 — Configuration des Knowledge Bases

Priorité : MUST

Chaque base doit disposer de configurations adaptées à son utilisation.

Les paramètres pourront notamment concerner :

Les sources autorisées.

Les stratégies de découpage.

Les modèles d'embeddings.

Les stratégies de recherche.

Les filtres.

Les paramètres de récupération.

Les paramètres de génération.

Critères d'acceptation :

Les configurations sont propres à chaque base lorsque nécessaire.

Leur modification est contrôlée.

Les changements susceptibles d'invalider un index entraînent une opération de réindexation ou une migration maîtrisée.

FR-006 — Isolation des Knowledge Bases

Priorité : MUST

Les connaissances doivent être accessibles uniquement aux utilisateurs et applications autorisés.

Critères d'acceptation :

Une recherche ne doit jamais exposer des résultats provenant d'une base non autorisée.

Les filtres de sécurité ne peuvent pas être supprimés par une simple modification des paramètres de recherche.

L'isolation est vérifiée dans les tests.

4.3 Sources et ingestion

FR-007 — Gestion des sources

Priorité : MUST

Le système doit permettre de connecter différentes sources de connaissances.

Sources envisagées :

Importation de fichiers.

Répertoires documentaires.

API externes.

Bases de données.

Documentation web.

Systèmes de stockage externes.

Critères d'acceptation :

Chaque source est identifiable.

Son origine est conservée.

Son état de connexion est connu.

Les erreurs de connexion sont signalées.

FR-008 — Importation documentaire

Priorité : MUST

Le moteur doit accepter plusieurs formats documentaires.

Formats initiaux envisagés :

PDF.

DOCX.

TXT.

Markdown.

HTML.

Critères d'acceptation :

Les formats supportés sont identifiés.

Les documents exploitables sont importés.

Les documents invalides ou illisibles sont signalés.

L'importation ne doit pas corrompre les données déjà indexées.

FR-009 — Extraction et normalisation

Priorité : MUST

Le système doit extraire et normaliser le contenu des sources documentaires.

Critères d'acceptation :

Le contenu exploitable est extrait.

Les métadonnées utiles sont conservées.

Les erreurs d'extraction sont identifiables.

Le contenu original reste identifiable.

Le traitement respecte le format et la structure lorsque cela est nécessaire.

FR-010 — Gestion du cycle de vie documentaire

Priorité : MUST

Le système doit gérer les modifications, suppressions et réimportations des documents.

Critères d'acceptation :

Un document modifié peut être réindexé.

Un document supprimé ne doit plus apparaître dans les résultats.

Ses fragments et représentations vectorielles doivent être traités en conséquence.

L'historique des versions peut être retrouvé lorsque la politique de conservation le prévoit.

4.4 Traitement et indexation

FR-011 — Découpage documentaire

Priorité : MUST

Le système doit découper les contenus documentaires en unités adaptées à leur exploitation.

Critères d'acceptation :

Plusieurs stratégies de découpage peuvent être utilisées.

Les fragments conservent leur relation avec leur document d'origine.

Les métadonnées nécessaires à la traçabilité sont conservées.

Les paramètres de découpage sont configurables.

FR-012 — Gestion des embeddings

Priorité : MUST

Le moteur doit pouvoir utiliser différents modèles d'embeddings.

Critères d'acceptation :

Les fournisseurs ne sont pas imposés par le cœur du moteur.

Chaque représentation vectorielle est associée à son modèle de production.

Les incompatibilités entre modèles sont détectées.

Le changement de modèle peut déclencher une réindexation contrôlée.

FR-013 — Indexation et réindexation

Priorité : MUST

Le système doit gérer les index nécessaires aux différents mécanismes de recherche.

Critères d'acceptation :

L'état de l'indexation est consultable.

Les erreurs sont identifiables.

Les opérations peuvent être relancées selon des règles définies.

Les modifications documentaires sont répercutées dans les index.

Les réindexations ne provoquent pas d'incohérences non maîtrisées.

4.5 Recherche et récupération

FR-014 — Recherche vectorielle

Priorité : MUST

Le moteur doit permettre de rechercher des connaissances à partir de la similarité sémantique.

Critères d'acceptation :

Une requête peut être comparée aux représentations vectorielles indexées.

Les résultats sont classés selon leur pertinence.

Les résultats respectent les permissions d'accès.

Les paramètres de recherche sont configurables.

FR-015 — Recherche textuelle

Priorité : MUST

Le moteur doit permettre de rechercher des connaissances à partir de leur contenu textuel.

Critères d'acceptation :

Une recherche textuelle peut être exécutée indépendamment de la recherche vectorielle.

Les résultats sont classés selon une stratégie définie.

Les filtres et permissions sont respectés.

FR-016 — Recherche hybride

Priorité : MUST

Le moteur doit pouvoir combiner les résultats de la recherche vectorielle et de la recherche textuelle.

Critères d'acceptation :

Les deux mécanismes peuvent être utilisés dans une même requête.

Les résultats peuvent être fusionnés.

Les stratégies de combinaison sont configurables.

Le résultat final peut être évalué indépendamment des recherches individuelles.

FR-017 — Filtrage et classement

Priorité : MUST

Le moteur doit permettre de filtrer et de classer les résultats.

Critères d'acceptation :

Les filtres peuvent utiliser des métadonnées.

Les résultats respectent les permissions.

Les résultats peuvent être réordonnés selon leur pertinence.

Les critères de classement sont observables.

4.6 Génération augmentée

FR-018 — Génération à partir des connaissances récupérées

Priorité : MUST

Le moteur doit permettre de construire une réponse à partir des connaissances récupérées.

Critères d'acceptation :

La génération utilise le contexte fourni par le processus de recherche.

Le contexte respecte les limites définies.

Les instructions système distinguent les données sources des instructions.

Le moteur ne présente pas automatiquement les résultats récupérés comme des faits vérifiés.

FR-019 — Gestion des fournisseurs LLM

Priorité : MUST

Le système doit permettre d'utiliser différents fournisseurs de modèles de langage.

Critères d'acceptation :

Plusieurs fournisseurs peuvent être intégrés.

Le cœur du moteur reste indépendant d'un fournisseur particulier.

Le modèle utilisé peut être identifié.

Les erreurs et indisponibilités sont gérées.

FR-020 — Références documentaires

Priorité : MUST

Les réponses doivent pouvoir présenter les sources ayant contribué à leur génération.

Critères d'acceptation :

Chaque référence correspond à une source existante.

Le document d'origine est identifiable.

Le passage utilisé peut être retrouvé.

Une réponse sans source vérifiable ne doit pas être présentée comme une réponse documentée.

FR-021 — Gestion des connaissances insuffisantes

Priorité : MUST

Le système doit pouvoir reconnaître lorsque les informations disponibles ne permettent pas de répondre correctement.

Critères d'acceptation :

Une recherche insuffisante peut être détectée.

Le système peut indiquer que les connaissances disponibles sont insuffisantes.

Il ne doit pas inventer une source.

L'incertitude doit être distinguée d'une information confirmée.

4.7 Données structurées

FR-022 — Connexion aux données structurées

Priorité : MUST

Le moteur doit pouvoir exploiter des sources de données structurées.

Exemples :

Bases relationnelles.

Tables.

Données tabulaires.

API métier.

Critères d'acceptation :

Les sources structurées sont identifiables.

Leur accès respecte les permissions.

Les résultats conservent leur provenance.

Les données ne sont pas obligatoirement converties en documents textuels.

FR-023 — Interrogation contrôlée des données

Priorité : MUST

Le système doit pouvoir interroger les données structurées dans un cadre contrôlé.

Critères d'acceptation :

Les opérations autorisées sont définies.

Les accès non autorisés sont rejetés.

Les requêtes sont limitées par des règles de sécurité.

Les données sensibles ne sont pas exposées à des utilisateurs non autorisés.

FR-024 — Combinaison des connaissances

Priorité : SHOULD

Le moteur devrait pouvoir combiner des résultats documentaires et structurés dans une même réponse.

Critères d'acceptation :

Les résultats provenant des différentes sources restent identifiables.

Les références conservent leur origine.

Les incohérences entre sources peuvent être signalées.

La génération ne masque pas la provenance des informations.

4.8 API et intégration

FR-025 — Interface publique

Priorité : MUST

Le moteur doit exposer des interfaces documentées permettant aux applications clientes d'utiliser ses services.

Critères d'acceptation :

Les fonctionnalités publiques sont accessibles à travers des contrats définis.

Les entrées et sorties sont documentées.

Les erreurs sont normalisées.

Les applications clientes ne dépendent pas des modules internes.

FR-026 — Gestion des requêtes

Priorité : MUST

Le moteur doit pouvoir recevoir, traiter et suivre les requêtes des applications clientes.

Critères d'acceptation :

Chaque requête possède un contexte d'exécution identifiable.

Les permissions sont vérifiées.

Les erreurs sont retournées de manière compréhensible.

Les résultats peuvent être associés à la requête d'origine.

4.9 Administration et supervision

FR-027 — Administration

Priorité : SHOULD

Le moteur doit fournir des moyens de gérer :

Les organisations.

Les applications.

Les utilisateurs.

Les Knowledge Bases.

Les sources.

Les configurations.

Les tâches d'ingestion.

Une interface graphique complète n'est pas obligatoire dans la première version.

FR-028 — Journalisation et supervision

Priorité : MUST

Le système doit permettre de suivre son fonctionnement.

Critères d'acceptation :

Les erreurs sont enregistrées.

Les traitements importants sont traçables.

Les opérations d'administration sont identifiables.

Les indicateurs de fonctionnement sont consultables.

Les informations sensibles ne sont pas exposées dans les journaux.

5. Exigences non fonctionnelles (NFR)

5.1 Sécurité

NFR-001 — Isolation des organisations

Priorité : MUST

Aucune organisation ne doit pouvoir accéder aux données d'une autre organisation sans autorisation explicite.

NFR-002 — Contrôle des accès

Priorité : MUST

Les accès doivent être soumis à des contrôles d'authentification et d'autorisation.

NFR-003 — Protection des données sensibles

Priorité : MUST

Le système doit protéger les informations sensibles contre les accès, modifications et divulgations non autorisés.

NFR-004 — Protection contre les injections

Priorité : MUST

Les documents et contenus externes doivent être considérés comme des données non fiables.

Le moteur doit distinguer le contenu documentaire des instructions de contrôle du système.

NFR-005 — Gestion des secrets

Priorité : MUST

Les identifiants, clés API et secrets ne doivent pas être exposés dans les réponses, journaux ou configurations publiques.

5.2 Fiabilité et intégrité

NFR-006 — Intégrité des connaissances

Priorité : MUST

Les traitements ne doivent pas créer de relations incohérentes entre documents, fragments, index et références.

NFR-007 — Résilience

Priorité : MUST

Les erreurs temporaires doivent être gérées sans provoquer de corruption des connaissances.

NFR-008 — Traçabilité

Priorité : MUST

Les opérations importantes doivent pouvoir être retracées.

NFR-009 — Cohérence après modification

Priorité : MUST

La modification ou la suppression d'une connaissance doit être propagée de façon maîtrisée aux composants concernés.

5.3 Performance et évolutivité

NFR-010 — Performance

Priorité : MUST

Le moteur doit fournir des temps de réponse adaptés à son usage.

Les objectifs chiffrés de latence devront être définis à partir de scénarios de charge et de mesures représentatives.

NFR-011 — Évolutivité

Priorité : MUST

L'architecture doit permettre une augmentation progressive :

Du nombre d'organisations.

Du nombre de bases de connaissances.

Du volume documentaire.

Du nombre de requêtes simultanées.

Du nombre de fournisseurs intégrés.

NFR-012 — Gestion des traitements volumineux

Priorité : SHOULD

Les traitements importants doivent pouvoir être exécutés sans bloquer inutilement les autres opérations.

5.4 Maintenabilité et extensibilité

NFR-013 — Modularité

Priorité : MUST

Les responsabilités doivent être séparées et les interfaces entre composants clairement définies.

NFR-014 — Extensibilité

Priorité : MUST

L'ajout de nouveaux fournisseurs, connecteurs et stratégies ne doit pas imposer une réécriture du cœur.

NFR-015 — Maintenabilité

Priorité : MUST

Le système doit être documenté, testé et organisé afin de faciliter sa maintenance.

NFR-016 — Interopérabilité

Priorité : MUST

Le moteur doit pouvoir être intégré à différentes applications et environnements.

NFR-017 — Portabilité

Priorité : SHOULD

Le déploiement doit pouvoir être adapté à différents environnements sans dépendance métier ou infrastructure inutilement restrictive.

5.5 Observabilité et évaluation

NFR-018 — Observabilité

Priorité : MUST

Le système doit permettre de comprendre son état, ses erreurs, ses traitements et ses performances.

NFR-019 — Évaluation de la qualité

Priorité : MUST

La qualité des résultats de recherche et des réponses générées doit pouvoir être mesurée à l'aide de scénarios de test reproductibles.

NFR-020 — Vérifiabilité

Priorité : MUST

Les exigences fonctionnelles et non fonctionnelles doivent pouvoir être vérifiées par des tests ou des preuves objectives.

6. Exigences relatives à la confidentialité et à la gouvernance des données

Le moteur devra permettre de définir des politiques relatives :

À la conservation des documents.

À la suppression des données.

À la conservation des journaux.

À la gestion des historiques.

À l'accès aux informations sensibles.

Aux transferts vers des fournisseurs externes.

À la localisation des données lorsque cela est requis.

Les obligations réglementaires applicables dépendront des organisations, des juridictions et des usages. Elles devront être étudiées avant chaque déploiement concerné.

7. Exigences de qualité des réponses

Une réponse générée ne devra pas être évaluée uniquement sur sa fluidité linguistique.

Les dimensions suivantes devront être mesurées :

Pertinence des documents récupérés.

Pertinence des passages récupérés.

Fidélité au contexte documentaire.

Exactitude des références.

Capacité à reconnaître l'insuffisance des informations.

Absence de contradiction injustifiée.

Respect des permissions.

Reproductibilité des évaluations.

Les métriques et seuils chiffrés seront définis dans les spécifications de recherche et d'évaluation.

8. Cas d'utilisation de référence

Les cas suivants permettront de vérifier que le moteur répond aux besoins définis.

UC-001 — Assistant documentaire

Une organisation importe des documents dans une Knowledge Base.

Un utilisateur pose une question.

Le moteur retrouve les passages pertinents et retourne une réponse accompagnée des références documentaires.

UC-002 — Plusieurs bases indépendantes

Une organisation possède plusieurs bases de connaissances.

Une application interroge une base précise.

Le moteur ne doit pas retourner des informations issues d'autres bases sans autorisation.

UC-003 — Plusieurs applications clientes

Deux applications utilisent le même moteur.

Elles disposent de permissions et de périmètres de connaissances différents.

Le moteur doit maintenir leur séparation.

UC-004 — Changement de fournisseur d'embeddings

Une organisation souhaite utiliser un autre modèle d'embeddings.

Le moteur doit permettre cette évolution avec une gestion contrôlée des index concernés.

UC-005 — Recherche hybride

Un utilisateur effectue une recherche nécessitant à la fois une correspondance textuelle précise et une compréhension sémantique.

Le moteur combine les résultats.

UC-006 — Informations insuffisantes

Un utilisateur pose une question dont la réponse ne figure pas dans les connaissances accessibles.

Le moteur indique que les informations sont insuffisantes plutôt que d'inventer une réponse documentaire.

UC-007 — Données structurées

Une application demande une information provenant d'une source structurée.

Le moteur vérifie les autorisations, interroge la source dans le cadre autorisé et restitue le résultat avec sa provenance.

UC-008 — Suppression documentaire

Un administrateur supprime un document.

Le moteur doit s'assurer que les informations correspondantes ne sont plus récupérables dans les recherches suivantes.

9. Exclusions de la première version

Les éléments suivants ne sont pas exigés pour la première version fonctionnelle :

Création d'un LLM propriétaire.

Entraînement d'un modèle généraliste.

Application métier complète.

Interface conversationnelle obligatoire.

Agent autonome exécutant des opérations métier.

Automatisation générale des processus d'entreprise.

Prise en charge immédiate de tous les formats documentaires.

Prise en charge immédiate de toutes les bases de données existantes.

Ces possibilités pourront être étudiées ultérieurement.

10. Points à approfondir dans les spécifications suivantes

Les exigences de ce cahier des charges nécessitent des études complémentaires.

Sujet

Document de référence

Organisation et isolation

02, 03, 04, 11

Modèle de données

04

Knowledge Bases

05

Connecteurs et ingestion

06

Chunking et embeddings

07

Recherche hybride et classement

08

Fournisseurs LLM et génération

09

Contrats des interfaces

10

Sécurité et permissions

11

Sources structurées

12

Validation de la qualité

13

Performance et déploiement

14

Les exigences de ce document devront être conservées et reliées aux futures spécifications.

11. Conditions générales de validation

Le cahier des charges sera considéré comme validé lorsque :

Les exigences fonctionnelles seront examinées.

Les exigences non fonctionnelles seront examinées.

Les priorités seront approuvées.

Les critères d'acceptation seront jugés suffisamment vérifiables.

Les ambiguïtés importantes seront résolues ou explicitement reportées.

Les dépendances seront cohérentes avec DEPENDENCY_MAP.md.

Les décisions seront cohérentes avec DECISION_LOG.md.

Le document sera approuvé explicitement.

12. Conclusion

Ce cahier des charges définit les capacités attendues de Universal RAG Engine.

Il constitue la base de travail pour les prochaines spécifications.

Il ne prescrit pas prématurément les technologies, frameworks, bases de données ou fournisseurs.

La conception technique devra démontrer comment chaque exigence pourra être satisfaite.

Principe directeur : définir les besoins, étudier les contraintes, concevoir l'architecture, puis développer.
