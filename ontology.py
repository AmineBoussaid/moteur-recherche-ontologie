from rdflib import Graph, Literal, RDF, RDFS, Namespace

# Namespace
EX = Namespace("http://example.org/biblio#")

# Création du graphe
g = Graph()
g.bind("ex", EX)

# =========================
# CLASSES
# =========================
classes = ["Personne", "Lecteur", "Livre", "Auteur", "Categorie"]
for c in classes:
    g.add((EX[c], RDF.type, RDFS.Class))

# Hiérarchie
g.add((EX.Lecteur, RDFS.subClassOf, EX.Personne))

# =========================
# PROPRIÉTÉS
# =========================
proprietes = ["emprunte", "ecritPar", "appartientA", "aDocument", "datePublication"]
for p in proprietes:
    g.add((EX[p], RDF.type, RDF.Property))

# =========================
# INDIVIDUS
# =========================
# Personnes
g.add((EX.Karim, RDF.type, EX.Lecteur))
g.add((EX.Dupont, RDF.type, EX.Auteur))

# Livres
livres = ["LivreIA", "LivreBD", "LivreWeb", "LivreML", "LivreAlgo", "LivreWebDev", "LivreBDAvance", "LivreReseau"]
for l in livres:
    g.add((EX[l], RDF.type, EX.Livre))
    g.add((EX[l], EX.ecritPar, EX.Dupont))

# =========================
# CATEGORIES
# =========================
categories = {
    "LivreIA": "Informatique",
    "LivreBD": "Informatique",
    "LivreWeb": "Multimedia",
    "LivreML": "MachineLearning",
    "LivreAlgo": "Algorithmes",
    "LivreWebDev": "Web",
    "LivreBDAvance": "BasesDeDonnees",
    "LivreReseau": "Reseaux"
}

for c in set(categories.values()):
    g.add((EX[c], RDF.type, EX.Categorie))

for livre, cat in categories.items():
    g.add((EX[livre], EX.appartientA, EX[cat]))

# =========================
# RELATIONS LECTEUR → LIVRE
# =========================
g.add((EX.Karim, EX.emprunte, EX.LivreIA))
g.add((EX.Karim, EX.emprunte, EX.LivreML))

# =========================
# DATE DE PUBLICATION
# =========================
dates = {
    "LivreIA": "2025-01-01",
    "LivreBD": "2024-09-15",
    "LivreWeb": "2025-03-10",
    "LivreML": "2025-02-20",
    "LivreAlgo": "2024-11-05",
    "LivreWebDev": "2025-01-30",
    "LivreBDAvance": "2025-03-05",
    "LivreReseau": "2025-02-12"
}

for livre, date in dates.items():
    g.add((EX[livre], EX.datePublication, Literal(date)))

# =========================
# DOCUMENTS HTML (dans static/documents/)
# =========================
docs = {
    "LivreIA": "static/documents/LivreIA.html",
    "LivreBD": "static/documents/LivreBD.html",
    "LivreWeb": "static/documents/LivreWeb.html",
    "LivreML": "static/documents/LivreML.html",
    "LivreAlgo": "static/documents/LivreAlgo.html",
    "LivreWebDev": "static/documents/LivreWebDev.html",
    "LivreBDAvance": "static/documents/LivreBDAvance.html",
    "LivreReseau": "static/documents/LivreReseau.html"
}

for livre, path in docs.items():
    g.add((EX[livre], EX.aDocument, Literal(path)))

# =========================
# SAUVEGARDE
# =========================
g.serialize("biblio.owl", format="xml")
print("✅ Ontologie complète créée et documents indexés : biblio.owl")
