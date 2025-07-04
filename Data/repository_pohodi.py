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

    def dobi_pohode(self) -> List[pohod]:
        self.cur.execute("""
               SELECT id, datum_zacetka, datum_konca, pot
                FROM pohodi2
                Order by datum_zacetka desc    
        """)

        pohodi_seznam = [pohod.from_dict(t) for t in self.cur.fetchall()]
        return pohodi_seznam
    
    def dobi_pohode_dto(self) -> List[pohodDto]:
        self.cur.execute("""
                SELECT 
                    p.id, 
                    r.route_name as ime, 
                    p.datum_zacetka, 
                    p.datum_konca, 
                    r.start_point as zacetna_lokacija, 
                    r.route_difficulty as zahtevnost, 
                    r.route_time as trajanje_ur, 
                    r.height_diff as visinska_razlika_m, 
                    r.gear_summer as opis, 
                    r.gear_winter as lokacija 
                FROM pohodi2 p
                LEFT JOIN poti_po_gorah r ON p.pot = r.id
                ORDER BY p.datum_zacetka DESC;
        """)

        pohodi_seznam = [pohodDto.from_dict(t) for t in self.cur.fetchall()]
        return pohodi_seznam
    
    def dobi_pohod_dto(self, id) -> pohodDto:
        self.cur.execute("""
                SELECT 
                    p.id, 
                    r.route_name, 
                    p.datum_zacetka, 
                    p.datum_konca, 
                    r.start_point, 
                    r.route_difficulty, 
                    r.route_time, 
                    r.height_diff, 
                    r.gear_summer, 
                    r.gear_winter
                FROM pohodi2 p
                LEFT JOIN poti_po_gorah r ON p.pot = r.id
                WHERE p.id = %s;                    
        """, (id,))
            #   SELECT id, datum_zacetka, datum_konca, pot
            #   FROM pohodi2
            #   WHERE id = %s 



        pohod = pohodDto.from_dict(self.cur.fetchone())
        return pohod
    
    def dodaj_pohod(self, p : pohod):
        self.cur.execute("""
               INSERT into pohodi2(datum_zacetka, datum_konca, pot)
                VALUES (%s, %s, %s) 
                """, (p.datum_zacetka, p.datum_konca, p.pot))
        self.conn.commit()

    def posodobi_pohod(self, p : pohod):
        self.cur.execute("""
            Update pohodi2 set datum_zacetka = %s, datum_konca = %s where id = %s
        """, (p.datum_zacetka, p.datum_konca, p.id))
        self.conn.commit()
        
    def prijavi_uporabnika_na_pohod(self, uporabnik_id: int, pohod_id: int):
        self.cur.execute("""
        INSERT INTO prijava_na_pohod (uporabnik_id, pohod_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
        """, (uporabnik_id, pohod_id))
        self.conn.commit()
        
    def odstrani_pohod(self, id: int):
        self.cur.execute("DELETE FROM prijava_na_pohod WHERE pohod_id = %s", (id,))
 
        self.cur.execute("DELETE FROM pohodi2 WHERE id = %s", (id,))
        self.conn.commit()
    

    # def dobi_opremo(self) -> List[oprema]:
    #     self.cur.execute("""
    #            SELECT id, ime_opreme, vrsta_opreme, opis
    #             FROM oprema 
    #             Order by id asc    
    #     """)

    #     oprema_seznam = [oprema.from_dict(t) for t in self.cur.fetchall()]
    #     return oprema_seznam
    