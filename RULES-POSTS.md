# Projet 2 : publications annonces Woto (fil Facebook et Instagram)

Séparé du projet 1 (stories : `RULES.md`, `state.json`, `README.md`). Ne jamais modifier les fichiers du projet 1 depuis ce projet.

Créneaux, heure de Bruxelles : 7h30, 12h15, 17h00, 19h30 et 21h30, tous les jours (5 par jour, décision de Vincent du 23 novembre 2026). Une publication Facebook et une publication Instagram par créneau. Programmation 48 h à l'avance : chaque passage remplit tous les créneaux vides d'aujourd'hui (pas encore passés), de demain et du surlendemain. Planning dans `POSTS.md` (aujourd'hui, demain, après-demain), suivi dans `state-posts.json`.

## Choix de la voiture
- Scan complet : `python3 scripts/scan.py --out inventory.json`. Ne jamais choisir depuis la page d'accueil.
- Garages : `garages.json` est partagé avec le projet 1 (lecture). Tout vendeur du scan absent de `garages.json` est un nouveau garage : l'ajouter avec son logo recadré sur le nom dans `assets/logos/`, il passe en priorité.
- Un garage différent à chaque créneau. Un garage ne repasse pas tant que tous les autres garages ayant des voitures disponibles ne sont pas passés (sur `state-posts.json`). Ordre aléatoire à chaque tour.
- Une voiture présente dans `state-posts.json` OU dans `state.json` (stories) ne passe pas, sauf en boucle (voir Boucle sans fin).
- Réservation (règle de Vincent du 23 novembre 2026, après le doublon Renault Espace) : dès qu'une voiture est choisie, `git pull`, revérifier `state.json` et `state-posts.json`, puis ajouter l'entrée avec `"status": "reserve"` et pousser sur main AVANT de rendre les visuels. Si le push est refusé, `git pull --rebase` et revérifier. Les publications ont la priorité sur les stories : en cas de doublon, c'est la story qui change (la tâche stories s'en charge).
- Écarter : vendue ou indisponible, prix ou kilométrage absent, écart de kilométrage fiche/description sans explication, aucune photo correcte. Car-Pass dans la description : afficher ce chiffre.

## Boucle sans fin (règle de Vincent du 23 novembre 2026)
- La diffusion ne s'arrête jamais. Priorité 1 : les voitures jamais montrées (ni dans `state.json`, ni dans `state-posts.json`), et parmi elles les nouveaux arrivages repérés au scan, en premier.
- Quand il n'y a plus aucune voiture jamais montrée, on recommence la boucle : une voiture déjà montrée redevient possible, en prenant celle dont la dernière apparition (story ou publication) est la plus ancienne. Elle doit toujours être au stock, au même prix ou au nouveau prix affiché sur la fiche.
- Même en boucle, une voiture ne repasse pas si elle est apparue (story ou publication) dans les 7 derniers jours, et jamais deux fois le même jour.
- Les nouveaux arrivages restent toujours prioritaires, même au milieu d'une boucle.
- Ne jamais laisser un créneau vide faute de voiture « neuve » : on passe à la boucle.

## Visuel
- `scripts/render_post.py`, gabarit B validé par Vincent le 6 novembre 2026. Deux fichiers par créneau : `--format fb` (1080 × 1080) et `--format ig` (1080 × 1350), dans `posts/AAAA-MM-JJ/woto-<voiture>-<7h30|12h15|17h|19h30|21h30>-<fb|ig>.jpg`.
- Logo de `assets/logos/` et sa bulle blanche. Première photo sans cadre ni bandeau, voiture entière : régler `--focus`, `--vfocus` et `--photo-h` (790 à 850 en ig) pour que toit, roues et pare-chocs ne soient jamais coupés. Regarder chaque JPEG avant publication. Jamais d'image générée par IA.

## Texte de la publication (identique Facebook et Instagram)
```
Véhicule disponible sur Woto.

<Modèle court> · <prix>
<km> · <année> · <carburant> · <Auto|Manuelle>
Chez <nom du garage>

L'annonce complète vous attend sur l'app et le site Woto.
```
Pas de lien dans le texte : la page a épuisé son quota mensuel de liens dans les publications (Meta, compte sans Meta One, retour le 1er de chaque mois). Même « woto.be » écrit seul est détecté et bloque la programmation. Les liens Woto vont donc dans le premier commentaire, où ils restent cliquables (vérifié le 6 novembre 2026).
Jamais de tag de page : en tapant le nom du garage, Facebook propose une page (ex. « Luxury Cars Center SRL ») et le retour à la ligne l'accepte. Toujours appuyer sur Échap juste après le nom du garage, puis vérifier dans l'aperçu que la ligne « Chez … » est en noir, sans lien. Attention : l'aperçu de l'agenda peut masquer un tag (vu le 7 novembre : « BCS Franzese » est sorti en « BCS Franzese Automobile 🔥 »). Après programmation, rouvrir la publication Facebook avec « Modifier la publication » et vérifier que le texte du champ est exactement celui tapé. Le but est de ramener les gens sur Woto, jamais sur une page Facebook.
Ne jamais citer AutoScout24 ni un autre site d'annonces.

## Programmation (Meta Business Suite, Claude in Chrome)
Compositeur : `https://business.facebook.com/latest/composer/?asset_id=1202971056232237&business_id=1632957036893573`
1. Deux publications séparées par créneau : une avec « Publier dans » = Woto seul (visuel fb), une avec woto_app seul (visuel ig).
2. Visuel : copier le JPEG dans `/mnt/user-data/outputs/` et le passer directement à `file_upload` depuis ce chemin (vérifié le 12 novembre 2026). Plus besoin du dossier Mac `Woto Stories` : c'est lui qui a bloqué le créneau du 12/11 7h30. Astuce `HTMLInputElement.prototype.click` : surcharger pour garder le champ dans `window.__fi`, cliquer « Ajouter une photo/vidéo », rattacher le champ à `document.body`, le trouver avec `find`.
3. Facebook : désactiver « Partager dans la story Facebook » et confirmer « Ne pas partager cette publication ».
4. « Définir la date et l'heure » : heures, minutes, puis date. Vérifier par capture date et heure, puis « Programmer ». Fenêtre boost : « Peut-être plus tard ». Ne jamais cliquer « Publier » pour un créneau futur, ne jamais booster.
5. Vérifier dans l'agenda que chaque créneau a ses deux publications (icônes Facebook et Instagram).

## Jamais de créneau vide (règle de Vincent du 12 novembre 2026)
- Chaque passage de programmation remplit tous les créneaux vides d'aujourd'hui (pas encore passés), de demain et du surlendemain, pas seulement le surlendemain.
- Créneau du jour manqué (visuel prêt mais rien dans Meta) : la tâche du premier commentaire le publie tout de suite (« Publier », Woto seul puis woto_app seul, story Facebook désactivée, « Peut-être plus tard » au boost), puis poste le commentaire. Si aucun visuel n'est prêt, elle prévient Vincent.
- Ne jamais laisser à Vincent une action « à faire à la main ».

## Premier commentaire (posté à la sortie, tâches de 7h35, 12h20, 17h05, 19h35 et 21h35)
Meta Business Suite ne programme pas de commentaire : il est posté par une tâche planifiée, sur la publication sortie, depuis Statistiques de la publication (Contenu > Publications et reels).
- Facebook, créneau de 7h30 seulement : `@followers` (choisir la suggestion « @followers » dans la liste) puis :
  `La <modèle>, c'est une entrée en matière. Voir l'annonce sur Woto : https://www.woto.be/<chemin de la fiche> — Tout le stock de <garage> : https://www.woto.be/professional/<slug>`
- Facebook, autres créneaux (12h15, 17h, 19h30, 21h30) : même texte sans `@followers`.
- Liens toujours sur `https://www.woto.be/...` (chemin de la fiche = URL du scan sans `https://app.woto.be/`). Échap après le nom du garage pour éviter un tag de page.
- Instagram : `La <modèle>, c'est une entrée en matière. L'annonce et tout le stock de <garage> sont sur Woto.` (sans @followers, liens non cliquables sur Instagram).
- Accord : « La » ou « Le » selon le modèle (la Porsche, la Maserati, le Kia Sportage...).
- Ne poster un commentaire qu'une fois par publication : vérifier qu'il n'existe pas déjà. Vérifier après envoi que les liens sont bleus (cliquables).

- Rattrapage (règle de Vincent du 15 novembre 2026, « comme tous les jours, ne change jamais ») : chaque passage (tâches de commentaire et programmation) vérifie aussi les créneaux d'aujourd'hui et d'hier déjà sortis dont l'entrée de state-posts.json n'a pas `"comment": "ok"`, et poste leur commentaire de la même façon (avec `@followers` pour un créneau de 7h30), jusqu'au bout, sans demander. Vu le 15/11 : Mac éteint à 7h35, commentaire de la Panda posté à 10h30 en rattrapage.

Si le Mac, Chrome ou Meta ne répond pas : ne rien contourner, prévenir Vincent ; le passage suivant rattrape.
