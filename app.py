from flask import Flask, render_template, request
from rdflib import Graph, Namespace
import os

EX = Namespace("http://example.org/biblio#")
app = Flask(__name__)

# Charger l'ontologie
g = Graph()
g.parse("biblio.owl", format="xml")

# =========================
# Fonctions utilitaires
# =========================
def extraire_resume(doc_path, n_lignes=7):
    if os.path.exists(doc_path):
        with open(doc_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return "".join(lines[:n_lignes])
    return "📄 Document introuvable"

# =========================
# Recherches
# =========================
def rechercher_par_categorie(categorie):
    q = f"""
    PREFIX ex: <http://example.org/biblio#>
    SELECT ?livre ?doc ?date WHERE {{
        ?livre a ex:Livre ;
               ex:appartientA ex:{categorie} ;
               ex:aDocument ?doc ;
               ex:datePublication ?date .
    }}
    """
    results = []
    for row in g.query(q):
        results.append({
            "livre": row.livre.split("#")[-1],
            "doc": str(row.doc),
            "resume": extraire_resume(str(row.doc)),
            "date": str(row.date)
        })
    return results

def rechercher_par_auteur(auteur):
    q = f"""
    PREFIX ex: <http://example.org/biblio#>
    SELECT ?livre ?doc ?date WHERE {{
        ?livre a ex:Livre ;
               ex:ecritPar ex:{auteur} ;
               ex:aDocument ?doc ;
               ex:datePublication ?date .
    }}
    """
    results = []
    for row in g.query(q):
        results.append({
            "livre": row.livre.split("#")[-1],
            "doc": str(row.doc),
            "resume": extraire_resume(str(row.doc)),
            "date": str(row.date)
        })
    return results

def rechercher_par_date(date):
    q = f"""
    PREFIX ex: <http://example.org/biblio#>
    SELECT ?livre ?doc ?date WHERE {{
        ?livre a ex:Livre ;
               ex:datePublication "{date}" ;
               ex:aDocument ?doc .
    }}
    """
    results = []
    for row in g.query(q):
        results.append({
            "livre": row.livre.split("#")[-1],
            "doc": str(row.doc),
            "resume": extraire_resume(str(row.doc)),
            "date": str(row.date)
        })
    return results

def rechercher_livres_empruntes(lecteur):
    q = f"""
    PREFIX ex: <http://example.org/biblio#>
    SELECT ?livre ?doc ?date WHERE {{
        ex:{lecteur} ex:emprunte ?livre .
        ?livre ex:aDocument ?doc ;
               ex:datePublication ?date .
    }}
    """
    results = []
    for row in g.query(q):
        results.append({
            "livre": row.livre.split("#")[-1],
            "doc": str(row.doc),
            "resume": extraire_resume(str(row.doc)),
            "date": str(row.date)
        })
    return results

# =========================
# Route principale
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    recherche_type = None
    critere = ""
    if request.method == "POST":
        recherche_type = request.form.get("type")
        critere = request.form.get("critere")
        if recherche_type == "categorie":
            results = rechercher_par_categorie(critere)
        elif recherche_type == "auteur":
            results = rechercher_par_auteur(critere)
        elif recherche_type == "date":
            results = rechercher_par_date(critere)
    return render_template("index.html", results=results, type=recherche_type, critere=critere)

# =========================
# Lancer le serveur
# =========================
if __name__ == "__main__":
    app.run(debug=True)
