import pandas as pd
import sqlite3

# Charger les données nettoyées
df = pd.read_csv("data/cleaned_data1.csv")

# Connexion à la base SQLite
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Création de la table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Year INTEGER,
    Month TEXT,
    Quarter TEXT,
    Province TEXT,
    MainCategory TEXT,
    GroupCategory TEXT,
    SubCategory TEXT,
    Total INTEGER
)
""")

# Insertion des données dans la table
df.to_sql("transitions", conn, if_exists="replace", index=False)

print("✅ Base de données 'database.db' créée avec la table 'transitions'")

# Fermeture de la connexion
conn.close()
