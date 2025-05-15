import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
import Data.auth as auth
import datetime
import os

from Data.models import pohodi, pohodiDto, oprema, opremaDto, udelezenci, udelezenciDto, uporabnik, uporabnikDto
from typing import List

DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

class Repo:
    def __init__(self):
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def dobi_pohode(self) -> List[pohodi]:
        self.cur.execute("""
               SELECT id, ime_pohoda, datum, zacetna_lokacija, zahtevnost, povprecna_ocena,
                trajanje_ur, visinska_razlika, opis, lokacija 
                FROM pohodi 
                Order by datum asc    
        """)

        pohodi_seznam = [pohodi.from_dict(t) for t in self.cur.fetchall()]
        return pohodi_seznam
    
    def dobi_pohode_dto(self) -> List[pohodiDto]:
        self.cur.execute("""
               SELECT id, ime_pohoda, datum, zacetna_lokacija, zahtevnost, povprecna_ocena,
                trajanje_ur, visinska_razlika, opis, lokacija 
                FROM pohodiDto 
                Order by datum asc    
        """)

        pohodi_seznam = [pohodiDto.from_dict(t) for t in self.cur.fetchall()]
        return pohodi_seznam
    
    def dobi_opremo(self) -> List[oprema]:
        self.cur.execute("""
               SELECT id, ime_opreme, vrsta_opreme, opis
                FROM oprema 
                Order by id asc    
        """)

        oprema_seznam = [oprema.from_dict(t) for t in self.cur.fetchall()]
        return oprema_seznam
    
    def dodaj_pohod(self, p : pohodi):
        self.cur.execute("""
               INSERT into pohodi(id, ime_pohoda, datum, zacetna_lokacija, zahtevnost, trajanje_ur, 
                visinska_razlika, opis, lokacija)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
                """, (p.id, p.ime_pohoda, p.datum, p.zacetna_lokacija, p.zahtevnost, p.trajanje_ur,
                      p.visinska_razlika, p.opis, p.lokacija))
        self.conn.commit()

    def posodobi_pohod(self, p : pohodi):
        self.cur.execute("""
            Update pohodi set datum = %s, zahtevnost = %s, trajanje_ur = %s, opis = %s where id = %s
        """, (p.datum, p.zahtevnost, p.trajanje_ur, p.opis, p.id))
        self.conn.commit()

    def dodaj_uporabnika(self, u : uporabnik):
        self.cur.execute("""
            INSERT into uporabnik(uporabnisko_ime, vloga, geslo, zadnja_prijava)
            VALUES (%s, %s, %s, %s)
            """, (u.uporabnisko_ime,u.vloga, u.geslo, u.zadnja_prijava))
        self.conn.commit()

    def dobi_uporabnika(self, uporabnisko_ime:str) -> uporabnik:
        self.cur.execute("""
            SELECT uporabnisko_ime, vloga, geslo, zadnja_prijava
            FROM uporabnik
            WHERE uporabnisko_ime = %s
        """, (uporabnisko_ime,))
            
        u = uporabnik.from_dict(self.cur.fetchone())
        return u
    
    def posodobi_uporabnika(self, u: uporabnik):
        self.cur.execute("""
            Update uporabnik set zadnja_prijava = %s where uporabnisko_ime = %s
            """, (u.zadnja_prijava,u.uporabnisko_ime))
        self.conn.commit()
    
