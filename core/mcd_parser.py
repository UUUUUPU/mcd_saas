import yaml, json

def parse_mcd_file(path):
    if path.endswith(".yaml") or path.endswith(".yml"):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    elif path.endswith(".json"):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    elif path.endswith(".txt"):
        # parse simple : une ligne = "Table: champ1, champ2, ..."
        mcd = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    table, fields = line.strip().split(":")
                    mcd[table.strip()] = [x.strip() for x in fields.split(",")]
        return mcd
    else:
        raise ValueError("Format de fichier non supporté. Utilise YAML, JSON ou TXT.")