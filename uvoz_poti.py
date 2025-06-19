import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
import pandas as pd
from datetime import datetime
import Data.auth as auth  # datoteka auth.py naj vsebuje: password = "..."


# Podatki za povezavo
database = auth.db
host = auth.host
port = 5432
user = auth.user
password = auth.password

# Ustvari povezavo
conn = psycopg2.connect(database=database, host=host, port=port, user=user, password=password)
conn.set_client_encoding('UTF8')
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


def ustvari_tabelo_poti(ime_tabele : str) -> None:
    cur.execute(f"""
        DROP table if exists {ime_tabele};
        CREATE table if not exists  {ime_tabele}(  
            id SERIAL PRIMARY KEY,
            ime TEXT,
            zacetna_lokacija TEXT,
            zahtevnost TEXT,
            trajanje_ur INTEGER,
            visinska_razlika_m INTEGER,
            opis TEXT,
            lokacija TEXT
        );
    """)
    conn.commit()

def preberi_csv(ime_datoteke : str) -> pd.DataFrame:
    df = pd.read_csv(ime_datoteke, sep=",", index_col=0, encoding="utf-8")  # ali cp1250
    return df


def preimenuj_stolpce_poti(df: pd.DataFrame) -> pd.DataFrame:
    """
    Funkcija preimenuje stolpce v DataFrame-u, da ustrezajo camelCase konvenciji.
    """
    df = df.rename(columns={
            "Id": "id",
            "Ime pohoda": "ime",
            "Začetna lokacija": "zacetna_lokacija",
            "Zahtevnost": "zahtevnost",
            "Trajanje (h)": "trajanje_ur",
            "Višinska razlika (m)": "visinska_razlika_m",
            "Opis": "opis",
            "Lokacija": "lokacija"
        }
    ) 
    return df


def transformiraj_poti(df: pd.DataFrame) -> pd.DataFrame:

    # Definiramo vrstni red stolpcev, kot so definirani v tabeli
    columns = [
     "ime", "zacetna_lokacija", "zahtevnost", "trajanje_ur", "visinska_razlika_m", "opis", "lokacija"
    ]
    
    # Poskrbimo, da DataFrame vsebuje točno te stolpce v pravem vrstnem redu
    df = df.reindex(columns=columns)
    return df

def zapisi_df(df: pd.DataFrame) -> None:

    ime_tabele = "poti"

    # Poskrbimo, da tabela obstaja
    ustvari_tabelo_poti(ime_tabele)
    
    # Če DataFrame nima stolpca 'Index', ga dodamo iz indeksa
    df = df.reset_index()

    # Prvi korak: Stolpci v csvju so drugače poimenovani,
    # kot bi si jih želeli imeti v bazi.
    df = preimenuj_stolpce_poti(df)
    
    # Transformiramo podatke v DataFrame-u
    df = transformiraj_poti(df)
    
    # shranimo stolpce v seznam
    columns = df.columns.tolist()

    # Pretvorimo podatke v seznam tuple-ov
    records = df.values.tolist()

    print(f'velikost: {records}')
    
    # Pripravimo SQL ukaz za vstavljanje podatkov
    sql = f'INSERT INTO {ime_tabele} ({", ".join(columns)}) VALUES %s'
    
    # Uporabimo execute_values za množični vnos
    # Izvede po en insert ukaz na vrstico oziroma record iz seznama records
    # V odzadju zadeva deluje precej bolj optimlano kot en insert na ukaz!
    # Za množičen vnos je potrebno uporabiti psycopg2.extras.execute_values
    psycopg2.extras.execute_values(cur, sql, records)
    
    # Potrdimo spremembe v bazi
    conn.commit()

   
    
if __name__ == "__main__":
    # Preberi CSV datoteko, pri čemer privzamemo, da je datoteka
    # "customers-100.csv" v isti mapi kot tvoj skript ali podaj absolutno pot.
    df = preberi_csv("Data/poti.csv")
    
    # Zapiši podatke iz DataFrame-a v tabelo "customers"
    zapisi_df(df)
    
    print("CSV datoteka je bila uspešno zabeležena v bazi.")
