def transform(mcd):
    tables = []

    for entite in mcd["entites"]:
        tables.append({
            "table": entite["nom"],
            "colonnes": entite["attributs"]
        })

    return tables