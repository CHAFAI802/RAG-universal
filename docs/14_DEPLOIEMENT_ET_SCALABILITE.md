# UNIVERSAL RAG ENGINE

## Document 14 — Déploiement et scalabilité

**Version :** 1.0
**Statut :** VALIDATED
**Projet :** RAG-universal
**Date :** 2026-11-21

---

# 1. Objectif

Ce document définit les principes de déploiement, d'exploitation et de montée en capacité de Universal RAG Engine.

Il précise notamment :

- Les frontières entre architecture logique et architecture de déploiement.
- Les principes de structuration des environnements et des unités de déploiement.
- Les exigences de disponibilité, de résilience et de continuité de service.
- Les principes de dimensionnement et de gestion de capacité.
- Les stratégies conceptuelles de montée en charge des différentes catégories de traitements.
- La gestion des ressources partagées et la prévention des interférences entre organisations.
- Les principes de sauvegarde, de restauration et de reprise après incident.
- Le cycle de livraison, de mise à jour et de retour à une version précédente.
- L'observabilité opérationnelle et le suivi de la santé du moteur.
- Les frontières avec la sécurité, les tests et les autres spécifications.

Cette spécification reste au niveau fonctionnel, architectural et opérationnel. Elle ne choisit ni fournisseur cloud, ni système d'exploitation, ni orchestrateur, ni outil de déploiement, ni base de données, ni technologie de supervision. Elle ne fixe pas non plus de seuils chiffrés qui ne sont pas définis dans les exigences approuvées.

# 2. Références et dépendances

Cette spécification s'appuie sur les documents suivants :

- `00_VISION_ET_OBJECTIFS.md` — vision, indépendance applicative et principes fondateurs.
- `DEPENDENCY_MAP.md` — dépendances entre les spécifications.
- `DECISION_LOG.md` — décisions architecturales et conceptuelles retenues.
- `01_CAHIER_DES_CHARGES.md` — exigences fonctionnelles et non fonctionnelles.
- `02_ARCHITECTURE_GLOBALE.md` — domaines et capacités générales du moteur.
- `03_ARCHITECTURE_MODULAIRE.md` — responsabilités et frontières des modules.
- `04_MODELE_DE_DONNEES.md` — ressources, configurations, Jobs, Audit Events et provenance.
- `05_KNOWLEDGE_BASES.md` — périmètres des connaissances, associations et règles d'utilisation.
- `06_PIPELINE_INGESTION.md` — traitements documentaires et gestion du cycle de vie des connaissances.
- `07_CHUNKING_ET_EMBEDDINGS.md` — traitements de préparation et de représentation des contenus.
- `08_MOTEUR_DE_RECHERCHE.md` — indexation, retrieval et disponibilité des résultats.
- `09_GENERATION_ET_LLM.md` — génération, fournisseurs et modes de traitement des requêtes.
- `10_API_SPECIFICATION.md` — contrats et comportements exposés aux applications clientes.
- `11_SECURITE_ET_ISOLATION.md` — authentification, autorisation, isolation et protection.
- `12_DONNEES_STRUCTUREES.md` — connexions, interrogation et restitution des données structurées.
- `13_TESTS_ET_EVALUATION.md` — vérification, évaluation, preuves et critères de qualité.

Ce document organise les conditions d'exécution des capacités définies par ces spécifications. Il ne redéfinit ni leurs responsabilités fonctionnelles ni leurs contrats.

# 3. Périmètre et principes fondamentaux

## 3.1 Déploiement indépendant des applications clientes

Universal RAG Engine est un moteur autonome consommé par des applications clientes distinctes. Son déploiement ne doit pas dépendre du cycle de livraison, de la technologie ou de l'infrastructure d'une application cliente particulière.

Une application cliente peut évoluer, être remplacée ou être indisponible sans que cela impose de reconstruire le moteur. Réciproquement, une évolution interne du moteur doit pouvoir être livrée sans exiger une modification simultanée de toutes les applications clientes, dans les limites des contrats de compatibilité définis par le document 10.

## 3.2 Architecture logique et déploiement physique

Les domaines et modules définis dans les documents 02 et 03 représentent des responsabilités logiques. Ils ne déterminent pas automatiquement le nombre de processus, de serveurs, de conteneurs ou de services physiques.

Plusieurs modules peuvent être regroupés dans une même unité de déploiement. Un module ou une capacité peut également être isolé lorsque les besoins de charge, de sécurité, de disponibilité, d'évolution ou d'exploitation le justifient.

La séparation physique doit découler d'un besoin démontré et non d'une correspondance systématique entre chaque module logique et un service indépendant.

## 3.3 Principes directeurs

Le déploiement et l'exploitation respectent les principes suivants :

1. Le moteur conserve son indépendance par rapport aux applications clientes.
2. Les responsabilités logiques restent identifiables, même lorsque plusieurs capacités sont déployées ensemble.
3. Les composants peuvent évoluer et être dimensionnés selon leurs profils de charge lorsqu'une séparation est justifiée.
4. Les données persistantes et les traitements sans état ne sont pas confondus.
5. L'augmentation de capacité ne doit pas affaiblir l'isolation des organisations ni les autorisations.
6. Une panne partielle ne doit pas être présentée comme un fonctionnement complet et normal.
7. Les sauvegardes et restaurations doivent préserver la cohérence des connaissances, de leurs versions et de leurs représentations dérivées.
8. Les changements doivent être vérifiables, traçables et réversibles dans la mesure compatible avec les migrations effectuées.
9. Les choix d'infrastructure doivent rester remplaçables autant que raisonnablement possible.
10. Les objectifs opérationnels doivent être mesurables et reliés aux besoins réels, sans introduire de seuils arbitraires dans cette spécification.

# 4. Modèle général de déploiement

## 4.1 Capacités logiques concernées

Le déploiement doit prendre en compte les ensembles de capacités définis par l'architecture globale :

- **Control Plane :** gouvernance, administration, configuration et gestion des périmètres.
- **Knowledge Processing :** accès aux sources, ingestion, préparation, embeddings et indexation.
- **Query Engine :** réception des requêtes, retrieval, accès aux données structurées et génération.
- **Cross-cutting Services :** sécurité, gestion des opérations, audit et observabilité.
- **External Provider Adapters :** intégration des fournisseurs et environnements externes.

Ces ensembles servent à raisonner sur les dépendances, la capacité et les défaillances. Ils ne constituent pas une topologie physique imposée.

## 4.2 Profils de déploiement

Le moteur peut être exploité selon différents profils, à choisir en fonction des usages, des contraintes et des capacités disponibles :

1. **Profil regroupé :** plusieurs capacités du moteur sont exécutées dans un ensemble d'unités réduit. Ce profil peut convenir à un environnement de développement, de validation ou à une installation de capacité limitée.
2. **Profil séparé :** les capacités dont les charges ou les contraintes diffèrent sont réparties entre plusieurs unités de déploiement. Cette séparation peut concerner notamment les interfaces, les traitements différés, la recherche ou les intégrations externes.
3. **Profil distribué :** les capacités sont réparties sur plusieurs ressources d'exécution ou domaines d'infrastructure afin de répondre à des besoins de capacité, de disponibilité ou d'isolation.
4. **Profil hybride :** certaines capacités sont hébergées par l'environnement du moteur tandis que d'autres sont fournies par des services externes ou administrés séparément.

Ces profils sont des catégories conceptuelles et peuvent évoluer. Aucun profil n'est déclaré obligatoire pour toutes les installations.

## 4.3 Unités de déploiement

Une unité de déploiement regroupe un ou plusieurs composants qui sont installés, configurés, mis à jour et exploités comme un ensemble cohérent.

La définition des unités doit tenir compte :

- Des responsabilités et dépendances fonctionnelles.
- Des besoins de ressources et des profils de charge.
- Des exigences de sécurité et des frontières de confiance.
- Des besoins de disponibilité et des conséquences d'une panne.
- Des besoins de mise à jour et de compatibilité.
- Des possibilités de supervision, de sauvegarde et de restauration.

Le découpage définitif des unités relève de la conception technique et peut différer selon le profil de déploiement.

# 5. Environnements et séparation des usages

## 5.1 Environnements distincts

Le cycle de vie du moteur peut nécessiter des environnements distincts pour le développement, les tests, la validation avant livraison et l'exploitation opérationnelle.

La présence et le nombre exacts de ces environnements dépendent du contexte d'exploitation. Cette spécification n'impose pas une nomenclature ni un nombre fixe d'environnements.

## 5.2 Isolation entre environnements

Les environnements ne doivent pas partager implicitement leurs données, secrets, identités techniques ou ressources sensibles.

Les données utilisées pour les tests et évaluations doivent être choisies et protégées conformément aux exigences de sécurité et de confidentialité. Une copie de données opérationnelles ne peut pas être considérée comme automatiquement appropriée pour un environnement non opérationnel.

## 5.3 Promotion des versions

Une version ou configuration destinée à un environnement plus sensible doit provenir d'un processus de livraison identifiable. Les écarts de configuration entre environnements doivent être connus et maîtrisés.

Une validation dans un environnement ne constitue une preuve valable pour un autre que si les différences pertinentes d'infrastructure, de configuration, de dépendances et de données sont prises en compte.

# 6. Gestion des composants avec et sans état

## 6.1 Capacités d'exécution sans état persistant local

Les capacités qui ne conservent pas leur état métier de manière locale peuvent, lorsque leur conception le permet, être exécutées en plusieurs instances afin de répartir la charge ou d'améliorer la disponibilité.

Leur multiplication ne doit pas créer de dépendance à une session locale ou à un état temporaire non partagé qui compromettrait la continuité des opérations.

## 6.2 Ressources et services conservant un état

Les données métier, fichiers originaux, versions, configurations, index, générations, résultats ou autres informations persistantes doivent disposer d'un mécanisme de conservation et de cohérence adapté à leur nature.

Leur réplication, partitionnement, sauvegarde ou restauration doivent respecter leurs relations et leur cycle de vie. La multiplication des instances de calcul ne suffit pas à rendre une ressource avec état hautement disponible.

## 6.3 État temporaire et opérations suivies

Les opérations longues ou différées doivent pouvoir être suivies conformément aux concepts `Job` et aux contrats API correspondants.

L'interruption ou le remplacement d'une unité de calcul ne doit pas faire disparaître silencieusement l'état durable d'une opération déjà acceptée. La reprise, l'annulation ou la déclaration d'échec doivent préserver une représentation fidèle de son résultat.

Les mécanismes précis de coordination, de file d'attente, de verrouillage ou de stockage de l'état relèvent de la conception technique.

# 7. Scalabilité et montée en capacité

## 7.1 Scalabilité adaptée aux profils de charge

Le moteur traite des catégories de charge différentes :

- Les requêtes interactives adressées à l'API.
- Les recherches documentaires et structurées.
- Les générations utilisant des modèles de langage.
- Les accès à des fournisseurs externes.
- Les traitements différés d'ingestion, d'extraction, de chunking, d'embeddings et d'indexation.
- Les opérations d'administration, d'audit et d'évaluation.

Ces catégories peuvent avoir des besoins différents en calcul, mémoire, réseau, stockage, concurrence et temps d'exécution. Le dimensionnement doit donc être fondé sur des profils d'utilisation distincts plutôt que sur une hypothèse de charge uniforme.

## 7.2 Montée en capacité verticale et horizontale

La capacité peut être augmentée par l'allocation de ressources supplémentaires à une unité existante ou par l'ajout d'instances d'exécution lorsque les composants et leurs dépendances le permettent.

Le choix entre ces approches dépend notamment :

- Des limites propres aux composants et aux ressources persistantes.
- Du degré de parallélisme possible.
- Des contraintes de cohérence et de coordination.
- Des coûts et limites imposés par les fournisseurs externes.
- Des objectifs de disponibilité et de latence.

La scalabilité horizontale ne peut pas être présumée pour un composant qui dépend d'un état local, d'une ressource exclusive ou d'une capacité externe non extensible.

## 7.3 Traitements différés et capacité de traitement

Les traitements d'ingestion et de préparation peuvent être coûteux et de durée variable. Leur capacité doit être gérée sans rendre les requêtes interactives inutilement indisponibles.

Le moteur doit pouvoir distinguer la demande acceptée, le traitement en attente, le traitement en cours, le traitement terminé et le traitement en échec, selon le modèle de suivi défini par les documents 04, 06 et 10.

La concurrence des traitements doit être maîtrisée afin d'éviter la saturation des fournisseurs, des stockages ou des autres capacités partagées.

## 7.4 Gestion des pointes et de la saturation

Le moteur doit reconnaître les situations dans lesquelles la demande dépasse temporairement ou durablement la capacité disponible.

Dans ces situations, les comportements doivent rester explicites : limitation, attente, rejet contrôlé, priorité ou dégradation fonctionnelle peuvent être envisagés selon la nature de la capacité.

Une surcharge ne doit pas conduire à accepter indéfiniment des opérations qui ne peuvent pas être exécutées, à perdre des demandes acceptées ou à contourner les contrôles de sécurité.

Les quotas, limites, priorités et mécanismes de régulation précis restent à définir selon les profils d'exploitation.

## 7.5 Élasticité et évolution de la capacité

Lorsque l'environnement le permet, la capacité d'exécution peut être adaptée à l'évolution de la charge. Toute adaptation doit préserver la disponibilité des données, la cohérence des opérations en cours, l'isolation et la traçabilité.

Les délais d'adaptation, les règles de déclenchement et les limites d'élasticité sont des paramètres techniques à déterminer ultérieurement.

# 8. Isolation des ressources et équité entre organisations

Le moteur doit pouvoir accueillir plusieurs organisations et plusieurs Knowledge Bases sans qu'une charge excessive provenant d'un périmètre dégrade silencieusement les autres.

La gestion de capacité doit prendre en compte :

- La séparation logique des données et des ressources protégées.
- Les limites de consommation applicables aux organisations, applications ou capacités.
- Les effets des traitements lourds sur les requêtes interactives.
- Les accès concurrents aux fournisseurs et sources externes.
- Les ressources partagées, notamment calcul, mémoire, stockage, réseau et services externes.
- La possibilité d'identifier l'origine d'une consommation anormale.

La régulation de capacité ne remplace jamais les autorisations définies dans le document 11. Une limite de consommation ou une priorité d'exécution ne constitue pas un droit d'accès à une ressource.

Les politiques précises de quotas, de facturation ou de répartition de coûts ne sont pas décidées dans cette spécification.

# 9. Disponibilité et continuité de service

## 9.1 Disponibilité des capacités

La disponibilité doit être examinée par capacité et par dépendance. Le moteur ne doit pas être considéré comme entièrement disponible si une capacité essentielle à l'opération demandée est indisponible.

Les objectifs de disponibilité doivent distinguer, lorsque nécessaire, l'API, le contrôle et l'administration, l'ingestion, le retrieval, la génération, les données structurées et les services externes.

## 9.2 Défaillances partielles

Une panne d'un fournisseur de génération, d'une source structurée, d'un service d'embeddings ou d'une ressource d'indexation ne doit pas nécessairement être assimilée à une panne totale du moteur.

Lorsque les contrats et les règles fonctionnelles le permettent, certaines capacités indépendantes peuvent rester utilisables. Par exemple, une recherche seule peut rester possible lorsque la génération est indisponible, à condition que les résultats soient effectivement disponibles et autorisés.

Le moteur doit toutefois signaler clairement la capacité indisponible et ne pas présenter un résultat incomplet comme complet.

## 9.3 Redondance et domaines de défaillance

La conception de déploiement doit identifier les ressources dont la panne entraîne une interruption importante et déterminer si une redondance est nécessaire.

La redondance doit être évaluée au niveau des unités d'exécution, des données persistantes, des accès réseau et des dépendances externes. Plusieurs instances ne procurent pas une réelle tolérance aux pannes si elles dépendent toutes d'une même ressource critique non protégée.

Les choix de réplication, de bascule et de distribution géographique sont reportés à la conception technique.

## 9.4 Maintenance et indisponibilités planifiées

Les opérations de maintenance doivent être préparées afin de limiter leurs effets sur les utilisateurs et les opérations en cours.

Lorsqu'une interruption est nécessaire, son périmètre, ses conséquences, les capacités concernées et les conditions de retour au service doivent être identifiables.

# 10. Résilience et fonctionnement dégradé

## 10.1 Gestion des dépendances externes

Les fournisseurs de modèles, les sources documentaires ou structurées et les autres services externes peuvent être indisponibles, lents, limités ou temporairement incompatibles.

Le moteur doit distinguer ces défaillances des erreurs internes et éviter qu'une dépendance défaillante provoque une accumulation incontrôlée de demandes ou une indisponibilité étendue.

Les délais d'attente, tentatives de reprise, mécanismes d'isolation des pannes et politiques de repli seront définis dans la conception technique et les contrats d'intégration concernés.

## 10.2 Reprise contrôlée

Une reprise doit tenir compte de l'état durable de l'opération et de ses effets éventuels avant l'interruption.

La répétition d'un traitement ne doit pas créer de doublons incontrôlés, activer des représentations incomplètes ou annuler des données valides. Les garanties attendues doivent être précisées selon la nature de chaque opération.

## 10.3 Fonctionnement dégradé

Un fonctionnement dégradé n'est acceptable que si ses limites sont explicites et si les garanties de sécurité, d'intégrité et de provenance restent respectées.

Le moteur doit notamment distinguer :

- Une capacité pleinement disponible.
- Une capacité disponible avec des limites déclarées.
- Une capacité partiellement disponible avec un résultat partiel identifiable.
- Une capacité indisponible.

Le choix des fonctions maintenues ou suspendues dépend de leurs dépendances et des contrats fonctionnels. Aucun contournement de sécurité ne peut être utilisé comme mécanisme de repli.

# 11. Sauvegarde, restauration et protection des données persistantes

## 11.1 Périmètre de sauvegarde

La stratégie de sauvegarde doit identifier les catégories de données nécessaires à la reconstruction cohérente du service, notamment :

- Les données de gouvernance, d'identité et de configuration.
- Les organisations, Knowledge Bases, sources et associations.
- Les documents, versions et artefacts originaux lorsque le moteur en assure la conservation.
- Les contenus extraits et représentations dérivées selon leur importance et leur possibilité de reconstruction.
- Les configurations d'index et les informations nécessaires à leur reconstruction ou restauration.
- Les opérations suivies, journaux d'audit et informations de traçabilité soumises à conservation.
- Les jeux et résultats d'évaluation lorsque leur conservation est requise.

Les secrets et éléments d'authentification sont protégés selon les règles du document 11 et ne doivent pas être exposés dans les sauvegardes ou rapports.

## 11.2 Données originales et données dérivées

La possibilité de reconstruire une donnée dérivée à partir d'une source ne signifie pas que cette source sera toujours accessible, inchangée ou disponible au moment d'une restauration.

La stratégie doit distinguer les données originales difficiles ou impossibles à reconstituer, les métadonnées nécessaires à la cohérence, et les représentations qui peuvent éventuellement être recalculées.

La décision de sauvegarder ou de reconstruire une représentation doit tenir compte du coût, du délai, de la reproductibilité, de la provenance et des exigences de continuité.

## 11.3 Cohérence des sauvegardes

Une sauvegarde doit permettre de retrouver un état cohérent entre les ressources persistantes liées. Une collection de copies indépendantes réalisées à des moments incompatibles ne constitue pas nécessairement une sauvegarde cohérente du moteur.

La cohérence attendue doit couvrir les relations entre les sources, les éléments de connaissance, les versions, les représentations dérivées, les index et leurs générations.

## 11.4 Restauration et vérification

La restauration doit être considérée comme une capacité opérationnelle à vérifier, et non comme une simple existence de fichiers de sauvegarde.

Les procédures de restauration doivent prévoir la vérification de l'intégrité, de la cohérence, de l'accès, de la traçabilité et de la disponibilité des capacités restaurées.

Des exercices de restauration doivent être réalisés selon une fréquence et un périmètre définis dans les politiques opérationnelles. Les résultats et limites doivent être documentés.

## 11.5 Objectifs de reprise

Les objectifs de perte de données acceptable et de délai de remise en service doivent être définis selon les catégories de données et les besoins du service.

Aucune valeur de RPO, de RTO, de fréquence de sauvegarde ou de durée de conservation n'est fixée dans cette version. Ces objectifs doivent être décidés, justifiés et vérifiables avant la mise en exploitation correspondante.

# 12. Livraison, mise à jour et retour arrière

## 12.1 Versionnement des composants et configurations

Les versions du moteur, de ses unités de déploiement, de ses interfaces et de ses configurations doivent être identifiables.

La traçabilité d'une installation doit permettre de déterminer quelles versions et configurations sont actives dans un environnement donné.

## 12.2 Compatibilité des évolutions

Une évolution peut concerner le code, les contrats, les configurations, les données persistantes, les index ou les intégrations externes.

Les mises à jour doivent prendre en compte la compatibilité entre les versions qui interagissent et les conséquences éventuelles sur les données existantes. Les règles de versionnement de l'API restent définies par le document 10.

## 12.3 Migrations et modifications persistantes

Les changements qui modifient les structures ou significations des données persistantes doivent être préparés et vérifiés avant leur application.

Une migration ne doit pas être considérée comme réversible par défaut. Lorsqu'un retour à une version précédente ne peut pas être réalisé sans risque après une migration, la stratégie de retour doit prévoir une solution adaptée, telle qu'une restauration contrôlée ou une évolution corrective.

Les mécanismes physiques de migration et leur orchestration relèvent de la conception technique.

## 12.4 Déploiement progressif

Lorsque le profil d'exploitation le permet, les mises à jour peuvent être introduites progressivement afin de réduire l'impact d'une évolution défectueuse.

La possibilité d'un déploiement progressif dépend de la compatibilité des versions, de la gestion de l'état, des migrations et des dépendances. Cette approche n'est pas une garantie de disponibilité sans interruption.

## 12.5 Retour arrière

La stratégie de livraison doit identifier les conditions dans lesquelles une version peut être rétablie et les cas où un retour arrière est impossible ou dangereux.

Le retour arrière doit préserver l'intégrité des données, la cohérence des contrats et la sécurité. Il ne doit pas réintroduire une version vulnérable ou incompatible sans décision explicite.

# 13. Configuration opérationnelle et gestion des secrets

Les configurations nécessaires à l'exploitation doivent être distinguées des données métier et des secrets.

Elles doivent permettre d'identifier les paramètres propres à un environnement, les paramètres propres à une organisation ou à une capacité, et les références aux dépendances externes.

Les secrets, clés, identifiants de connexion et autres valeurs sensibles sont gérés exclusivement selon les principes du document 11. Ils ne doivent pas être intégrés en clair dans les artefacts de livraison, les journaux ou les rapports.

Une modification de configuration doit être traçable et ne doit pas créer implicitement un accès ou une autorisation nouvelle.

Les formats, sources de configuration, outils et mécanismes de rotation ne sont pas choisis ici.

# 14. Observabilité et exploitation opérationnelle

## 14.1 Objectifs de l'observabilité

L'observabilité doit permettre de comprendre l'état du moteur, de détecter les dégradations, de localiser les défaillances et d'évaluer la capacité disponible.

Elle doit couvrir les capacités logiques et leurs dépendances, sans se limiter à vérifier que le processus principal est actif.

## 14.2 Informations de suivi

Selon la capacité concernée, le suivi opérationnel peut notamment porter sur :

- La disponibilité des interfaces et capacités principales.
- Les délais de réponse, volumes et taux d'échec.
- Les files ou charges de traitements différés.
- La durée, le résultat et les erreurs des Jobs.
- L'utilisation des ressources de calcul, mémoire, stockage et réseau.
- La disponibilité et les limites rencontrées auprès des fournisseurs externes.
- L'état des index et la disponibilité des générations requises.
- Les erreurs d'accès aux sources et aux données structurées.
- Les événements d'administration, de sécurité et d'audit.
- Les résultats des sauvegardes, restaurations et opérations de maintenance.

## 14.3 Journaux, métriques et traces

Les journaux, métriques et traces répondent à des besoins complémentaires. Leur collecte doit permettre d'établir des liens entre une demande, les opérations associées et les dépendances impliquées, lorsque cela est nécessaire et autorisé.

Les informations collectées doivent respecter les règles de minimisation, de confidentialité, de rétention et de contrôle d'accès du document 11.

## 14.4 Alertes et incidents

Les alertes doivent être reliées à des conditions de dégradation ou de risque opérationnel clairement identifiées. Elles doivent permettre de distinguer un incident réel d'une variation normale de charge.

Les procédures de traitement des incidents, d'escalade, de communication et de clôture doivent être définies dans les procédures opérationnelles du projet.

# 15. Gestion de capacité et planification des ressources

La capacité doit être évaluée à partir de scénarios représentatifs et de mesures recueillies dans les environnements concernés.

La planification doit tenir compte notamment :

1. Du nombre et de la répartition des organisations, applications clientes et Knowledge Bases.
2. Du volume des sources, documents, versions, ressources structurées et connaissances dérivées.
3. Du volume et de la fréquence des requêtes interactives.
4. Du profil des traitements différés et de leurs besoins en calcul.
5. De la concurrence d'accès aux fournisseurs et aux sources.
6. De la taille des données persistantes et de leur évolution.
7. Des besoins de sauvegarde, de restauration, de rétention et de supervision.
8. Des pointes de consommation et des marges nécessaires à la continuité du service.
9. Des limites et coûts des dépendances externes.

Les estimations doivent être révisées lorsque les usages, les volumes, les modèles ou les dépendances changent.

Les capacités maximales, valeurs de dimensionnement, ratios, budgets et seuils d'alerte ne sont pas fixés dans ce document. Ils devront être déterminés par des mesures, des tests et des décisions documentées.

# 16. Portabilité et évolution de l'environnement

Le moteur doit limiter les dépendances inutiles à un environnement d'hébergement précis. Les responsabilités fonctionnelles doivent rester séparées des choix de déploiement lorsque cela est raisonnablement possible.

La portabilité n'implique pas que toutes les infrastructures soient équivalentes ni que le déplacement d'une installation soit automatique. Les différences de stockage, de réseau, de sécurité, de performance, de services managés et de dépendances externes doivent être évaluées.

Toute migration d'environnement doit préserver les données, les configurations, les autorisations, les contrats et la traçabilité, ou rendre explicites les adaptations nécessaires.

# 17. Responsabilités et frontières entre spécifications

Le document 14 définit les principes de déploiement et d'exploitation. Il ne devient pas propriétaire des règles fonctionnelles des capacités qu'il héberge.

| Sujet | Document responsable | Contribution du document 14 |
|---|---|---|
| Exigences et objectifs opérationnels | 01 — Cahier des charges | Relier les objectifs de capacité, de disponibilité et de fiabilité aux besoins approuvés |
| Domaines et capacités générales | 02 — Architecture globale | Définir les éléments logiques à prendre en compte dans le déploiement |
| Frontières et responsabilités modulaires | 03 — Architecture modulaire | Identifier les candidats à un déploiement regroupé ou séparé sans imposer une correspondance physique |
| Ressources, configurations et Jobs | 04 — Modèle de données | Préserver la cohérence des informations persistantes et des opérations suivies |
| Knowledge Bases et périmètres | 05 — Knowledge Bases | Respecter la séparation des espaces de connaissances |
| Ingestion et traitements documentaires | 06 — Pipeline ingestion | Prendre en compte les charges, reprises et états des traitements |
| Chunking et embeddings | 07 — Chunking et embeddings | Prendre en compte les besoins de calcul et dépendances des traitements |
| Recherche et indexation | 08 — Moteur de recherche | Préserver disponibilité, cohérence et capacité des index et recherches |
| Génération et fournisseurs LLM | 09 — Génération et LLM | Prendre en compte les dépendances, limites et charges de génération |
| Contrats d'intégration | 10 — API | Préserver la compatibilité des interfaces lors des évolutions |
| Sécurité et isolation | 11 — Sécurité et isolation | Appliquer les contrôles de sécurité, de secrets, d'accès et de journalisation |
| Données structurées | 12 — Données structurées | Prendre en compte les connexions, limites et indisponibilités des sources |
| Tests et évaluation | 13 — Tests et évaluation | Vérifier les objectifs opérationnels, la résilience, la capacité et les restaurations |

# 18. Correspondance avec les exigences fonctionnelles

Le déploiement et la scalabilité ne remplacent pas les capacités fonctionnelles. Ils doivent toutefois fournir les conditions d'exécution, de continuité et de suivi permettant de les exploiter.

| Exigence | Domaine concerné | Contribution de cette spécification |
|---|---|---|
| FR-001 à FR-006 | Organisations, applications, identités, autorisations et Knowledge Bases | Fournir un environnement d'exécution préservant la séparation des périmètres et les contrôles définis |
| FR-007 à FR-013 | Sources, ingestion, cycle documentaire, chunking, embeddings et indexation | Assurer la capacité d'exécuter et de suivre les traitements associés |
| FR-014 à FR-017 | Recherche vectorielle, textuelle, hybride, filtrage et classement | Préserver les ressources et la capacité nécessaires à la recherche autorisée |
| FR-018 à FR-021 | Génération, citations et gestion des connaissances insuffisantes | Gérer les dépendances de génération et permettre des comportements explicitement dégradés lorsque compatibles |
| FR-022 à FR-024 | Données structurées | Prendre en compte les connexions, limites, charges et indisponibilités des sources |
| FR-025 à FR-026 | Interface publique et gestion des requêtes | Maintenir la disponibilité des interfaces et le suivi des demandes acceptées |
| FR-027 à FR-028 | Administration, journalisation et supervision | Permettre l'exploitation contrôlée, la traçabilité et le suivi opérationnel |

Cette contribution porte sur les conditions opérationnelles. Les règles fonctionnelles et les contrats restent définis dans leurs spécifications propriétaires.

# 19. Correspondance avec les exigences non fonctionnelles

Les exigences non fonctionnelles nécessitent des contributions combinées de l'architecture, de la sécurité, des composants fonctionnels, des tests et de l'exploitation. Le tableau suivant décrit la contribution spécifique du déploiement et de la scalabilité.

| Exigence | Besoin | Contribution de cette spécification | Spécification complémentaire |
|---|---|---|---|
| NFR-001 | Isolation des organisations | Préserver la séparation des ressources, traitements et domaines de consommation | 11 — Sécurité et isolation |
| NFR-002 | Contrôle des accès | Fournir des frontières d'exécution et de configuration compatibles avec les contrôles d'accès | 11 — Sécurité et isolation |
| NFR-003 | Protection des données sensibles | Encadrer l'hébergement, la conservation, la sauvegarde et l'accès opérationnel aux données | 11 — Sécurité et isolation |
| NFR-004 | Protection contre les injections | Éviter qu'un fonctionnement distribué ou dégradé contourne les validations et contrôles | 11 — Sécurité et isolation ; 09 — Génération et LLM |
| NFR-005 | Gestion des secrets | Prévoir une gestion séparée des configurations et secrets dans tous les environnements | 11 — Sécurité et isolation |
| NFR-006 | Intégrité des connaissances | Préserver la cohérence entre données originales, représentations dérivées et index lors des opérations de déploiement et de reprise | 04 — Modèle de données ; 06 à 08 |
| NFR-007 | Résilience | Définir les principes de redondance, défaillance partielle, reprise et restauration | 13 — Tests et évaluation |
| NFR-008 | Traçabilité | Maintenir le suivi des versions, opérations, événements et dépendances | 04 — Modèle de données ; 11 — Sécurité et isolation |
| NFR-009 | Cohérence après modification | Maîtriser les mises à jour, migrations, reprises et évolutions des représentations | 06 — Pipeline ingestion ; 08 — Moteur de recherche |
| NFR-010 | Performance | Définir les principes de mesure, dimensionnement et allocation des ressources | 13 — Tests et évaluation |
| NFR-011 | Évolutivité | Permettre l'augmentation de capacité et l'évolution des unités de déploiement | 02 et 03 — Architecture ; 13 — Tests et évaluation |
| NFR-012 | Traitements volumineux | Organiser la capacité, la concurrence et la régulation des traitements différés | 06 — Pipeline ingestion ; 13 — Tests et évaluation |
| NFR-013 | Modularité | Préserver les frontières logiques même lorsque les modules sont regroupés physiquement | 03 — Architecture modulaire |
| NFR-014 | Extensibilité | Permettre l'ajout ou le remplacement de capacités et de dépendances sans imposer une refonte globale | 03 — Architecture modulaire ; 10 — API |
| NFR-015 | Maintenabilité | Encadrer les mises à jour, la configuration, les migrations et l'exploitation | 13 — Tests et évaluation |
| NFR-016 | Interopérabilité | Préserver la capacité d'intégration avec les applications, sources et fournisseurs | 10 — API ; 06 et 12 |
| NFR-017 | Portabilité | Limiter les dépendances de déploiement inutiles et expliciter les conditions de migration | 02 et 03 — Architecture |
| NFR-018 | Observabilité | Définir les informations de santé, de capacité, d'erreur et de suivi opérationnel | 04 — Modèle de données ; 11 — Sécurité et isolation |
| NFR-019 | Évaluation de la qualité | Permettre des environnements et ressources reproductibles pour les campagnes d'évaluation | 13 — Tests et évaluation |
| NFR-020 | Vérifiabilité | Rendre les versions, configurations, incidents, restaurations et preuves opérationnelles identifiables | 13 — Tests et évaluation |

Cette correspondance ne signifie pas que le déploiement garantit seul chacune de ces exigences. Les contrôles fonctionnels, architecturaux et de sécurité restent définis dans les spécifications complémentaires.

# 20. Éléments explicitement non décidés

Les sujets suivants sont volontairement reportés et ne doivent pas être interprétés comme des décisions implicites :

1. Le fournisseur cloud, l'hébergeur ou le type d'infrastructure.
2. Le système d'exploitation, le format d'image, le runtime ou le système de conteneurisation.
3. L'orchestrateur, le gestionnaire de processus ou la plateforme d'exécution.
4. Le nombre, la taille et l'emplacement des unités de déploiement.
5. Le découpage final des modules entre processus, services et machines.
6. Les moteurs de stockage, bases de données, systèmes de fichiers et technologies de cache.
7. Les technologies de réplication, partitionnement, sauvegarde et restauration.
8. Les solutions de supervision, de journalisation, de métriques et de traces.
9. Les outils de livraison, d'intégration continue et de gestion des configurations.
10. Les objectifs chiffrés de disponibilité, latence, débit, capacité, concurrence et consommation.
11. Les valeurs RPO et RTO, les fréquences de sauvegarde et les durées de rétention.
12. Les quotas, limites, priorités et mécanismes précis de régulation.
13. Les politiques de déploiement progressif, de bascule et de retour arrière propres à chaque infrastructure.
14. Les régions, zones de disponibilité et stratégies de distribution géographique.
15. Les budgets d'infrastructure, modèles de facturation et règles d'allocation de coûts.
16. Les procédures opérationnelles détaillées, astreintes et niveaux de support.

Ces décisions seront prises après validation des besoins, mesures représentatives et études techniques. Lorsqu'elles engagent durablement l'architecture, elles seront consignées dans le Decision Log ou dans un ADR approprié.

# 21. Conditions de validation

Le document pourra être validé lorsque :

1. La distinction entre architecture logique et déploiement physique sera claire.
2. Les profils de déploiement seront présentés sans imposer une topologie unique.
3. Le découpage des unités de déploiement sera fondé sur les besoins et non sur une séparation automatique des modules.
4. Les environnements et leurs principes d'isolation seront définis au niveau conceptuel.
5. Les composants avec état et sans état seront distingués.
6. Les besoins de montée en capacité interactive et de traitements différés seront couverts.
7. La scalabilité préservera l'isolation et l'équité entre organisations.
8. La disponibilité, les défaillances partielles et le fonctionnement dégradé seront traités sans compromettre la sécurité ni l'intégrité.
9. Les principes de sauvegarde, restauration et reprise seront cohérents avec le modèle de données.
10. Le cycle de livraison, les migrations, la compatibilité et le retour arrière seront couverts.
11. L'observabilité et la gestion opérationnelle seront délimitées par rapport à la sécurité et aux tests.
12. Les 28 exigences fonctionnelles et les 20 exigences non fonctionnelles auront une contribution opérationnelle identifiée.
13. Les frontières avec les documents 00 à 13 seront cohérentes.
14. Les objectifs et seuils chiffrés non approuvés, ainsi que les choix technologiques prématurés, seront exclus.
15. Les sujets reportés seront explicitement documentés.

# 22. Conclusion

Le déploiement et la scalabilité de Universal RAG Engine doivent permettre d'exploiter ses capacités de manière indépendante, fiable et évolutive, tout en préservant les frontières logiques, les données, les autorisations et la traçabilité.

Le moteur doit pouvoir fonctionner dans des environnements de taille et de complexité différentes, depuis un profil regroupé jusqu'à une architecture distribuée, sans que le modèle fonctionnel dépende d'une topologie ou d'un fournisseur particulier.

La capacité, la disponibilité, la reprise et l'exploitation doivent être démontrables par des mesures, des tests et des procédures vérifiables.

**Le déploiement adapte les ressources à l'usage du moteur ; il ne doit jamais modifier les garanties fonctionnelles, de sécurité et de cohérence qui fondent Universal RAG Engine.**
