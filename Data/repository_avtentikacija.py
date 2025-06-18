import psycopg2
import psycopg2.extras
import Data.auth as auth
from Data.models import Uporabnik
import os
import bcrypt

DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

class Repo:
    def __init__(self):
        self.conn = psycopg2.connect(
            database=auth.db,
            host=auth.host,
            user=auth.user,
            password=auth.password,
            port=DB_PORT
        )
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # def dodaj_uporabnika(self, uporabnik: Uporabnik):
    #    self.cur.execute("""
    #        INSERT INTO uporabniki (ime, priimek, uporabnisko_ime, geslo, telefon, email)
    #        VALUES (%s, %s, %s, %s, %s, %s)
    #    """, (uporabnik.ime, uporabnik.priimek, uporabnik.uporabnisko_ime,
    #          uporabnik.geslo, uporabnik.telefon, uporabnik.email))
    #    self.conn.commit()
        
    def dodaj_uporabnika(self, uporabnik: Uporabnik):
        """Shrani uporabnika v bazo s hashiranim geslom."""
        self.cur.execute("""
            INSERT INTO uporabniki (ime, priimek, uporabnisko_ime, geslo, telefon, email)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (uporabnik.ime, uporabnik.priimek, uporabnik.uporabnisko_ime,
        uporabnik.geslo, uporabnik.telefon, uporabnik.email))
        self.conn.commit()

    def pridobi_uporabnika_po_uporabniskem_imenu(self, uporabnisko_ime: str) -> Uporabnik:
        self.cur.execute("""
            SELECT * FROM uporabniki WHERE uporabnisko_ime = %s
        """, (uporabnisko_ime,))
        row = self.cur.fetchone()
        if row:
            return Uporabnik.from_dict(row)
        else:
            raise Exception("Uporabnik ne obstaja.")

    def obstaja_uporabnik(self, uporabnisko_ime: str) -> bool:
        self.cur.execute("""
            SELECT 1 FROM uporabniki WHERE uporabnisko_ime = %s
        """, (uporabnisko_ime,))
        return self.cur.fetchone() is not None
    
    
    def dobi_id_uporabnika(self, uporabnisko_ime):
        self.cur.execute("SELECT id FROM uporabniki WHERE uporabnisko_ime = %s", (uporabnisko_ime,))
        row = self.cur.fetchone()
        return row[0] if row else None


    def pridobi_prijave_uporabnika(self, uporabnisko_ime):
        self.cur.execute("""
            SELECT
                p.id AS pohod_id,
                pp.uporabnik_id,
                pp.pohod_id,
                poti.ime AS pot_ime,
                p.datum_zacetka,
                p.datum_konca
            FROM prijava_na_pohod pp
            JOIN uporabniki u ON pp.uporabnik_id = u.id
            JOIN pohodi2 p ON pp.pohod_id = p.id
            JOIN poti ON p.pot = poti.id
            WHERE u.uporabnisko_ime = %s
            ORDER BY p.datum_zacetka
        """, (uporabnisko_ime,))

        prijave = self.cur.fetchall()
        if prijave:
            print("Polja v prijavi:", prijave[0].keys())  # za debug
        return prijave

    def izbrisi_prijavo(self, pohod_id, uporabnik_id):
        self.cur.execute("""
            DELETE FROM prijava_na_pohod 
            WHERE pohod_id = %s AND uporabnik_id = %s
        """, (pohod_id, uporabnik_id))
        self.conn.commit()


