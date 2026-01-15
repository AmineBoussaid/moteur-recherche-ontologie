from rdflib import Graph, Namespace
import webbrowser

EX = Namespace("http://example.org/biblio#")

# Charger l'ontologie
g = Graph()
g.parse("biblio.owl", format="xml")

# =========================
# FONCTIONS DE RECHERCHE
# =========================

def rechercher_par_categorie(categorie):
    print(f"\n🔍 Résultats pour la catégorie : {categorie}")

    q = f"""
    PREFIX ex: <http://example.org/biblio#>
    SELECT ?livre ?doc WHERE {{
        ?livre a ex:Livre ;
               ex:appartientA ex:{categorie} ;
               ex:aDocument ?doc .
    }}
    """

    for row in g.query(q):
        livre = row.livre.split("#")[-1]
        doc = str(row.doc)

        print(f"\n📘 Livre : {livre}")
        print(f"📄 Document : {doc}")

        ouvrir = input("➡️ Ouvrir le document ? (o/n) : ")
        if ouvrir.lower() == "o":
            webbrowser.open(doc)


def rechercher_livres_empruntes(lecteur):
    print(f"\n👤 Livres empruntés par : {lecteur}")

    q = f"""
    PREFIX ex: <http://example.org/biblio#>
    SELECT ?livre ?doc WHERE {{
        ex:{lecteur} ex:emprunte ?livre .
        ?livre ex:aDocument ?doc .
    }}
    """

    for row in g.query(q):
        print("-", row.livre.split("#")[-1])
        print("  📄", row.doc)

# =========================
# INTERFACE UTILISATEUR
# =========================

while True:
    print("\n====== MOTEUR DE RECHERCHE ONTOLOGIQUE ======")
    print("1. Rechercher des documents par catégorie")
    print("2. Afficher les documents des livres empruntés")
    print("0. Quitter")

    choix = input("Votre choix : ")

    if choix == "1":
        cat = input("Nom de la catégorie : ")
        rechercher_par_categorie(cat)

    elif choix == "2":
        nom = input("Nom du lecteur : ")
        rechercher_livres_empruntes(nom)

    elif choix == "0":
        print("👋 Fin du moteur de recherche")
        break

    else:
        print("❌ Choix invalide")
