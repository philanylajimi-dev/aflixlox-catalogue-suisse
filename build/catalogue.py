"""
AF Lix Lox — catalogue professionnel Suisse.

Modèle de données du catalogue : l'ordre des sections, des gammes et des
références, les noms affichés, les contenances et les accroches courtes.

Les prix viennent de `source/shopify-products.json` (export de la boutique),
sauf override explicite dans PRIX_VALIDES : ce sont les tarifs confirmés par
AF Lix Lox, qui priment sur ceux du site.

Une référence n'apparaît dans le catalogue que si elle est listée ici ET
qu'elle possède une image et une description complètes côté boutique.
"""

# --------------------------------------------------------------------------- #
# Tarifs confirmés — priment sur le prix de la boutique.
# --------------------------------------------------------------------------- #

PRIX_COLORATION = "10.40"        # tube 100 ml, gamme Color (avec ammoniaque)
PRIX_COLORATION_EKSTRA = "10.90"  # tube 100 ml, Ekstra Color (sans ammoniaque)
PRIX_BIDON_10L = "50.00"          # le bidon de 10 litres
PRIX_MASQUE_1500 = "19.45"        # le pot de 1 500 ml

PRIX_VALIDES = {
    "shampoing-aux-amandes-frequent-care-pour-lavages-frequents-bidon-de-10-litres": PRIX_BIDON_10L,
    "shampoing-aux-graines-de-lin-pour-lavages-frequents-bidon-de-10-litres": PRIX_BIDON_10L,
    "shampoing-pour-cheveux-secs-bidon-de-10-litres": PRIX_BIDON_10L,
    "masque-soin-cheveux-secs-1500-ml": PRIX_MASQUE_1500,
}

# Doublon catalogue : même poudre grise 9 tons, deux fiches. On n'en garde qu'une.
EXCLUS = {"poudre-decolorante-grise-a-neuf-tons-500-g-5017"}


# --------------------------------------------------------------------------- #
# Offres commerciales
# --------------------------------------------------------------------------- #

OFFRES_PREMIERE = [
    {
        "rang": "01",
        "famille": "Coloration 100 ml",
        "titre": "24 tubes achetés,<br>24 offerts",
        "image": "coloration-color-7-0-100-ml",
        "lignes": [
            ("Tubes livrés", "48"),
            ("Total", "249.60 CHF"),
            ("Revient à", "5.20 CHF le tube"),
        ],
        "note": "Tons au choix. Montants établis sur la gamme Color à 10.40 CHF le tube&nbsp;; Ekstra Color sans ammoniaque est à 10.90 CHF.",
        "vedette": True,
    },
    {
        "rang": "02",
        "famille": "Shampoing 10 L",
        "titre": "Le 2<sup>e</sup> bidon<br>à moitié prix",
        "image": "shampoing-pour-cheveux-secs-bidon-de-10-litres",
        "lignes": [
            ("1<sup>er</sup> bidon", "50.00 CHF"),
            ("2<sup>e</sup> bidon", "25.00 CHF"),
            ("Les deux", "75.00 CHF"),
        ],
        "note": "Amande, graines de lin ou cheveux secs, au choix.",
        "vedette": False,
    },
    {
        "rang": "03",
        "famille": "Masques &amp; soins",
        "titre": "−50 % sur toute<br>la première commande",
        "image": "masque-soin-cheveux-secs-1500-ml",
        "lignes": [
            ("Masque Dry 1 500 ml", "19.45 CHF"),
            ("Première commande", "9.73 CHF"),
            ("Sur le reste du catalogue", "−50 %"),
        ],
        "note": "La remise s'applique à l'ensemble des masques, soins et autres références.",
        "vedette": False,
    },
]

OFFRES_SUIVANTES = [
    {
        "famille": "Coloration 100 ml",
        "formules": [
            {"achat": "12 achetés", "offert": "+ 2 offerts", "total": "14 tubes",
             "prix": "124.80 CHF", "unite": "8.91 CHF le tube"},
            {"achat": "24 achetés", "offert": "+ 6 offerts", "total": "30 tubes",
             "prix": "249.60 CHF", "unite": "8.32 CHF le tube"},
        ],
        "note": "Montants calculés sur la gamme Color à 10.40 CHF le tube.",
    },
    {
        "famille": "Shampoing 10 L",
        "formules": [
            {"achat": "À l'unité", "offert": "", "total": "1 bidon de 10 litres",
             "prix": "50.00 CHF", "unite": "5.00 CHF le litre"},
        ],
    },
    {
        "famille": "Masques, soins et reste du catalogue",
        "formules": [
            {"achat": "À l'unité", "offert": "", "total": "Sans minimum",
             "prix": "Tarif professionnel", "unite": "Prix affichés dans le catalogue"},
        ],
    },
]


# --------------------------------------------------------------------------- #
# Gammes de coloration — présentées en gamme, pas en tube par tube.
# --------------------------------------------------------------------------- #

GAMMES_COLORATION = [
    {
        "nom": "Color",
        "sous_titre": "Keratin &amp; Argan",
        "image": "coloration-color-7-0-100-ml",
        "accroche": "Coloration permanente kératine et huile d'argan, couverture "
                    "optimale des cheveux blancs.",
        "contenance": "Tube 100 ml",
        "prix": PRIX_COLORATION,
        "nuances": "65 nuances",
        "familles": ["Naturels", "Cendrés", "Dorés", "Cuivrés", "Acajou",
                     "Rouges", "Chocolat", "Super éclaircissants"],
        "echelle": "De 1/0 noir à 12/21 super éclaircissant",
    },
    {
        "nom": "Ekstra Color",
        "sous_titre": "Sans ammoniaque",
        "image": "coloration-sans-ammoniaque-ekstra-color-7-0-100-ml",
        "accroche": "Même tenue, sans ammoniaque : confort en cabine et odeur "
                    "nettement plus discrète au bac.",
        "contenance": "Tube 100 ml",
        "prix": PRIX_COLORATION_EKSTRA,
        "nuances": "37 nuances + 4 boosters",
        "familles": ["Naturels", "Cendrés", "Dorés", "Cuivrés", "Acajou",
                     "Super éclaircissants", "Boosters argent, bleu, violet, rouge"],
        "echelle": "De 1/0 noir à 11/3 super éclaircissant",
    },
]


# --------------------------------------------------------------------------- #
# Catalogue — sections, gammes, références.
#
# Chaque référence : (handle, nom affiché, contenance, accroche courte).
# --------------------------------------------------------------------------- #

SECTIONS = [
    {
        "id": "bidons",
        "numero": "03",
        "titre": "Bidons 10 litres",
        "nav": "Bidons 10 L",
        "intro": "Le format qui fait tourner le bac. Trois shampoings de lavage "
                 "courant, en bidon salon.",
        "groupes": [
            {
                "nom": "Shampoings de bac",
                "marque": "ProfesiaHair",
                "note": "50.00 CHF le bidon · deuxième bidon à −50 % sur la première commande",
                "produits": [
                    ("shampoing-pour-cheveux-secs-bidon-de-10-litres",
                     "Shampoing Dry Hair Care", "10 L",
                     "Protéines de lait, pour cheveux secs et ternes."),
                    ("shampoing-aux-amandes-frequent-care-pour-lavages-frequents-bidon-de-10-litres",
                     "Shampoing amande Frequent Care", "10 L",
                     "Formule douce, pensée pour les lavages quotidiens."),
                    ("shampoing-aux-graines-de-lin-pour-lavages-frequents-bidon-de-10-litres",
                     "Shampoing graines de lin Frequent Care", "10 L",
                     "Respecte la fibre fragilisée par les services techniques."),
                ],
            },
        ],
    },
    {
        "id": "masques",
        "numero": "04",
        "titre": "Masques grand format",
        "nav": "Masques",
        "intro": "Les contenances qui tiennent la saison. Le 1 500 ml en tête, "
                 "puis les pots de 1 000 ml de chaque gamme.",
        "groupes": [
            {
                "nom": "Grands formats",
                "marque": "ProfesiaHair",
                "note": "−50 % sur la première commande",
                "produits": [
                    ("masque-soin-cheveux-secs-1500-ml",
                     "Masque Dry Hair Care", "1 500 ml",
                     "Régénère et démêle après décoloration ou permanente."),
                    ("masque-reconstruction-capillaire-botox-1000-ml",
                     "Masque Botox Hair Therapy", "1 000 ml",
                     "Acide hyaluronique, referme les écailles du cheveu."),
                    ("masque-soin-colorant-cheveux-colores-1000-ml",
                     "Masque Color Hair Care", "1 000 ml",
                     "Restructure et préserve l'éclat de la couleur."),
                    ("masque-capillaire-pour-cheveux-traites-fluidaliss-1000-ml",
                     "Masque Fluidaliss", "1 000 ml",
                     "Collagène, soie et kératine pour cheveux traités."),
                ],
            },
        ],
    },
    {
        "id": "soins",
        "numero": "05",
        "titre": "Soins par gamme",
        "nav": "Soins",
        "intro": "Chaque shampoing avec son masque et ses compléments, pour "
                 "composer une cabine cohérente.",
        "groupes": [
            {
                "nom": "Dry Hair Care",
                "marque": "ProfesiaHair",
                "note": "Cheveux secs et ternes",
                "produits": [
                    ("shampoing-soin-cheveux-secs-pour-cheveux-secs-1000-ml",
                     "Shampoing Dry Hair Care", "1 000 ml",
                     "Protéines de lait, hydrate sans alourdir."),
                    ("masque-soin-cheveux-secs-500-ml",
                     "Masque Dry Hair Care", "500 ml",
                     "Démêle et discipline les cheveux abîmés."),
                    ("shampoing-soin-cheveux-secs-300-ml",
                     "Shampoing Dry Hair Care", "300 ml",
                     "Mêmes protéines de lait, en format à emporter."),
                    ("creme-hydratante-pour-cheveux-secs-200-ml",
                     "Crème hydratante Dry", "200 ml",
                     "Sans rinçage, protège la cuticule et les pointes."),
                ],
            },
            {
                "nom": "Color Hair Care",
                "marque": "ProfesiaHair",
                "note": "Cheveux colorés",
                "produits": [
                    ("shampoing-color-care-pour-cheveux-colores-1000-ml",
                     "Shampoing Color Care", "1 000 ml",
                     "Extraits de myrtille et protection UV."),
                    ("masque-soin-colorant-cheveux-colores-500-ml",
                     "Masque Color Care", "500 ml",
                     "Compense le stress de la coloration."),
                    ("shampoing-color-care-pour-cheveux-colores-300-ml",
                     "Shampoing Color Care", "300 ml",
                     "Myrtille et protection UV, à vendre au client."),
                    ("spray-protecteur-de-couleur-200-ml",
                     "Spray thermoprotecteur", "200 ml",
                     "Protège du fer et du sèche-cheveux, facilite le brushing."),
                ],
            },
            {
                "nom": "Botox Hair Therapy",
                "marque": "ProfesiaHair",
                "note": "Reconstruction après service technique",
                "produits": [
                    ("botox-hair-therapy-reconstruction-shampoo-1000-ml",
                     "Shampoing reconstructeur Botox", "1 000 ml",
                     "Huiles d'argan et de macadamia, cheveux fragilisés."),
                    ("masque-reconstruction-capillaire-botox-500-ml",
                     "Masque reconstructeur Botox", "500 ml",
                     "Texture dense, rend souplesse et brillance."),
                    ("shampoing-reconstruction-capillaire-botox-300-ml",
                     "Shampoing reconstructeur Botox", "300 ml",
                     "La formule reconstructrice en petit format."),
                    ("serum-reconstruction-capillaire-botox-12-ampoules-x-10-ml",
                     "Sérum Botox en ampoules", "12 × 10 ml",
                     "Se transforme en crème au contact de l'eau."),
                    ("apres-shampoing-biphase-botox-200-ml",
                     "Après-shampoing biphasé Botox", "200 ml",
                     "Sans rinçage, discipline les frisottis."),
                    ("masque-spray-botox-hair-therapy-10-en-1-200-ml",
                     "Masque spray Botox 10 en 1", "200 ml",
                     "Nourrit, démêle et protège de la chaleur en un geste."),
                    ("traitement-capillaire-botox-sachet-de-12-ml-5-sachets",
                     "Traitement Botox monodose", "5 × 12 ml",
                     "Produit frais à chaque application."),
                ],
            },
            {
                "nom": "Fluidaliss",
                "marque": "ProfesiaHair",
                "note": "Cheveux colorés et traités chimiquement",
                "produits": [
                    ("shampoing-pour-cheveux-traites-fluidaliss-1000-ml",
                     "Shampoing Fluidaliss", "1 000 ml",
                     "Collagène, soie et kératine ; protège la couleur."),
                    ("masque-capillaire-pour-cheveux-traites-fluidaliss-500-ml",
                     "Masque Fluidaliss", "500 ml",
                     "Nourrit et discipline les frisottis."),
                    ("shampoing-fluidaliss-300-ml",
                     "Shampoing Fluidaliss", "300 ml",
                     "Collagène, soie et kératine, format maison."),
                    ("huile-pour-cheveux-traites-fluidaliss-50-ml",
                     "Huile Fluidaliss", "50 ml",
                     "Finition brillance sur longueurs et pointes."),
                ],
            },
            {
                "nom": "Curl Hair Care",
                "marque": "ProfesiaHair",
                "note": "Cheveux bouclés et ondulés",
                "produits": [
                    ("shampoing-curls-pour-cheveux-boucles-1000-ml",
                     "Shampoing Curls", "1 000 ml",
                     "Collagène hydrolysé, soutient la boucle."),
                    ("masque-cheveux-boucles-curls-hair-care-500-ml",
                     "Masque Curls", "500 ml",
                     "Donne corps et définition sans alourdir."),
                    ("shampoing-curls-pour-cheveux-boucles-300-ml",
                     "Shampoing Curls", "300 ml",
                     "Collagène hydrolysé, à emporter après le service."),
                    ("fluide-boucles-soin-boucles-250-ml",
                     "Fluide Boucles", "250 ml",
                     "Définit la boucle, effet antistatique."),
                ],
            },
            {
                "nom": "Frequent Hair Care",
                "marque": "ProfesiaHair",
                "note": "Lavages fréquents",
                "produits": [
                    ("shampoing-frequent-aux-agrumes-de-sicile-1000-ml",
                     "Shampoing agrumes de Sicile", "1 000 ml",
                     "Formule douce pour un usage quotidien."),
                    ("apres-shampoing-frequent-aux-agrumes-de-sicile-1000-ml",
                     "Après-shampoing agrumes", "1 000 ml",
                     "Démêle et rend les cheveux faciles à coiffer."),
                    ("spray-denouant-les-noeuds-frequents-250-ml",
                     "Spray démêlant", "250 ml",
                     "Sans rinçage, n'alourdit pas."),
                ],
            },
            {
                "nom": "No Yellow Care",
                "marque": "ProfesiaHair",
                "note": "Anti-jaunissement",
                "produits": [
                    ("shampoing-anti-jaunissement-no-yellow-care-1000-ml",
                     "Shampoing No Yellow", "1 000 ml",
                     "Protéines de soie, neutralise jaunes et cuivrés."),
                    ("shampooing-anti-jaunissement-no-yellow-care-500-ml",
                     "Shampoing No Yellow", "500 ml",
                     "Le format d'appoint, à garder au bac."),
                ],
            },
            {
                "nom": "Loss Hair Care",
                "marque": "ProfesiaHair",
                "note": "Cheveux fins et chute",
                "produits": [
                    ("shampoing-anti-chute-loss-hair-care-1000-ml",
                     "Shampoing anti-chute", "1 000 ml",
                     "Algues marines et protéines fortifiantes."),
                    ("lotion-energisante-pour-le-soin-des-cheveux-contre-la-chute-12-flacons-de-10-ml",
                     "Lotion énergisante en ampoules", "12 × 10 ml",
                     "Cure sur le cuir chevelu, sans rinçage."),
                    ("lotion-energisante-anti-chute-150-ml",
                     "Lotion énergisante", "150 ml",
                     "Le flacon, pour un usage à la maison."),
                    ("shampoing-anti-chute-aux-algues-marines-300-ml",
                     "Shampoing anti-chute", "300 ml",
                     "Algues marines, pour la cure à domicile."),
                ],
            },
            {
                "nom": "Greasy &amp; Dandruff Care",
                "marque": "ProfesiaHair",
                "note": "Cuir chevelu gras, pellicules",
                "produits": [
                    ("shampooing-anti-graisse-cheveux-gras-1000-ml",
                     "Shampoing anti-gras", "1 000 ml",
                     "Antisébum, laisse les cheveux légers."),
                    ("shampooing-antipelliculaire-1000-ml",
                     "Shampoing antipelliculaire", "1 000 ml",
                     "Extraits de romarin, sans dessécher le cuir chevelu."),
                    ("shampooing-anti-gras-pour-cheveux-gras-300-ml",
                     "Shampoing anti-gras", "300 ml",
                     "Antisébum, en format de revente."),
                    ("shampooing-antipelliculaire-soin-capillaire-300-ml",
                     "Shampoing antipelliculaire", "300 ml",
                     "Romarin, pour l'entretien entre deux visites."),
                ],
            },
        ],
    },
    {
        "id": "technique",
        "numero": "06",
        "titre": "Technique salon",
        "nav": "Technique",
        "intro": "Lissage, permanente et réparation : les protocoles réservés "
                 "au poste technique.",
        "groupes": [
            {
                "nom": "Ekstra Liss",
                "marque": "ProfesiaHair",
                "note": "Lissage kératine en trois étapes",
                "produits": [
                    ("shampoing-preparateur-ekstra-liss-n-1-500-ml",
                     "N° 1 — Shampoing préparateur", "500 ml",
                     "Ouvre la fibre avant le lissage."),
                    ("shampoing-lissant-ekstra-liss-keratin-n-2-500-ml",
                     "N° 2 — Shampoing lissant kératine", "500 ml",
                     "Le cœur du protocole, à la kératine."),
                    ("solution-lissante-solution-ekstra-liss-n-3-500-ml",
                     "N° 3 — Solution lissante", "500 ml",
                     "Fixe le résultat en fin de protocole."),
                ],
            },
            {
                "nom": "Nano Repair",
                "marque": "ProfesiaHair",
                "note": "Lissage réparateur, tenue jusqu'à 4 mois",
                "produits": [
                    ("traitement-nano-reparateur-500-ml",
                     "Traitement Nano Repair", "500 ml",
                     "Étape salon : collagène et acide glycolique."),
                    ("fluido-nano-repair-at-home-250-ml",
                     "Fluido Nano Repair", "250 ml",
                     "S'active à la chaleur du fer et du séchoir."),
                    ("masque-nano-repair-a-domicile-500-ml",
                     "Masque Nano Repair", "500 ml",
                     "Le masque d'entretien, anti-frisottis."),
                    ("shampoing-preparateur-nano-repair-300-ml",
                     "Shampoing Nano Repair", "300 ml",
                     "Le lavage quotidien après un lissage."),
                ],
            },
            {
                "nom": "Ekstra Wave",
                "marque": "ProfesiaHair",
                "note": "Permanente sans ammoniaque",
                "produits": [
                    ("permanente-ekstra-wave-500-ml",
                     "Permanente Ekstra Wave", "500 ml",
                     "Boucles souples sur cheveux naturels, colorés ou fins."),
                    ("neutralisant-ekstra-wave-1000-ml",
                     "Neutralisant Ekstra Wave", "1 000 ml",
                     "Fixe et stabilise la boucle."),
                ],
            },
        ],
    },
    {
        "id": "homme",
        "numero": "07",
        "titre": "Profesia X Men",
        "nav": "Homme",
        "intro": "Coiffage et rasage pour l'espace barbier.",
        "groupes": [
            {
                "nom": "Coiffage",
                "marque": "Profesia X Men",
                "note": "",
                "produits": [
                    ("gel-capillaire-belief-30124-profesia-x-men",
                     "Gel Belief", "Réf. 30124",
                     "Fixation forte, fini brillant et défini."),
                    ("gel-capillaire-acqua-di-vi-20100-profesia-x-men",
                     "Gel Acqua di Vi", "Réf. 20100",
                     "Fixation forte pour coiffures structurées."),
                    ("gel-capillaire-one-trillion-00186-fixation-forte-500-ml",
                     "Gel One Trillion", "500 ml",
                     "Fixation forte, tenue du matin au soir."),
                    ("gel-coiffant-noir-50121-profesia-x-men",
                     "Gel Black pigmenté", "500 ml",
                     "Met en valeur les cheveux gris, s'élimine au lavage."),
                    ("poudre-volumisante-effet-mat-80121-profesia-x-men",
                     "Poudre volumisante", "Réf. 80121",
                     "Volume immédiat, fini mat, sans alourdir."),
                    ("cire-a-largile-effet-mat-09121-profesia-x-men",
                     "Cire à l'argile", "100 ml",
                     "Effet mat, volume et texture."),
                    ("pate-mate-70121-profesia-x-men",
                     "Pâte mate", "100 ml",
                     "Tenue modelable, texture légère qui ne colle pas."),
                    ("belief-extreme-water-wax-06121-profesia-x-men",
                     "Extreme Water Wax", "100 ml",
                     "Très forte tenue, définition extrême."),
                    ("acqua-wax-night-40121-profesia-x-men",
                     "Acqua Wax Night", "100 ml",
                     "Cire de coiffage, fini maîtrisé."),
                    ("spray-salin-65121-profesia-x-men",
                     "Spray salin", "250 ml",
                     "Effet retour de plage, tenue légère."),
                ],
            },
            {
                "nom": "Rasage",
                "marque": "Profesia X Men",
                "note": "",
                "produits": [
                    ("apres-rasage-glace-effet-rafraichissant-23900-x-men-400ml",
                     "Après-rasage glacé", "400 ml",
                     "Fraîcheur glacée, peaux sensibles."),
                    ("apres-rasage-belief-effet-relaxant-20900-profesia-x-men",
                     "Après-rasage Belief", "400 ml",
                     "Effet relaxant et apaisant."),
                    ("creme-apres-rasage-belief-90121-profesia-x-men",
                     "Crème après-rasage Belief", "250 ml",
                     "Absorption rapide, hydrate et apaise."),
                ],
            },
        ],
    },
    {
        "id": "divers",
        "numero": "08",
        "titre": "Autour du poste",
        "nav": "Divers",
        "intro": "Ce qui complète la commande.",
        "groupes": [
            {
                "nom": "Accessoires et divers",
                "marque": "",
                "note": "",
                "produits": [
                    ("hair-color-chart",
                     "Nuancier Hair Color Chart", "Nuancier",
                     "Pour montrer les nuances au client avant le service."),
                    ("rouleau-de-lit-jetable-roial",
                     "Rouleau de lit jetable", "RO.IAL",
                     "Papier jetable pour lits et tables de soin."),
                    ("b-scrub-aux-sels-de-la-mer-morte-300-g",
                     "B-Scrub sels de la mer Morte", "300 g",
                     "Gommage corporel, pour l'espace esthétique."),
                ],
            },
        ],
    },
]

# Les contenances affichées proviennent des fiches produit. Lorsque le fournisseur
# ne la précise pas, on affiche la référence fabricant plutôt qu'un volume inventé.

ACTIVATEURS = {
    "titre": "Activateurs",
    "sous_titre": "Émulsion oxydante crème, pour Color et Ekstra Color",
    "contenance": "Flacon de 1 000 ml",
    "image": "activateur-20-volumes-1000-ml",
    "lignes": [
        ("10 vol. · 3 %", "activateur-10-volumes-1000-ml"),
        ("20 vol. · 6 %", "activateur-20-volumes-1000-ml"),
        ("30 vol. · 9 %", "activateur-30-volumes-1000-ml"),
        ("40 vol. · 12 %", "activateur-40-volumes-1000-ml"),
    ],
}

DECOLORANTS = {
    "titre": "Poudres décolorantes",
    "produits": [
        ("poudre-decolorante-grise-9-tons-500-g",
         "Poudre grise 9 tons", "Pot 500 g",
         "Texture compacte qui ne vole pas, toutes techniques."),
        ("poudre-decolorante-blanche-9-tons-500-g",
         "Poudre blanche 9 tons", "Pot 500 g",
         "Éclaircissement maximal, à mélanger à l'activateur."),
        ("poudre-decolorante-bleue-7-tons-500-g",
         "Poudre bleue 7 tons", "Pot 500 g",
         "Parfum lavande, évite les reflets jaune-orangé."),
        ("poudre-decolorante-bleue-sachet-de-30-g-5-unites",
         "Poudre bleue en sachets", "5 × 30 g",
         "La même poudre en doses, pour les petits services."),
    ],
}
