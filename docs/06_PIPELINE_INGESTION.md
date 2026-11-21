# UNIVERSAL RAG ENGINE

## Document 06 — Pipeline d'ingestion

**Version :** 1.0
**Statut :** VALIDATED
**Projet :** RAG-universal

---

# 1. Objectif

Ce document définit le rôle, le périmètre et le fonctionnement conceptuel du pipeline d'ingestion de Universal RAG Engine.

Il décrit comment les connaissances provenant de sources documentaires sont identifiées, sélectionnées, acquises, représentées, préparées et rendues disponibles dans les Knowledge Bases autorisées.

Il précise notamment :

- La place du pipeline dans l'architecture globale.
- Les relations entre sources, Knowledge Bases et Knowledge Items.
- Les grandes étapes du parcours documentaire.
- La distinction entre document, version, artefact original et contenu extrait.
- La préparation des contenus en vue de leur découpage, de leur vectorisation et de leur indexation.
- La gestion conceptuelle des changements, des suppressions et des erreurs.
- La traçabilité de l'origine des connaissances.
- La séparation entre ingestion documentaire et accès aux données structurées.

Ce document reste au niveau fonctionnel et conceptuel. Il ne définit pas les technologies, les protocoles, les algorithmes, les structures physiques ou les mécanismes détaillés d'exécution.

# 2. Références et dépendances

Cette spécification s'appuie sur les documents suivants :

- `00_VISION_ET_OBJECTIFS.md` — vision, indépendance métier et principes fondateurs.
- `DEPENDENCY_MAP.md` — dépendances entre les spécifications.
- `DECISION_LOG.md` — décisions fondatrices validées.
- `01_CAHIER_DES_CHARGES.md` — exigences fonctionnelles et non fonctionnelles.
- `02_ARCHITECTURE_GLOBALE.md` — organisation générale du moteur.
- `03_ARCHITECTURE_MODULAIRE.md` — responsabilités des modules.
- `04_MODELE_DE_DONNEES.md` — entités et relations conceptuelles.
- `05_KNOWLEDGE_BASES.md` — gestion des bases, sources et associations.

Les concepts de référence utilisés ici comprennent notamment :

- Organization.
- Knowledge Base et Knowledge Base Configuration.
- Knowledge Source, Source Connection et Knowledge Base Source Association.
- Knowledge Item et Knowledge Base Item Association.
- Document, Document Version, Original Artifact et Extracted Content.
- Chunk Set, Chunk et Embedding.
- Provider et Model Reference.
- Index, Index Configuration, Index Generation et Index Entry.
- Job et Audit Event.

# 3. Position du pipeline dans le moteur

Le pipeline d'ingestion appartient à l'ensemble **Knowledge Lifecycle** défini dans l'architecture modulaire.

Sa responsabilité est de coordonner la préparation des connaissances documentaires. Il ne possède pas les règles métier des modules spécialisés et ne remplace pas les capacités de recherche ou de génération.

Il travaille notamment avec :

- Source Management et Source Connectors pour accéder aux sources.
- Knowledge Base Management pour connaître le périmètre de destination.
- Document Management pour l'identité des documents et de leurs versions.
- Extraction et Normalization pour produire des contenus exploitables.
- Chunking et Embedding pour préparer les représentations de recherche.
- Index Management pour rendre les connaissances indexables et disponibles.
- Job Management, Audit et Observability pour le suivi transversal.

Le pipeline coordonne ces capacités ; il ne doit pas absorber leurs responsabilités propres.

# 4. Périmètre

## 4.1 Dans le périmètre

Le pipeline documentaire couvre les étapes conceptuelles suivantes :

1. Déclenchement d'une opération d'ingestion.
2. Vérification du contexte, de la source et de la Knowledge Base ciblées.
3. Accès à la source au moyen d'une Source Connection autorisée.
4. Découverte des éléments documentaires disponibles.
5. Sélection des éléments destinés à une Knowledge Base.
6. Identification ou création du Document correspondant.
7. Acquisition et rattachement de l'Original Artifact à une Document Version.
8. Extraction et normalisation du contenu.
9. Préparation des contenus pour le découpage.
10. Coordination avec les capacités de Chunking, Embedding et Index Management.
11. Vérification de la disponibilité des connaissances dans la Knowledge Base.
12. Suivi des changements, réimportations, erreurs et suppressions relevant du cycle documentaire.

## 4.2 Hors du périmètre détaillé

Ce document ne définit pas :

- Les stratégies détaillées de connexion à chaque fournisseur ou source.
- Les formats et algorithmes d'extraction spécialisés.
- Les stratégies et paramètres de chunking.
- Les modèles, dimensions et stratégies de calcul des embeddings.
- Les structures et algorithmes d'indexation.
- Les mécanismes de recherche et de classement.
- Les contrats API détaillés.
- Les mécanismes physiques de traitement asynchrone.
- Les règles détaillées d'authentification, d'autorisation et de gestion des secrets.
- Les mécanismes détaillés d'accès et d'interrogation des données structurées.

Ces sujets relèvent des spécifications spécialisées.

# 5. Principes fondamentaux du pipeline

## 5.1 Séparation entre source et connaissance intégrée

Une Knowledge Source représente une origine d'informations. Son association à une Knowledge Base ne signifie pas que tous les éléments exposés par cette source sont automatiquement intégrés à cette base.

La sélection et la mise à disposition d'un élément précis sont représentées par la Knowledge Base Item Association.

## 5.2 Séparation entre source et connexion

La Knowledge Source identifie l'origine. Source Connection représente une modalité configurée permettant d'y accéder.

Le pipeline utilise une connexion autorisée sans confondre les informations de connexion avec l'identité de la source.

## 5.3 Respect du périmètre de la Knowledge Base

Chaque opération d'ingestion est rattachée à une Knowledge Base de destination et à un contexte d'autorisation vérifié.

La réutilisation d'une source dans plusieurs bases ne fusionne ni leurs contenus, ni leurs configurations, ni leurs permissions.

## 5.4 Préservation de l'identité documentaire

Document représente l'identité logique durable d'un élément documentaire. Document Version représente un état précis de son contenu. Une nouvelle version ne remplace pas l'identité du document.

## 5.5 Préservation de l'original

Original Artifact et Extracted Content sont des concepts distincts. Le contenu extrait ne remplace pas l'artefact original et doit rester relié à la Document Version dont il provient.

## 5.6 Séparation des représentations

Document, Document Version, Extracted Content, Chunk Set, Chunk, Embedding et Index Entry représentent des éléments distincts du parcours de préparation et d'indexation.

Le pipeline ne doit pas confondre ces représentations.

## 5.7 Disponibilité contrôlée

Une connaissance ne doit pas être présentée comme disponible pour la recherche tant que les conditions de préparation et d'indexation requises pour la capacité concernée ne sont pas satisfaites.

## 5.8 Traçabilité de bout en bout

Toute représentation préparée doit conserver une relation permettant de remonter à son origine documentaire et à la Knowledge Base dans laquelle elle est utilisée.

# 6. Entrées et résultats du pipeline

## 6.1 Entrées conceptuelles

Une opération d'ingestion documentaire s'appuie notamment sur :

- Une Knowledge Source enregistrée.
- Une Source Connection autorisée.
- Une Knowledge Base de destination.
- Une Knowledge Base Source Association valide lorsque l'ingestion provient d'une source associée à la base.
- Un ou plusieurs éléments documentaires sélectionnés.
- Les configurations fonctionnelles applicables.
- Un contexte d'identité, d'organisation et d'autorisation vérifié.

Une ingestion directe, par exemple un dépôt de fichier, doit également être représentée comme provenant d'une origine identifiable conformément au modèle de sources.

## 6.2 Résultats conceptuels

Selon le parcours et les capacités demandées, le pipeline contribue à produire ou à mettre à jour :

- Un Document et sa Document Version.
- Un ou plusieurs Original Artifacts associés à cette version.
- Un ou plusieurs Extracted Contents.
- Un ou plusieurs Chunk Sets et leurs Chunks.
- Les Embeddings requis.
- Les Index Entries et les générations d'index concernées.
- Une Knowledge Base Item Association représentant la mise à disposition de l'élément dans la base.
- Les informations de suivi et de traçabilité nécessaires.

Le pipeline ne crée pas nécessairement une nouvelle entité à chaque exécution : il doit distinguer une nouvelle opération de traitement d'une nouvelle identité documentaire ou d'une nouvelle version.

# 7. Parcours conceptuel d'ingestion documentaire

Le pipeline est organisé en étapes fonctionnelles. Cet ordre représente le parcours logique général ; il ne prescrit pas une séquence technique détaillée ni un mode d'exécution particulier.

## 7.1 Déclenchement et cadrage

Une opération d'ingestion peut être déclenchée par une application autorisée, un administrateur, une action de synchronisation ou un autre mécanisme de gestion de source.

Le moteur identifie :

- L'organisation concernée.
- La Knowledge Base de destination.
- La source et la connexion concernées, le cas échéant.
- L'acteur ou l'identité applicative à l'origine de l'opération.
- Les éléments demandés ou la portée de découverte.

Une opération ne doit pas être exécutée dans une Knowledge Base simplement parce qu'une source est connue du moteur. L'association et les autorisations applicables doivent être vérifiées.

## 7.2 Accès à la source

Le pipeline demande au connecteur approprié d'accéder à la Knowledge Source au moyen d'une Source Connection autorisée.

Cette étape permet de vérifier que la source est accessible et que les informations nécessaires à son exploitation sont disponibles.

Les erreurs d'accès doivent être identifiables et ne doivent pas être confondues avec des erreurs d'extraction ou de traitement documentaire.

## 7.3 Découverte et sélection des éléments

La source peut exposer un ou plusieurs éléments documentaires.

Le pipeline doit distinguer :

- Les éléments découverts dans la source.
- Les éléments sélectionnés pour une Knowledge Base.
- Les éléments déjà associés à cette base.
- Les éléments nouveaux ou ayant évolué depuis leur dernière prise en compte.

La sélection peut être explicite ou découler des règles d'utilisation définies pour la source et la Knowledge Base.

La découverte d'un document ne signifie pas automatiquement son intégration dans une Knowledge Base.

## 7.4 Identification du document

Pour chaque élément documentaire sélectionné, le moteur doit déterminer s'il correspond à un Document déjà connu ou s'il s'agit d'un nouvel élément documentaire.

L'identification doit préserver la distinction entre :

- L'origine dans la source.
- L'identité logique du Document.
- La version précise du contenu.

Une nouvelle acquisition ne doit pas créer sans contrôle des Documents ou des versions en double.

Les critères précis d'identification, de détection des doublons et de changement de contenu seront définis dans les spécifications détaillées.

## 7.5 Acquisition et rattachement de l'original

Le contenu original est acquis ou référencé selon la nature de la source.

Il est représenté par un Original Artifact associé à la Document Version concernée.

Le moteur doit préserver l'origine et l'intégrité logique de l'artefact. Les règles de conservation, de stockage et de vérification technique ne sont pas définies dans ce document.

## 7.6 Versionnement documentaire

Lorsqu'un Document nouveau ou modifié est reconnu, le modèle doit permettre de créer ou d'identifier la Document Version correspondante.

Une version représente un état précis du contenu. Les versions antérieures restent distinguables conformément aux politiques de conservation.

Le pipeline doit éviter de confondre :

- La répétition d'une acquisition d'un contenu inchangé.
- La modification d'un document existant.
- La création d'un nouveau document.

La méthode de comparaison et les règles exactes de versionnement sont reportées aux spécifications spécialisées.

## 7.7 Extraction du contenu

Le contenu exploitable est extrait à partir de la Document Version et de son ou ses Original Artifacts.

Le résultat est représenté par un ou plusieurs Extracted Contents reliés à cette version.

L'extraction peut préserver les éléments de structure utiles à la compréhension et à la traçabilité du contenu, selon les capacités du format et du traitement applicable.

Un échec d'extraction doit être identifiable et ne doit pas transformer un contenu incomplet en connaissance prête à la recherche.

## 7.8 Normalisation

Les contenus extraits sont préparés sous une forme cohérente pour les étapes suivantes.

La normalisation doit préserver les informations nécessaires à l'interprétation et à la provenance. Elle ne doit pas supprimer silencieusement des informations qui seraient nécessaires à l'exploitation du document.

Les règles de nettoyage, de préservation de structure et de normalisation propres aux formats seront définies dans les spécifications d'extraction et de préparation.

## 7.9 Préparation des représentations de recherche

Les Extracted Contents prêts pour la préparation sont transmis aux capacités concernées :

- Chunking pour produire les Chunk Sets et les Chunks.
- Embedding pour produire les représentations vectorielles compatibles.

Le pipeline coordonne ces capacités sans définir leurs stratégies internes.

Les règles de découpage et de production des embeddings relèvent du document 07 — Chunking et embeddings.

## 7.10 Indexation

Les représentations préparées sont transmises à Index Management afin d'être prises en compte dans les index concernés par la Knowledge Base.

Les Index Entries et Index Generations permettent de représenter les éléments inclus dans une génération d'index déterminée.

Le pipeline vérifie le résultat fonctionnel de cette étape, mais ne définit pas les structures, stratégies de construction ou mécanismes de remplacement des générations.

Ces sujets relèvent du document 08 — Moteur de recherche et indexation.

## 7.11 Mise à disposition dans la Knowledge Base

La Knowledge Base Item Association représente l'intégration ou la mise à disposition du Knowledge Item dans la base.

Le pipeline doit distinguer l'existence de cette association, l'état de préparation de la connaissance et sa disponibilité effective pour une capacité de recherche donnée.

Un élément incomplet, en échec ou non indexé pour la capacité demandée ne doit pas être présenté comme pleinement disponible pour cette capacité.

La disponibilité doit respecter le périmètre d'accès de la Knowledge Base et les autorisations applicables.

# 8. Association d'une source et intégration d'un élément

Le pipeline applique la distinction validée dans les documents 04 et 05.

| Concept | Signification pour l'ingestion |
|---|---|
| Knowledge Base Source Association | La source est associée à la Knowledge Base et peut être exploitée selon les autorisations et paramètres applicables. |
| Knowledge Base Item Association | Un élément précis est intégré ou mis à disposition dans la Knowledge Base. |

Conséquences :

1. Associer une source ne signifie pas importer automatiquement tous ses documents.
2. Sélectionner un document pour une base ne duplique pas automatiquement son identité logique.
3. Un même Document peut être associé à plusieurs Knowledge Bases selon les règles de propriété et d'autorisation.
4. Chaque association avec une Knowledge Base conserve son propre contexte d'utilisation.
5. Le retrait d'une association dans une base ne supprime pas automatiquement la source ou le Document utilisé ailleurs.

# 9. Synchronisation et évolution des sources

Une source peut évoluer après une première ingestion. Le pipeline doit permettre de prendre en compte les nouveaux éléments, les modifications et les suppressions détectés dans la source.

## 9.1 Nouveaux éléments

Un élément nouvellement découvert peut être identifié, sélectionné et intégré selon le parcours d'ingestion.

## 9.2 Éléments modifiés

Lorsqu'un document existant a changé, son identité logique doit être préservée et une nouvelle Document Version peut être créée conformément aux règles de versionnement.

Les représentations dérivées liées à la version précédente doivent rester distinguables des représentations issues de la nouvelle version.

## 9.3 Éléments inchangés

Une synchronisation répétée d'un élément inchangé ne doit pas provoquer de duplication incontrôlée des documents, versions ou représentations.

Les critères permettant de conclure qu'un élément est inchangé seront définis ultérieurement.

## 9.4 Éléments supprimés ou disparus de la source

La disparition d'un élément de la source doit être distinguée d'une demande de suppression de l'identité documentaire ou de l'élément dans le moteur.

Le moteur doit appliquer les règles de cycle de vie et de conservation définies pour la Knowledge Base et la source. Une disparition à la source ne doit pas provoquer une suppression globale non autorisée d'un élément encore utilisé ailleurs.

Les politiques précises de synchronisation et de suppression seront définies dans les spécifications spécialisées.

# 10. Réutilisation d'une source dans plusieurs Knowledge Bases

Une même Knowledge Source peut être associée à plusieurs Knowledge Bases.

Le pipeline doit préserver les distinctions suivantes :

- Une source possède une identité propre.
- Chaque Knowledge Base Source Association décrit son utilisation dans une base.
- Chaque Knowledge Base Item Association décrit les éléments effectivement mis à disposition dans cette base.
- Chaque Knowledge Base conserve ses propres configurations et permissions.

La réutilisation d'une source ne signifie pas que toutes les bases sélectionnent les mêmes documents ni qu'elles partagent automatiquement les mêmes états de disponibilité.

Le partage entre organisations différentes demeure soumis aux autorisations explicites prévues par le modèle de gouvernance.

# 11. Sources structurées : frontière avec l'ingestion documentaire

Les Structured Sources et Structured Resources font partie du modèle global des connaissances, mais elles ne doivent pas être forcées dans le parcours documentaire décrit aux sections précédentes.

Leur parcours conceptuel est distinct :

```text
STRUCTURED SOURCE
       |
       v
SOURCE CONNECTION
       |
       v
DISCOVERY / IDENTIFICATION
       |
       v
STRUCTURED RESOURCES
       |
       v
KNOWLEDGE BASE ITEM ASSOCIATION
       |
       v
STRUCTURED DATA ACCESS
```

Ce parcours concerne l'identification et la mise à disposition contrôlée des ressources structurées.

Une Structured Resource n'est pas automatiquement convertie en Document, Extracted Content, Chunk ou Embedding. Une éventuelle représentation dérivée destinée à une capacité particulière nécessitera une décision et une spécification appropriées.

La découverte, la description, l'autorisation et l'interrogation des ressources structurées relèvent principalement du document 12 — Données structurées.

# 12. Échecs, reprise et intégrité

Le pipeline doit permettre d'identifier les erreurs survenues pendant les différentes étapes : accès à la source, acquisition, extraction, normalisation, préparation, embeddings ou indexation.

Les principes suivants s'appliquent :

1. Une erreur doit être rattachable à l'étape concernée et à l'élément affecté.
2. Un échec partiel ne doit pas être présenté comme une ingestion entièrement réussie.
3. Les opérations susceptibles d'être reprises doivent pouvoir l'être sans duplication incontrôlée des connaissances.
4. Une représentation incomplète ou invalide ne doit pas être activée comme connaissance disponible.
5. Une erreur sur un élément ne doit pas nécessairement empêcher le traitement d'autres éléments indépendants ; le résultat global doit rendre les éléments en échec identifiables.
6. Les opérations doivent respecter l'intégrité des relations entre Document, Document Version, Original Artifact, Extracted Content, Chunk Set, Chunk, Embedding et Index Entry.
7. Les traitements interrompus ou répétés ne doivent pas réintroduire des données obsolètes ou supprimées.

Les garanties précises de reprise, de répétition sûre, de cohérence et de concurrence seront définies dans les spécifications techniques correspondantes.

# 13. Suppression et retrait des connaissances

Le pipeline doit distinguer plusieurs opérations qui n'ont pas les mêmes conséquences :

- Retirer une Knowledge Base Source Association.
- Retirer une Knowledge Base Item Association.
- Retirer un document d'une source.
- Supprimer une Document Version selon les règles de conservation.
- Supprimer le Document et ses représentations dérivées.

Le retrait d'une source ou d'un élément d'une Knowledge Base ne doit pas supprimer automatiquement un Document ou un Original Artifact qui reste utilisé dans une autre base ou soumis à une obligation de conservation.

Lorsqu'une suppression est autorisée, les représentations dérivées et les références d'index concernées doivent être prises en compte. La suppression ne doit pas être déclarée achevée si des représentations accessibles continuent d'exposer le contenu supprimé.

Les règles de conservation, de suppression définitive, de sauvegarde et d'audit relèvent notamment des documents 11 et 14.

# 14. Sécurité et isolation pendant l'ingestion

Toutes les opérations d'ingestion sont soumises aux règles de gouvernance et de sécurité.

Les principes suivants s'appliquent :

1. L'identité de l'acteur et le contexte organisationnel doivent être établis et vérifiés.
2. L'accès à la Knowledge Source et à la Source Connection doit être autorisé.
3. La Knowledge Base de destination doit appartenir au périmètre autorisé ou faire l'objet d'un accès explicite.
4. Les éléments sélectionnés ne doivent être rendus disponibles que dans les Knowledge Bases autorisées.
5. Les données d'une organisation ne doivent pas être exposées à une autre organisation par l'intermédiaire d'une ingestion ou d'une association.
6. Les documents et contenus externes sont considérés comme des données non fiables ; leur contenu ne doit pas être interprété comme une instruction de contrôle du moteur.
7. Les informations sensibles des connexions et fournisseurs ne doivent pas être exposées dans les résultats ou les journaux.

Les mécanismes d'authentification, d'autorisation, de gestion des secrets et de défense contre les contenus malveillants sont détaillés dans le document 11 — Sécurité et isolation.

# 15. Traçabilité et suivi

Le pipeline doit permettre de relier les étapes de préparation aux éléments concernés.

La traçabilité conceptuelle doit permettre de retrouver :

- La Knowledge Source et la Source Connection utilisées.
- La Knowledge Base de destination.
- La Knowledge Base Source Association et la Knowledge Base Item Association concernées.
- Le Document et la Document Version traités.
- Le ou les Original Artifacts acquis ou référencés.
- Les Extracted Contents produits.
- Les Chunk Sets et Chunks issus de la préparation.
- Les Embeddings et Model References utilisés, lorsque cela s'applique.
- Les Index, Index Generations et Index Entries concernés.
- Le Job associé à l'opération et les événements d'audit pertinents.

Cette traçabilité ne signifie pas que chaque étape doit obligatoirement devenir une entité autonome. Le modèle de données validé détermine les entités ; les spécifications détaillées préciseront les informations de suivi nécessaires.

# 16. Responsabilités et frontières avec les autres modules

| Capacité | Responsabilité dans le pipeline |
|---|---|
| Source Management | Gérer l'identité et la configuration des sources. |
| Source Connectors | Accéder aux sources et récupérer les éléments exposés. |
| Knowledge Base Management | Fournir le contexte de destination et les associations autorisées. |
| Document Management | Gérer l'identité des documents et de leurs versions. |
| Ingestion Orchestration | Coordonner le parcours d'ingestion. |
| Extraction | Produire les contenus extraits à partir des versions documentaires. |
| Normalization | Préparer les contenus extraits pour les étapes suivantes. |
| Chunking | Produire les Chunk Sets et Chunks. |
| Embedding | Produire les représentations vectorielles compatibles. |
| Index Management | Prendre en compte les représentations dans les index et générations concernés. |
| Job Management | Suivre les opérations d'ingestion et leur état général. |
| Audit et Observability | Conserver les événements pertinents et rendre le fonctionnement observable. |

L'Ingestion Orchestration coordonne ces responsabilités sans devenir propriétaire des règles internes de chaque module.

# 17. Couverture des exigences

## 17.1 Exigences fonctionnelles principalement couvertes

| Exigence | Besoin | Contribution de cette spécification |
|---|---|---|
| FR-007 | Gestion des sources | Décrit l'accès aux sources, les connexions et leur utilisation dans une Knowledge Base. |
| FR-008 | Importation documentaire | Décrit la découverte, la sélection, l'acquisition et l'enregistrement des documents. |
| FR-009 | Extraction et normalisation | Décrit la production des contenus extraits et leur préparation. |
| FR-010 | Cycle de vie documentaire | Décrit les modifications, nouvelles versions, synchronisations et suppressions. |
| FR-011 | Découpage documentaire | Définit la place du Chunking dans le pipeline et sa relation avec le contenu extrait. |
| FR-012 | Gestion des embeddings | Définit la coordination avec Embedding et la conservation du lien avec les modèles utilisés. |
| FR-013 | Indexation et réindexation | Décrit le passage vers Index Management et la disponibilité des générations. |
| FR-028 | Journalisation et supervision | Définit les besoins de traçabilité et de suivi des opérations. |

Les FR-014 à FR-017 relèvent principalement du document 08. Les FR-022 à FR-024 relèvent principalement du document 12. Cette spécification définit leurs frontières avec l'ingestion documentaire sans les remplacer.

## 17.2 Exigences non fonctionnelles concernées

| Exigence | Besoin | Contribution de cette spécification |
|---|---|---|
| NFR-001 à NFR-005 | Sécurité | Contexte d'accès, isolation, traitement des contenus non fiables et protection des informations sensibles. |
| NFR-006 | Intégrité des connaissances | Préservation des relations entre les représentations originales et dérivées. |
| NFR-007 | Résilience | Identification des échecs et principes de reprise contrôlée. |
| NFR-008 | Traçabilité | Conservation de la provenance des connaissances. |
| NFR-009 | Cohérence après modification | Propagation contrôlée des changements et suppressions. |
| NFR-012 | Traitements volumineux | Prise en compte des opérations d'ingestion suivies comme Jobs. |
| NFR-014 | Extensibilité | Séparation des connecteurs et capacités spécialisées. |
| NFR-018 | Observabilité | Suivi des étapes, erreurs et opérations. |
| NFR-020 | Vérifiabilité | Identification des résultats et erreurs permettant des contrôles reproductibles. |

Cette couverture est spécifique au périmètre de l'ingestion. Elle ne remplace pas la matrice globale de couverture du modèle de données ni les autres spécifications.

# 18. Sujets reportés aux spécifications spécialisées

Les sujets suivants sont volontairement reportés :

| Sujet | Document responsable |
|---|---|
| Définition des entités et cardinalités | 04 — Modèle de données |
| Gestion fonctionnelle des Knowledge Bases et associations | 05 — Knowledge Bases |
| Connecteurs, extraction et ingestion | 06 — Pipeline d'ingestion |
| Formats, stratégies de découpage et Chunk Sets | 07 — Chunking et embeddings |
| Modèles, compatibilité et production des embeddings | 07 — Chunking et embeddings |
| Index, générations, index entries et disponibilité en recherche | 08 — Moteur de recherche |
| Recherche, fusion et classement | 08 — Moteur de recherche |
| Contrats d'intégration externes | 10 — API |
| Authentification, autorisation, isolation et secrets | 11 — Sécurité et isolation |
| Découverte et exploitation des Structured Resources | 12 — Données structurées |
| Tests de qualité et métriques d'évaluation | 13 — Tests et évaluation |
| Exécution, déploiement et capacité de traitement | 14 — Déploiement et scalabilité |

# 19. Éléments explicitement non décidés

Ce document ne fixe pas :

- Les technologies ou bibliothèques d'extraction.
- Les protocoles de connexion aux sources.
- Les formats documentaires pris en charge dans chaque version du produit.
- Les critères techniques de détection des doublons et des changements.
- Les stratégies détaillées de normalisation.
- Les tailles, chevauchements ou algorithmes de chunking.
- Les fournisseurs ou modèles d'embeddings à sélectionner.
- Les stratégies physiques d'indexation.
- Les mécanismes de traitement asynchrone et de reprise.
- Les structures de stockage et les transactions.
- Les règles détaillées de conservation et d'effacement.

Ces choix seront étudiés dans les spécifications concernées et consignés dans le Decision Log lorsqu'ils constituent des décisions architecturales.

# 20. Conditions de validation

Le document pourra être validé lorsque :

1. Le rôle et le périmètre du pipeline d'ingestion seront approuvés.
2. La distinction entre Knowledge Source, Source Connection et Knowledge Base Source Association sera claire.
3. La distinction entre association d'une source et association d'un élément de connaissance sera respectée.
4. Le parcours Document, Document Version, Original Artifact et Extracted Content sera cohérent avec le modèle de données.
5. La place de Chunk Set, Chunk, Embedding et Index Generation sera correctement délimitée.
6. La mise à disposition d'une connaissance dans une Knowledge Base sera distinguée de sa simple découverte dans une source.
7. Les modifications, synchronisations, erreurs et suppressions seront couvertes au niveau conceptuel.
8. La séparation entre ingestion documentaire et données structurées sera préservée.
9. Les frontières de responsabilité avec les autres modules seront cohérentes.
10. Les exigences concernées du cahier des charges seront couvertes.
11. Les détails relevant des spécifications ultérieures ne seront pas anticipés.

# 21. Conclusion

Le pipeline d'ingestion transforme des éléments documentaires provenant de sources identifiées en connaissances préparées et rendues disponibles dans les Knowledge Bases autorisées.

Il préserve la distinction entre l'origine des informations, leur sélection dans une base, l'identité du document, ses versions, les artefacts originaux et les représentations dérivées nécessaires à la recherche.

Il coordonne les capacités spécialisées sans absorber leurs responsabilités et conserve la provenance des connaissances tout au long de leur préparation.

Les données structurées suivent un parcours distinct et ne sont pas forcées dans le pipeline documentaire.

**Le pipeline d'ingestion est le parcours contrôlé qui transforme une source documentaire en connaissance exploitable, sans perdre son identité, sa provenance ni son périmètre d'accès.**
