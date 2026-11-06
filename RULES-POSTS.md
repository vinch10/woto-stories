# Projet 2 : publications annonces Woto (fil Facebook et Instagram)

Séparé du projet 1 (stories : `RULES.md`, `state.json`, `README.md`). Ne jamais modifier les fichiers du projet 1 depuis ce projet.

Créneaux, heure de Bruxelles : 7h30 et 17h00, tous les jours. Une publication Facebook et une publication Instagram par créneau. Programmation 48 h à l'avance : chaque matin, on programme le surlendemain. Planning dans `POSTS.md` (aujourd'hui, demain, après-demain), suivi dans `state-posts.json`.

## Choix de la voiture
- Scan complet : `python3 scripts/scan.py --out inventory.json`. Ne jamais choisir depuis la page d'accueil.
- Garages : `garages.json` est partagé avec le projet 1 (lecture). Tout vendeur du scan absent de `garages.json` est un nouveau garage : l'ajouter avec son logo recadré sur le nom dans `assets/logos/`, il passe en priorité.
- Un garage différent à chaque créneau. Un garage ne repasse pas tant que tous les autres garages ayant des voitures disponibles ne sont pas passés (sur `state-posts.json`). Ordre aléatoire à chaque tour.
- Jamais deux fois le même véhicule : une voiture présente dans `state-posts.json` OU dans `state.json` (stories) ne passe pas.
- Écarter : vendue ou indisponible, prix ou kilométrage absent, écart de kilométrage fiche/description sans explication, aucune photo correcte. Car-Pass dans la description : afficher ce chiffre.

## Visuel
- `scripts/render_post.py`, gabarit B validé par Vincent le 6 novembre 2026. Deux fichiers par créneau : `--format fb` (1080 × 1080) et `--format ig` (1080 × 1350), dans `posts/AAAA-MM-JJ/woto-<voiture>-<7h30|17h>-<fb|ig>.jpg`.
- Logo de `assets/logos/` et sa bulle blanche. Première photo sans cadre ni bandeau, voiture entière : régler `--focus`, `--vfocus` et `--photo-h` (790 à 850 en ig) pour que toit, roues et pare-chocs ne soient jamais coupés. Regarder chaque JPEG avant publication. Jamais d'image générée par IA.

## Texte de la publication (identique Facebook et Instagram)
```
Véhicule disponible sur Woto.

<Modèle court> · <prix>
<km> · <année> · <carburant> · <Auto|Manuelle>
Chez <nom du garage>

L'annonce complète vous attend sur l'app et le site Woto.
```
Pas de lien dans le texte : la page a épuisé son quota mensuel de liens (Meta, compte sans Meta One, retour le 1er de chaque mois) et un lien dans le texte bloque la programmation. Ne jamais citer AutoScout24 ni un autre site d'annonces.

## Programmation (Meta Business Suite, Claude in Chrome)
Compositeur : `https://business.facebook.com/latest/composer/?asset_id=1202971056232237&business_id=1632957036893573`
1. Deux publications séparées par créneau : une avec « Publier dans » = Woto seul (visuel fb), une avec woto_app seul (visuel ig).
2. Visuel : déposer le JPEG dans le dossier Mac `Woto Stories` (device_commit_files), le récupérer (device_stage_files), puis `file_upload` depuis `/mnt/user-data/uploads/Woto Stories/`, avec la même astuce `HTMLInputElement.prototype.click` que le projet 1.
3. Facebook : désactiver « Partager dans la story Facebook » et confirmer « Ne pas partager cette publication ».
4. « Définir la date et l'heure » : heures, minutes, puis date. Vérifier par capture date et heure, puis « Programmer ». Fenêtre boost : « Peut-être plus tard ». Ne jamais cliquer « Publier » pour un créneau futur, ne jamais booster.
5. Vérifier dans l'agenda que chaque créneau a ses deux publications (icônes Facebook et Instagram).

## Premier commentaire (posté à la sortie, tâches de 7h35 et 17h05)
Meta Business Suite ne programme pas de commentaire : il est posté par une tâche planifiée, sur la publication sortie, depuis Statistiques de la publication (Contenu > Publications et reels).
- Facebook, 7h35 : `@followers` (choisir la suggestion « @followers » dans la liste) puis `La <modèle>, c'est une entrée en matière. Tout le stock de <garage> est à voir sur Woto.`
- Facebook, 17h05 : même texte sans `@followers`.
- Instagram : même texte, sans `@followers`.
- Accord : « La » ou « Le » selon le modèle (la Porsche, la Maserati, le Kia Sportage...).
- Le lien vers la page garage `https://www.woto.be/professional/<slug>` est à remettre dans le commentaire Facebook dès que le quota de liens le permet (le compositeur affiche « 0 liens restants » quand il est épuisé).
- Ne poster un commentaire qu'une fois par publication : vérifier qu'il n'existe pas déjà.

Si le Mac, Chrome ou Meta ne répond pas : ne rien contourner, prévenir Vincent.
