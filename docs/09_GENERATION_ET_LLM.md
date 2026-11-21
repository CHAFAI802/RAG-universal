# UNIVERSAL RAG ENGINE

## Document 09 — Génération et LLM

**Version :** 1.0
**Statut :** VALIDATED
**Projet :** RAG-universal

---

# 1. Objectif

Ce document définit le rôle et le périmètre fonctionnel du Generation Engine et son interaction avec les modèles de langage (LLM).

Il précise les modes de génération, les informations pouvant être transmises au modèle, les relations avec les résultats de recherche, les fournisseurs et modèles utilisés, ainsi que les principes de production de réponses traçables.

Cette spécification reste au niveau conceptuel et fonctionnel. Elle ne définit pas les fournisseurs, les modèles particuliers, les formats d'API, les gabarits de prompts, les paramètres numériques ni les mécanismes techniques d'exécution.

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

Les exigences fonctionnelles principalement concernées sont FR-018 à FR-021. Le document contribue également à FR-019, FR-020, FR-024 et FR-026, ainsi qu'aux exigences non fonctionnelles relatives à la sécurité, la fiabilité, la traçabilité, l'interopérabilité et l'évaluation.

# 3. Position dans l'architecture

Le Generation Engine appartient à l'ensemble fonctionnel Knowledge Query.

Il produit une réponse à partir d'une demande et, selon le mode de génération, des informations contextuelles qui lui sont fournies.

Il utilise les capacités des fournisseurs et modèles de langage à travers les frontières d'intégration définies par l'architecture modulaire.

Le Generation Engine ne remplace pas :

- la réception et la validation des requêtes ;
- l'authentification et l'autorisation ;
- le Retrieval Engine ;
- le sous-système Structured Data Access ;
- la sélection et la préparation des connaissances récupérées ;
- la gestion des fournisseurs et de leurs configurations ;
- la gestion des citations et de la provenance.

Il consomme les informations qui lui sont fournies par les composants responsables et ne doit pas contourner leurs responsabilités.

# 4. Responsabilité principale

La responsabilité principale du Generation Engine est de produire une réponse à une Query en utilisant un modèle de langage et les informations autorisées disponibles pour le mode demandé.

Le moteur doit distinguer clairement l'origine informationnelle de la réponse :

- réponse produite directement par un LLM, sans Retrieval dans les Knowledge Bases pour cette Query ;
- réponse produite par un LLM après Retrieval de connaissances autorisées.

La présence d'un LLM dans les deux modes ne signifie pas que leurs réponses ont le même fondement informationnel.

# 5. Modes de traitement

Trois modes généraux doivent rester distincts dans Universal RAG Engine.

## 5.1 Retrieval Only

Ce mode relève du Retrieval Engine et ne déclenche pas de génération LLM.

Il retourne les résultats de recherche avec leur provenance. Il est décrit dans le document 08 et n'est pas une responsabilité du Generation Engine.

## 5.2 Direct LLM Generation

Dans ce mode, le LLM reçoit la demande et les éventuelles instructions ou informations explicitement fournies dans le contexte de la requête, sans qu'un Retrieval dans les Knowledge Bases soit effectué pour cette Query.

La réponse peut s'appuyer sur les connaissances générales du modèle et sur les informations présentes dans son entrée.

La réponse ne doit pas être présentée comme ayant été vérifiée ou fondée sur les Knowledge Bases de Universal RAG Engine.

Ce mode peut être utilisé sans sélectionner de Knowledge Base.

## 5.3 Retrieval-Augmented Generation

Dans ce mode, une opération de Retrieval est effectuée au préalable dans les connaissances autorisées.

Les résultats retenus sont fournis au Generation Engine dans un contexte préparé par les composants responsables de la recherche et de l'orchestration.

Le LLM produit une réponse en tenant compte de ce contexte.

La réponse doit conserver sa relation avec la Query, les résultats récupérés et les sources qui ont effectivement contribué à son contenu.

Le contexte peut contenir des connaissances documentaires, des résultats structurés ou une combinaison des deux.

## 5.4 Distinction des modes

| Mode | Retrieval dans les Knowledge Bases | Génération LLM | Résultat principal |
|---|---|---|---|
| `RETRIEVAL_ONLY` | Oui | Non | Retrieval Results |
| `DIRECT_LLM` | Non, pour cette Query | Oui | Generated Answer non fondée sur un Retrieval des Knowledge Bases |
| `RETRIEVAL_AUGMENTED` | Oui | Oui | Generated Answer liée aux connaissances récupérées et utilisées |

Le mode de traitement doit être identifiable afin que l'application cliente puisse comprendre la nature du résultat reçu.

# 6. Entrées du Generation Engine

Selon le mode demandé, le Generation Engine peut recevoir :

- la Query d'origine ;
- les instructions applicables au traitement ;
- les informations contextuelles fournies explicitement et autorisées ;
- les résultats de Retrieval retenus, pour une génération augmentée ;
- les références de provenance associées aux résultats ;
- les contraintes de réponse applicables ;
- la référence du modèle et la configuration de fournisseur sélectionnées.

Les données d'entrée doivent être distinguées selon leur origine et leur rôle. Les contenus documentaires ou structurés récupérés sont des données à exploiter, et non des instructions de contrôle du moteur.

Le Generation Engine ne doit pas accepter comme autorisation une instruction contenue dans un document ou un résultat externe.

# 7. Contexte de génération

Pour une génération augmentée, les informations récupérées doivent être préparées et transmises dans un contexte cohérent.

La préparation et la sélection de ce contexte relèvent des responsabilités d'orchestration et de Context Assembly définies dans l'architecture modulaire.

Le Generation Engine consomme ce contexte ; il ne doit pas refaire la recherche ni accéder directement aux sources documentaires ou structurées pour compléter lui-même les résultats.

Le contexte transmis doit préserver les références de provenance permettant de relier les informations à leurs sources.

Le concept de contexte de génération ne rend pas obligatoire une entité persistante supplémentaire dans le modèle de données. Sa représentation et son éventuelle conservation seront décidées dans les spécifications spécialisées.

# 8. Fournisseurs et modèles de langage

Le Generation Engine doit rester indépendant d'un fournisseur particulier.

Il utilise les concepts déjà définis dans le modèle de données :

- `Provider` : fournisseur ou environnement exposant une capacité externe ;
- `Model Reference` : identification d'un modèle précis ;
- `Provider Configuration` : configuration par laquelle le moteur utilise un fournisseur et, lorsque nécessaire, un modèle particulier.

Un fournisseur peut proposer plusieurs modèles. Le modèle sélectionné doit être identifiable pour chaque génération.

Le moteur ne doit pas confondre le fournisseur, le modèle et la configuration d'utilisation.

Les capacités et limites du modèle retenu doivent être prises en compte dans le choix et l'exécution du traitement.

# 9. Indépendance et interchangeabilité des LLM

Le remplacement d'un fournisseur ou d'un modèle ne doit pas imposer de modifier les responsabilités métier du Generation Engine ni celles des applications clientes.

Les différences de capacités, de formats d'entrée et de sortie et de limites entre modèles doivent être prises en charge à la frontière d'intégration.

L'interchangeabilité ne signifie pas que deux modèles produisent des réponses identiques ou possèdent les mêmes capacités.

Les conséquences d'un changement de modèle sur la qualité, le comportement, les coûts et la compatibilité doivent pouvoir être évaluées.

# 10. Production de la réponse

Le Generation Engine produit une `Generated Answer` associée à la Query d'origine.

Selon le mode de génération, la réponse peut être :

- une réponse directe issue du LLM ;
- une réponse augmentée par les informations récupérées.

La réponse doit pouvoir être distinguée des Retrieval Results qui l'ont éventuellement précédée.

Les informations relatives au mode de génération et au modèle utilisé doivent être disponibles pour assurer la compréhension et la traçabilité du résultat.

Le format de réponse détaillé et les métadonnées exposées aux applications clientes seront définis dans la spécification API.

# 11. Fidélité aux connaissances récupérées

Pour une génération augmentée, le Generation Engine doit être conçu pour produire une réponse fondée sur les informations qui lui ont été fournies.

Les informations récupérées ne doivent pas être présentées comme établissant davantage que ce qu'elles permettent réellement d'affirmer.

Le moteur doit distinguer :

- les informations explicitement présentes dans le contexte ;
- les déductions raisonnablement tirées de ces informations ;
- les informations qui ne sont pas établies par le contexte disponible.

Le recours à un LLM ne garantit pas à lui seul l'exactitude de la réponse. La fidélité et la qualité doivent être évaluées par les mécanismes de test et d'évaluation.

# 12. Gestion des connaissances insuffisantes

Lorsque les résultats récupérés ne permettent pas de répondre suffisamment à la Query, la génération augmentée doit pouvoir signaler cette insuffisance.

Le Generation Engine ne doit pas inventer de références ni prétendre qu'une information provient des Knowledge Bases lorsqu'elle n'est pas établie par les éléments fournis.

La décision de répondre, de limiter la réponse ou de signaler l'insuffisance doit tenir compte du mode demandé et des règles de génération applicables.

L'absence ou l'insuffisance de résultats ne nécessite pas, à elle seule, une nouvelle entité dans le modèle de données : elle peut être représentée par l'état ou le résultat de la Query et de la Generated Answer.

Pour le mode Direct LLM Generation, le moteur doit éviter de présenter une réponse générale du modèle comme une réponse vérifiée par les connaissances du moteur.

# 13. Citations et provenance

Une réponse augmentée doit pouvoir être reliée aux sources qui ont effectivement contribué à sa production.

Le Generation Engine doit préserver les références de provenance reçues avec le contexte.

La gestion des citations relève de la responsabilité de Citation and Provenance, en collaboration avec le processus de génération.

Les principes suivants s'appliquent :

- une citation doit pointer vers une source identifiable ;
- une citation documentaire doit permettre de retrouver la version et le passage pertinent ;
- une citation structurée doit permettre d'identifier la source et la ressource concernées ;
- un résultat récupéré mais non utilisé dans la réponse ne doit pas être automatiquement présenté comme une citation ;
- une réponse `DIRECT_LLM` ne doit pas recevoir artificiellement des citations provenant des Knowledge Bases ;
- la présence d'une citation ne constitue pas, à elle seule, une preuve que la réponse l'interprète correctement.

Les règles détaillées de vérification des citations seront définies dans les spécifications d'évaluation et d'API.

# 14. Données documentaires et structurées dans la génération

Le Generation Engine peut recevoir un contexte combinant :

- des passages documentaires issus du Retrieval Engine ;
- des résultats issus du Structured Data Access ;
- les références de provenance associées à chaque élément.

Les deux catégories doivent rester distinguables dans le contexte et dans les références de la réponse.

Le Generation Engine ne doit pas transformer une donnée structurée en fait documentaire ni masquer son origine.

Il ne doit pas interroger directement une base externe ni contourner les contrôles appliqués par Structured Data Access.

# 15. Sécurité et traitement des contenus non fiables

Les documents, contenus web, résultats structurés et autres informations externes transmis au modèle doivent être considérés comme des données potentiellement non fiables.

Le Generation Engine doit préserver la séparation entre :

- les instructions de contrôle du moteur ;
- les instructions et contraintes validées de l'application ;
- la question de l'utilisateur ;
- les contenus et résultats récupérés.

Un contenu récupéré ne doit pas pouvoir modifier les règles de sécurité, élargir les permissions, révéler des secrets ou déclencher une opération non autorisée.

Les contrôles d'identité, d'autorisation et d'isolation restent assurés par les composants responsables. Le LLM ne constitue pas une frontière de sécurité.

# 16. Erreurs et indisponibilité des fournisseurs

Le processus de génération doit pouvoir reconnaître et signaler les situations dans lesquelles une réponse ne peut pas être produite correctement.

Les situations concernées comprennent notamment :

- indisponibilité du fournisseur ;
- modèle non disponible ou capacité non prise en charge ;
- entrée incompatible avec le modèle ;
- dépassement d'une limite applicable ;
- réponse incomplète ou inexploitable ;
- échec de génération.

Une erreur de génération ne doit pas être présentée comme une réponse réussie.

Les règles détaillées de reprise, de temporisation et de gestion des tentatives relèvent des spécifications d'exécution et de déploiement.

# 17. Traçabilité et conservation

Pour chaque génération, le moteur doit pouvoir identifier, selon les politiques de conservation applicables :

- la Query d'origine ;
- le mode de génération ;
- le Provider et le Model Reference utilisés ;
- la Provider Configuration pertinente, lorsque nécessaire ;
- les Retrieval Results utilisés pour une génération augmentée ;
- les citations associées à la réponse ;
- l'état ou le résultat de la génération.

La conservation du texte complet des entrées et des réponses n'est pas imposée par cette spécification. Elle doit respecter les politiques de confidentialité, de rétention et les exigences applicables à chaque déploiement.

# 18. Relations avec les autres composants

| Composant | Relation avec le Generation Engine |
|---|---|
| Public API et Access Layer | Transmettent la demande et le contexte d'accès vérifié, puis exposent le résultat selon les contrats publics |
| Query Orchestration | Détermine le mode de traitement et coordonne le parcours de la Query |
| Retrieval Engine | Fournit les résultats de recherche pour une génération augmentée |
| Structured Data Access | Fournit les résultats structurés autorisés pouvant contribuer au contexte |
| Context Assembly | Prépare les informations retenues et leurs références pour la génération |
| Provider / Model Integration | Donne accès aux capacités du fournisseur et du modèle sélectionnés |
| Citation and Provenance | Relie la réponse aux sources effectivement utilisées |
| Audit and Observability | Permettent de suivre les opérations et les erreurs selon les règles applicables |
| Evaluation | Mesure la qualité, la fidélité et le comportement des réponses |

# 19. Couverture des exigences

## 19.1 Exigences fonctionnelles principalement couvertes

| Exigence | Besoin | Couverture conceptuelle |
|---|---|---|
| FR-018 | Génération à partir des connaissances récupérées | Définit la génération augmentée, ses entrées et sa relation avec Retrieval |
| FR-019 | Gestion des fournisseurs LLM | Distingue Provider, Model Reference et Provider Configuration |
| FR-020 | Références documentaires | Définit la provenance et les citations des réponses augmentées |
| FR-021 | Gestion des connaissances insuffisantes | Définit le signalement des limites du contexte disponible |
| FR-024 | Combinaison des connaissances | Permet la génération à partir de résultats documentaires et structurés |
| FR-026 | Gestion des requêtes | Associe la réponse à la Query et à son contexte d'exécution |

Cette couverture décrit la contribution du Generation Engine. Elle ne remplace pas les spécifications spécialisées du Retrieval Engine, de l'API, de la sécurité et de l'évaluation.

## 19.2 Exigences non fonctionnelles concernées

Le Generation Engine contribue notamment aux exigences suivantes :

- **NFR-001 à NFR-005 :** isolation, contrôle d'accès, protection des données, contenus non fiables et secrets ;
- **NFR-006 à NFR-009 :** intégrité, résilience, traçabilité et cohérence ;
- **NFR-010 à NFR-012 :** performance et évolutivité ;
- **NFR-013 à NFR-017 :** modularité, extensibilité, maintenabilité et interopérabilité ;
- **NFR-018 à NFR-020 :** observabilité, évaluation et vérifiabilité.

Les objectifs mesurables et leurs méthodes de vérification seront définis dans les spécifications de tests, d'évaluation et de déploiement.

# 20. Éléments reportés

Les sujets suivants ne sont pas définis dans cette spécification :

- les fournisseurs et modèles particuliers à sélectionner ;
- les gabarits et stratégies détaillées de prompts ;
- les formats techniques des messages transmis aux modèles ;
- les paramètres numériques de génération ;
- les règles détaillées de sélection ou de routage des modèles ;
- les mécanismes techniques de streaming ;
- les contrats API détaillés ;
- les politiques précises de conservation des entrées et réponses ;
- les métriques et seuils d'évaluation ;
- les mécanismes techniques de reprise et de limitation des appels.

Ces sujets seront traités dans les spécifications spécialisées et les décisions techniques ultérieures.

# 21. Conditions de validation

Le document pourra être validé lorsque :

1. Le rôle et les limites du Generation Engine seront approuvés.
2. Les modes `DIRECT_LLM` et `RETRIEVAL_AUGMENTED` seront clairement distingués.
3. Le mode `RETRIEVAL_ONLY` restera distinct de la génération.
4. La relation entre Query, Retrieval Results et Generated Answer sera cohérente avec le document 04.
5. La distinction entre Provider, Model Reference et Provider Configuration sera respectée.
6. Les réponses augmentées conserveront leur provenance.
7. Les résultats documentaires et structurés resteront distinguables.
8. La génération ne contournera pas les mécanismes de sécurité et d'autorisation.
9. La gestion des connaissances insuffisantes sera définie au niveau fonctionnel.
10. Les exigences concernées du cahier des charges seront couvertes.
11. Les détails techniques prématurés seront évités.
12. La cohérence avec les documents 00 à 08 sera vérifiée.

# 22. Conclusion

Le Generation Engine produit des réponses à partir d'un modèle de langage, dans un mode direct ou augmenté par les connaissances récupérées.

Il reste indépendant du Retrieval Engine, des sources documentaires, des sources structurées et des fournisseurs particuliers. Il exploite les résultats et les contextes préparés par les composants responsables, tout en préservant les informations nécessaires à la traçabilité.

Une réponse directe par LLM et une réponse générée après Retrieval doivent rester clairement distinguables afin que les applications clientes puissent comprendre le fondement informationnel du résultat.

**Le Generation Engine produit la réponse ; le Retrieval Engine retrouve les connaissances ; la provenance permet de comprendre sur quelles informations la réponse s'appuie.**
