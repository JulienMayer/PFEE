# PFEE – Implémentation de l’Algorithme de Grover pour la Résolution de Systèmes Binaires Quadratiques

Projet de fin d’études réalisé par **Julien Mayer** et **Arthur Stievenard**, en collaboration avec **Ludovic Perret** (LIP6 – Sorbonne Université).

## 🧠 Objectif du projet

Ce projet a pour but l’implémentation de **l’algorithme de Grover** pour la résolution de **systèmes d’équations quadratiques sur F₂** (problème MQ), utilisé notamment en **cryptographie post-quantique**. En s’appuyant sur l’article scientifique _“Solving Binary MQ with Grover’s Algorithm”_ (Schwabe & Westerbaan), nous avons développé deux versions d’oracles quantiques pour expérimenter cette approche sur des cas concrets.

## 🧪 Technologies utilisées

- **Python 3**
- **Qiskit** – simulation de circuits quantiques
- **(optionnel)** Julia – pour la rédaction des équations
- **Git / GitHub** – collaboration et gestion de versions

## 📂 Contenu du dépôt

- `src/` – Code source (oracle 1, oracle 2, simulateurs)
- `Rapport PFEE.pdf` – Rapport complet du projet
- `Présentation PFEE.pptx` – Slides de soutenance
- `README.md` – Ce fichier

## 🧩 Description des oracles

Deux circuits quantiques ont été développés comme oracles pour Grover :

- **Oracle 1** : consomme plus de qubits (≈ n + m + 2) mais réduit la profondeur.
- **Oracle 2** : consomme moins de qubits (≈ n + log₂(m)) mais nécessite plus d’étapes et de portes, notamment une logique de comptage.

Les deux oracles utilisent des portes quantiques standards : `X`, `CNOT`, `Toffoli`, `SWAP`, avec une gestion fine de la réversibilité et du nettoyage des registres auxiliaires.

## 🧱 Architecture technique

- L’entrée du circuit est un système d’équations représenté sous forme de **matrices symétriques**.
- Chaque oracle est construit dynamiquement en Python à l’aide de Qiskit.
- Des exemples issus du rapport ont été utilisés pour valider les résultats.

## 🧪 Résultats

L’implémentation permet de **trouver les solutions d’un système quadratique sur F₂** avec l’algorithme de Grover. Sur un exemple de deux équations, les deux oracles retournent :

Solutions : ['011', '110', '101']


Ces résultats montrent la **cohérence fonctionnelle** des deux approches.

En termes de ressources :
| Oracle | Qubits | X gates | CNOT | Toffoli |
|--------|--------|---------|------|---------|
| 1      | 168    | 27 710  | 1 156 680 | 13 770 |
| 2      | 94     | 55 250  | 2 316 276 | 27 702 |

## 📚 Problèmes rencontrés

- Complexité du **compteur quantique** dans l’oracle 2 : initialement prévu via un polynôme primitif, il a été simplifié en encodage binaire standard.
- **Écarts** entre le nombre de portes théoriques et ceux mesurés : causés par des choix d’implémentation (compteur, transpilation).

## ✅ Apprentissage & Expérience

- **Approfondissement de Qiskit** : construction de circuits avancés, transpilation, gestion des registres.
- **Compréhension approfondie de Grover** : fonctionnement, adaptation aux problèmes MQ.
- **Travail collaboratif et rigueur scientifique** : organisation autour de réunions régulières, suivi via GitHub, partage sur Dropbox.
- **Premiers pas en Julia** : bien que non retenu, le langage a été exploré.

## 🚀 Améliorations envisagées

- Intégrer **Julia** pour l’écriture formelle et la génération automatique des équations.
- Refonte complète du **workflow Git** : passer de Dropbox à un pipeline Git + CI pour les tests automatiques.
- Optimiser le **deuxième oracle** pour réduire le coût en portes Toffoli.

## 📈 Perspectives

Ce projet illustre les limites et les potentiels du calcul quantique appliqué à la cryptanalyse. En particulier :

- Des circuits relativement compacts suffisent à casser des instances de sécurité 80 bits.
- Le compromis **temps / qubits** est central pour l’implémentation pratique d’un oracle Grover.
- L'efficacité dépend fortement de la gestion fine des portes et registres.

## 👨‍🏫 Supervision

- **Ludovic Perret**, enseignant-chercheur à Sorbonne Université, spécialiste en cryptographie post-quantique.

## 👨‍💻 Auteurs

- **Julien Mayer** – [GitHub](https://github.com/JulienMayer)
- **Arthur Stievenard**

## 📜 Licence

Ce projet est partagé à des fins académiques. Tous droits réservés aux auteurs et à leurs encadrants.

---

> *PFEE – Une application concrète de l’informatique quantique à la cryptanalyse moderne.*
