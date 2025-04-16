import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium import Choropleth, Tooltip
from streamlit_folium import st_folium
import json
from db import (
    get_transitions_by_year,
    get_transitions_by_status,
    get_total_by_province,
    get_total_by_immigration_category
)

# Sélecteurs en haut de page
years = list(range(2015, 2024))
selected_year = st.selectbox("🗓️ Année", years)

df = get_transitions_by_year(selected_year)

# Titre et config
st.set_page_config(page_title="Destination Canada", page_icon="🇨🇦")
st.title("🇨🇦 Destination Canada")
st.markdown("📊 Transitions par statut")
st.markdown("🗓️ Choisissez une année")

# Données
@st.cache_data
def load_data():
    return pd.read_csv("data/cleaned_data1.csv")

df = load_data()

# Filtres
years = sorted(df["Year"].dropna().unique())
provinces = ["Toutes"] + sorted(df["Province"].dropna().unique())
statuses = ["Tous"] + sorted(df["GroupCategory"].dropna().unique())

selected_year = st.selectbox("🗓️ Année", years, index=years.index(2015))
selected_province = st.selectbox("🏩 Province", provinces)
selected_status = st.selectbox("🧳 Statut temporaire", statuses)

# Filtrage
filtered_df = df[df["Year"] == selected_year]
if selected_province != "Toutes":
    filtered_df = filtered_df[filtered_df["Province"] == selected_province]
if selected_status != "Tous":
    filtered_df = filtered_df[filtered_df["GroupCategory"] == selected_status]

# Onglets
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Transitions par statut",
    "🏩 Provinces populaires",
    "📈 Évolution dans le temps",
    "🗺️ Carte interactive"
])

# Tab 1
with tab1:
    st.subheader("📊 Nombre de transitions par statut temporaire")
    if filtered_df.empty:
        st.warning("⚠️ Aucune donnée disponible pour ces filtres.")
    else:
        grouped = filtered_df.groupby("GroupCategory")["Total"].sum().sort_values(ascending=False)
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        grouped.plot(kind="bar", ax=ax1)
        ax1.set_ylabel("Nombre de transitions")
        ax1.set_xlabel("Statut temporaire")
        st.pyplot(fig1)

# Tab 2
with tab2:
    st.subheader("🏩 Top 5 provinces de destination")
    if filtered_df.empty:
        st.warning("⚠️ Aucune donnée disponible pour ces filtres.")
    else:
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

# Tab 3
with tab3:
    if selected_status != "Tous":
        subset = df[df["GroupCategory"] == selected_status]
        if subset.empty:
            st.warning("⚠️ Aucune donnée disponible pour ce statut.")
        else:
            st.subheader(f"📈 Évolution du statut « {selected_status} » dans le temps")
            evolution_df = subset.groupby("Year")["Total"].sum().reset_index()
            fig3, ax3 = plt.subplots(figsize=(10, 4))
            ax3.plot(evolution_df["Year"], evolution_df["Total"], marker="o")
            ax3.set_xlabel("Année")
            ax3.set_ylabel("Nombre de transitions")
            st.pyplot(fig3)
    else:
        st.info("Sélectionnez un statut pour afficher son évolution.")

# Tab 4
with tab4:
    st.subheader("🗺️ Carte interactive des transitions par province")
    subset = filtered_df[filtered_df["Year"] == selected_year]
    if subset.empty:
        st.warning("⚠️ Aucune donnée pour cette année avec les filtres sélectionnés.")
    else:
        province_totals = (
            subset.groupby("Province")["Total"]
            .sum()
            .reset_index()
        )

        # Charger GeoJSON
        with open("data/canada_provinces.geo.json", "r", encoding="utf-8") as f:
            geojson_data = json.load(f)

        # Corriger si besoin
        for f in geojson_data["features"]:
            if isinstance(f["properties"]["prov_name_en"], list):
                f["properties"]["prov_name_en"] = f["properties"]["prov_name_en"][0]

        # Carte
        m = folium.Map(location=[56.1304, -106.3468], zoom_start=4, tiles="cartodbpositron")

        # Choropleth
        Choropleth(
            geo_data=geojson_data,
            data=province_totals,
            columns=["Province", "Total"],
            key_on="feature.properties.prov_name_en",
            fill_color="YlGnBu",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Nombre de transitions"
        ).add_to(m)

        st_folium(m, width=800, height=550)

