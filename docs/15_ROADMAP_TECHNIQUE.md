# UNIVERSAL RAG ENGINE

## Document 15 — Roadmap technique

**Version :** 1.0
**Statut :** VALIDATED
**Projet :** RAG-universal
**Date :** 2026-11-21

---

# 1. Objectif

Ce document organise la progression de réalisation de Universal RAG Engine à partir de la vision, des exigences et des spécifications validées.

Il définit :

- Les principes de passage des spécifications à la réalisation.
- Les grandes phases de construction et leur ordre de dépendance.
- Les capacités attendues à l'issue de chaque phase.
- Les prérequis et conditions de sortie des phases.
- Les activités transversales qui doivent accompagner toute la réalisation.
- La traçabilité entre les exigences, les spécifications, les travaux et les preuves.
- Le processus de décision pour les choix techniques qui restent ouverts.
- Les conditions générales permettant de considérer une capacité comme prête à être livrée.

Cette roadmap constitue un cadre de séquencement et de pilotage. Elle n'est ni un calendrier contractuel, ni un plan de tâches détaillé, ni une sélection de technologies. Elle doit pouvoir être affinée à mesure que les décisions techniques et les résultats des premières réalisations deviennent disponibles.

# 2. Références et dépendances

Cette spécification s'appuie sur les documents suivants :

- `00_VISION_ET_OBJECTIFS.md` — vision, objectifs, indépendance applicative et limites du produit.
- `DEPENDENCY_MAP.md` — dépendances et ordre de construction des spécifications.
- `DECISION_LOG.md` — décisions architecturales et conceptuelles retenues.
- `01_CAHIER_DES_CHARGES.md` — exigences fonctionnelles et non fonctionnelles de référence.
- `02_ARCHITECTURE_GLOBALE.md` — domaines et capacités générales du moteur.
- `03_ARCHITECTURE_MODULAIRE.md` — responsabilités et frontières des modules.
- `04_MODELE_DE_DONNEES.md` — entités, relations, provenance et concepts opérationnels.
- `05_KNOWLEDGE_BASES.md` — espaces de connaissances, sources, associations et règles d'utilisation.
- `06_PIPELINE_INGESTION.md` — ingestion et cycle de vie des connaissances documentaires.
- `07_CHUNKING_ET_EMBEDDINGS.md` — préparation, segmentation et représentations vectorielles.
- `08_MOTEUR_DE_RECHERCHE.md` — indexation, recherche, récupération et classement.
- `09_GENERATION_ET_LLM.md` — contexte, fournisseurs de modèles et génération.
- `10_API_SPECIFICATION.md` — contrats d'intégration avec les applications clientes.
- `11_SECURITE_ET_ISOLATION.md` — authentification, autorisation, isolation et protection.
- `12_DONNEES_STRUCTUREES.md` — découverte, accès et interrogation des données structurées.
- `13_TESTS_ET_EVALUATION.md` — vérification, validation, qualité et preuves.
- `14_DEPLOIEMENT_ET_SCALABILITE.md` — exécution, capacité, résilience et exploitation.

Les spécifications 00 à 14 constituent le socle de référence de cette roadmap. Leurs responsabilités ne sont pas redéfinies ici.

# 3. Principes de réalisation

## 3.1 Respecter l'indépendance du moteur

La réalisation doit produire un moteur autonome, exploitable par plusieurs applications clientes différentes. Les besoins d'une application cliente particulière ne doivent pas introduire de dépendance métier dans le cœur du moteur.

Les interfaces clientes consomment les capacités exposées par le moteur. Elles ne doivent pas devenir propriétaires de ses règles de gouvernance, de sécurité, de recherche, de génération ou de cycle de vie des connaissances.

## 3.2 Construire à partir des contrats validés

Chaque capacité doit être réalisée à partir des exigences, des responsabilités modulaires, du modèle de données et des contrats qui lui sont applicables.

Une implémentation ne doit pas créer implicitement une nouvelle entité métier, une nouvelle règle d'accès ou une nouvelle responsabilité de module simplement parce que cela paraît plus facile techniquement. Toute évolution conceptuelle doit être examinée, justifiée et documentée avant d'être intégrée.

## 3.3 Progresser par incréments vérifiables

La réalisation doit être découpée en incréments verticaux apportant une capacité identifiable et testable. Un incrément doit traverser les composants nécessaires à son usage réel, sans attendre la construction complète de tous les modules.

Chaque incrément doit préserver les comportements déjà validés et fournir des preuves de conformité à ses critères d'acceptation.

## 3.4 Appliquer la sécurité dès le départ

La sécurité, l'isolation des organisations, la protection des secrets et la provenance ne constituent pas une phase tardive de finition. Elles doivent être prises en compte dès les fondations et vérifiées dans chaque capacité qui manipule des identités, des sources, des connaissances, des résultats ou des fournisseurs.

Les contrôles de sécurité critiques ne peuvent pas être compensés par un bon fonctionnement fonctionnel ou par un score de qualité RAG élevé.

## 3.5 Évaluer la qualité en continu

Les tests logiciels et l'évaluation de la qualité RAG doivent accompagner la construction progressive du moteur. Les jeux d'évaluation doivent évoluer avec les capacités réalisées, sans attendre la fin du projet.

Une amélioration d'un modèle, d'un fournisseur, d'une stratégie de recherche ou d'une configuration doit être appréciée au regard de ses effets sur les résultats, la sécurité, les coûts et les exigences opérationnelles concernées.

## 3.6 Ne pas imposer une topologie physique prématurée

Les modules logiques ne deviennent pas automatiquement des services déployés séparément. Le regroupement ou la séparation des composants doit être décidé à partir des besoins démontrés de charge, de sécurité, de disponibilité, d'évolution et d'exploitation, conformément au document 14.

## 3.7 Séparer décisions et hypothèses

Une technologie, un fournisseur, un outil ou une valeur chiffrée ne doit pas être considéré comme retenu tant qu'une décision explicite ne l'a pas confirmé. Les hypothèses d'étude restent identifiées comme telles et ne doivent pas devenir des dépendances cachées de l'architecture.

# 4. Vue d'ensemble de la progression

La progression est organisée en phases qui s'appuient les unes sur les autres. Certaines activités peuvent se dérouler en parallèle lorsque leurs dépendances sont satisfaites, mais cet éventuel parallélisme ne doit pas effacer les critères de sortie de chaque phase.

| Phase | Intitulé | Résultat principal |
|---|---|---|
| P0 | Préparation de la réalisation | Référentiel de travail, décisions préalables et critères de livraison prêts |
| P1 | Fondations du moteur et gouvernance | Socle exécutable, organisations, identités, applications, autorisations et Knowledge Bases |
| P2 | Sources et cycle de vie documentaire | Sources connectées et documents acquis, versionnés et suivis |
| P3 | Préparation et recherche documentaire | Chunks, embeddings, index, générations et recherche documentaire vérifiable |
| P4 | Accès aux données structurées | Sources structurées découvertes, contrôlées et interrogeables |
| P5 | Génération et orchestration RAG | Modes de requête, contexte, réponses, incertitude et citations intégrés |
| P6 | API et intégration des applications clientes | Contrats publics consolidés et intégration indépendante démontrée |
| P7 | Qualification opérationnelle et mise en service | Capacité, sécurité, résilience, restauration et exploitation démontrées |

Les tests, l'évaluation, la sécurité, l'observabilité et la documentation ne sont pas confinés à une phase particulière. Ils sont appliqués à chaque phase et approfondis à mesure que le moteur gagne en capacités.

# 5. Phase P0 — Préparation de la réalisation

## 5.1 Objectif

Transformer le référentiel de spécifications validées en une base de travail exploitable pour la conception technique et la planification détaillée, sans commencer l'implémentation sur des points encore ambigus.

## 5.2 Travaux attendus

- Confirmer la présence et la cohérence des documents validés 00 à 14.
- Vérifier la synchronisation de leurs en-têtes avec `STATUS.md`.
- Relire la `DEPENDENCY_MAP.md` et le `DECISION_LOG.md` pour identifier les dépendances et décisions encore ouvertes.
- Établir une matrice de traçabilité exploitable entre FR, NFR, spécifications, capacités et futurs tests.
- Identifier les sujets nécessitant une décision d'architecture (ADR) avant leur mise en œuvre.
- Définir les critères communs de revue de code, de qualité, de sécurité et de livraison.
- Constituer un backlog initial regroupé par capacités et dépendances, plutôt que par technologie seule.
- Définir les environnements et moyens d'essai nécessaires au démarrage, sans choisir prématurément leurs fournisseurs.

## 5.3 Points à arbitrer avant les phases concernées

Les sujets ci-dessous doivent être étudiés au moment où ils deviennent nécessaires. Leur présence dans cette liste ne signifie pas qu'ils doivent tous être tranchés avant tout travail préparatoire :

- Langage, environnement d'exécution et structure du dépôt.
- Mécanismes de persistance et de gestion des migrations.
- Stockage des artefacts documentaires et des données dérivées.
- Stratégie de recherche textuelle, vectorielle et hybride.
- Exécution et suivi des traitements différés.
- Fournisseurs, modèles et politiques de sélection des capacités LLM et embeddings.
- Gestion des connexions aux sources et des secrets.
- Stratégie d'authentification et d'autorisation concrète.
- Outils de tests, d'évaluation, d'intégration continue et d'observabilité.
- Profils de déploiement et objectifs opérationnels chiffrés.

Chaque décision engageant durablement l'architecture doit être consignée dans le `DECISION_LOG.md` ou dans un ADR, avec son contexte, les options examinées, les conséquences et le statut de décision.

## 5.4 Conditions de sortie

La phase est prête à se terminer lorsque :

1. Les documents de référence sont identifiés et leur statut vérifié.
2. Les exigences ont une méthode de vérification ou une justification de traitement identifiée.
3. Les dépendances majeures des premières capacités sont comprises.
4. Les décisions nécessaires au démarrage de P1 sont arbitrées ou explicitement circonscrites.
5. Le backlog initial permet de suivre les exigences, les livrables et leurs preuves.
6. Aucun choix provisoire n'est présenté comme une décision validée.

# 6. Phase P1 — Fondations du moteur et gouvernance

## 6.1 Objectif

Construire le socle autonome sur lequel les capacités de connaissance pourront être ajoutées sans dépendance à une application cliente particulière.

## 6.2 Capacités attendues

- Structure générale du moteur et séparation de ses responsabilités logiques.
- Gestion du cycle de vie des organisations.
- Gestion des identités humaines et de service.
- Enregistrement et identification des applications clientes.
- Appartenance organisationnelle et attribution des rôles et permissions.
- Politiques d'autorisation et accès explicites aux ressources.
- Isolation logique des organisations et des Knowledge Bases.
- Création, configuration et administration des Knowledge Bases.
- Socle des connexions aux sources et configurations, sans supposer que toutes les familles de sources sont déjà prises en charge.
- Gestion initiale des événements d'audit et des opérations suivies lorsqu'elles sont nécessaires.
- Première surface API permettant à une application cliente distincte d'utiliser le moteur.

## 6.3 Dépendances principales

Documents 02, 03, 04, 05, 10 et 11. Les principes du document 14 s'appliquent à l'organisation des environnements dès le départ.

## 6.4 Conditions de sortie

1. Une organisation et ses ressources sont isolées conformément aux règles validées.
2. Une application cliente peut être identifiée indépendamment du moteur.
3. Les identités et autorisations sont évaluées côté moteur, et non déléguées à l'application cliente.
4. Les opérations d'accès non autorisées sont refusées et testées.
5. Une Knowledge Base peut être créée, configurée et administrée dans son périmètre autorisé.
6. Les événements de gouvernance importants sont traçables.
7. Les contrats nécessaires aux phases suivantes sont utilisables et testés.

# 7. Phase P2 — Sources et cycle de vie documentaire

## 7.1 Objectif

Permettre au moteur d'identifier des sources documentaires autorisées, d'en acquérir les documents et de préserver leur identité, leurs versions et leur provenance.

## 7.2 Capacités attendues

- Gestion de l'identité des sources et séparation entre sources et connexions.
- Association des sources aux Knowledge Bases.
- Découverte et sélection contrôlée des éléments documentaires.
- Acquisition et conservation des artefacts originaux.
- Création et suivi des documents et de leurs versions.
- Extraction et normalisation des contenus documentaires.
- Mise à jour, synchronisation, retrait et suppression conformément aux règles de cycle de vie.
- Gestion des opérations longues, des échecs partiels et de la reprise contrôlée.
- Conservation de la provenance entre la source, le document, la version et les contenus extraits.

## 7.3 Dépendances principales

Documents 04, 05, 06, 10, 11 et 14. Les fondations de gouvernance et d'autorisation de P1 sont des prérequis.

## 7.4 Conditions de sortie

1. Une source et sa connexion restent des concepts distincts.
2. L'association d'une source à une Knowledge Base ne provoque pas l'intégration automatique de tous ses éléments.
3. Un document, ses versions, ses artefacts originaux et ses contenus extraits restent distinguables.
4. Les changements et retraits préservent la cohérence et la provenance.
5. Les traitements interrompus ou partiellement échoués sont identifiables.
6. Les accès aux sources et documents respectent les autorisations prévues.
7. Les tests couvrent les parcours nominaux, les erreurs et les cas de reprise pertinents.

# 8. Phase P3 — Préparation et recherche documentaire

## 8.1 Objectif

Transformer les contenus documentaires préparés en représentations recherchables, puis fournir des capacités de récupération pertinentes et traçables.

## 8.2 Capacités attendues

- Production de Chunk Sets et de Chunks à partir des contenus extraits.
- Conservation des positions et de la provenance des Chunks.
- Production et gestion des Embeddings compatibles avec leurs modèles de référence.
- Distinction entre les représentations documentaires et les représentations propres aux requêtes.
- Gestion des Index, configurations, générations et entrées d'index.
- Construction et activation contrôlée de générations d'index.
- Recherche vectorielle et textuelle.
- Recherche hybride et combinaison des résultats lorsque les capacités sont disponibles.
- Filtrage selon les Knowledge Bases, les associations et les autorisations.
- Classement, restitution des résultats et gestion des résultats vides ou incomplets.
- Suivi de la cohérence entre connaissances disponibles et éléments effectivement présents dans les générations d'index.

## 8.3 Dépendances principales

Documents 04, 05, 06, 07, 08, 11, 13 et 14. La phase P2 fournit les contenus documentaires nécessaires. Les tests et évaluations doivent être associés à chaque évolution de segmentation, d'embedding ou de recherche.

## 8.4 Conditions de sortie

1. Les Chunks et Embeddings conservent leurs liens avec les contenus et versions sources.
2. Les représentations vectorielles incompatibles ne sont pas mélangées.
3. Les générations d'index sont identifiables et leur état est vérifiable.
4. Les recherches ne retournent que des connaissances autorisées.
5. Les résultats conservent leur provenance et leur contexte de récupération.
6. La qualité du retrieval est évaluée sur des jeux de référence documentés.
7. Les modifications et suppressions ne laissent pas de connaissances obsolètes accessibles sans contrôle.

# 9. Phase P4 — Accès aux données structurées

## 9.1 Objectif

Fournir une capacité d'accès aux données structurées qui respecte leur nature propre et ne les force pas dans le pipeline documentaire.

## 9.2 Capacités attendues

- Connexion aux sources structurées au moyen de connexions autorisées.
- Découverte et description des Structured Resources.
- Sélection explicite des ressources mises à disposition dans une Knowledge Base.
- Compréhension des schémas, champs, types et relations connus.
- Interprétation d'une demande en une intention structurée ou un plan contrôlable.
- Validation de la ressource, des champs, des opérations et des limites avant exécution.
- Évaluation des autorisations avant tout accès effectif à la source.
- Exécution contrôlée, pagination et gestion des résultats partiels.
- Préservation des types, de la provenance, de la fraîcheur et des limites de restitution.
- Restitution de résultats structurés compatibles avec le modèle de Retrieval Result.
- Protection des sources contre les accès libres, les requêtes abusives et les injections.

## 9.3 Dépendances principales

Documents 04, 05, 08, 10, 11, 12, 13 et 14. Les fondations de gouvernance de P1 sont indispensables. Cette phase peut avancer en partie en parallèle de P2 ou P3 si les contrats communs et les contrôles de sécurité sont stables ; l'intégration au parcours de recherche unifié reste soumise à leurs contrats.

## 9.4 Conditions de sortie

1. Une source structurée reste distincte de ses connexions et de ses ressources.
2. La découverte d'une ressource ne l'autorise pas automatiquement à être interrogée.
3. Toute interrogation est validée et autorisée avant exécution.
4. Le LLM et les applications clientes ne disposent pas d'un accès libre à la source sous-jacente.
5. Les résultats préservent types, provenance, fraîcheur et caractère complet ou partiel.
6. Les contrôles couvrent les accès interdits, les champs sensibles et les limites de requête.
7. La qualité et l'exactitude des résultats sont évaluées sur des cas représentatifs.

# 10. Phase P5 — Génération et orchestration RAG

## 10.1 Objectif

Assembler les capacités de recherche et de génération dans un traitement de requête cohérent, explicable et contrôlé.

## 10.2 Capacités attendues

- Réception et caractérisation d'une Query.
- Prise en compte du contexte d'identité, d'application, d'organisation et des Knowledge Bases autorisées.
- Distinction des modes `RETRIEVAL_ONLY`, `DIRECT_LLM` et `RETRIEVAL_AUGMENTED`.
- Préparation d'un contexte à partir des résultats autorisés et réellement utiles.
- Utilisation contrôlée des fournisseurs et modèles.
- Production de réponses et gestion des erreurs de génération.
- Gestion explicite de l'incertitude et des connaissances insuffisantes.
- Conservation de la relation entre demande, résultats récupérés, réponse et citations.
- Distinction entre résultats récupérés et informations ayant effectivement contribué à la réponse.
- Combinaison de résultats documentaires et structurés sans perte de provenance.
- Protection contre les injections et les contenus non fiables.

## 10.3 Dépendances principales

Documents 04, 08, 09, 10, 11, 12 et 13. La disponibilité des capacités de retrieval documentaire et/ou structuré dépend des phases P3 et P4. Le mode `DIRECT_LLM` ne doit toutefois pas être artificiellement rendu dépendant d'une Knowledge Base.

## 10.4 Conditions de sortie

1. Les trois modes de traitement sont distincts et leurs résultats sont correctement qualifiés.
2. Les réponses augmentées sont liées aux résultats et aux sources réellement utilisés.
3. Les citations ne sont pas attribuées artificiellement à des résultats non utilisés.
4. Les réponses ne présentent pas une génération directe comme fondée sur une Knowledge Base.
5. Les refus, incertitudes et absences de connaissance sont représentés de manière non trompeuse.
6. Les données envoyées aux modèles respectent les autorisations et règles de minimisation.
7. Les tests de sécurité et les évaluations de fidélité, d'exactitude et de citation sont satisfaisants selon les critères approuvés.

# 11. Phase P6 — API et intégration des applications clientes

## 11.1 Objectif

Consolider l'accès aux capacités du moteur par une frontière API stable, documentée et indépendante des applications clientes.

Cette phase ne signifie pas que l'API doit attendre la fin du moteur pour exister. Les contrats et interfaces minimaux sont introduits dès P1, puis étendus et stabilisés avec chaque capacité. P6 vérifie l'intégration transversale et la cohérence de l'ensemble.

## 11.2 Capacités attendues

- Exposition cohérente des capacités de gouvernance et d'administration autorisées.
- Exposition des fonctions de gestion des Knowledge Bases et des sources.
- Déclenchement et suivi des traitements documentaires.
- Exposition des recherches documentaires et structurées.
- Exposition distincte des modes de génération.
- Restitution des résultats, citations, erreurs et informations de suivi prévues par les contrats.
- Compatibilité des versions et gestion contrôlée des évolutions contractuelles.
- Intégration démontrée avec au moins une application cliente indépendante du moteur, sans introduire de logique métier cliente dans le cœur.

## 11.3 Dépendances principales

Documents 03, 04, 05, 10, 11, ainsi que les capacités des phases P1 à P5. Les contrats API restent la référence : une intégration cliente ne doit pas contourner les autorisations ou appeler directement les composants internes.

## 11.4 Conditions de sortie

1. Les capacités exposées respectent les contrats validés.
2. Les erreurs, états partiels et opérations longues sont restitués sans ambiguïté.
3. Les applications clientes ne contournent pas la sécurité du moteur.
4. L'intégration ne dépend pas d'un framework ou d'un domaine métier particulier côté client.
5. Les changements de contrat suivent un processus de compatibilité et de dépréciation identifié.
6. Les tests de contrat et d'intégration couvrent les principaux parcours exposés.

# 12. Phase P7 — Qualification opérationnelle et mise en service

## 12.1 Objectif

Démontrer que la version candidate du moteur peut être déployée et exploitée dans un environnement cible avec un niveau de sécurité, de capacité, de disponibilité et de reprise conforme aux objectifs approuvés.

## 12.2 Capacités attendues

- Déploiement reproductible dans les environnements retenus.
- Gestion contrôlée des configurations et secrets.
- Surveillance de la santé des composants et des dépendances externes.
- Suivi des charges interactives et des traitements différés.
- Mesures de latence, débit, concurrence et consommation de ressources.
- Validation des limites et mécanismes de protection contre la surcharge.
- Tests de panne, fonctionnement dégradé et reprise.
- Sauvegardes et restaurations vérifiées, y compris la cohérence entre données originales et représentations dérivées.
- Procédures de livraison, migration, retour arrière et récupération.
- Audit, alertes, journaux, métriques et traces adaptés à l'exploitation.
- Vérification des scénarios de mise à jour et de compatibilité des applications clientes.

## 12.3 Dépendances principales

Documents 11, 13 et 14, ainsi que l'ensemble des capacités fonctionnelles nécessaires au profil de livraison visé. Les objectifs de service, volumes, budgets et profils d'utilisation doivent être approuvés avant d'en déduire un dimensionnement.

## 12.4 Conditions de sortie

1. Le déploiement est répétable et la configuration est maîtrisée.
2. Les objectifs opérationnels approuvés sont mesurés dans des conditions représentatives.
3. Les scénarios de panne et de reprise sont testés.
4. Les sauvegardes peuvent être restaurées et leur cohérence vérifiée.
5. Les secrets et données sensibles ne sont pas exposés dans les journaux ou les rapports.
6. Les mécanismes d'observabilité permettent de diagnostiquer les incidents importants.
7. Les risques résiduels, limites connues et procédures d'exploitation sont documentés.
8. Aucun défaut critique de sécurité, d'isolation ou d'intégrité ne demeure ouvert sans décision formelle de traitement.

# 13. Activités transversales obligatoires

Les activités suivantes s'appliquent à toutes les phases, de P0 à P7.

## 13.1 Sécurité et gouvernance

- Vérifier les contrôles d'identité et d'autorisation à chaque frontière pertinente.
- Préserver l'isolation des organisations et des Knowledge Bases.
- Appliquer le moindre privilège aux connexions et fournisseurs.
- Protéger les secrets et minimiser les données exposées.
- Vérifier les contenus non fiables et les risques d'injection.
- Tracer les opérations importantes sans journaliser inutilement les données sensibles.

## 13.2 Tests, évaluation et régression

- Associer les tests aux exigences et risques correspondants.
- Exécuter les tests adaptés à chaque incrément.
- Maintenir des jeux de référence et des cas d'évaluation versionnés.
- Comparer les évolutions de retrieval, de génération, de modèles et de configurations.
- Vérifier les contrats et les interactions entre modules.
- Conserver les résultats et preuves permettant de comprendre les décisions de validation.
- Empêcher qu'un score global masque un échec critique de sécurité ou d'intégrité.

## 13.3 API et intégration

- Maintenir une frontière API cohérente au fur et à mesure de l'ajout des capacités.
- Valider les contrats, les erreurs, les limites et les comportements de compatibilité.
- Vérifier l'utilisation du moteur par un consommateur indépendant.
- Éviter de rendre les applications clientes propriétaires des règles internes du moteur.

## 13.4 Observabilité et exploitation

- Rendre identifiables les opérations, leurs états et leurs erreurs.
- Distinguer succès, échec, résultat partiel et résultat incomplet.
- Mesurer les comportements qui conditionnent les objectifs opérationnels.
- Préparer les procédures de diagnostic et de reprise avec les capacités concernées.

## 13.5 Documentation et décisions

- Mettre à jour les spécifications uniquement lorsque les décisions ou apprentissages justifient leur évolution.
- Conserver les décisions techniques et leurs justifications dans les registres appropriés.
- Documenter les écarts par rapport aux spécifications avant leur acceptation.
- Garder `STATUS.md` cohérent avec les statuts réellement vérifiés des documents.

# 14. Dépendances entre les phases

| Phase | Prérequis majeurs | Dépendance structurante |
|---|---|---|
| P0 | Documents 00 à 14 et registres de décisions | Référentiel cohérent et décisions initiales identifiées |
| P1 | P0 ; architecture, modèle de données, sécurité et API | Gouvernance et isolation avant exposition des connaissances |
| P2 | P1 ; Knowledge Bases et pipeline documentaire | Sources et documents dans un périmètre autorisé |
| P3 | P1 et P2 ; chunking, embeddings et recherche | Contenus préparés avant indexation et retrieval documentaire |
| P4 | P1 ; Knowledge Bases, sécurité, modèle et spécification structurée | Accès autorisé et ressources découvertes avant interrogation |
| P5 | P1 et contrats de P3 et/ou P4 selon le mode | Retrieval contrôlé avant génération augmentée ; génération directe indépendante des KB |
| P6 | Contrats de P1 à P5 selon les capacités exposées | Intégration transversale et stabilité de la frontière publique |
| P7 | Capacités nécessaires au profil cible, tests et déploiement | Preuves fonctionnelles, de sécurité et opérationnelles avant mise en service |

Le chemin documentaire principal suit P1 → P2 → P3 → P5. Le chemin structuré suit P1 → P4 → P5. La stabilisation des contrats API accompagne ces chemins et leur intégration globale est consolidée en P6. P7 qualifie le profil de livraison retenu.

# 15. Traçabilité avec les exigences fonctionnelles

La roadmap doit permettre de relier chaque exigence à une phase de réalisation, à une capacité livrable et à une preuve de vérification. La correspondance suivante indique le principal point d'intégration ; elle ne signifie pas que les exigences transversales ne doivent être vérifiées qu'une seule fois.

| Exigences | Domaine | Phase(s) principalement concernée(s) |
|---|---|---|
| FR-001 à FR-006 | Organisations, applications, identités, permissions, gouvernance et Knowledge Bases | P1, puis toutes les phases pour les contrôles d'accès |
| FR-007 | Gestion des sources et connexions | P1, P2 et P4 |
| FR-008 à FR-010 | Importation, extraction, normalisation et cycle de vie documentaire | P2 |
| FR-011 à FR-012 | Chunking et embeddings | P3 |
| FR-013 | Indexation et réindexation | P3 |
| FR-014 à FR-017 | Recherche vectorielle, textuelle, hybride, filtrage et classement | P3, P4 et P5 |
| FR-018 à FR-021 | Génération augmentée, fournisseurs LLM, citations et connaissances insuffisantes | P5 |
| FR-022 (connexion), FR-023 (interrogation contrôlée) et FR-024 (combinaison) | Données structurées | P4 et P5 |
| FR-025 à FR-026 | Interface publique et gestion des requêtes | P1 et P6, avec extension progressive |
| FR-027 à FR-028 | Administration, journalisation et supervision | P1, P6 et P7 |

# 16. Traçabilité avec les exigences non fonctionnelles

Les NFR ne sont pas des tâches finales isolées. Leur contribution doit être vérifiée au fur et à mesure de la construction du moteur.

| Exigence | Besoin | Phases de prise en compte et de preuve |
|---|---|---|
| NFR-001 | Isolation des organisations | P1, puis vérification dans P2 à P7 |
| NFR-002 | Contrôle des accès | P1, puis tests dans chaque capacité exposée |
| NFR-003 | Protection des données sensibles | P1 à P7 selon les données et transferts concernés |
| NFR-004 | Protection contre les injections | P2 à P6, avec contrôles renforcés en P4 et P5 |
| NFR-005 | Gestion des secrets | P1, puis intégrations sources et fournisseurs P2 à P7 |
| NFR-006 | Intégrité des connaissances | P2 à P5 et vérification de sauvegarde/restauration en P7 |
| NFR-007 | Résilience | Tests tout au long du projet ; qualification renforcée en P7 |
| NFR-008 | Traçabilité | P1 à P7 |
| NFR-009 | Cohérence après modification | P2 à P5, puis tests opérationnels en P7 |
| NFR-010 | Performance | Mesures progressives en P3 à P7 selon les objectifs approuvés |
| NFR-011 | Évolutivité | P1 à P7 ; validation de capacité en P7 |
| NFR-012 | Traitements volumineux | P2, P3, P4 et P7 |
| NFR-013 | Modularité | P1 à P6 et tests de frontières continus |
| NFR-014 | Extensibilité | P1 à P6, notamment sources, modèles et fournisseurs |
| NFR-015 | Maintenabilité | Toutes les phases |
| NFR-016 | Interopérabilité | P1, P2, P4 et P6 |
| NFR-017 | Portabilité | P0 et P7, puis à chaque évolution de l'environnement cible |
| NFR-018 | Observabilité | P1 à P7, avec qualification opérationnelle en P7 |
| NFR-019 | Évaluation de la qualité | P2 à P6, puis régression continue |
| NFR-020 | Vérifiabilité | Toutes les phases, avec preuves conservées |

# 17. Conditions générales de passage et de livraison

Une phase ou un incrément ne peut être considéré comme terminé sur la seule base de l'existence du code ou d'une démonstration ponctuelle.

Le passage est conditionné par les éléments suivants, adaptés à la portée du livrable :

1. Les exigences et spécifications concernées sont identifiées.
2. Les responsabilités et contrats des composants impliqués sont respectés.
3. Les tests applicables sont exécutés et leurs résultats sont conservés.
4. Les risques de sécurité, d'isolation et d'intégrité ont été vérifiés.
5. Les erreurs, limites et comportements partiels sont caractérisés.
6. La provenance et la traçabilité nécessaires sont préservées.
7. Les effets sur les capacités déjà livrées ont été évalués.
8. Les décisions techniques et écarts éventuels sont documentés.
9. Les critères opérationnels applicables sont mesurés lorsque le livrable les engage.
10. Les défauts critiques ne sont pas dissimulés par une moyenne, un score ou une appréciation globale.

Une livraison peut être limitée à un périmètre fonctionnel explicite. Elle doit alors indiquer les capacités disponibles, celles qui ne le sont pas, les limites connues et les exigences non encore couvertes. Une capacité non disponible ne doit pas être présentée comme opérationnelle.

# 18. Gestion des décisions et des changements de roadmap

La roadmap est un document évolutif, mais ses modifications doivent rester contrôlées.

Une modification peut être nécessaire lorsqu'une preuve technique, une exigence clarifiée, un risque ou une dépendance réelle remet en cause l'ordre ou le contenu des phases.

Toute modification importante doit :

- identifier le motif et les éléments de preuve ;
- préciser les phases, exigences et documents concernés ;
- distinguer les corrections de rédaction des changements de décision ;
- évaluer les impacts sur la sécurité, les données, les contrats, les tests et le déploiement ;
- être enregistrée dans le `DECISION_LOG.md` ou un ADR lorsqu'elle constitue une décision d'architecture ;
- maintenir la cohérence des documents dépendants et de `DEPENDENCY_MAP.md`.

La roadmap ne peut pas, à elle seule, autoriser une modification des exigences ou du modèle de données validés.

# 19. Éléments explicitement non décidés

Cette roadmap ne choisit pas et ne fixe pas :

- Le langage de programmation, les frameworks et les bibliothèques.
- Le moteur de base de données, les stockages documentaires ou vectoriels.
- Les technologies de recherche, de files de messages ou d'exécution asynchrone.
- Les fournisseurs cloud, les régions ou les plateformes d'hébergement.
- Les fournisseurs LLM, les modèles et leurs versions.
- Les outils de tests, d'évaluation, d'intégration continue ou de supervision.
- Le nombre exact de services, processus, conteneurs ou machines.
- Les capacités matérielles, les budgets, les coûts ou les effectifs nécessaires.
- Les dates, durées, charges de travail et échéances contractuelles.
- Les volumes cibles, débits, latences, taux de disponibilité, RPO ou RTO.
- Les seuils définitifs d'acceptation ou les règles de mise en production propres à un environnement.
- Les fonctionnalités optionnelles ou extensions qui ne figurent pas dans les exigences validées.

Ces sujets doivent être instruits à partir des besoins confirmés, des mesures, des études et des décisions formelles. Leur absence de cette roadmap ne constitue pas une décision implicite.

# 20. Conditions de validation

Le document pourra être validé lorsque :

1. La relation entre les spécifications validées et les phases de réalisation sera claire.
2. L'ordre des phases respectera les dépendances structurantes du moteur.
3. Les capacités documentaires et structurées conserveront leurs parcours distincts avant leur combinaison dans le traitement des requêtes.
4. La gouvernance, l'autorisation et l'isolation seront intégrées dès les fondations et maintenues dans toutes les phases.
5. Les tests et l'évaluation seront continus et non reportés à la fin du projet.
6. Les livrables et conditions de sortie permettront de vérifier les progrès réels.
7. La frontière API et l'indépendance des applications clientes seront préservées.
8. Le déploiement physique ne sera pas imposé par le seul découpage logique des modules.
9. Les exigences FR-001 à FR-028 auront une phase ou un ensemble de phases de réalisation identifiable.
10. Les exigences NFR-001 à NFR-020 auront des points de prise en compte et de vérification identifiables.
11. Les choix techniques non décidés resteront explicitement ouverts.
12. Les dates, budgets, volumes et seuils non approuvés ne seront pas inventés.
13. La cohérence avec les documents 00 à 14, `DEPENDENCY_MAP.md` et `DECISION_LOG.md` sera vérifiée.
14. Les conditions générales de passage et de livraison permettront de distinguer une capacité codée d'une capacité réellement vérifiée.

# 21. Conclusion

La roadmap technique organise la réalisation de Universal RAG Engine en incréments cohérents, traçables et vérifiables. Elle donne un ordre de construction fondé sur les dépendances fonctionnelles et les exigences de sécurité, sans enfermer le projet dans une technologie, un fournisseur ou une topologie prématurés.

Les fondations de gouvernance précèdent l'exploitation des connaissances. Le parcours documentaire et le parcours structuré sont construits selon leurs besoins propres, puis réunis au niveau du traitement des requêtes et de la génération. L'API, les tests, l'évaluation, l'observabilité et la sécurité accompagnent le moteur à chaque étape.

**La roadmap n'est pas une promesse de dates : c'est un ordre de réalisation contrôlable, dans lequel chaque étape doit produire une capacité démontrable et des preuves suffisantes avant de servir de fondation à la suivante.**
