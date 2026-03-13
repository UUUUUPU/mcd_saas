class Entite:
    def __int__(self, nom, attributs):
        self.nom = nom
        self.attributs = attributs

class Relation:
    def __int__(self, nom, type_relation, entites):
        self.nom = nom 
        self.type_relation = type_relation
        self.entites = entites
