import pandas as pd
import sqlite3
import os

# --- Étape 1 : Charger le CSV nettoyé ---
csv_path = "data/cleaned_data1.csv"
db_path = "database.db"

if not os.path.exists(csv_path):
    print(f"❌ Le fichier {csv_path} est introuvable.")
    exit()

df = pd.read_csv(csv_path, sep=",")

print("Colonnes présentes dans le fichier :")
print(df.columns.tolist())

# Garder uniquement les colonnes utiles
df = df[[
    "Year", "Month", "Quarter", "Province",
    "MainCategory", "GroupCategory", "SubCategory", "Total"
]]

# Renommer les colonnes pour la base SQL
df = df.rename(columns={
    "EN_YEAR": "Year",
    "EN_MONTH": "Month",
    "EN_QUARTER": "Quarter",
    "EN_PROVINCE_TERRITORY": "Province",
    "EN_IMMIGRATION_CATEGORY-MAIN_CATEGORY": "MainCategory",
    "EN_IMMIGRATION_CATEGORY-GROUP": "GroupCategory",
    "EN_IMMIGRATION_CATEGORY-COMPONENT": "SubCategory",
    "TOTAL": "Total"
})

# Nettoyer la colonne Total
df["Total"] = pd.to_numeric(df["Total"], errors="coerce")
df = df.dropna(subset=["Total"])
# --- 🔚 FIN DU BLOC AJOUTÉ ---

# --- Étape 2 : Connexion à SQLite et création de la table ---
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS transitions")

cursor.execute("""
CREATE TABLE transitions (
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

df.to_sql("transitions", conn, if_exists="append", index=False)

print("✅ La base de données a bien été créée avec la table 'transitions' !")
cursor.execute("SELECT COUNT(*) FROM transitions")
print("Nombre de lignes :", cursor.fetchone()[0])

conn.close()
