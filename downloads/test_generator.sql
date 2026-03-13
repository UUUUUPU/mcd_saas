
CREATE TABLE TYPE_USERS (
    id_type_user INT AUTO_INCREMENT,
    libelle VARCHAR(255),
    PRIMARY KEY (id_type_user)
);

CREATE TABLE UTILISATEURS (
    id_user INT AUTO_INCREMENT,
    matricule VARCHAR(255),
    noms VARCHAR(255),
    prenoms VARCHAR(255),
    sexe VARCHAR(255),
    telephone VARCHAR(255),
    adresse VARCHAR(255),
    est_actif VARCHAR(255),
    login VARCHAR(255),
    mot_de_passe VARCHAR(255),
    id_type_user INT,
    PRIMARY KEY (id_user),
    FOREIGN KEY (id_type_user) REFERENCES TYPE_USERS(id_type_user)
);
