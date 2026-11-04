# Stories annonces Woto : règles

Créneaux, heure de Bruxelles : 7h30, 16h00, 20h00, tous les jours. Une story par créneau, sur Facebook et Instagram.

Les 3 stories du lendemain sont préparées et programmées chaque matin, et affichées dans `README.md` : Vincent voit toujours aujourd'hui et demain, et peut intervenir. Un visuel retiré par Vincent n'est pas reprogrammé.

## Choix de la voiture
- Avant chaque choix, scanner tout le stock avec `python3 scripts/scan.py` : il lit le sitemap des annonces et des garages, donc toutes les fiches, pas seulement la page d'accueil. Si le nombre de fiches lues diffère du sitemap, le signaler. Ne jamais choisir à partir de la page d'accueil.
- Comparer les vendeurs du scan à `garages.json` : tout vendeur absent est un nouveau garage.
- Un garage différent à chaque passage. Un garage ne repasse pas tant que tous les autres garages connus ne sont pas passés. Ordre aléatoire à chaque tour.
- Garage nouveau repéré sur le site : l'ajouter à `garages.json`, il passe en priorité.
- Voiture au hasard dans le stock du garage. Règle absolue de Vincent : ne jamais publier deux fois le même véhicule. Une voiture présente dans `state.json` ne repasse jamais, sans exception ni délai. Avant de programmer, vérifier l'URL de la fiche dans `state.json` et le calendrier Meta.
- Un garage qui n'a plus que des voitures déjà publiées est sauté, jusqu'à ce qu'il en ajoute une nouvelle. Si plus aucune voiture nouvelle n'est disponible, laisser le créneau vide et le signaler.
- Écarter une fiche si : voiture vendue ou fiche indisponible, prix ou kilométrage absent, écart de kilométrage sans explication, aucune photo correcte.
- Kilométrage : si la description donne un chiffre certifié Car-Pass, afficher ce chiffre, même s'il diffère du champ arrondi de la fiche. Sinon, afficher le champ.

## Visuel
- Rendu avec `scripts/render_story.py`, sans changer le gabarit et sans `--cta` : le visuel ne porte aucun bouton dessiné, le bouton est le vrai sticker.
- Photo : première photo de la galerie sans cadre ni bandeau de garage, qui montre la voiture entière. Régler `--focus` pour centrer la voiture.
- Logo : celui de `assets/logos/` s'il existe, sinon celui de la fiche. S'il s'agit d'une affiche, garder seulement le bandeau avec le nom.
- Gabarit validé par Vincent le 4 novembre 2026, référence : `stories/reference-gabarit.jpg`. La bulle verte ne doit jamais écraser la photo : ne pas modifier la courbe, les couleurs, la typo ni les positions.
- Regarder le JPEG avant publication et le comparer à la référence. La voiture doit être entière et bien visible : toit jamais coupé par la courbe, roues et pare-chocs jamais coupés par les bords. Le bas de la photo doit laisser la place au sticker. Texte exact, logo propre. Si ce n'est pas le cas, régler `--focus`, changer de photo ou de voiture. Ne jamais publier un visuel qui ne respecte pas ces points.
- Jamais d'image générée par IA.

## Texte
- Modèle court (`BMW X4`), prix (`24 999 €`), puis `km  ·  année  ·  carburant  ·  boîte`, avec `Auto` ou `Manuelle`.
- Données reprises telles quelles de la fiche, rien d'inventé.
- Ne jamais citer AutoScout24 ni un autre site d'annonces.

## Programmation : Meta Business Suite, deux stories séparées par créneau
Décision de Vincent du 4 novembre 2026 : le sticker Lien passé par Meta est cliquable sur Instagram, mais pas sur Facebook, où il n'est qu'une image morte. Chaque créneau donne donc deux programmations distinctes, avec le même visuel. GHL n'est plus utilisé pour les stories annonces.

Lien de chaque story : la fiche sur `https://www.woto.be/...`, pas `app.woto.be`.

Compositeur : `https://business.facebook.com/latest/story_composer/?asset_id=1202971056232237&business_id=1632957036893573`, via Claude in Chrome. Prendre une capture avant chaque clic : la fenêtre et la mise en page changent.

**Commun aux deux stories**
1. Dans « Partager sur », décocher l'autre réseau : `woto_app` pour la story Facebook, `Woto` pour la story Instagram. Vérifier le compte affiché.
2. Déposer le JPEG dans le dossier Mac `Woto Stories`, le mettre en attente pour la session, puis l'envoyer depuis `/mnt/user-data/uploads/Woto Stories/` avec `file_upload`. Il n'y a pas de champ fichier avant le clic : surcharger `HTMLInputElement.prototype.click` en JavaScript pour garder le champ dans `window.__fi`, cliquer « Ajouter une photo/vidéo », rattacher ce champ à `document.body`, puis le trouver avec `find`.

**Story Facebook : lien « Voir plus », jamais de sticker**
3. « Ajouter un lien » → coller la fiche → « Appliquer ». Le bouton devient « Modifier le lien ».

**Story Instagram : vrai sticker, jamais « Ajouter un lien »**
3. « Modifier » → « Plus de stickers » → « Lien ». Lien : la fiche. Texte personnalisé : `Voir l'annonce →`. Le formulaire remonte après la saisie du lien : reprendre une capture avant de cliquer sur le texte. Le formulaire peut garder d'anciennes valeurs : tout effacer avant de saisir. « Appliquer ».
4. Glisser le sticker en bas de la photo, sous la voiture, au-dessus du logo. Vérifier au zoom : ni voiture ni logo masqués. « Appliquer ».

**Programmer chacune**
5. « Programmer » : cliquer les heures et taper `7`, `16` ou `20`, cliquer les minutes et taper `30` ou `00`, puis choisir la date. Le calendrier peut s'ouvrir au-dessus du champ. Vérifier par capture le compte, la date et l'heure, puis « Programmer ». Ne jamais cliquer « Partager maintenant ».
6. Contrôler dans l'agenda Meta qu'il y a une story Facebook et une story Instagram au bon créneau, et ouvrir chaque aperçu : sticker sur Instagram seulement.

Une carte verte vide peut rester dans l'agenda après la suppression d'une story : aperçu indisponible et aucune date de programmation. Ne rien cliquer dessus.

Si le Mac, Chrome ou Meta ne répond pas, ne pas se rabattre sur GHL : prévenir Vincent.
