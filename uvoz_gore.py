import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
import pandas as pd
from datetime import datetime
import Data.auth as auth  # Make sure this file contains db, user, host, password


# DB connection
database = auth.db
host = auth.host
port = 5432
user = auth.user
password = auth.password

conn = psycopg2.connect(database=database, host=host, port=port, user=user, password=password)
conn.set_client_encoding('UTF8')
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def ustvari_tabelo_gore(ime_tabele: str) -> None:
    cur.execute(f"""
        DROP TABLE IF EXISTS {ime_tabele};
        CREATE TABLE IF NOT EXISTS {ime_tabele} (
            id SERIAL PRIMARY KEY,
            mountain_id INTEGER,
            name TEXT,
            country TEXT,
            mountain_range TEXT,
            height_m INTEGER,
            coordinates TEXT,
            type TEXT,
            popularity TEXT,
            num_paths INTEGER,
            num_gps_paths INTEGER,
            description TEXT
        );
    """)
    conn.commit()

def preberi_csv(ime_datoteke: str) -> pd.DataFrame:
    df = pd.read_csv(ime_datoteke, sep=",", quotechar='"', encoding="utf-8")
    return df

def preimenuj_stolpce(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={
        "id": "mountain_id",
        "Name": "name",
        "Country": "country",
        "Mountain Range": "mountain_range",
        "Height(m)": "height_m",
        "Coordinates": "coordinates",
        "Type": "type",
        "Popularity": "popularity",
        "Number of Paths": "num_paths",       
        "Number of GPS Paths": "num_gps_paths",
        "Description": "description"
    })
    return df

def transformiraj(df: pd.DataFrame) -> pd.DataFrame:
    # Fix decimal commas in coordinates (optional parsing step)
    df["coordinates"] = df["coordinates"].apply(lambda x: x.replace(",", ".") if isinstance(x, str) else x)

    # Convert any % popularity to keep as string (you can parse it further if needed)
    
    columns = [
        "mountain_id", "name", "country", "mountain_range",
        "height_m", "coordinates", "type", "popularity",
        "num_paths", "num_gps_paths", "description"
    ]
    return df[columns]

def zapisi_df(df: pd.DataFrame) -> None:
    ime_tabele = "gore_podrobnosti"

    ustvari_tabelo_gore(ime_tabele)
    df = preimenuj_stolpce(df)
    df = transformiraj(df)

    records = df.values.tolist()
    columns = df.columns.tolist()

    sql = f'INSERT INTO {ime_tabele} ({", ".join(columns)}) VALUES %s'
    psycopg2.extras.execute_values(cur, sql, records)
    conn.commit()

if __name__ == "__main__":
    df = preberi_csv("Data/julijske_alpe_details2.csv")  # Adjust path as needed
    zapisi_df(df)
    print("Gore uspešno zapisane v bazo.")
