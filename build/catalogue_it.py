"""
AF Lix Lox — Svizzera Italiana.

Catalogo italiano : tre sezioni, tre offerte di lancio, nient'altro.

Ce n'est pas la traduction du catalogue français : la sélection, les prix et les
offres sont propres à cette version. Les deux catalogues partagent uniquement
les visuels, le logo et la direction artistique.

Les prix ci-dessous sont les prix de lancement communiqués par AF Lix Lox. Ils
remplacent ceux de la boutique pour ces références, et ne concernent que ce
catalogue.
"""

# --------------------------------------------------------------------------- #
# Offerte di lancio
# --------------------------------------------------------------------------- #
#
# `grande` est la ligne qui doit se voir de loin : les quantités en chiffres,
# « gratis » en accent. `nota` reste courte, jamais une condition inventée.

OFFERTE = [
    {
        "id": "shampoo",
        "rango": "01",
        "sezione": "Shampoo",
        "grande": [("n", "1 × 1000 ml"), ("op", "+"), ("n", "3 × 300 ml"),
                   ("free", "gratis")],
        "sintesi": "1 × 1000 ml + 3 × 300 ml",
        "nota": "Su tutte le otto linee.",
    },
    {
        "id": "maschere",
        "rango": "02",
        "sezione": "Maschere",
        "grande": [("n", "1"), ("op", "+"), ("n", "1"), ("free", "gratis")],
        "sintesi": "1 + 1",
        "nota": "Su tutte le quattro linee, nei due formati.",
    },
    {
        "id": "colorazioni",
        "rango": "03",
        "sezione": "Colorazioni",
        "grande": [("n", "24"), ("op", "+"), ("n", "24"), ("free", "gratis")],
        "sintesi": "24 + 24",
        "nota": "Su entrambe le gamme.",
    },
]


# --------------------------------------------------------------------------- #
# Shampoo — otto linee, due formati
# --------------------------------------------------------------------------- #
#
# (linea, sottotitolo, handle 300 ml, handle 1000 ml, prezzo 300, prezzo 1000)
# Le visuel affiché est celui du 1000 ml : c'est le format de cabine.

SHAMPOO = [
    ("Dry Hair Care", "Capelli secchi",
     "shampoing-soin-cheveux-secs-300-ml",
     "shampoing-soin-cheveux-secs-pour-cheveux-secs-1000-ml", "10,20", "16,80"),
    ("Color Hair Care", "Capelli colorati",
     "shampoing-color-care-pour-cheveux-colores-300-ml",
     "shampoing-color-care-pour-cheveux-colores-1000-ml", "10,20", "16,80"),
    ("Curl Hair Care", "Capelli ricci",
     "shampoing-curls-pour-cheveux-boucles-300-ml",
     "shampoing-curls-pour-cheveux-boucles-1000-ml", "10,20", "16,80"),
    ("Fluidaliss", "Capelli lisci",
     "shampoing-fluidaliss-300-ml",
     "shampoing-pour-cheveux-traites-fluidaliss-1000-ml", "10,20", "16,80"),
    ("Loss Hair Care", "Capelli fragili",
     "shampoing-anti-chute-aux-algues-marines-300-ml",
     "shampoing-anti-chute-loss-hair-care-1000-ml", "10,20", "16,80"),
    ("Greasy Hair Care", "Capelli grassi",
     "shampooing-anti-gras-pour-cheveux-gras-300-ml",
     "shampooing-anti-graisse-cheveux-gras-1000-ml", "10,20", "16,80"),
    ("Dandruff Hair Care", "Forfora",
     "shampooing-antipelliculaire-soin-capillaire-300-ml",
     "shampooing-antipelliculaire-1000-ml", "10,20", "16,80"),
    ("Botox Hair Therapy", "Capelli danneggiati",
     "shampoing-reconstruction-capillaire-botox-300-ml",
     "botox-hair-therapy-reconstruction-shampoo-1000-ml", "11,20", "17,20"),
]


# --------------------------------------------------------------------------- #
# Maschere — quattro linee, due formati
# --------------------------------------------------------------------------- #
#
# Le grand format n'est pas le même partout : 1500 ml chez Dry, 1000 ml ailleurs.

MASCHERE = [
    ("Dry Hair Care", "Capelli secchi",
     "masque-soin-cheveux-secs-500-ml", "masque-soin-cheveux-secs-1500-ml",
     "500 ml", "1500 ml", "13,50", "19,90"),
    ("Color Hair Care", "Capelli colorati",
     "masque-soin-colorant-cheveux-colores-500-ml",
     "masque-soin-colorant-cheveux-colores-1000-ml",
     "500 ml", "1000 ml", "13,50", "19,90"),
    ("Fluidaliss", "Capelli lisci",
     "masque-capillaire-pour-cheveux-traites-fluidaliss-500-ml",
     "masque-capillaire-pour-cheveux-traites-fluidaliss-1000-ml",
     "500 ml", "1000 ml", "13,50", "19,90"),
    ("Botox Hair Therapy", "Capelli danneggiati",
     "masque-reconstruction-capillaire-botox-500-ml",
     "masque-reconstruction-capillaire-botox-1000-ml",
     "500 ml", "1000 ml", "14,90", "19,90"),
]


# --------------------------------------------------------------------------- #
# Colorazioni — due gamme, nessun tubo presentato singolarmente
# --------------------------------------------------------------------------- #

COLORAZIONI = [
    {
        "nome": "Crema Colorante",
        "sotto": "Keratin &amp; Argan",
        "immagine": "coloration-color-7-0-100-ml",
        "formato": "Tubo 100 ml",
        "prezzo": "8,50",
    },
    {
        "nome": "Crema Colorante",
        "sotto": "Senza Ammoniaca",
        "immagine": "coloration-sans-ammoniaque-ekstra-color-7-0-100-ml",
        "formato": "Tubo 100 ml",
        "prezzo": "8,90",
    },
]

COLORAZIONI_CLAIM = "Tutte le tonalità disponibili"
COLORAZIONI_NOTA = ("Indicateci i numeri di tono al momento dell'ordine. "
                    "Le tonalità delle due gamme possono essere combinate "
                    "liberamente.")
