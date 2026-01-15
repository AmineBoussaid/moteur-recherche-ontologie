from rdflib import Graph, Namespace
import webbrowser
import os

EX = Namespace("http://example.org/biblio#")

# Charger l'ontologie
g = Graph()
g.parse("biblio.owl", format="xml")

# =========================
# FONCTIONS
# =========================
def afficher_infos_document(doc_path):
    """Affiche un résumé du document HTML"""
    if os.path.exists(doc_path):
        try:
            with open(doc_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                print("📄 Contenu résumé :")
                for line in lines[:7]:  # premières lignes du document
                    print("  ", line.strip())
        except Exception as e:
            print("❌ Impossible de lire le document :", e)
    else:
        print("❌ Document introuvable :", doc_path)

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
    results = list(g.query(q))
    if not results:
        print("❌ Aucun document trouvé pour cette catégorie.")
        return
    for row in results:
        livre = row.livre.split("#")[-1]
        doc = str(row.doc)
        print(f"\n📘 Livre : {livre}")
        afficher_infos_document(doc)
        if input("➡️ Ouvrir le document complet ? (o/n) : ").lower() == "o":
            webbrowser.open(doc)

def rechercher_par_auteur(auteur):
    print(f"\n🔍 Résultats pour l'auteur : {auteur}")
    q = f"""
    PREFIX ex: <http://example.org/biblio#>
    SELECT ?livre ?doc WHERE {{
        ex:{auteur} ex:ecritPar ?livre .
        ?livre ex:aDocument ?doc .
    }}
    """
    results = list(g.query(q))
    if not results:
        print("❌ Aucun document trouvé pour cet auteur.")
        return
    for row in results:
        livre = row.livre.split("#")[-1]
        doc = str(row.doc)
        print(f"\n📘 Livre : {livre}")
        afficher_infos_document(doc)
        if input("➡️ Ouvrir le document complet ? (o/n) : ").lower() == "o":
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
    results = list(g.query(q))
    if not results:
        print("❌ Aucun livre emprunté trouvé pour ce lecteur.")
        return
    for row in results:
        livre = row.livre.split("#")[-1]
        doc = str(row.doc)
        print(f"\n📘 Livre emprunté : {livre}")
        afficher_infos_document(doc)
        if input("➡️ Ouvrir le document complet ? (o/n) : ").lower() == "o":
            webbrowser.open(doc)

# =========================
# INTERFACE UTILISATEUR AMÉLIORÉE
# =========================
def menu_principal():
    while True:
        print("\n==============================")
        print("📚 MOTEUR DE RECHERCHE ONTOLOGIQUE")
        print("==============================")
        print("1️⃣  Rechercher des documents par catégorie")
        print("2️⃣  Rechercher des documents par auteur")
        print("3️⃣  Afficher les documents des livres empruntés")
        print("0️⃣  Quitter")
        choix = input("\nVotre choix : ")

        if choix == "1":
            cat = input("Nom de la catégorie : ")
            rechercher_par_categorie(cat)
        elif choix == "2":
            auteur = input("Nom de l'auteur : ")
            rechercher_par_auteur(auteur)
        elif choix == "3":
            nom = input("Nom du lecteur : ")
            rechercher_livres_empruntes(nom)
        elif choix == "0":
            print("👋 Fin du moteur de recherche")
            break
        else:
            print("❌ Choix invalide")

# Lancer le menu
menu_principal()
