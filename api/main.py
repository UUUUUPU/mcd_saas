# from fastapi import FastAPI, UploadFile
# from core.parser import load_mcd
# from core.transformer import transform
# from core.sql_generator import generate_mysql

# app = FastAPI()

# @app.post("/generate")
# async def generate(file: UploadFile):

#     content = await file.read()

#     with open("temp.yaml","wb") as f:
#         f.write(content)

#     mcd = load_mcd("temp.yaml")

#     tables = transform(mcd)

#     sql = generate_mysql(tables)

#     return {"sql": sql}


#####
# from fastapi import FastAPI
# from core.mcd_transformer import transform_mcd_to_mld
# from core.sql_generator import generate_sql

# app = FastAPI()


# @app.get("/")
# def home():
#     return {"message": "MCD SaaS API running"}


# @app.post("/generate_sql")
# def generate_sql_api(data: dict):

#     # récupérer les données envoyées
#     entities = data["entities"]
#     relations = data["relations"]

#     # transformer MCD → MLD
#     tables = transform_mcd_to_mld(entities, relations)

#     # choisir le SGBD (mysql par défaut)
#     db_type = data.get("db", "mysql")

#     # générer le SQL
#     sql = generate_sql(tables, db=db_type)

#     return {
#         "database": db_type,
#         "tables": tables,
#         "sql": sql
#     }


# @app.post("/generate_tables")
# def generate_tables(data: dict):

#     entities = data["entities"]
#     relations = data["relations"]

#     tables = transform_mcd_to_mld(entities, relations)

#     return {
#         "tables": tables
#     }


from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil, os, json
import graphviz

from core.parser import parse_model
from core.mld_generator import mcd_to_mld
from core.sql_generator import generate_sql

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Servir le front-end
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return FileResponse("static/index.html")


import graphviz
def mcd_to_image(mcd: dict, relations: list = None, output_path: str = "MCD"):
    """
    Génère un MCD en image PNG à partir du dictionnaire mcd et relations
    relations : liste de tuples (left_table, right_table, type)
    """
    dot = graphviz.Digraph(format='png')
    dot.attr(rankdir='LR')  # disposition de gauche à droite

    # Créer les noeuds pour chaque table
    for table, fields in mcd.items():
        # Détecter la PK
        pk_fields = [f for f in fields if f.startswith("PK ")]
        label = f"<<TABLE BORDER='1' CELLBORDER='1' CELLSPACING='0'>"
        label += f"<TR><TD BGCOLOR='lightblue'><B>{table}</B></TD></TR>"
        for f in fields:
            if f in pk_fields or f.startswith("PK "):
                f_name = f.replace("PK ", "")
                label += f"<TR><TD><B>{f_name}</B></TD></TR>"
            else:
                label += f"<TR><TD>{f}</TD></TR>"
        label += "</TABLE>>"

        dot.node(table, label=label, shape="plain")

    # Ajouter les relations si fournies
    if relations:
        for left, right, rel_type in relations:
            if rel_type == "1-N":
                dot.edge(left, right, arrowhead='crow', label="1-N")
            elif rel_type == "1-1":
                dot.edge(left, right, arrowhead='none', label="1-1")
            elif rel_type == "N-N":
                dot.edge(left, right, arrowhead='crow', label="N-N", style="dashed")

    dot.render(output_path, cleanup=True)  # génère output_path.png

    dot = graphviz.Digraph(format='png')
    
    for table, fields in mcd.items():
        label = f"{table}\n" + "\n".join(fields)
        dot.node(table, label=label, shape="box")
    dot.render(output_path, cleanup=True)  # génère output_path.png


@app.post("/generate")
async def generate(file: UploadFile = File(...), db: str = "mysql"):
    # Sauvegarde du fichier uploadé
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse MCD
    mcd = parse_model(path)

    # Transformation MCD -> MLD
    mld, relations = mcd_to_mld(mcd)

    # Génération SQL
    sql = generate_sql(mld, relations, db=db)

    # Préparer les fichiers téléchargeables
    base_name = os.path.splitext(file.filename)[0]

    # 1️ MCD image
    # Génération MCD image
    mcd_img_path = os.path.join(DOWNLOAD_DIR, f"{base_name}_MCD")
    mcd_to_image(mcd, relations, mcd_img_path)
    mcd_img_file = f"{mcd_img_path}.png"

    # 2️ MLD texte
    mld_file_path = os.path.join(DOWNLOAD_DIR, f"{base_name}_MLD.txt")
    with open(mld_file_path, "w", encoding="utf-8") as f:
        json.dump(mld, f, indent=2)

    # 3️ SQL
    sql_file_path = os.path.join(DOWNLOAD_DIR, f"{base_name}.sql")
    with open(sql_file_path, "w", encoding="utf-8") as f:
        f.write(sql)

    return JSONResponse({
        "mcd": mcd,
        "mld": mld,
        "sql": sql,
        "mcd_img": f"/download/{os.path.basename(mcd_img_file)}",
        "mld_file": f"/download/{os.path.basename(mld_file_path)}",
        "sql_file": f"/download/{os.path.basename(sql_file_path)}"
    })


@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/octet-stream', filename=filename)
    return {"error": "Fichier introuvable"}