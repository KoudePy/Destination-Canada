import sqlite3

# Charger et exécuter le fichier SQL de création du schéma
with open("scripts/schema.sql", "r", encoding="utf-8") as f:
    schema_sql = f.read()

# Connexion à la base SQLite
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Exécution du schéma
cursor.executescript(schema_sql)

# Commit et fermeture
conn.commit()
conn.close()

print("Schéma SQL relationnel exécuté avec succès !")

