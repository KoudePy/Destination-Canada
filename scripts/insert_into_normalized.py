import pandas as pd
import sqlite3

# Charger les données nettoyées
csv_path = "data/cleaned_data1.csv"
df = pd.read_csv(csv_path)

# Mapping FR -> EN des provinces
province_mapping = {
    "Québec": "Quebec",
    "Colombie-Britannique": "British Columbia",
    "Terre-Neuve-et-Labrador": "Newfoundland and Labrador",
    "Nouveau-Brunswick": "New Brunswick",
    "Nouvelle-Écosse": "Nova Scotia",
    "Île-du-Prince-Édouard": "Prince Edward Island",
    "Territoires du Nord-Ouest": "Northwest Territories",
    "T.-N.-L.": "Newfoundland and Labrador",
    "C.-B.": "British Columbia",
    "N.-É.": "Nova Scotia",
    "Î.-P.-É.": "Prince Edward Island",
    "T. N.-O.": "Northwest Territories",
    "T. N. O.": "Northwest Territories"
}

# Connexion à la base
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Insérer dans la table provinces (avec noms anglais)
provinces = df["Province"].dropna().unique()
for prov in provinces:
    english_name = province_mapping.get(prov, prov)
    cursor.execute("INSERT OR IGNORE INTO provinces (name) VALUES (?)", (english_name,))

# Insérer dans la table status_categories
statuses = df["GroupCategory"].dropna().unique()
for status in statuses:
    cursor.execute("INSERT OR IGNORE INTO status_categories (name) VALUES (?)", (status,))

# Insérer dans la table immigration_categories
immigration_cats = df[["MainCategory", "GroupCategory", "SubCategory"]].dropna().drop_duplicates()
for _, row in immigration_cats.iterrows():
    cursor.execute("""
        INSERT OR IGNORE INTO immigration_categories (main_category, group_category, sub_category)
        VALUES (?, ?, ?)
    """, (row["MainCategory"], row["GroupCategory"], row["SubCategory"]))

# Insérer les lignes principales avec les IDs
for _, row in df.iterrows():
    # Récupérer les IDs liés avec nom anglais
    prov_eng = province_mapping.get(row["Province"], row["Province"])
    cursor.execute("SELECT id FROM provinces WHERE name = ?", (prov_eng,))
    province_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM status_categories WHERE name = ?", (row["GroupCategory"],))
    status_id = cursor.fetchone()[0]

    cursor.execute("""
        SELECT id FROM immigration_categories
        WHERE main_category = ? AND group_category = ? AND sub_category = ?
    """, (row["MainCategory"], row["GroupCategory"], row["SubCategory"]))
    immigration_cat_id = cursor.fetchone()[0]

    # Insérer dans la table transitions
    cursor.execute("""
        INSERT INTO transitions (year, month, quarter, province_id, status_id, immigration_cat_id, total)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        row["Year"], row["Month"], row["Quarter"],
        province_id, status_id, immigration_cat_id,
        int(row["Total"])
    ))

conn.commit()
conn.close()

print("Importation complète dans la base normalisée avec provinces en anglais !")
