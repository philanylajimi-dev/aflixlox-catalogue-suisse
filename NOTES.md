# Points à confirmer avant diffusion

## Sources utilisées

`products_export_1.csv` est introuvable sur le poste et absent de l'historique
Git du thème. Les données viennent donc de la boutique elle-même — celle du
nouveau site, `f8hvn5-ix.myshopify.com` — via l'API Admin : titres, statuts,
prix, visuels. Les descriptions proviennent de `data/product-descriptions.json`
du thème, c'est-à-dire des textes retravaillés pour le nouveau site.

## Prix

Trois tarifs sont ceux du brief et priment sur la boutique :

| Référence | Catalogue | Boutique |
|---|---|---|
| Coloration 100 ml | 10.40 CHF | 10.40 CHF (Color) · **10.90 CHF (Ekstra Color)** |
| Bidon 10 L | 50.00 CHF | 72.00 CHF |
| Masque 1 500 ml | 19.45 CHF | 19.45 CHF |

**Ekstra Color.** La boutique vend la gamme sans ammoniaque 10.90 CHF, pas
10.40. Le brief fixant un tarif unique pour les colorations 100 ml, et les
offres (48 tubes à 249.60 CHF, 14 à 124.80) ne tombant juste qu'à 10.40, le
catalogue affiche 10.40 sur les deux gammes. **À confirmer** : si Ekstra Color
reste à 10.90, il faut soit une ligne de prix distincte, soit des offres
séparées.

**Les autres prix** sont ceux de la boutique. Deux des trois tarifs confirmés y
correspondant exactement, ils ont été traités comme des tarifs professionnels.
Rien n'a été inventé : aucun prix n'apparaît qui ne vienne du brief ou de la
boutique. À valider référence par référence si la grille pro diffère.

**TVA.** Le catalogue n'indique ni HT ni TTC, faute d'information. À trancher.

## Anomalies relevées dans la boutique

- **Activateur 30 vol. 150 ml : 3.42 CHF**, quand les trois autres volumes sont
  à 3.40. Affiché tel quel. Probable coquille à corriger côté boutique.
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
