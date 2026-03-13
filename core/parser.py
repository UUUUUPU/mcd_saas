import json
import yaml
import os

def parse_model(path):
    """
    Lit un fichier MCD (.yaml, .json ou .txt)
    et retourne un dictionnaire Python
    """
    ext = os.path.splitext(path)[1].lower()

    # YAML
    if ext in [".yaml", ".yml"]:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    # JSON
    elif ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # TXT (format simple)
    elif ext == ".txt":
        tables = {}
        current_table = None

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Détecte le nom de table
                if line.endswith(":"):
                    current_table = line[:-1].strip()
                    tables[current_table] = []
                elif current_table:
                    # Supprime les tirets et espaces en début de ligne
                    clean_field = line.lstrip("- ").strip()
                    if clean_field:  # ignore les lignes vides
                        tables[current_table].append(clean_field)
        return tables

    else:
        raise ValueError("Format de fichier non supporté. Utilisez YAML, JSON ou TXT.")