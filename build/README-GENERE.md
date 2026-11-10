# Source unique du site

**Depuis le 05/11/2026, ce dossier `build/` du dépôt est la source unique du site.**

L'ancienne source `04_SCRIPTS/build/` (et `build-et-sync.py`) est obsolète : sa copie
s'était arrêtée au 27/08/2026 alors que tout le travail suivant (polices RGPD du 19/10,
tarifs, vignettes du Coin des curieux, formulaire, Calligraphie) a été fait ici.
La relancer aurait écrasé ces modifications. Elle a été renommée `build-et-sync.py.OBSOLETE`.

## Modifier un texte du site

1. `git pull` (Béatrice publie ses articles via Sveltia CMS, qui commite sur `main`).
2. Modifier `template.html`, `context.py` ou `generate.py` dans ce dossier.
3. `cd build && python parse.py && python generate.py` (régénère les pages à la racine).
4. Vérifier en local, puis `git commit` et `git push`.

GitHub Actions relance les mêmes étapes 3 après chaque publication d'article depuis le CMS.

`exercices/index.html` n'est pas généré : c'est une page de renvoi vers `/calligraphie/`
(05/11/2026), à conserver telle quelle.
