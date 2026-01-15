from rdflib import Graph, Literal, RDF, RDFS, Namespace

# Namespace
EX = Namespace("http://example.org/biblio#")

# Création du graphe
g = Graph()
g.bind("ex", EX)

# =========================
# CLASSES (micro-monde)
# =========================
classes = [
    "Personne",
    "Lecteur",
    "Livre",
    "Auteur",
    "Categorie"
]

for c in classes:
    g.add((EX[c], RDF.type, RDFS.Class))

# Hiérarchie
g.add((EX.Lecteur, RDFS.subClassOf, EX.Personne))

# =========================
# PROPRIÉTÉS
# =========================
proprietes = [
    "emprunte",
    "ecritPar",
    "appartientA",
    "aDocument"
]

for p in proprietes:
    g.add((EX[p], RDF.type, RDF.Property))

# =========================
# INDIVIDUS
# =========================
# Personnes
g.add((EX.Karim, RDF.type, EX.Lecteur))
g.add((EX.Dupont, RDF.type, EX.Auteur))

# Livres existants
g.add((EX.LivreIA, RDF.type, EX.Livre))
g.add((EX.LivreBD, RDF.type, EX.Livre))
g.add((EX.LivreWeb, RDF.type, EX.Livre))

# Nouveaux livres pour tests
g.add((EX.LivreML, RDF.type, EX.Livre))
g.add((EX.LivreAlgo, RDF.type, EX.Livre))
g.add((EX.LivreWebDev, RDF.type, EX.Livre))
g.add((EX.LivreBDAvance, RDF.type, EX.Livre))
g.add((EX.LivreReseau, RDF.type, EX.Livre))

# =========================
# CATEGORIES
# =========================
# Catégories existantes
g.add((EX.Informatique, RDF.type, EX.Categorie))
g.add((EX.Multimedia, RDF.type, EX.Categorie))

# Nouvelles catégories
g.add((EX.MachineLearning, RDF.type, EX.Categorie))
g.add((EX.Algorithmes, RDF.type, EX.Categorie))
g.add((EX.Web, RDF.type, EX.Categorie))
g.add((EX.BasesDeDonnees, RDF.type, EX.Categorie))
g.add((EX.Reseaux, RDF.type, EX.Categorie))

# =========================
# RELATIONS LIVRE → CATEGORIE
# =========================
g.add((EX.LivreIA, EX.appartientA, EX.Informatique))
g.add((EX.LivreBD, EX.appartientA, EX.Informatique))
g.add((EX.LivreWeb, EX.appartientA, EX.Multimedia))

g.add((EX.LivreML, EX.appartientA, EX.MachineLearning))
g.add((EX.LivreAlgo, EX.appartientA, EX.Algorithmes))
g.add((EX.LivreWebDev, EX.appartientA, EX.Web))
g.add((EX.LivreBDAvance, EX.appartientA, EX.BasesDeDonnees))
g.add((EX.LivreReseau, EX.appartientA, EX.Reseaux))

# =========================
# RELATIONS LIVRE → AUTEUR
# =========================
livres = [
    EX.LivreIA, EX.LivreBD, EX.LivreWeb,
    EX.LivreML, EX.LivreAlgo, EX.LivreWebDev,
    EX.LivreBDAvance, EX.LivreReseau
]

for livre in livres:
    g.add((livre, EX.ecritPar, EX.Dupont))

# =========================
# RELATIONS LECTEUR → LIVRE
# =========================
g.add((EX.Karim, EX.emprunte, EX.LivreIA))
# tu peux ajouter d’autres emprunts pour tester
#g.add((EX.Karim, EX.emprunte, EX.LivreML))

# =========================
# INDEXATION DES DOCUMENTS
# =========================
g.add((EX.LivreIA, EX.aDocument, Literal("documents/LivreIA.html")))
g.add((EX.LivreBD, EX.aDocument, Literal("documents/LivreBD.html")))
g.add((EX.LivreWeb, EX.aDocument, Literal("documents/LivreWeb.html")))

g.add((EX.LivreML, EX.aDocument, Literal("documents/LivreML.html")))
g.add((EX.LivreAlgo, EX.aDocument, Literal("documents/LivreAlgo.html")))
g.add((EX.LivreWebDev, EX.aDocument, Literal("documents/LivreWebDev.html")))
g.add((EX.LivreBDAvance, EX.aDocument, Literal("documents/LivreBDAvance.html")))
g.add((EX.LivreReseau, EX.aDocument, Literal("documents/LivreReseau.html")))

# =========================
# SAUVEGARDE
# =========================
g.serialize("biblio.owl", format="xml")
print("✅ Ontologie complète créée et documents indexés : biblio.owl")
