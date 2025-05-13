import streamlit as st

st.set_page_config(page_title="Destination Canada", page_icon="🇨🇦")
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from db import log_access

# Connexion à la base SQLite
# Ouvrir la connexion SQLite une seule fois
conn = sqlite3.connect('expatriation.db', check_same_thread=False)
cursor = conn.cursor()
 # S’assurer que la table access_logs existe
cursor.execute("""
   CREATE TABLE IF NOT EXISTS access_logs (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     event_time DATETIME NOT NULL,
     user_id INTEGER NOT NULL,
     action TEXT,
     ip_address TEXT,
     user_agent TEXT,
     page TEXT,
     FOREIGN KEY (user_id) REFERENCES users(id)
  );
""")
conn.commit()
current_user_id = 1

@st.cache_resource
def get_connection():
    return sqlite3.connect("database.db", check_same_thread=False)

conn = get_connection()

# Titre de l'application
st.title("📊 Transitions vers la résidence permanente au Canada")

# Choix de la requête
option = st.selectbox("📂 Choisis une vue :", [
    "Transitions par année",
    "Transitions par statut temporaire",
    "Top provinces de destination"
])

log_access(
    conn,
    current_user_id,
    action=f"view_{option.lower().replace(' ', '_')}",
    page=option
)
option = st.sidebar.selectbox("📂 Choisis une vue :", [
    "Exploration", "Cartographie", "Tableau croisé", "Top provinces de destination"
])
log_access(
    conn,
    current_user_id,
    action=f"view_{option.lower().replace(' ', '_')}",
    page=option
)
# Fonctions de requêtes
def fetch_data(query):
    return pd.read_sql_query(query, conn)

if option == "Transitions par année":
    df = fetch_data("""
        SELECT Year, SUM(Total) AS total_transitions
        FROM transitions
        GROUP BY Year
        ORDER BY Year;
    """)
    st.subheader("Nombre total de transitions par année")
    st.bar_chart(df.set_index("Year"))

elif option == "Transitions par statut temporaire":
    df = fetch_data("""
        SELECT GroupCategory, SUM(Total) AS total
        FROM transitions
        GROUP BY GroupCategory
        ORDER BY total DESC;
    """)
    st.subheader("Répartition des statuts temporaires")
    st.dataframe(df)

elif option == "Top provinces de destination":
    df = fetch_data("""
        SELECT Province, SUM(Total) AS total
        FROM transitions
        GROUP BY Province
        ORDER BY total DESC
        LIMIT 5;
    """)
    st.subheader("Top 5 provinces de destination")
    st.bar_chart(df.set_index("Province"))

# Fermeture (optionnel ici car cache_resource gère ça)
# conn.close()
