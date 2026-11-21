# UNIVERSAL RAG ENGINE

## Document 13 — Tests et évaluation

**Version :** 1.0
**Statut :** VALIDATED
**Projet :** RAG-universal
**Date :** 2026-11-21

---

# 1. Objectif

Ce document définit les principes de vérification, de validation et d'évaluation de la qualité de Universal RAG Engine.

Il établit un cadre commun permettant de vérifier que le moteur :

- respecte les exigences fonctionnelles et non fonctionnelles du cahier des charges ;
- applique correctement les responsabilités et les frontières définies par l'architecture ;
- préserve l'intégrité, la provenance et les périmètres d'accès des connaissances ;
- fournit des résultats de recherche pertinents et des réponses générées suffisamment fiables ;
- traite correctement les connaissances documentaires et les données structurées ;
- reste vérifiable au fil des évolutions du moteur, des fournisseurs, des modèles et des configurations.

Cette spécification définit les catégories de tests, les dimensions de qualité, les principes de constitution des jeux d'évaluation, les modalités de comparaison et les critères généraux de validation.

Elle reste indépendante des langages, bibliothèques, frameworks de test, plateformes d'intégration continue, fournisseurs de modèles et infrastructures d'exécution.

# 2. Références et dépendances

Cette spécification s'appuie sur les documents suivants :

- `00_VISION_ET_OBJECTIFS.md` — vision, indépendance applicative et principes fondateurs.
- `DEPENDENCY_MAP.md` — ordre et dépendances entre les spécifications.
- `DECISION_LOG.md` — décisions architecturales et conceptuelles retenues.
- `01_CAHIER_DES_CHARGES.md` — exigences fonctionnelles et non fonctionnelles à vérifier.
- `02_ARCHITECTURE_GLOBALE.md` — domaines et capacités générales du moteur.
- `03_ARCHITECTURE_MODULAIRE.md` — responsabilités et frontières des modules.
- `04_MODELE_DE_DONNEES.md` — modèle conceptuel, provenance et entités d'évaluation.
- `05_KNOWLEDGE_BASES.md` — périmètres des connaissances, associations et autorisations.
- `06_PIPELINE_INGESTION.md` — cycle de vie des sources et des connaissances documentaires.
- `07_CHUNKING_ET_EMBEDDINGS.md` — préparation des contenus, Chunk Sets, Chunks et Embeddings.
- `08_MOTEUR_DE_RECHERCHE.md` — recherche, récupération, filtrage et classement.
- `09_GENERATION_ET_LLM.md` — préparation du contexte et génération des réponses.
- `10_API_SPECIFICATION.md` — contrats d'intégration et comportements exposés.
- `11_SECURITE_ET_ISOLATION.md` — authentification, autorisation, isolation et protection.
- `12_DONNEES_STRUCTUREES.md` — découverte, interrogation et restitution des données structurées.

Les entités `Evaluation Dataset`, `Evaluation Case`, `Evaluation Metric`, `Evaluation Run` et `Evaluation Result` sont celles du modèle de données validé. Le présent document précise leur usage conceptuel sans redéfinir le modèle de données.

# 3. Positionnement et principes généraux

## 3.1 Vérification et validation

La **vérification** cherche à établir si un composant, un module ou le moteur respecte les exigences et les contrats qui lui sont applicables.

La **validation** cherche à établir si le comportement obtenu répond effectivement au besoin attendu dans des situations représentatives d'utilisation.

Les deux démarches sont complémentaires. Un moteur peut satisfaire ses contrats techniques tout en retournant des connaissances peu pertinentes ; inversement, une réponse ponctuellement correcte ne prouve pas que les contrôles d'accès, la provenance ou la fiabilité du système sont respectés.

## 3.2 Tests logiciels et évaluation RAG

Deux familles de travaux doivent être distinguées :

1. **Tests du système :** vérification des comportements fonctionnels et techniques, des interfaces, des règles de sécurité, des erreurs, de l'intégrité et des propriétés opérationnelles.
2. **Évaluation de la qualité RAG :** mesure de la qualité des connaissances retrouvées, de leur adéquation à la demande, de leur utilisation par le modèle et de la fiabilité des réponses produites.

Une évaluation RAG ne remplace pas les tests logiciels. Elle ne démontre pas, à elle seule, la sécurité ou la conformité des contrats. De même, des tests logiciels réussis ne démontrent pas la pertinence des réponses.

## 3.3 Principes obligatoires

Les démarches de test et d'évaluation respectent les principes suivants :

1. Chaque vérification doit être rattachée à une exigence, un risque, un contrat ou un comportement attendu identifiable.
2. Les résultats doivent être interprétables et, lorsque nécessaire, reproductibles.
3. Les scénarios doivent couvrir les comportements attendus, les erreurs, les limites et les cas adverses pertinents.
4. Les tests doivent vérifier les frontières entre modules, pas uniquement le fonctionnement isolé de chaque module.
5. La sécurité et l'isolation ne peuvent pas être compensées par un bon score de qualité fonctionnelle.
6. Les résultats de recherche, les réponses générées et les citations doivent être évalués séparément lorsque leurs critères diffèrent.
7. Les données de test doivent respecter les exigences de confidentialité, d'accès, de rétention et de sécurité.
8. Les seuils d'acceptation doivent être définis et justifiés pour le périmètre évalué ; aucun seuil universel n'est imposé par cette spécification.
9. Toute évolution du moteur, d'un modèle, d'un fournisseur ou d'une configuration susceptible d'affecter les résultats doit pouvoir être évaluée par comparaison.
10. Un score agrégé ne doit jamais masquer un échec critique dans une dimension particulière.

# 4. Périmètre

Cette spécification couvre :

- les tests fonctionnels du moteur et de ses capacités ;
- les tests des frontières et contrats entre modules ;
- les tests d'intégration et de parcours complet ;
- les tests de sécurité, d'isolation et de protection des données ;
- les tests d'intégrité, de traçabilité et de cycle de vie des connaissances ;
- les tests de résilience, de compatibilité et de comportement sous charge ;
- l'évaluation de la qualité du chunking, des embeddings, du retrieval et de la génération ;
- la gestion des jeux de données, cas, métriques, exécutions et résultats d'évaluation ;
- la régression et la comparaison des versions ou configurations du moteur ;
- la conservation des éléments de preuve et la traçabilité des validations.

Cette spécification ne définit pas les implémentations des modules testés. Elle ne choisit pas les outils, langages, frameworks, systèmes de reporting ou plateformes de déploiement qui seront utilisés.

# 5. Niveaux et catégories de tests

Les catégories suivantes sont complémentaires. Un même scénario peut relever de plusieurs catégories selon le risque qu'il couvre.

| Catégorie | Finalité | Exemple de périmètre |
|---|---|---|
| Tests unitaires | Vérifier un comportement isolé et déterministe | règles de validation, transformation, calcul ou décision |
| Tests de composants | Vérifier une capacité cohérente à l'intérieur d'un module | orchestration d'ingestion, construction de contexte, filtrage |
| Tests de contrats | Vérifier la conformité aux contrats entre composants ou avec une application cliente | format, validation, erreurs et compatibilité des échanges |
| Tests d'intégration | Vérifier la coopération réelle de plusieurs composants | source, ingestion, indexation puis récupération |
| Tests de bout en bout | Vérifier un parcours fonctionnel complet | demande cliente jusqu'aux résultats ou à la réponse |
| Tests de régression | Détecter une dégradation par rapport à une référence connue | résultats de recherche ou comportements validés auparavant |
| Tests de sécurité | Vérifier les contrôles et les résistances aux usages abusifs | accès interdit, fuite interorganisationnelle, injection |
| Tests de résilience | Vérifier le comportement en présence de pannes ou d'états partiels | indisponibilité fournisseur, reprise, interruption |
| Tests de performance | Caractériser le comportement sous différentes charges | latence, débit, concurrence et consommation de ressources |
| Tests de compatibilité | Vérifier la coexistence de versions, formats et configurations prises en charge | modèles, connecteurs, versions d'API et générations d'index |
| Tests d'acceptation | Vérifier que les capacités satisfont les scénarios d'usage attendus | parcours complets et critères d'acceptation métier |

Un test unitaire réussi ne garantit pas l'intégration correcte des composants. Un test de bout en bout réussi sur un scénario unique ne garantit pas la couverture des exigences, des risques ou des cas limites.

# 6. Couverture fonctionnelle du moteur

Les tests doivent couvrir les domaines fonctionnels validés, en respectant les responsabilités décrites dans les documents spécialisés.

| Domaine | Capacités à vérifier | Références principales |
|---|---|---|
| Gouvernance et identité | organisation, applications clientes, identités, rôles, permissions, accès et isolation | 04, 05, 10, 11 |
| Knowledge Bases | création, configuration, associations de sources et d'éléments, séparation des bases | 04, 05, 11 |
| Sources et ingestion documentaire | connexion autorisée, découverte, import, extraction, normalisation, versions, retrait et reprise | 04, 06, 11, 14 |
| Chunking et embeddings | cohérence des représentations, provenance, compatibilité des modèles et gestion des changements | 04, 07, 11 |
| Indexation | cohérence des index, générations, entrées, activation et retrait | 04, 06, 08, 14 |
| Recherche | recherche vectorielle, textuelle, hybride, filtrage, classement, multi-bases et absence de résultat | 05, 08, 11 |
| Génération | modes direct, retrieval-only et retrieval-augmented, contexte, réponse, refus et citations | 04, 08, 09, 11 |
| API et intégration cliente | contrats, authentification, autorisations, validation des demandes, erreurs et suivi des opérations | 10, 11 |
| Données structurées | découverte, description, autorisation, interrogation, limites, provenance et fraîcheur | 04, 05, 08, 11, 12 |
| Administration et opérations | configuration, suivi des Jobs, audit, erreurs et observabilité | 04, 10, 11, 14 |

La couverture doit inclure des scénarios nominaux, des entrées invalides, des ressources absentes, des autorisations refusées, des résultats vides, des opérations partielles et des interruptions pertinentes.

# 7. Vérification de la chaîne de connaissance

Le cycle de connaissance doit être vérifié comme un ensemble cohérent, en complément des tests propres à chaque étape.

## 7.1 Ingestion et provenance

Les tests vérifient notamment que :

- une connaissance conserve son origine identifiable ;
- un document et ses versions restent distinguables ;
- les contenus extraits sont rattachés à la version correcte ;
- une erreur ou une interruption n'est pas présentée comme une ingestion complète ;
- une actualisation ne mélange pas silencieusement des versions différentes ;
- le retrait d'un élément d'une Knowledge Base ne supprime pas automatiquement la source ou les autres associations ;
- les contenus dérivés ne perdent pas le périmètre d'accès de leur origine.

## 7.2 Chunking et embeddings

Les tests et évaluations doivent permettre de vérifier :

- la cohérence entre le contenu source et les Chunks produits ;
- l'absence de perte ou de duplication non maîtrisée dans le découpage ;
- la conservation des références de provenance et de position ;
- la compatibilité entre les embeddings comparés ou utilisés ensemble ;
- l'identification du modèle et de la configuration ayant produit chaque représentation ;
- le comportement du moteur lorsqu'une représentation est absente, obsolète ou incompatible.

La qualité du découpage et celle des embeddings doivent être analysées séparément de la qualité finale du retrieval afin d'aider à localiser les causes d'une dégradation.

## 7.3 Indexation et recherche

Les tests vérifient notamment que :

- une génération d'index représente un état identifiable et cohérent ;
- les entrées d'index correspondent aux éléments autorisés et effectivement intégrés ;
- les résultats proviennent d'une génération compatible avec la recherche demandée ;
- les connaissances retirées ou révoquées ne restent pas accessibles au-delà des garanties définies ;
- les filtres d'accès s'appliquent avant la restitution des résultats ;
- la recherche fonctionne correctement lorsqu'il n'existe aucun résultat pertinent.

## 7.4 Génération et citations

Les tests vérifient que :

- `RETRIEVAL_ONLY` retourne des résultats sans présenter de réponse générée ;
- `DIRECT_LLM` est identifiable comme une génération sans récupération préalable dans une Knowledge Base ;
- `RETRIEVAL_AUGMENTED` utilise uniquement le contexte autorisé effectivement récupéré ;
- les citations référencent des éléments réels ayant contribué à la réponse ;
- les résultats simplement récupérés ne sont pas automatiquement présentés comme des citations ;
- une réponse ne prétend pas être fondée sur la Knowledge Base lorsque le mode utilisé ne l'est pas ;
- l'insuffisance ou l'absence de connaissances peut conduire à une réponse prudente, une demande de précision ou une absence de réponse selon les règles définies.

# 8. Évaluation de la qualité RAG

## 8.1 Principe

L'évaluation RAG mesure plusieurs dimensions qui doivent rester distinguables. Une réponse apparemment correcte peut être issue d'un mauvais résultat de recherche, d'une connaissance fortuite ou d'une affirmation non justifiée. L'évaluation doit donc examiner le retrieval, le contexte fourni au modèle, la réponse et les citations.

## 8.2 Dimensions d'évaluation

| Dimension | Question évaluée | Exemples de critères |
|---|---|---|
| Pertinence du retrieval | Les éléments utiles sont-ils retrouvés ? | présence des éléments attendus, pertinence des premiers résultats, couverture des informations nécessaires |
| Qualité du classement | Les résultats les plus utiles apparaissent-ils suffisamment tôt ? | ordre des résultats pertinents et stabilité du classement |
| Qualité du contexte | Le contexte retenu est-il suffisant, pertinent et non contradictoire ? | précision, couverture, redondance et bruit du contexte |
| Pertinence de la réponse | La réponse traite-t-elle effectivement la demande ? | adéquation à la question, complétude proportionnée et absence de digression |
| Fidélité au contexte | Les affirmations sont-elles soutenues par les connaissances fournies ? | absence d'affirmations non étayées, respect des limites des sources |
| Exactitude factuelle | Les informations produites correspondent-elles aux références disponibles ? | faits, valeurs, dates, relations et interprétations corrects |
| Qualité des citations | Les références permettent-elles de vérifier les affirmations ? | exactitude, pertinence, couverture et traçabilité |
| Gestion de l'incertitude | Le moteur reconnaît-il les connaissances insuffisantes ? | refus ou réserve appropriés, absence d'invention, demande de précision pertinente |
| Qualité des résultats structurés | Les données retournées correspondent-elles à la demande et aux contraintes ? | exactitude des valeurs, respect des filtres, agrégations et provenance |
| Qualité combinée | Les données documentaires et structurées sont-elles combinées sans contradiction ? | cohérence, attribution correcte des sources et absence de double comptage injustifié |

## 8.3 Métriques de recherche

Selon le cas d'usage, l'évaluation du retrieval peut utiliser des mesures de pertinence et de classement telles que :

- **Precision@k :** proportion de résultats pertinents parmi les premiers résultats considérés.
- **Recall@k :** proportion des éléments pertinents attendus retrouvés parmi les premiers résultats.
- **Mean Reciprocal Rank (MRR) :** position du premier résultat pertinent, agrégée sur les cas évalués.
- **Normalized Discounted Cumulative Gain (nDCG) :** qualité du classement en tenant compte des niveaux de pertinence et de la position des résultats.

Le choix des métriques dépend du besoin évalué. Elles ne sont pas toutes pertinentes pour chaque recherche, et leurs définitions de pertinence doivent être documentées dans le jeu d'évaluation.

## 8.4 Métriques de génération

L'évaluation de la génération peut examiner notamment :

- la pertinence de la réponse par rapport à la demande ;
- la fidélité des affirmations au contexte récupéré ;
- l'exactitude par rapport aux références disponibles ;
- la couverture des éléments attendus ;
- la qualité et la précision des citations ;
- la capacité à reconnaître les limites des connaissances ;
- l'absence d'information confidentielle ou non autorisée.

Une réponse n'a pas à reprendre textuellement une réponse de référence pour être considérée comme correcte. L'évaluation doit tenir compte du sens, des éléments factuels attendus et des contraintes propres au cas.

## 8.5 Métriques des données structurées

Les évaluations des résultats structurés peuvent porter sur :

- l'exactitude des éléments et valeurs retournés ;
- la conformité aux filtres, conditions et limites autorisés ;
- l'exactitude des agrégations ou relations attendues ;
- l'exhaustivité au regard du périmètre demandé ;
- la fraîcheur annoncée des données ;
- la conservation de la provenance vers la source et la ressource interrogées.

Les critères d'évaluation doivent distinguer une erreur dans l'interprétation de la demande, une erreur de planification, une erreur d'exécution sur la source et une erreur de restitution.

# 9. Jeux de données et cas d'évaluation

## 9.1 Evaluation Dataset

Un `Evaluation Dataset` représente un ensemble organisé de cas destiné à évaluer une capacité, une version ou une configuration du moteur.

Un jeu d'évaluation doit posséder un périmètre et un objectif identifiables. Il peut être spécialisé par domaine fonctionnel, langue, type de source, catégorie de demande, risque ou dimension de qualité.

Un jeu de données d'évaluation n'est pas nécessairement une copie de données de production. Il doit être constitué de données de test contrôlées, de données publiques, de données synthétiques ou de données réelles dûment autorisées et protégées.

## 9.2 Evaluation Case

Un `Evaluation Case` représente un scénario individuel du jeu d'évaluation.

Selon son objectif, un cas peut inclure conceptuellement :

- une demande ou situation d'entrée ;
- le contexte d'utilisation pertinent ;
- les connaissances ou ressources de référence ;
- les résultats considérés pertinents, éventuellement avec des niveaux de pertinence ;
- les faits, éléments ou contraintes attendus dans la réponse ;
- les conditions d'autorisation applicables ;
- les critères et métriques adaptés au cas.

Tous les cas n'ont pas besoin des mêmes références. Un cas destiné à tester l'absence de réponse pertinente doit notamment permettre de vérifier que le moteur ne fabrique pas une réponse supposée.

## 9.3 Qualité et gouvernance des jeux d'évaluation

Les jeux d'évaluation doivent :

1. Être versionnés ou autrement identifiables dans le temps.
2. Conserver l'origine et les conditions d'utilisation des données de référence.
3. Être représentatifs des demandes, sources, langues et difficultés visées.
4. Inclure des cas nominaux, limites, ambigus, négatifs et adverses adaptés au périmètre.
5. Éviter les doublons qui fausseraient artificiellement les résultats.
6. Séparer autant que nécessaire les cas utilisés pour le réglage de ceux utilisés pour l'évaluation finale.
7. Protéger les données personnelles, confidentielles et les secrets.
8. Être révisés lorsque les sources, connaissances, attentes ou usages changent.
9. Documenter les limites de couverture et les biais connus.

Les données de référence ne doivent pas être exposées au modèle évalué au point de rendre l'évaluation artificiellement facile ou de provoquer une fuite entre données d'entraînement, réglage et évaluation.

# 10. Évaluateurs et jugement de qualité

## 10.1 Références explicites

Lorsque cela est possible, les résultats doivent être comparés à des références définies et vérifiables : documents ou passages pertinents, valeurs attendues, faits requis, résultats structurés attendus ou critères d'acceptation.

Les références doivent être contrôlées et leur niveau de certitude connu. Une réponse de référence ne doit pas être considérée comme infaillible lorsqu'elle est elle-même ambiguë, incomplète ou dépendante d'un contexte évolutif.

## 10.2 Évaluation humaine

L'évaluation humaine est nécessaire pour les dimensions qui nécessitent un jugement qualitatif ou contextuel, notamment la pertinence réelle, la clarté, la suffisance de la réponse et la gravité d'une erreur.

Les consignes d'évaluation doivent être définies pour limiter les divergences entre évaluateurs. Les désaccords significatifs doivent pouvoir être identifiés et examinés plutôt que masqués par une moyenne.

## 10.3 Évaluateurs automatisés et LLM-as-a-Judge

Un évaluateur automatisé, y compris un LLM utilisé comme juge, peut compléter les références déterministes et l'évaluation humaine.

Son résultat ne constitue pas une vérité indépendante. Sa fiabilité doit être mesurée par comparaison avec un ensemble de jugements humains ou de références vérifiées. Les biais, la sensibilité à la formulation, les variations de modèle et les erreurs de notation doivent être pris en compte.

Aucun résultat produit par un LLM juge ne doit, à lui seul, valider une exigence critique de sécurité, d'autorisation, d'intégrité ou de confidentialité.

# 11. Reproductibilité et comparabilité

## 11.1 Contexte d'une évaluation

Pour permettre une interprétation correcte d'un résultat, une `Evaluation Run` doit être rattachable, selon le périmètre du test, aux informations pertinentes telles que :

- la version du moteur et de ses composants ;
- la version de l'`Evaluation Dataset` ;
- les `Evaluation Metric` utilisées et leurs définitions ;
- les Knowledge Bases et les instantanés ou états de connaissances concernés ;
- les versions de sources ou de données de référence pertinentes ;
- les générations d'index utilisées ;
- les configurations de chunking, d'embeddings et de recherche ;
- le fournisseur, le modèle et la configuration de génération ;
- les instructions, modèles de prompt et paramètres de génération concernés ;
- les conditions d'exécution utiles à l'interprétation des résultats.

Le niveau de détail conservé doit être proportionné à l'objectif de reproductibilité et respecter les règles de sécurité. Les secrets et données sensibles ne doivent pas être copiés dans les rapports d'évaluation.

## 11.2 Répétabilité et variabilité

La répétition d'une évaluation ne garantit pas nécessairement des résultats identiques, notamment lorsque des modèles externes, des données évolutives ou des services non déterministes sont utilisés.

Les évaluations doivent distinguer :

- la répétabilité dans des conditions identiques ou contrôlées ;
- la reproductibilité à partir des versions et configurations identifiées ;
- la variabilité inhérente à certains fournisseurs ou modèles ;
- les changements réels de qualité entre deux versions ou configurations.

Lorsque des résultats varient, l'écart doit être interprété avec les conditions d'exécution, et ne pas être automatiquement considéré comme une régression ou une amélioration.

# 12. Régression et critères d'acceptation

## 12.1 Références de comparaison

Une version ou configuration évaluée peut être comparée à une référence acceptée précédemment. Cette comparaison doit porter sur le même périmètre ou expliciter les différences de jeux de données, métriques et conditions d'exécution.

Les comparaisons doivent permettre d'identifier :

- les améliorations ;
- les dégradations ;
- les changements neutres ;
- les résultats non comparables ;
- les nouvelles limites ou les risques introduits.

## 12.2 Seuils et critères

Les seuils d'acceptation sont définis pour une capacité ou un contexte donné, en fonction des exigences, des risques et des usages visés.

Ils peuvent être distincts selon les domaines, les langues, les catégories de demandes, les niveaux de criticité et les métriques. Ils doivent être établis avant l'évaluation à laquelle ils s'appliquent, afin d'éviter un ajustement opportuniste après observation des résultats.

Cette spécification ne fixe pas de valeur numérique universelle de précision, de rappel, de fidélité, de latence ou de taux d'erreur. Ces valeurs nécessitent des objectifs validés et des mesures adaptées au contexte réel.

## 12.3 Dégradations critiques

Un score global satisfaisant ne peut pas compenser :

- une fuite de données entre organisations ou périmètres d'accès ;
- une restitution d'informations non autorisées ;
- une exécution non autorisée sur une source structurée ;
- une perte grave de provenance ou d'intégrité ;
- une citation inventée ou liée à une source inexistante lorsqu'elle présente une preuve ;
- une régression qui invalide une exigence critique ou un contrat essentiel.

Ces cas nécessitent un traitement explicite selon leur gravité et les règles de validation applicables.

# 13. Sécurité, confidentialité et robustesse

Les tests de sécurité sont obligatoires et indépendants des scores de qualité RAG.

Ils couvrent selon les risques :

- les accès non authentifiés ou insuffisamment autorisés ;
- les tentatives d'accès à une autre organisation, une autre Knowledge Base ou une autre ressource ;
- les changements de rôle, de permission, de Membership ou de Resource Access Grant ;
- les retraits et révocations d'accès ;
- les fuites de données dans les résultats, réponses, citations, erreurs, journaux ou rapports ;
- les contenus documentaires non fiables et les tentatives d'injection d'instructions ;
- les demandes visant à contourner les permissions ou à accéder à des champs ou ressources interdits ;
- les requêtes structurées malveillantes, hors périmètre ou excessivement coûteuses ;
- les réponses qui révèlent des secrets ou des informations absentes du contexte autorisé ;
- les comportements en cas de panne d'un fournisseur ou d'un composant de sécurité.

Les scénarios adverses doivent être contrôlés et réalisés dans des environnements et sur des données autorisés. Les tests ne doivent pas introduire de risque non maîtrisé pour des sources ou systèmes externes.

# 14. Résilience, performance et comportement opérationnel

Les tests doivent contribuer à caractériser la capacité du moteur à fonctionner dans des conditions normales et dégradées.

Les dimensions examinées peuvent comprendre :

- temps de réponse selon les capacités sollicitées ;
- débit et comportement sous demandes concurrentes ;
- évolution du comportement avec le volume de connaissances et de résultats ;
- comportement lorsque les sources, modèles ou fournisseurs sont lents ou indisponibles ;
- traitement des délais dépassés, interruptions et réponses partielles ;
- reprise et prévention des doublons après une interruption ;
- disponibilité et cohérence des générations d'index ;
- dégradation contrôlée lorsqu'une capacité secondaire n'est pas disponible ;
- traçabilité suffisante des opérations et des erreurs.

Les objectifs chiffrés de performance, de disponibilité, de capacité et de reprise relèvent des exigences validées et du document 14 — Déploiement et scalabilité. Le document 13 définit comment ces objectifs doivent être vérifiés, sans les inventer.

# 15. Organisation des campagnes d'évaluation

Les activités de vérification peuvent être organisées à différents moments du cycle de vie du moteur :

| Moment | Objectif principal | Activités pertinentes |
|---|---|---|
| Pendant le développement | Détecter rapidement les erreurs locales | tests unitaires, composants et contrats |
| Lors de l'intégration | Vérifier la coopération entre modules | tests d'intégration, provenance, sécurité et cohérence |
| Avant une livraison | Vérifier les parcours et risques essentiels | tests de bout en bout, régression, sécurité, compatibilité et évaluation RAG |
| Périodiquement | Détecter les dérives et changements externes | campagnes d'évaluation complètes, suivi de qualité et tests de résilience |
| Après un changement important | Vérifier les conséquences d'une évolution | campagne ciblée et comparaison avec les références concernées |
| En environnement opérationnel | Détecter les incidents sans exposer les données | contrôles de disponibilité et scénarios synthétiques autorisés |

La fréquence, le degré d'automatisation et les environnements d'exécution seront définis dans les spécifications d'implémentation et de déploiement. Aucun outil ou fournisseur d'intégration continue n'est imposé ici.

# 16. Résultats, preuves et traçabilité

Les résultats doivent permettre de comprendre ce qui a été testé, dans quelles conditions, avec quels critères et avec quel résultat.

Le modèle de données fournit les concepts suivants :

- `Evaluation Dataset` : ensemble organisé de cas d'évaluation ;
- `Evaluation Case` : cas individuel du jeu ;
- `Evaluation Metric` : mesure utilisée ;
- `Evaluation Run` : exécution identifiée sur un jeu et un contexte donnés ;
- `Evaluation Result` : résultat associé à un cas et à une ou plusieurs métriques.

Les rapports et éléments de preuve doivent, selon leur nature, permettre de retrouver :

- l'exigence ou le risque couvert ;
- le scénario et les conditions d'exécution ;
- les versions et configurations pertinentes ;
- le résultat observé et le résultat attendu ;
- la métrique et la méthode d'évaluation utilisées ;
- les écarts, limites, erreurs et décisions prises ;
- l'état de validation ou les actions correctives restantes.

Un rapport de campagne ne doit pas être interprété comme une preuve que toutes les exigences sont couvertes si sa portée est partielle. Les résultats doivent mentionner les absences de couverture et les limites connues.

# 17. Responsabilités et frontières entre spécifications

Le document 13 définit le cadre de vérification et d'évaluation. Il ne devient pas propriétaire des capacités testées.

| Sujet | Spécification responsable | Contribution du document 13 |
|---|---|---|
| Exigences et critères attendus | 01 — Cahier des charges | Traduire les exigences en vérifications et preuves |
| Architecture et responsabilités | 02 et 03 | Vérifier les contrats et frontières définis |
| Entités et traçabilité des évaluations | 04 — Modèle de données | Utiliser les entités d'évaluation existantes |
| Knowledge Bases et périmètres | 05 — Knowledge Bases | Vérifier associations, séparation et accès |
| Ingestion documentaire | 06 — Pipeline ingestion | Vérifier intégrité, cycle de vie et provenance |
| Chunking et embeddings | 07 — Chunking et embeddings | Évaluer la qualité et la cohérence des représentations |
| Retrieval et indexation | 08 — Moteur de recherche | Évaluer pertinence, classement et filtrage |
| Génération | 09 — Génération et LLM | Évaluer fidélité, utilité, incertitude et citations |
| Contrats externes | 10 — API | Vérifier conformité et compatibilité des interfaces |
| Sécurité | 11 — Sécurité et isolation | Tester les règles de protection et d'autorisation |
| Données structurées | 12 — Données structurées | Évaluer exactitude, autorisation, provenance et fraîcheur |
| Exécution et capacité opérationnelle | 14 — Déploiement et scalabilité | Vérifier les objectifs opérationnels définis |

# 18. Correspondance avec les exigences fonctionnelles

Le document 13 contribue à la vérification des 28 exigences fonctionnelles. La couverture ci-dessous identifie les domaines de test principaux ; elle ne remplace pas les critères d'acceptation détaillés définis dans le cahier des charges et les spécifications spécialisées.

| Exigences | Domaine concerné | Vérifications principales |
|---|---|---|
| FR-001 à FR-006 | Organisations, applications, identités, autorisations et Knowledge Bases | propriété, séparation des périmètres, accès autorisés et refus d'accès |
| FR-007 | Sources | identité, connexion, association et accès contrôlé |
| FR-008 à FR-010 | Importation, extraction et cycle de vie documentaires | versions, intégrité, provenance, mise à jour, retrait et reprise |
| FR-011 à FR-012 | Chunking et embeddings | cohérence des représentations, compatibilité et provenance |
| FR-013 | Indexation et réindexation | cohérence des générations, disponibilité et retrait des entrées |
| FR-014 à FR-017 | Recherche vectorielle, textuelle, hybride, filtrage et classement | pertinence, classement, absence de résultat et respect des autorisations |
| FR-018 à FR-021 | Génération, citations et connaissances insuffisantes | fidélité, exactitude, traçabilité, modes distincts et gestion de l'incertitude |
| FR-022 à FR-024 | Connexion, interrogation et combinaison des données structurées | interprétation, autorisation, exécution, exactitude et provenance |
| FR-025 à FR-026 | Interface publique et gestion des requêtes | conformité des contrats, validation, erreurs et suivi |
| FR-027 à FR-028 | Administration, journalisation et supervision | privilèges, audit, traçabilité et suivi des opérations |

# 19. Correspondance avec les exigences non fonctionnelles

Les vingt exigences non fonctionnelles doivent être vérifiées par des méthodes adaptées. Certaines exigent plusieurs types de tests ou une preuve architecturale et opérationnelle, et ne peuvent pas être réduites à une seule métrique.

| Exigence | Besoin | Contribution des tests et de l'évaluation |
|---|---|---|
| NFR-001 | Isolation des organisations | tests d'accès croisé, de séparation des ressources et de contexte |
| NFR-002 | Contrôle des accès | tests positifs et négatifs d'authentification, autorisation et révocation |
| NFR-003 | Protection des données sensibles | tests de fuite, minimisation, exposition et conservation |
| NFR-004 | Protection contre les injections | tests adverses sur les contenus, demandes et contextes transmis au modèle |
| NFR-005 | Gestion des secrets | vérification de l'absence de divulgation dans les réponses, journaux et rapports |
| NFR-006 | Intégrité des connaissances | tests de cohérence entre sources, versions et représentations dérivées |
| NFR-007 | Résilience | tests de panne, reprise, interruption et fonctionnement dégradé |
| NFR-008 | Traçabilité | vérification de la provenance et de l'identification des opérations |
| NFR-009 | Cohérence après modification | tests de mise à jour, synchronisation, retrait et réindexation |
| NFR-010 | Performance | campagnes de mesure selon les objectifs définis |
| NFR-011 | Évolutivité | tests de capacité et vérifications lors de l'augmentation des volumes ou usages |
| NFR-012 | Traitements volumineux | tests de charge, concurrence, suivi et reprise des traitements |
| NFR-013 | Modularité | tests de contrats et de non-régression aux frontières des modules |
| NFR-014 | Extensibilité | tests d'ajout ou de remplacement de fournisseurs, sources et capacités compatibles |
| NFR-015 | Maintenabilité | vérification de la clarté des tests, de la traçabilité et de la détection des régressions |
| NFR-016 | Interopérabilité | tests de contrats, formats, versions et intégrations clientes ou fournisseurs |
| NFR-017 | Portabilité | vérifications sur les environnements et configurations déclarés compatibles |
| NFR-018 | Observabilité | tests de production et de consultation des événements, métriques et traces attendus |
| NFR-019 | Évaluation de la qualité | jeux d'évaluation versionnés, métriques définies et résultats comparables |
| NFR-020 | Vérifiabilité | liens entre exigences, cas, métriques, exécutions, résultats et preuves |

# 20. Éléments explicitement non décidés

Les sujets suivants sont volontairement reportés et ne constituent pas des décisions implicites :

1. Les frameworks, bibliothèques et outils de tests.
2. Les plateformes d'intégration continue et d'exécution des campagnes.
3. Les environnements techniques et infrastructures de test.
4. Les seuils chiffrés d'acceptation pour chaque métrique ou objectif opérationnel.
5. Les jeux de données d'évaluation définitifs et leurs contenus métier.
6. Les algorithmes précis de calcul des métriques et les outils d'évaluation.
7. Le choix des évaluateurs humains, modèles juges ou services externes.
8. Les protocoles de constitution, de revue et de publication des jeux de référence.
9. Le calendrier détaillé des campagnes et leur fréquence.
10. Les règles de blocage ou d'autorisation de livraison propres à chaque environnement.
11. Les procédures de test de pénétration et les modalités d'intervention de tiers.
12. Les objectifs chiffrés de latence, débit, disponibilité, capacité et reprise, qui relèvent des exigences et du document 14.
13. Les modalités techniques de conservation des rapports et preuves.
14. Les éventuelles exigences réglementaires ou sectorielles supplémentaires qui seraient définies pour un contexte d'utilisation particulier.

Ces choix seront précisés après validation des exigences et des spécifications concernées, puis consignés dans les décisions d'architecture lorsqu'ils engagent le projet.

# 21. Conditions de validation

Le document pourra être validé lorsque :

1. La distinction entre tests logiciels et évaluation de la qualité RAG sera claire.
2. Les niveaux et catégories de tests couvriront les responsabilités du moteur sans imposer d'outil.
3. Les principaux domaines fonctionnels disposeront de catégories de vérifications identifiables.
4. La chaîne de connaissance préservera les exigences d'intégrité et de provenance.
5. Le retrieval, la génération, les citations et les données structurées seront évalués selon des dimensions distinctes.
6. Les jeux d'évaluation et cas de référence seront gouvernés et versionnés.
7. Les évaluateurs humains et automatisés auront des limites clairement définies.
8. La reproductibilité et la comparaison entre versions ou configurations seront couvertes.
9. Les tests de sécurité et d'isolation resteront indépendants des scores de qualité.
10. La régression, les critères d'acceptation et le traitement des dégradations critiques seront définis au niveau conceptuel.
11. Les 28 exigences fonctionnelles et les 20 exigences non fonctionnelles auront une contribution de test ou d'évaluation identifiée.
12. Les frontières avec les documents 01 à 12 et 14 seront cohérentes.
13. Les choix techniques, outils et seuils chiffrés prématurés seront exclus.

# 22. Conclusion

La stratégie de tests et d'évaluation de Universal RAG Engine doit démontrer à la fois la conformité du système et la qualité des connaissances qu'il restitue et des réponses qu'il produit.

Elle distingue les tests logiciels de l'évaluation RAG, organise la vérification selon les domaines et les risques, et s'appuie sur des jeux d'évaluation, des métriques explicites, des références vérifiables et des exécutions traçables.

Elle considère la sécurité, l'isolation, l'intégrité et la provenance comme des exigences essentielles qui ne peuvent pas être compensées par de bonnes performances moyennes.

**La qualité du moteur ne se résume pas à produire une réponse plausible : elle doit être vérifiable, justifiable, reproductible dans des conditions identifiées et conforme aux autorisations applicables.**
