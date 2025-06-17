import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
import Data.auth as auth  # V datoteki auth.py imaš db, user, host, password

# DB povezava
database = auth.db
host = auth.host
port = 5432
user = auth.user
password = auth.password

conn = psycopg2.connect(database=database, host=host, port=port, user=user, password=password)
conn.set_client_encoding('UTF8')
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def ustvari_tabelo_uporabniki(ime_tabele: str = "uporabniki") -> None:
    cur.execute(f"""
        DROP TABLE IF EXISTS {ime_tabele};
        CREATE TABLE IF NOT EXISTS {ime_tabele} (
            id SERIAL PRIMARY KEY,
            ime TEXT NOT NULL,
            priimek TEXT NOT NULL,
            uporabnisko_ime TEXT UNIQUE NOT NULL,
            geslo TEXT NOT NULL,
            telefon TEXT,
            email TEXT UNIQUE
        );
    """)
    conn.commit()

def dodaj_primer_uporabnikov():
    uporabniki = [
        ("Ana", "Novak", "anovak", "geslo123", "041234567", "ana.novak@gmail.com"),
        ("Miha", "Kovač", "mkovac", "geslo456", "031111222", "miha.kovac@yahoo.com"),
        ("Tina", "Zupan", "tzupan", "1234abcd", "051222333", "tina.zupan@email.si"),
        ("Jan", "Horvat", "jhorvat", "pass4321", "068000999", "jan.horvat@xmail.com")
    ]

    sql = """
        INSERT INTO uporabniki (ime, priimek, uporabnisko_ime, geslo, telefon, email)
        VALUES %s
    """
    psycopg2.extras.execute_values(cur, sql, uporabniki)
    conn.commit()

if __name__ == "__main__":
    ustvari_tabelo_uporabniki()
    dodaj_primer_uporabnikov()
    print("Tabela 'uporabniki' ustvarjena in napolnjena.")
