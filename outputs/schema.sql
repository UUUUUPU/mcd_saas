CREATE TABLE ETUDIANT (
    id_etudiant INT,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    PRIMARY KEY (id_etudiant)
);

CREATE TABLE COURS (
    id_cours INT,
    titre VARCHAR(255),
    PRIMARY KEY (id_cours)
);

CREATE TABLE INSCRIPTION (
    id_etudiant INT,
    id_cours INT,
    date_inscription VARCHAR(255)
);

ALTER TABLE INSCRIPTION
ADD CONSTRAINT fk_etudiant_inscription
FOREIGN KEY (etudiant_id)
REFERENCES ETUDIANT(etudiant_id);

ALTER TABLE INSCRIPTION
ADD CONSTRAINT fk_cours_inscription
FOREIGN KEY (cours_id)
REFERENCES COURS(cours_id);

