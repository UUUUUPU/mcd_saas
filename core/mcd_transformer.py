def transform_mcd_to_mld(entities, relations):

    tables = {}

    # tables des entités
    for entity, fields in entities.items():

        pk = f"id_{entity.lower()}"

        tables[entity] = [f"PK {pk}"]

        for f in fields:
            if f != pk:
                tables[entity].append(f)

    # gestion relations
    for rel_name, rel in relations.items():

        if rel["type"] == "N:N":

            e1 = rel["from"]
            e2 = rel["to"]

            table = rel_name

            tables[table] = [
                f"FK id_{e1.lower()}",
                f"FK id_{e2.lower()}"
            ]

    return tables