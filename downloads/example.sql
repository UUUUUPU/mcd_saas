
CREATE TABLE TYPE_USERS (
    id_type_user INT AUTO_INCREMENT,
    libelle VARCHAR(255),
    PRIMARY KEY (id_type_user)
);

CREATE TABLE UTILISATEURS (
    id_user INT AUTO_INCREMENT,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    id_type_user INT,
    PRIMARY KEY (id_user),
    FOREIGN KEY (id_type_user) REFERENCES TYPE_USERS(id_type_user)
);

CREATE TABLE PROJETS (
    id_projet INT AUTO_INCREMENT,
    nom VARCHAR(255),
    date_debut VARCHAR(255),
    date_fin VARCHAR(255),
    PRIMARY KEY (id_projet)
);

CREATE TABLE TACHES (
    id_tache INT AUTO_INCREMENT,
    description VARCHAR(255),
    date_echeance VARCHAR(255),
    id_projet INT,
    id_user INT,
    PRIMARY KEY (id_tache),
    FOREIGN KEY (id_projet) REFERENCES PROJETS(id_projet)
);

CREATE TABLE DEPARTEMENTS (
    id_dept INT AUTO_INCREMENT,
    nom VARCHAR(255),
    PRIMARY KEY (id_dept)
);

CREATE TABLE EMPLOYES (
    id_emp INT AUTO_INCREMENT,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    id_dept INT,
    PRIMARY KEY (id_emp)
);

CREATE TABLE CLIENTS (
    id_client INT AUTO_INCREMENT,
    nom VARCHAR(255),
    email VARCHAR(255),
    PRIMARY KEY (id_client)
);

CREATE TABLE FACTURES (
    id_facture INT AUTO_INCREMENT,
    montant VARCHAR(255),
    date VARCHAR(255),
    id_client INT,
    PRIMARY KEY (id_facture),
    FOREIGN KEY (id_client) REFERENCES CLIENTS(id_client)
);

CREATE TABLE PROJET_CLIENT (
    id_projet INT AUTO_INCREMENT,
    id_client INT,
    PRIMARY KEY (id_projet),
    FOREIGN KEY (id_client) REFERENCES CLIENTS(id_client)
);

CREATE TABLE EMPLOYE_TACHE (
    id_emp INT AUTO_INCREMENT,
    id_tache INT,
    PRIMARY KEY (id_emp),
    FOREIGN KEY (id_tache) REFERENCES TACHES(id_tache)
);
