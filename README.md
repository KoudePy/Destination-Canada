[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/pvyz0boK)
# Projet Streamlit
**Auteurs:**

*Marouan K. : marouan@datarockstars.ai*

*Matis C. : matis@datarockstars.ai*

*Bilel O. : bilel@datarockstars.ai*

## Démarrage

- Naviguez jusqu'à ce dossier : `cd projet-fil-rouge-{username_github}`
- Vérifiez que vous voyez bien les fichiers de ce dépôt lorsque vous exécutez `ls`.

### MacOS / Linux

- Dans le terminal, exécutez la commande suivante : `bash setup.sh` pour démarrer le projet. Vous n'aurez pas à le faire les prochaines fois.
- Exécutez maintenant, `bash run.sh` pour afficher le site crée à l'aide de Streamlit.

### Windows

Exécutez les commandes suivantes, dans l'ordre :
- Pour installer les librairies utiles et initialiser la base de données :

`pip install --update pip`

`pip install -r requirements.txt`

`python3 setup.py`
- Pour lancer votre application Streamlit :
`streamlit run main.py`

### Nettoyage des données

Ce script (`clean_data.py`) permet de nettoyer le fichier `data1.csv` :
- Conversion des champs en format exploitable
- Nettoyage des colonnes
- Sauvegarde dans `data/cleaned_data1.csv`


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

![Page d'accueil](<Page 1.png>)
![Graphique bar 1](<page 2.png>)
![Graphique Bar](<page 3.png>)
![Carte du Canada](<page 4.png>)
---

## 🧾 Licence

Ce projet est développé à des fins pédagogiques. Les données utilisées sont ouvertes et disponibles publiquement via le portail open.canada.ca.
