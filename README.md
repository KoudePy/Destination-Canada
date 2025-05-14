
# 🇨🇦 Destination Canada – Analyse des parcours vers la résidence permanente

Ce projet vise à explorer les trajectoires d’expatriés au Canada ayant effectué une transition depuis un statut temporaire (étudiant, travailleur, réfugié...) vers un statut de résident permanent.

Réalisé dans le cadre du **projet fil rouge – Bootcamp Data Rockstars**.

---

## 📦 Données

- **Source officielle :** Immigration, Réfugiés et Citoyenneté Canada (IRCC)
- **Nom du dataset :** Transition from Temporary Resident to Permanent Resident Status – Monthly IRCC Updates
- **Format initial :** CSV (nettoyé en `cleaned_data1.csv`)
- **Format final :** base de données relationnelle SQLite
- **Lien source :** [open.canada.ca – IRCC](https://open.canada.ca/data/en/dataset)

---

## 🧠 Fonctionnalités de l'application

- 🔐 Connexion utilisateur avec rôles (Admin, Analyste, Visiteur)
- 📊 Filtres dynamiques : année, province, statut
- 🗺️ Carte interactive des transitions par province
- 🌍 Analyse par pays d'origine
- 📋 Tableau croisé dynamique
- 📸 Export des graphiques (PNG) et des données (CSV)
- 🧭 Navigation multi-pages

---

## 🧪 Technologies utilisées

- Python 3.11
- Streamlit
- SQLite3
- Pandas, Matplotlib, Folium
- Authentification avec `session_state`

---

## 🚀 Lancer l’application

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application principale
streamlit run eda_app_sql.py
```

---

## ✍️ Auteurs

Projet réalisé par :

- Koudedia Magssa – Data Analyst (Bootcamp Data Rockstars)
- Encadré par l’équipe pédagogique de Data Rockstars

---

## 🗂️ Structure du projet (extrait)

```
📁 data/
    ├── cleaned_data1.csv
    ├── canada_provinces.geo.json
📁 scripts/
    ├── clean_data.py
    ├── create_database.py
📁 src/
    ├── views/
    ├── controllers/
📄 eda_app_sql.py
📄 main.py
📄 requirements.txt
```

---

## 📸 Captures et démonstration

![Page d'accueil](</src/assets/images/Page%201.png>)
![Graphique bar 1](</src/assets/images/page%202.png>)
![Graphique Bar](</src/assets/images/page%203.png>)
![Carte du Canada](</src/assets/images/page%204.png>)
---

## 🧾 Licence

Ce projet est développé à des fins pédagogiques. Les données utilisées sont ouvertes et disponibles publiquement via le portail open.canada.ca.
