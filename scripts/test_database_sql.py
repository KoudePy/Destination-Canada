import unittest
import sqlite3
import os

DB_PATH = "database.db"

class TestDatabaseSchema(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_tables_exist(self):
        expected_tables = {"provinces", "status_categories", "immigration_categories", "transitions"}
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in self.cursor.fetchall()}
        for table in expected_tables:
            self.assertIn(table, tables, f"Table '{table}' is manquante dans la base.")

    def test_provinces_not_empty(self):
        self.cursor.execute("SELECT COUNT(*) FROM provinces")
        count = self.cursor.fetchone()[0]
        self.assertGreater(count, 0, "La table provinces est vide.")

    def test_transitions_foreign_keys(self):
        self.cursor.execute("""
            SELECT COUNT(*) FROM transitions
            WHERE province_id IS NULL OR status_id IS NULL OR immigration_cat_id IS NULL
        """)
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 0, "Certaines lignes transitions ont des clés étrangères NULL.")

if __name__ == '__main__':
    unittest.main()
