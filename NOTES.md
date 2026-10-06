# Points à confirmer avant diffusion

## Sources utilisées

`products_export_1.csv` est introuvable sur le poste et absent de l'historique
Git du thème. Les données viennent donc de la boutique elle-même — celle du
nouveau site, `f8hvn5-ix.myshopify.com` — via l'API Admin : titres, statuts,
prix, visuels. Les descriptions proviennent de `data/product-descriptions.json`
du thème, c'est-à-dire des textes retravaillés pour le nouveau site.

## Prix

Tarifs confirmés, identiques à ceux de la boutique sauf pour le bidon :

| Référence | Catalogue | Boutique |
|---|---|---|
| Coloration Color 100 ml | 10.40 CHF | 10.40 CHF |
| Coloration Ekstra Color 100 ml (sans ammoniaque) | 10.90 CHF | 10.90 CHF |
| Bidon 10 L | 50.00 CHF | 72.00 CHF |
| Masque 1 500 ml | 19.45 CHF | 19.45 CHF |

Les trois bidons de 10 litres sont les **seules** références dont le prix
diffère de l'export boutique. Les 76 autres sont affichées au prix de la
boutique, sans retouche.

**Les autres prix** n'ont pas été vérifiés référence par référence contre une
grille professionnelle : les tarifs confirmés correspondant exactement à la
boutique (hors bidon), ils ont été traités comme des tarifs professionnels.
Rien n'a été inventé.

**TVA.** Le catalogue n'indique ni HT ni TTC, faute d'information. À trancher.

## Offres affichées

Trois mécaniques distinctes, une par catégorie, non cumulables sur un même
produit — le catalogue le dit explicitement sous les trois cartes.

**Première commande**

| Catégorie | Offre | Montants |
|---|---|---|
| Colorations Color | 24 achetés + 24 offerts | 249.60 CHF, 48 tubes, 5.20 le tube |
| Colorations Ekstra Color | 24 achetés + 24 offerts | 261.60 CHF, 48 tubes, 5.45 le tube |
| Bidons 10 L | second bidon à −50 % | 50.00 + 25.00 = 75.00 CHF |
| Tout le reste | −50 % | hors colorations et bidons 10 L |

**Réassort**

| Catégorie | Paliers | Montants |
|---|---|---|
| Color (10.40) | 12 + 2 · 24 + 6 | 124.80 CHF (8.91/tube) · 249.60 CHF (8.32/tube) |
| Ekstra Color (10.90) | 12 + 2 · 24 + 6 | 130.80 CHF (9.34/tube) · 261.60 CHF (8.72/tube) |
| Bidons 10 L | à l'unité | 50.00 CHF |
| Tout le reste | à l'unité | tarif professionnel du catalogue |

Aucun palier n'a été ajouté au-delà des deux validés. Tous les montants et
prix unitaires ci-dessus sont recalculés à chaque génération et vérifiés.

## Anomalies relevées dans la boutique

- **Activateurs 150 ml : retirés du catalogue** sur demande. Seul le flacon de
  1 000 ml est présenté, dans les quatre volumes. Au passage, la boutique les
  vend 3.40 CHF sauf le 30 vol. à 3.42 — probable coquille à corriger de ce
  côté-là.
- **Poudre décolorante grise 9 tons, deux fiches** : `poudre-decolorante-grise-9-tons-500-g`
  (36.60) et `poudre-decolorante-grise-a-neuf-tons-500-g-5017` (35.00), même
  description. Seule la première est publiée ; la seconde est dans `EXCLUS`.
- **Coloration Color 6/44** est en brouillon dans la boutique : elle n'est pas
  comptée dans les 65 nuances annoncées.

## Références écartées

Faute d'image ou de description complète, comme demandé :

| Référence | Motif |
|---|---|
| HYDRALIFT ADVANCED 50 ML | ni visuel ni description |
| B-BURRO corps complexe 220 ml | pas de description |
| La crème corporelle BAVA+ 250 ml | pas de description |
| Bâtonnet de cire 75 g | pas de description |
| Crème après-rasage Belief 95121 | pas de description (le 90121 est publié) |

## Contenances

Trois produits X Men n'ont pas de contenance documentée : gel Belief (30124),
gel Acqua di Vi (20100) et poudre volumisante (80121). Le catalogue affiche leur
référence fabricant plutôt qu'un volume supposé. À compléter si vous l'avez.

## Comptage des nuances

- Color Keratin & Argan : **65 nuances** actives (66 fiches, dont une en
  brouillon).
- Ekstra Color sans ammoniaque : **37 nuances + 4 boosters** (argent, bleu,
  violet, rouge).

Ces chiffres sont affichés dans le catalogue ; ils bougeront si des tons sont
ajoutés ou retirés de la boutique.
