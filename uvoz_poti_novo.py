import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
import pandas as pd
from datetime import datetime
import Data.auth as auth  # Make sure your auth.py has db, user, host, password

# DB connection details
database = auth.db
host = auth.host
port = 5432
user = auth.user
password = auth.password

# Connect to PostgreSQL
conn = psycopg2.connect(database=database, host=host, port=port, user=user, password=password)
conn.set_client_encoding('UTF8')
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def ustvari_tabelo_poti_triglav(ime_tabele: str) -> None:
    cur.execute(f"""
        DROP TABLE IF EXISTS {ime_tabele};
        CREATE TABLE IF NOT EXISTS {ime_tabele} (
            id SERIAL PRIMARY KEY,
            mountain_id INTEGER,
            route_name TEXT,
            route_time TEXT,
            route_difficulty TEXT,
            start_point TEXT,
            height_diff INTEGER,
            gear_summer TEXT,
            gear_winter TEXT
        );
    """)
    conn.commit()

def preberi_csv(ime_datoteke: str) -> pd.DataFrame:
    df = pd.read_csv(ime_datoteke,dtype=str,keep_default_na=False,usecols=[
    "mountain_id", "route_name", "route_time", "route_difficulty",
    "start_point", "height_diff", "gear_summer", "gear_winter"])
    if 'ferata' in df.columns:
        df = df.drop(columns=['ferata'])
    return df

def preimenuj_stolpce(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={
        "mountain_id": "mountain_id",
        "route_name": "route_name",
        "route_time": "route_time",
        "route_difficulty": "route_difficulty",
        "start_point": "start_point",
        "height_diff": "height_diff",
        "gear_summer": "gear_summer",
        "gear_winter": "gear_winter"
    })
    return df

def transformiraj(df: pd.DataFrame) -> pd.DataFrame:
    print("Stolpci pred transformaciji:", df.columns.tolist())
    print("Prvih nekaj vrstic:\n", df.head())
    columns = [
        "mountain_id", "route_name", "route_time", "route_difficulty",
        "start_point", "height_diff", "gear_summer", "gear_winter"
    ]
    df = df[columns]  # Ensure correct column order
    print("Stolpci po transformaciji:", df.columns.tolist())
    return df

def zapisi_df(df: pd.DataFrame) -> None:
    ime_tabele = "poti_po_gorah"

    ustvari_tabelo_poti_triglav(ime_tabele)
    if 'ferata' in df.columns:
        df = df.drop(columns=['ferata'])

    df = preimenuj_stolpce(df)
    df = transformiraj(df)
    print("Stolpci za vnos v bazo:", df.columns.tolist())
    print(df.head())

    records = df.values.tolist()
    columns = df.columns.tolist()

    sql = f'INSERT INTO {ime_tabele} ({", ".join(columns)}) VALUES %s'
    psycopg2.extras.execute_values(cur, sql, records)
    conn.commit()

if __name__ == "__main__":
    df = preberi_csv("Data/poti2.csv")  
    zapisi_df(df)
    print("Podatki uspešno zapisani v bazo.")