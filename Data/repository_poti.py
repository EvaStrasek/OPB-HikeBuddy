import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
# import Data.auth as auth
import Data.auth as auth
import datetime 
import os

from Data.models import *
from typing import List

DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

class Repo:
    def __init__(self):
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
        self.conn.set_client_encoding('UTF8')
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def dobi_poti(self) -> List[pot]:
        self.cur.execute("""
               SELECT id, ime, zacetna_lokacija, zahtevnost, trajanje_ur, visinska_razlika_m, opis, lokacija
                FROM poti
        """)

        poti_seznam = [pot.from_dict(t) for t in self.cur.fetchall()]
        return poti_seznam
    
    def dobi_poti_dto(self) -> List[potDto]:
        self.cur.execute("""
               SELECT id, ime, zacetna_lokacija, zahtevnost, trajanje_ur, visinska_razlika_m, opis, lokacija
                FROM poti
        """)

        poti_seznam = [potDto.from_dict(t) for t in self.cur.fetchall()]
        return poti_seznam
    
    def dobi_pot(self, id) -> pot:
        self.cur.execute("""
               SELECT id, ime, zacetna_lokacija, zahtevnost, trajanje_ur, visinska_razlika_m, opis, lokacija
                FROM poti
                WHERE id = %s                         
        """, (id,))

        pot = pot.from_dict(self.cur.fetchone())
        return pot

    def dobi_pot_dto(self, id) -> potDto:
        self.cur.execute("""
               SELECT id, ime, zacetna_lokacija, zahtevnost, trajanje_ur, visinska_razlika_m, opis, lokacija
                FROM poti
                WHERE id = %s                         
        """, (id,))

        pot = potDto.from_dict(self.cur.fetchone())
        return pot
    
    def dodaj_pot(self, p : pot):
        self.cur.execute("""
               INSERT into poti(ime, zacetna_lokacija, zahtevnost, trajanje_ur, 
                visinska_razlika_m, opis, lokacija)
                VALUES (%s, %s, %s, %s, %s, %s, %s) 
                """, (p.ime, p.zacetna_lokacija, p.zahtevnost, p.trajanje_ur,
                      p.visinska_razlika_m, p.opis, p.lokacija))
        self.conn.commit()

    def posodobi_pot(self, p : pot):
        self.cur.execute("""
            Update poti set ime = %s, zacetna_lokacija = %s, zahtevnost = %s, 
                         trajanje_ur = %s, visinska_razlika_m = %s, opis = %s, lokacija = %s where id = %s
        """, (p.ime, p.zacetna_lokacija, p.zahtevnost, p.trajanje_ur,
                      p.visinska_razlika_m, p.opis, p.lokacija, p.id))
        self.conn.commit()