# Sujet blanc — CI/CD sécurisé (4h)

## Contexte

Tu reprends `api-tickets`, une petite API Flask de gestion de tickets pour le
support interne. Le code fonctionne mais n'a **aucune chaîne CI/CD** et un audit
rapide a relevé plusieurs problèmes de sécurité et de configuration. Ta mission
est de mettre en place la chaîne CI/CD vue en cours et de corriger les failles.

L'application doit pouvoir exécuter **au moins le CI en local** (build + test +
scan) avant tout déploiement.

## Contenu du dépôt fourni

- `app.py` — l'API (3 ressources : index/health, tickets, import)
- `tests/test_app.py` — 5 tests pytest (ils passent déjà, ne pas les casser)
- `requirements.txt` — dépendances figées
- `Dockerfile` — image actuelle (à auditer)
- `docker-compose.yml` — stack api + postgres (à auditer)
- `.env` — variables locales (à auditer **en priorité**)
- `README.md`

## Partie 1 — CI (build, test, sécurité) — obligatoire

1. Écris un workflow GitHub Actions qui, sur push/PR :
   - installe les dépendances et lance la suite **pytest** (le test doit
     bloquer le pipeline s'il échoue) ;
   - **build** l'image Docker ;
   - scanne l'image avec **Trivy** et fait **échouer** le job sur les
     vulnérabilités `HIGH` et `CRITICAL`.
2. Corrige les failles que Trivy et ta propre lecture révèlent. Au minimum :
   - réduis la surface de l'image (base, taille, user non-root) ;
   - traite les secrets exposés ;
   - corrige ce qui, dans `app.py`, ne doit pas tourner tel quel en prod.
3. Le CI doit pouvoir tourner **en local** (explique comment : `act`, ou
   reproduction manuelle des étapes `docker build` + `trivy image` + `pytest`).

## Partie 2 — CD (déploiement sur serveur) — obligatoire

1. Étends le pipeline pour **pousser l'image sur un registre** (Docker Hub)
   après succès du CI, en gérant les identifiants proprement (secrets).
2. Décris (et, si tu as le temps, code) le déploiement sur une **VM Linux**
   distante : connexion SSH, récupération de l'image, (re)démarrage du
   conteneur. Tu peux le faire via une étape SSH dans Actions **ou** via un
   playbook **Ansible** (install Docker, pull, run, idempotent).

## Partie 3 — Adaptation cloud (bonus, comme à l'examen)

Explique précisément ce que tu changerais pour que le déploiement vise une
**VM AWS (EC2)** plutôt qu'un serveur générique : où vivent les secrets, comment
la VM s'authentifie au registre, ce qui change dans le workflow ou le playbook.

## Livrable : rapport (2–4 pages, Markdown ou PDF)

Le rapport est l'essentiel de la note. Il doit contenir :

1. **Architecture de la chaîne** : un schéma (même ASCII) build → test → scan →
   push → deploy, et en une phrase le rôle de chaque étage.
2. **Tableau des failles** : pour chaque faille trouvée — où, pourquoi c'est un
   risque, comment tu l'as corrigée. Vise 5 entrées minimum.
3. **Choix techniques** : pourquoi cette image de base, ce point de blocage
   Trivy (severity / exit-code), ce mode de déploiement. Justifie, ne décris pas.
4. **Stratégie de secrets** : ce qui était exposé, où ça vit maintenant, et
   comment le pipeline y accède.
5. **Limites & suite** : ce que tu n'as pas eu le temps de faire et comment tu
   le ferais.

## Barème indicatif (pour t'auto-évaluer)

- CI fonctionnel (build + test bloquant + Trivy bloquant) — 30 %
- Corrections de failles pertinentes et justifiées — 25 %
- CD (push registre + déploiement décrit/codé) — 20 %
- Qualité du rapport (schéma, tableau failles, justifications) — 20 %
- Adaptation AWS crédible — 5 %

> Astuce examen : commence par lire **tous** les fichiers et lister les failles
> AVANT d'écrire une ligne de YAML. Le `.env` à lui seul contient de quoi
> remplir un tiers du tableau des failles.
