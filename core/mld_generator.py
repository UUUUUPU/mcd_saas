# def mcd_to_mld(mcd):
#     """
#     Transforme un MCD dict en MLD dict avec PK/FK
#     Détecte automatiquement N-N, 1-N et 1-1 par convention simple
#     """
#     mld = {}
#     relations = []

#     for table, fields in mcd.items():
#         # Premier champ = PK
#         pk = f"PK {fields[0]}"
#         mld[table] = [pk] + fields[1:]

#     # Détection automatique relations
#     for table in mld:
#         name = table.upper()
#         if "_" in table or name in ["INSCRIPTION", "PARTICIPATION"]:
#             # N-N
#             parts = table.split("_")
#             if len(parts) == 2:
#                 left, right = parts
#             else:
#                 left, right = "ETUDIANT", "COURS"  # convention simple
#             relations.append((left, right, "N-N"))
#         else:
#             # 1-N et 1-1 : convention, FK détecté dans table
#             for f in mld[table]:
#                 if f.startswith("FK "):
#                     fk_col = f.replace("FK ", "")
#                     # Si le nom contient “id_” + table, on considère 1-N
#                     ref_table = fk_col.replace("id_", "").upper()
#                     if ref_table != table.upper():
#                         relations.append((ref_table, table, "1-N"))
#                         # On peut ajouter 1-1 si UNIQUE demandé
#                         # relations.append((ref_table, table, "1-1"))

#     return mld, relations
def mcd_to_mld(mcd):

    mld = {}
    relations = []

    # Création du MLD
    for table, fields in mcd.items():
        pk = f"PK {fields[0]}"
        mld[table] = [pk] + fields[1:]

    # Détection des relations
    for table in mld:

        if "_" in table:
            parts = table.split("_")

            if len(parts) == 2 and parts[0] in mld and parts[1] in mld:
                left, right = parts
                relations.append((left, right, "N-N"))

    return mld, relations