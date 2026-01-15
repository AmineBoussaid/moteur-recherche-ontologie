from rdflib import Graph, Literal, RDF, RDFS, Namespace

EX = Namespace("http://example.org/biblio#")

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

# Livres
g.add((EX.LivreIA, RDF.type, EX.Livre))
g.add((EX.LivreBD, RDF.type, EX.Livre))
g.add((EX.LivreWeb, RDF.type, EX.Livre))

# Catégories
g.add((EX.Informatique, RDF.type, EX.Categorie))
g.add((EX.Multimedia, RDF.type, EX.Categorie))

# =========================
# RELATIONS SÉMANTIQUES
# =========================
g.add((EX.Karim, EX.emprunte, EX.LivreIA))

g.add((EX.LivreIA, EX.ecritPar, EX.Dupont))
g.add((EX.LivreBD, EX.ecritPar, EX.Dupont))
g.add((EX.LivreWeb, EX.ecritPar, EX.Dupont))

g.add((EX.LivreIA, EX.appartientA, EX.Informatique))
g.add((EX.LivreBD, EX.appartientA, EX.Informatique))
g.add((EX.LivreWeb, EX.appartientA, EX.Multimedia))

# =========================
# INDEXATION DES DOCUMENTS
# (POINT CLÉ DU SUJET)
# =========================
g.add((EX.LivreIA, EX.aDocument, Literal("documents/LivreIA.html")))
g.add((EX.LivreBD, EX.aDocument, Literal("documents/LivreBD.html")))
g.add((EX.LivreWeb, EX.aDocument, Literal("documents/LivreWeb.html")))

# =========================
# SAUVEGARDE
# =========================
g.serialize("biblio.owl", format="xml")
print("✅ Ontologie créée et documents indexés : biblio.owl")
