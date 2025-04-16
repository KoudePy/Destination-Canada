import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium import Choropleth
from streamlit_folium import st_folium
import json
from db import (
    get_transitions_by_year,
    get_transitions_by_status,
    get_total_by_province,
    get_total_by_immigration_category
)

# Config
st.set_page_config(page_title="Destination Canada (SQL)", page_icon="🇨🇦")

# 🔐 Gestion des utilisateurs
st.sidebar.title("🔐 Connexion")
user_role = st.sidebar.selectbox(
    "Sélectionnez votre rôle",
    ["Visiteur", "Analyste", "Admin"]
)

st.title("🇨🇦 Destination Canada – Vue SQL")
st.markdown("Analyse alimentée directement par la base relationnelle")

# Sélection d'année
years = list(range(2015, 2024))
selected_year = st.selectbox("📅 Année", years)

# Récupération des données SQL
df = get_transitions_by_year(selected_year)

# Filtres dynamiques
df = df.dropna(subset=["province_name", "status_name"])
provinces = ["Toutes"] + sorted(df["province_name"].unique())
statuses = ["Tous"] + sorted(df["status_name"].unique())

selected_province = st.selectbox("🏙️ Province", provinces)
selected_status = st.selectbox("🧳 Statut temporaire", statuses)

filtered_df = df.copy()
if selected_province != "Toutes":
    filtered_df = filtered_df[filtered_df["province_name"] == selected_province]
if selected_status != "Tous":
    filtered_df = filtered_df[filtered_df["status_name"] == selected_status]

# ✅ Export CSV si autorisé
if user_role in ["Analyste", "Admin"] and not filtered_df.empty:
    st.download_button(
        label="💾 Exporter les données filtrées (CSV)",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name=f"transitions_{selected_year}.csv",
        mime="text/csv"
    )
else:
    st.info("Connectez-vous comme analyste ou admin pour exporter les données.")

# Onglets
accueil, tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Accueil",
    "📊 Par statut temporaire",
    "🏙️ Provinces populaires",
    "📈 Évolution temporelle",
    "🗺️ Carte Folium (SQL)",
    "📋 Tableau croisé"
])

with accueil:
    st.subheader("📌 Résumé des chiffres clés")
    total_transitions = int(filtered_df["total"].sum())
    top_status = (
        filtered_df.groupby("status_name")["total"].sum().idxmax()
        if not filtered_df.empty else "-"
    )
    top_province = (
        filtered_df.groupby("province_name")["total"].sum().idxmax()
        if not filtered_df.empty else "-"
    )
    st.metric("Total transitions", f"{total_transitions:,}")
    st.metric("Statut dominant", top_status)
    st.metric("Province dominante", top_province)

with tab1:
    st.subheader("📊 Transitions par statut temporaire")
    if filtered_df.empty:
        st.warning("Aucune donnée.")
    else:
        grouped = filtered_df.groupby("status_name")["total"].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 4))
        grouped.plot(kind="bar", ax=ax)
        ax.set_ylabel("Transitions")
        ax.set_xlabel("Statut")
        st.pyplot(fig)

with tab2:
    st.subheader("🏙️ Top provinces")
    if filtered_df.empty:
        st.warning("Aucune donnée.")
    else:
        top_provinces = (
            filtered_df.groupby("province_name")["total"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        top_provinces.plot(kind="bar", ax=ax2, color="skyblue")
        ax2.set_ylabel("Transitions")
        ax2.set_xlabel("Province")
        st.pyplot(fig2)

with tab3:
    st.subheader("📈 Évolution du statut dans le temps")
    if selected_status == "Tous":
        st.info("Choisissez un statut pour visualiser l’évolution.")
    else:
        subset = get_transitions_by_status(selected_year, selected_status)
        if subset.empty:
            st.warning("Aucune donnée.")
        else:
            evolution = subset.groupby("year")["total"].sum().reset_index()
            fig3, ax3 = plt.subplots(figsize=(10, 4))
            ax3.plot(evolution["year"], evolution["total"], marker="o")
            ax3.set_ylabel("Transitions")
            ax3.set_xlabel("Année")
            st.pyplot(fig3)

with tab4:
    st.subheader("🗺️ Carte interactive Folium depuis SQL")
    if filtered_df.empty:
        st.warning("Pas de données pour afficher la carte.")
    else:
        province_totals = filtered_df.groupby("province_name")["total"].sum().reset_index()
        with open("data/canada_provinces.geo.json", "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
        for f in geojson_data["features"]:
            if isinstance(f["properties"]["prov_name_en"], list):
                f["properties"]["prov_name_en"] = f["properties"]["prov_name_en"][0]

        m = folium.Map(location=[56.1304, -106.3468], zoom_start=4)
        Choropleth(
            geo_data=geojson_data,
            data=province_totals,
            columns=["province_name", "total"],
            key_on="feature.properties.prov_name_en",
            fill_color="YlGnBu",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Nombre de transitions"
        ).add_to(m)
        st_folium(m, width=800, height=550)

with tab5:
    st.subheader("📋 Analyse croisée (pivot)")
    if filtered_df.empty:
        st.warning("Aucune donnée disponible.")
    else:
        pivot = pd.pivot_table(
            filtered_df,
            index="province_name",
            columns="status_name",
            values="total",
            aggfunc="sum",
            fill_value=0
        )
        st.dataframe(pivot, use_container_width=True)
