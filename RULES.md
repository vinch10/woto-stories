# Stories annonces Woto : règles

Créneaux, heure de Bruxelles : 7h30, 16h00, 20h00, tous les jours. Une story par créneau, sur Facebook et Instagram.

## Choix de la voiture
- Un garage différent à chaque passage. Un garage ne repasse pas tant que tous les autres garages connus ne sont pas passés. Ordre aléatoire à chaque tour.
- Garage nouveau repéré sur le site : l'ajouter à `garages.json`, il passe en priorité.
- Voiture au hasard dans le stock du garage, jamais une voiture déjà présente dans `state.json`, sauf si le garage n'a plus rien d'autre.
- Écarter une fiche si : voiture vendue ou fiche indisponible, prix ou kilométrage absent, kilométrage différent entre le champ et la description ou le titre, aucune photo correcte.

## Visuel
- Rendu avec `scripts/render_story.py`, sans changer le gabarit.
- Photo : première photo de la galerie sans cadre ni bandeau de garage, qui montre la voiture entière. Régler `--focus` pour centrer la voiture.
- Logo : celui de `assets/logos/` s'il existe, sinon celui de la fiche. S'il s'agit d'une affiche, garder seulement le bandeau avec le nom.
- Regarder le JPEG avant publication : voiture lisible, texte exact, logo propre. Sinon changer de photo ou de voiture.
- Jamais d'image générée par IA.

## Texte
- Modèle court (`BMW X4`), prix (`24 999 €`), puis `km  ·  année  ·  carburant  ·  boîte`, avec `Auto` ou `Manuelle`.
- Données reprises telles quelles de la fiche, rien d'inventé.
- Ne jamais citer AutoScout24 ni un autre site d'annonces.
