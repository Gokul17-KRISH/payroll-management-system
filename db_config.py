# =============================================================================
#  PAYROLL MANAGEMENT SYSTEM — Database Configuration (SQLite)
#  File   : db_config.py
#  Purpose: Handles all SQLite connection logic.
#           Zero external dependencies needed. 
# =============================================================================

import os
import sqlite3
import streamlit as st

# The SQLite database file will be created in the same directory as this script
DB_FILE = os.path.join(os.path.dirname(__file__), "payroll.db")

def get_connection():
    """
    Creates and returns a connection to the SQLite local database.
    """
    try:
        # Connect to the local SQLite file (creates it if it doesn't exist)
        conn = sqlite3.connect(DB_FILE)
        
        # Enforce foreign key constraints (SQLite disables them by default)
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Allow accessing columns by name instead of just index
        conn.row_factory = sqlite3.Row
        
        return conn
    except sqlite3.Error as err:
        st.error(f"❌ SQLite Connection Error: {err}")
        return None

def init_db():
    """
    Initializes the SQLite database and creates all tables if they
    don't already exist by running the schema.sql file.
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            sql_script = f.read()

        # Execute the entire script at once
        cursor.executescript(sql_script)
        conn.commit()

    except FileNotFoundError:
        st.error(f"❌ schema.sql not found at: {schema_path}")
    except sqlite3.Error as err:
        st.error(f"❌ Schema execution error: {err}")
    finally:
        cursor.close()
        conn.close()
