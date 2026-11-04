# Stories annonces Woto : règles

Créneaux, heure de Bruxelles : 7h30, 16h00, 20h00, tous les jours. Une story par créneau, sur Facebook et Instagram.

Les 3 stories du lendemain sont préparées et programmées chaque matin, et affichées dans `README.md` : Vincent voit toujours aujourd'hui et demain, et peut intervenir. Un visuel retiré par Vincent dans GHL n'est pas reprogrammé.

## Choix de la voiture
- Un garage différent à chaque passage. Un garage ne repasse pas tant que tous les autres garages connus ne sont pas passés. Ordre aléatoire à chaque tour.
- Garage nouveau repéré sur le site : l'ajouter à `garages.json`, il passe en priorité.
- Voiture au hasard dans le stock du garage, jamais une voiture déjà présente dans `state.json`, sauf si le garage n'a plus rien d'autre.
- Pas deux fois la même voiture en 7 jours. Un garage qui n'a que des voitures déjà passées dans ces 7 jours est sauté à ce tour.
- Écarter une fiche si : voiture vendue ou fiche indisponible, prix ou kilométrage absent, écart de kilométrage sans explication, aucune photo correcte.
- Kilométrage : si la description donne un chiffre certifié Car-Pass, afficher ce chiffre, même s'il diffère du champ arrondi de la fiche. Sinon, afficher le champ.

## Visuel
- Rendu avec `scripts/render_story.py`, sans changer le gabarit.
- Photo : première photo de la galerie sans cadre ni bandeau de garage, qui montre la voiture entière. Régler `--focus` pour centrer la voiture.
- Logo : celui de `assets/logos/` s'il existe, sinon celui de la fiche. S'il s'agit d'une affiche, garder seulement le bandeau avec le nom.
- Gabarit validé par Vincent le 4 novembre 2026 (courbe haute, voir `stories/2026-11-04/`) : ne pas modifier la courbe, les couleurs, la typo ni les positions.
- Regarder le JPEG avant publication et le comparer à `stories/2026-11-04/woto-annonce-trafic.jpg`. La voiture doit être entière et bien visible : toit jamais coupé par la courbe, roues et pare-chocs jamais coupés par les bords ni cachés par le bouton. Texte exact, logo propre. Si ce n'est pas le cas, régler `--focus`, changer de photo ou de voiture. Ne jamais publier un visuel qui ne respecte pas ces points.
- Jamais d'image générée par IA.

## Texte
- Modèle court (`BMW X4`), prix (`24 999 €`), puis `km  ·  année  ·  carburant  ·  boîte`, avec `Auto` ou `Manuelle`.
- Données reprises telles quelles de la fiche, rien d'inventé.
- Ne jamais citer AutoScout24 ni un autre site d'annonces.
