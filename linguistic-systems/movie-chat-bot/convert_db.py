import sqlite3
import pandas as pd
import os


def setup_database():
    # Convert the DB from csv to db format
    if os.path.exists('assets/films_processed.csv'):
        df = pd.read_csv('assets/films_processed.csv', sep='\t')
        conn = sqlite3.connect('assets/films_sql.db')
        df.to_sql('films', conn, if_exists='replace', index=False)
        conn.close()
        print("CSV was converted to SQLite")

    # Check the DB structure
    conn = sqlite3.connect('assets/films_sql.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("Tables:", tables)

    if tables:
        table_name = tables[0][0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print(f"Structure of {table_name}:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")

        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
        sample_data = cursor.fetchall()
        print("Data example:")
        for row in sample_data:
            print(f"  {row}")

    conn.close()


if __name__ == "__main__":
    setup_database()