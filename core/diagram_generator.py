# import os
# os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"
# from graphviz import Digraph

# def generate_diagram(tables, relations):

#     dot = Digraph(comment= "MLD Diagram")

#  # creer les tables

#     for table in tables:
#         dot.node(table["table"])
    
#  # creer les relations 
#     for relation  in relations:
#         dot.edge(relation["from"], relation["to"])

#     dot.render("mld_diagram", format="png", view=True)
    

import os
from graphviz import Digraph

# assure que Graphviz est dans le PATH
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"


def create_table_label(table_name, fields):

    label = f"""<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="lightblue"><B>{table_name}</B></TD></TR>
    """

    for field in fields:
        label += f"<TR><TD ALIGN='LEFT'>{field}</TD></TR>"

    label += "</TABLE>>"

    return label


def generate_diagram(tables, relations):

    dot = Digraph("MLD", format="png")
    dot.attr(rankdir="LR")

    # création des tables
    for table_name, fields in tables.items():

        label = create_table_label(table_name, fields)

        dot.node(
            table_name,
            label=label,
            shape="plaintext"
        )

    # création des relations
    for relation in relations:

        dot.edge(
            relation["from"],
            relation["to"],
            label=relation["label"]
        )

    dot.render("mld_diagram", view=True)