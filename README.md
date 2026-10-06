# AF Lix Lox — Catalogue professionnel Suisse

Catalogue de prix destiné aux salons de coiffure suisses, envoyé par WhatsApp.
Page statique, consultable sans compte, sans panier ni formulaire : les commandes
se passent dans la conversation.

Projet autonome. Il ne dépend pas du thème Shopify `aflixlox-shopify`, dont il
reprend seulement la direction artistique et les visuels produit.

## Structure

```
index.html              page générée — ne pas éditer à la main
assets/catalogue.css    direction artistique
assets/catalogue.js     navigation active + apparition des blocs
assets/img/p/           packshots, récupérés une fois sur le CDN Shopify
build/catalogue.py      le catalogue : sections, gammes, accroches, offres
build/generate.py       générateur
build/source/           export produits et descriptions de la boutique
```

## Régénérer

```sh
python3 build/generate.py             # reconstruit index.html
python3 build/generate.py --images    # télécharge aussi les visuels manquants
```

Aucune dépendance : Python 3 seul suffit.

Le script écarte automatiquement toute référence sans image ou sans description,
et signale sur la sortie d'erreur celles qu'il a laissées de côté.

## Modifier un prix ou un texte

Tout se passe dans `build/catalogue.py` :

- `PRIX_COLORATION`, `PRIX_BIDON_10L`, `PRIX_MASQUE_1500` — les tarifs confirmés
  par AF Lix Lox. Ils priment sur ceux de la boutique.
- `OFFRES_PREMIERE`, `OFFRES_SUIVANTES` — les conditions commerciales.
- `SECTIONS` — l'ordre des sections, les gammes, les noms affichés, les
  contenances et les accroches.

Les autres prix viennent de `build/source/shopify-products.json`. Pour les
rafraîchir, réexporter les produits depuis Shopify dans ce fichier
(`handle`, `title`, `price`, `status`, `image`).

## Mettre en ligne

La page est entièrement statique : n'importe quel hébergement de fichiers
convient. Avec GitHub Pages, pousser le dépôt puis activer Pages sur la branche
`main`, dossier racine.

## Points à confirmer

Voir `NOTES.md`.
