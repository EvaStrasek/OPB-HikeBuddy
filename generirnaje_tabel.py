import psycopg2
import os
import Data.auth as auth  # če imaš ločeno nastavitve

DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# Povezava na bazo
conn = psycopg2.connect(
    database=auth.db,
    host=auth.host,
    user=auth.user,
    password=auth.password,
    port=DB_PORT
)
cur = conn.cursor()

# Ukaz za ustvarjanje tabele
cur.execute("""
CREATE TABLE IF NOT EXISTS prijava_na_pohod (
    uporabnik_id INTEGER REFERENCES uporabniki(id),
    pohod_id INTEGER REFERENCES pohodi2(id),
    PRIMARY KEY (uporabnik_id, pohod_id),
    cas_prijave TIMESTAMP DEFAULT now()
)
""")

# Shrani spremembe
conn.commit()

# Zapri povezavo
cur.close()
conn.close()
