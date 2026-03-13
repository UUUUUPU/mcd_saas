# from core.diagram_generator import generate_diagram

# tables = [
#     {"table": "Etudiant"},
#     {"table": "Cours"},
#     {"table": "Inscription"}
# ]

# relations = [
#     {"from": "Etudiant", "to": "Inscription"},
#     {"from": "Cours", "to": "Inscription"}
# ]

# generate_diagram(tables, relations)

from core.diagram_generator import generate_diagram

tables = {
    "ETUDIANT": [
        "PK id_etudiant",
        "nom",
        "prenom"
    ],
    "COURS": [
        "PK id_cours",
        "titre"
    ],
    "INSCRIPTION": [
        "FK id_etudiant",
        "FK id_cours",
        "date_inscription"
    ]
}

relations = [
    {"from": "ETUDIANT", "to": "INSCRIPTION", "label": "1,N"},
    {"from": "COURS", "to": "INSCRIPTION", "label": "1,N"}
]

generate_diagram(tables, relations)