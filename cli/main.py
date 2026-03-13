# import sys
# import os
# import argparse
# import yaml
# import json

# # permettre l'import du dossier core
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from core.mcd_transformer import transform_mcd_to_mld
# from core.sql_generator import generate_sql


# def load_model(file_path):
#     """
#     Charger un fichier MCD JSON ou YAML
#     """

#     if file_path.endswith(".yaml") or file_path.endswith(".yml"):
#         with open(file_path, "r", encoding="utf-8") as f:
#             return yaml.safe_load(f)

#     elif file_path.endswith(".json"):
#         with open(file_path, "r", encoding="utf-8") as f:
#             return json.load(f)

#     else:
#         raise Exception("Format de fichier non supporté (utiliser json ou yaml)")


# def main():

#     parser = argparse.ArgumentParser(
#         description="Générateur MCD → MLD → SQL"
#     )

#     parser.add_argument(
#         "file",
#         help="fichier MCD (yaml ou json)"
#     )

#     parser.add_argument(
#         "--db",
#         default="mysql",
#         help="mysql | postgres | sqlite"
#     )

#     parser.add_argument(
#     "--output",
#     help="fichier SQL de sortie"
# )

#     args = parser.parse_args()

#     # charger le modèle
#     model = load_model(args.file)

#     entities = model["entities"]
#     relations = model["relations"]

#     # transformation MCD → MLD
#     tables = transform_mcd_to_mld(entities, relations)

#     # génération SQL
#     sql = generate_sql(tables, db=args.db)

#     print("\n==============================")
#     print("TABLES MLD")
#     print("==============================\n")

#     for table, fields in tables.items():
#         print(f"{table} : {fields}")

#     print("\n==============================")
#     print("SCRIPT SQL")
#     print("==============================\n")

#     print(sql)

#     if args.output:
#      with open(args.output, "w", encoding="utf-8") as f:
#         f.write(sql)

#     print(f"\nSQL sauvegardé dans {args.output}")


# if __name__ == "__main__":
#     main()



# import argparse
# from core.mcd_parser import parse_mcd_file
# from core.mld_generator import mcd_to_mld
# from core.sql_generator import generate_sql

# def main():
#     parser = argparse.ArgumentParser(description="Générateur SQL à partir d'un MCD")
#     parser.add_argument("file", help="Fichier MCD (YAML, JSON ou TXT)")
#     parser.add_argument("--db", choices=["mysql", "postgres", "sqlite"], default="mysql")
#     parser.add_argument("--output", help="Fichier SQL de sortie")
#     args = parser.parse_args()

#     # 1️⃣ Lecture du MCD
#     mcd = parse_mcd_file(args.file)

#     # Affichage du MCD
#     print("\n===== MCD =====\n")
#     for table, fields in mcd.items():
#         print(f"{table}: {fields}")

#     # 2️⃣ Transformation MCD -> MLD
#     mld, relations = mcd_to_mld(mcd)
#     print("\n===== MLD =====\n")
#     for table, fields in mld.items():
#         print(f"{table}: {fields}")

#     # 3️⃣ Génération SQL
#     sql = generate_sql(mld, relations, db=args.db)
#     print("\n===== SQL GENERÉ =====\n")
#     print(sql)

#     # 4️⃣ Sauvegarde si demandé
#     if args.output:
#         with open(args.output, "w", encoding="utf-8") as f:
#             f.write(sql)
#         print(f"\nSQL sauvegardé dans {args.output}")

# if __name__ == "__main__":
#     main()


import argparse
from core.mcd_parser import parse_mcd_file
from core.mld_generator import mcd_to_mld
from core.sql_generator import generate_sql

def main():
    parser = argparse.ArgumentParser(description="Générateur SQL à partir d'un MCD")
    parser.add_argument("file", help="Fichier MCD (YAML, JSON ou TXT)")
    parser.add_argument("--db", choices=["mysql", "postgres", "sqlite"], default="mysql")
    parser.add_argument("--output", help="Fichier SQL de sortie")
    args = parser.parse_args()

    # Lecture du MCD
    mcd = parse_mcd_file(args.file)

    print("\n===== MCD =====\n")
    for table, fields in mcd.items():
        print(f"{table}: {fields}")

    # MCD → MLD + détection relations
    mld, relations = mcd_to_mld(mcd)

    print("\n===== MLD =====\n")
    for table, fields in mld.items():
        print(f"{table}: {fields}")

    # Génération SQL
    sql = generate_sql(mld, relations, db=args.db)

    print("\n===== SQL GENERÉ =====\n")
    print(sql)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(sql)
        print(f"\nSQL sauvegardé dans {args.output}")

if __name__ == "__main__":
    main()