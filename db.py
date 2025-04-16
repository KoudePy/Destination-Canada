import sqlite3
from typing import Optional
import pandas as pd

# Connexion à la base SQLite avec cache
import streamlit as st

@st.cache_resource
def get_connection():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    return conn

# Récupérer toutes les transitions pour une année donnée
def get_transitions_by_year(year: int) -> pd.DataFrame:
    conn = get_connection()
    query = """
        SELECT t.*, p.name AS province_name, s.name AS status_name,
               i.main_category, i.group_category, i.sub_category
        FROM transitions t
        LEFT JOIN provinces p ON t.province_id = p.id
        LEFT JOIN status_categories s ON t.status_id = s.id
        LEFT JOIN immigration_categories i ON t.immigration_cat_id = i.id
        WHERE t.year = ?
    """
    return pd.read_sql_query(query, conn, params=(year,))

# Récupérer le total des transitions pour une province et une année
def get_total_by_province(year: int, province: str) -> Optional[int]:
    conn = get_connection()
    query = """
        SELECT SUM(t.total) AS total
        FROM transitions t
        JOIN provinces p ON t.province_id = p.id
        WHERE t.year = ? AND p.name = ?
    """
    cursor = conn.cursor()
    cursor.execute(query, (year, province))
    result = cursor.fetchone()
    return result[0] if result else 0

def get_transitions_by_status(year: int, status: str) -> pd.DataFrame:
    conn = get_connection()
    query = """
        SELECT t.*, p.name AS province_name, s.name AS status_name,
               i.main_category, i.group_category, i.sub_category
        FROM transitions t
        LEFT JOIN provinces p ON t.province_id = p.id
        LEFT JOIN status_categories s ON t.status_id = s.id
        LEFT JOIN immigration_categories i ON t.immigration_cat_id = i.id
        WHERE t.year = ? AND s.name = ?
    """
    return pd.read_sql_query(query, conn, params=(year, status))

def get_total_by_immigration_category(main_cat: str) -> Optional[int]:
    conn = get_connection()
    query = """
        SELECT SUM(t.total) AS total
        FROM transitions t
        JOIN immigration_categories i ON t.immigration_cat_id = i.id
        WHERE i.main_category = ?
    """
    cursor = conn.cursor()
    cursor.execute(query, (main_cat,))
    result = cursor.fetchone()
    return result[0] if result else 0
