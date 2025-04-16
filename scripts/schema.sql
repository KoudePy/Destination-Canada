-- Script SQL pour créer une base relationnelle propre pour le projet Destination Canada

-- Nettoyage des anciennes tables si elles existent
DROP TABLE IF EXISTS transitions;
DROP TABLE IF EXISTS provinces;
DROP TABLE IF EXISTS status_categories;
DROP TABLE IF EXISTS immigration_categories;

-- Table des provinces
CREATE TABLE provinces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- Table des statuts temporaires (GroupCategory)
CREATE TABLE status_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- Table des catégories d'immigration (Main/Sub)
CREATE TABLE immigration_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    main_category TEXT NOT NULL,
    group_category TEXT,
    sub_category TEXT
);

-- Table principale des transitions
CREATE TABLE transitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER,
    month TEXT,
    quarter TEXT,
    province_id INTEGER,
    status_id INTEGER,
    immigration_cat_id INTEGER,
    total INTEGER,
    FOREIGN KEY (province_id) REFERENCES provinces(id),
    FOREIGN KEY (status_id) REFERENCES status_categories(id),
    FOREIGN KEY (immigration_cat_id) REFERENCES immigration_categories(id)
);
