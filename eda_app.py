import streamlit as st
st.set_page_config(page_title="Destination Canada", page_icon="🇨🇦")

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Connexion base
@st.cache_resource
def get_connection():
    return sqlite3.connect("../database.db", check_same_thread=False)

conn = sqlite3.connect("database.db")

# Récupération des données
df = pd.read_sql_query("SELECT * FROM transitions", conn)

# Titre et intro
st.title("🇨🇦 Destination Canada")
st.markdown("Analyse des transitions vers la résidence permanente selon le statut temporaire, la province et l’année.")

# Filtres
years = sorted(df["Year"].dropna().unique())
provinces = sorted(df["Province"].dropna().unique())
statuses = sorted(df["GroupCategory"].dropna().unique())

col1, col2, col3 = st.columns(3)
selected_year = col1.selectbox("📅 Année", years)
selected_province = col2.selectbox("🏙️ Province", ["Toutes"] + provinces)
selected_status = col3.selectbox("🧳 Statut temporaire", ["Tous"] + statuses)

# Filtrage
filtered_df = df[df["Year"] == selected_year]

if selected_province != "Toutes":
    filtered_df = filtered_df[filtered_df["Province"] == selected_province]

if selected_status != "Tous":
    filtered_df = filtered_df[filtered_df["GroupCategory"] == selected_status]

# Graphiques
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Transitions par statut",
    "🏙️ Provinces populaires",
    "📈 Évolution dans le temps",
    "🗺️ Carte interactive"
])

with tab1:
    st.subheader("📊 Nombre de transitions par statut temporaire")
    grouped = filtered_df.groupby("GroupCategory")["Total"].sum().sort_values(ascending=False)

    fig1, ax1 = plt.subplots(figsize=(10, 4))
    grouped.plot(kind="bar", ax=ax1)
    ax1.set_ylabel("Nombre de transitions")
    ax1.set_xlabel("Statut temporaire")
    st.pyplot(fig1)

with tab2:
    st.subheader("🏙️ Top 5 provinces de destination")
    top_provinces = (
        filtered_df.groupby("Province")["Total"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    top_provinces.plot(kind="bar", ax=ax2, color="skyblue")
    ax2.set_ylabel("Nombre de transitions")
    ax2.set_xlabel("Province")
    st.pyplot(fig2)

with tab3:
    if selected_status != "Tous":
        st.subheader(f"📈 Évolution du statut « {selected_status} » dans le temps")
        evolution_df = (
            df[df["GroupCategory"] == selected_status]
            .groupby("Year")["Total"]
            .sum()
            .reset_index()
        )

        fig3, ax3 = plt.subplots(figsize=(10, 4))
        ax3.plot(evolution_df["Year"], evolution_df["Total"], marker="o", linestyle="-")
        ax3.set_xlabel("Année")
        ax3.set_ylabel("Nombre de transitions")
        st.pyplot(fig3)
    else:
        st.info("Choisis un statut temporaire pour voir son évolution.")
