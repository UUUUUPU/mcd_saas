# def generate_sql(tables, relations=None, db="mysql"):
#     sql = ""
#     if relations is None:
#         relations = []

#     # Génération des tables de base
#     for table, fields in tables.items():
#         columns = []
#         primary_keys = []

#         for field in fields:
#             if field.startswith("PK"):
#                 col = field.replace("PK ", "")
#                 columns.append(f"{col} INT")
#                 primary_keys.append(col)
#             elif field.startswith("FK"):
#                 col = field.replace("FK ", "")
#                 columns.append(f"{col} INT")
#             else:
#                 columns.append(f"{field} VARCHAR(255)")

#         all_defs = columns
#         if primary_keys:
#             all_defs.append(f"PRIMARY KEY ({', '.join(primary_keys)})")

#         sql += f"\nCREATE TABLE {table} (\n"
#         sql += ",\n".join("    " + d for d in all_defs)
#         sql += "\n);\n"

#     # Gestion des relations détectées
#     for left, right, rel_type in relations:
#         if rel_type == "N-N":
#             table_name = f"{left}_{right}"
#             pk_left = [f.replace("PK ", "") for f in tables[left] if f.startswith("PK")][0]
#             pk_right = [f.replace("PK ", "") for f in tables[right] if f.startswith("PK")][0]
#             sql += f"\nCREATE TABLE {table_name} (\n"
#             sql += f"    {pk_left} INT,\n"
#             sql += f"    {pk_right} INT,\n"
#             sql += f"    PRIMARY KEY ({pk_left}, {pk_right}),\n"
#             sql += f"    FOREIGN KEY ({pk_left}) REFERENCES {left}({pk_left}),\n"
#             sql += f"    FOREIGN KEY ({pk_right}) REFERENCES {right}({pk_right})\n"
#             sql += ");\n"

#         elif rel_type == "1-N":
#             # la table N reçoit la FK vers 1
#             pk_left = [f.replace("PK ", "") for f in tables[left] if f.startswith("PK")][0]
#             sql += f"\nALTER TABLE {right} ADD COLUMN {pk_left} INT;\n"
#             sql += f"ALTER TABLE {right} ADD FOREIGN KEY ({pk_left}) REFERENCES {left}({pk_left});\n"

#         elif rel_type == "1-1":
#             # table droite reçoit la FK et UNIQUE
#             pk_left = [f.replace("PK ", "") for f in tables[left] if f.startswith("PK")][0]
#             sql += f"\nALTER TABLE {right} ADD COLUMN {pk_left} INT UNIQUE;\n"
#             sql += f"ALTER TABLE {right} ADD FOREIGN KEY ({pk_left}) REFERENCES {left}({pk_left});\n"

#     return sql

# def generate_sql(tables, relations=None, db="mysql"):
#     sql = ""
#     if relations is None:
#         relations = []

#     # 1️⃣ Génération des tables de base avec PK
#     for table, fields in tables.items():
#         columns = []
#         primary_keys = []

#         for field in fields:
#             if field.startswith("PK"):
#                 col = field.replace("PK ", "")
#                 columns.append(f"{col} INT")
#                 primary_keys.append(col)
#             elif field.startswith("FK"):
#                 col = field.replace("FK ", "")
#                 columns.append(f"{col} INT")  # FK = INT
#             else:
#                 columns.append(f"{field} VARCHAR(255)")

#         all_defs = columns
#         if primary_keys:
#             all_defs.append(f"PRIMARY KEY ({', '.join(primary_keys)})")

#         sql += f"\nCREATE TABLE {table} (\n"
#         sql += ",\n".join("    " + d for d in all_defs)
#         sql += "\n);\n"

#     # 2️⃣ Gestion des relations détectées
#     for left, right, rel_type in relations:
#         if rel_type == "N-N":
#             # Table de liaison N-N
#             table_name = f"{left}_{right}"
#             pk_left = [f.replace("PK ", "") for f in tables[left] if f.startswith("PK")][0]
#             pk_right = [f.replace("PK ", "") for f in tables[right] if f.startswith("PK")][0]
#             sql += f"\nCREATE TABLE {table_name} (\n"
#             sql += f"    {pk_left} INT,\n"
#             sql += f"    {pk_right} INT,\n"
#             sql += f"    PRIMARY KEY ({pk_left}, {pk_right}),\n"
#             sql += f"    FOREIGN KEY ({pk_left}) REFERENCES {left}({pk_left}),\n"
#             sql += f"    FOREIGN KEY ({pk_right}) REFERENCES {right}({pk_right})\n"
#             sql += ");\n"

#         elif rel_type == "1-N":
#             # Table “N” reçoit la FK
#             pk_left = [f.replace("PK ", "") for f in tables[left] if f.startswith("PK")][0]
#             sql += f"\nALTER TABLE {right} ADD COLUMN {pk_left} INT;\n"
#             sql += f"ALTER TABLE {right} ADD FOREIGN KEY ({pk_left}) REFERENCES {left}({pk_left});\n"

#         elif rel_type == "1-1":
#             # Table “droite” reçoit la FK UNIQUE
#             pk_left = [f.replace("PK ", "") for f in tables[left] if f.startswith("PK")][0]
#             sql += f"\nALTER TABLE {right} ADD COLUMN {pk_left} INT UNIQUE;\n"
#             sql += f"ALTER TABLE {right} ADD FOREIGN KEY ({pk_left}) REFERENCES {left}({pk_left});\n"

#     return sql


def generate_sql(tables, relations=None, db="mysql"):
    """
    Génère le SQL à partir du MLD et des relations détectées.
    tables : dict {table: [PK/colonnes]}
    relations : list [(left_table, right_table, "N-N"/"1-N"/"1-1")]
    db : "mysql", "postgres", "sqlite"
    """

    sql = ""

    if relations is None:
        relations = []

    # 1️⃣ Création des tables
    for table, fields in tables.items():

        columns = []
        primary_keys = []
        foreign_keys = []

        for field in fields:

            # ----- PRIMARY KEY -----
            if field.startswith("PK"):
                col = field.replace("PK ", "")
                primary_keys.append(col)

                if db == "mysql":
                    columns.append(f"{col} INT AUTO_INCREMENT")
                elif db == "postgres":
                    columns.append(f"{col} SERIAL")
                else:
                    columns.append(f"{col} INTEGER")

            # ----- FOREIGN KEY automatique -----
            elif field.startswith("id_"):
                columns.append(f"{field} INT")

                ref_table = field.replace("id_", "").upper() + "S"

                if ref_table in tables:
                    foreign_keys.append(
                        f"FOREIGN KEY ({field}) REFERENCES {ref_table}({field})"
                    )

            # ----- Champ normal -----
            else:
                columns.append(f"{field} VARCHAR(255)")

        # assemblage
        all_defs = columns

        if primary_keys:
            all_defs.append(f"PRIMARY KEY ({', '.join(primary_keys)})")

        all_defs += foreign_keys

        sql += f"\nCREATE TABLE {table} (\n"
        sql += ",\n".join("    " + d for d in all_defs)
        sql += "\n);\n"

    # 2️⃣ Gestion des relations détectées
    for left, right, rel_type in relations:

        if rel_type == "N-N":

            table_name = f"{left}_{right}"

            pk_left = [f.replace("PK ", "") for f in tables[left] if f.startswith("PK")][0]
            pk_right = [f.replace("PK ", "") for f in tables[right] if f.startswith("PK")][0]

            sql += f"\nCREATE TABLE {table_name} (\n"
            sql += f"    {pk_left} INT,\n"
            sql += f"    {pk_right} INT,\n"
            sql += f"    PRIMARY KEY ({pk_left}, {pk_right}),\n"
            sql += f"    FOREIGN KEY ({pk_left}) REFERENCES {left}({pk_left}),\n"
            sql += f"    FOREIGN KEY ({pk_right}) REFERENCES {right}({pk_right})\n"
            sql += ");\n"

        elif rel_type == "1-N":

            pk_left = [f.replace("PK ", "") for f in tables[left] if f.startswith("PK")][0]

            sql += f"\nALTER TABLE {right} ADD COLUMN {pk_left} INT;\n"
            sql += f"ALTER TABLE {right} ADD FOREIGN KEY ({pk_left}) REFERENCES {left}({pk_left});\n"

        elif rel_type == "1-1":

            pk_left = [f.replace("PK ", "") for f in tables[left] if f.startswith("PK")][0]

            sql += f"\nALTER TABLE {right} ADD COLUMN {pk_left} INT UNIQUE;\n"
            sql += f"ALTER TABLE {right} ADD FOREIGN KEY ({pk_left}) REFERENCES {left}({pk_left});\n"

    return sql