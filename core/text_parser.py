def parse_relation(sentence):
    sentene = sentence.lower()

    if "etudiant" in sentence and "cours" in sentence:
        tables = {
            "ETUDIANT": [ 
                "PK id_etudiant",
                "nom",
                "prenom",
            ],
            "COURS": [
                "PK id_cours",
                "titre"
            ],

            "INSCRIPTION": [
                "PK id_etudiant",
                "PK id_cours",
                "date_inscription"
            ]
        }

        relations  = [
            {"from": "ETUDIANT", "to": "INSCRIPTION", "label": "1,N"},
            {"from": "COURS", "to": "INSCRIPTION", "label": "1,N"},

        ]

        return tables, relations
    return {}, []