import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

import Data.auth as auth
from Data.models import *
from typing import List, Optional
import os

DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

class Repo:
    def __init__(self):
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
        self.conn.set_client_encoding('UTF8')
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # ------------------- GORA -------------------

    def dobi_gore(self) -> List[Gora]:
        self.cur.execute("""
            SELECT * FROM gore_podrobnosti ORDER BY mountain_id
        """)
        rows = self.cur.fetchall()
        rezultat = []
        for g in rows:
            d = dict(g)
            if 'id' in d:  # če je v bazi še vedno 'id', ga preimenuj
                d['mountain_id'] = d.pop('id')
            rezultat.append(Gora(**d))
        return rezultat

    def dobi_goro(self, id: int) -> Optional[Gora]:
        self.cur.execute("""
            SELECT * FROM gore_podrobnosti WHERE mountain_id = %s
        """, (id,))
        row = self.cur.fetchone()
        return Gora(**row) if row else None

    def dodaj_goro(self, g: Gora):
        self.cur.execute("""
            INSERT INTO gore_podrobnosti (mountain_id, name, country, mountain_range, height_m, coordinates, type,
                popularity, num_paths, num_gps_paths, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            g.mountain_id, g.name, g.country, g.mountain_range, g.height_m, g.coordinates, g.type,
            g.popularity, g.num_paths, g.num_gps_paths, g.description
        ))
        self.conn.commit()

    def posodobi_goro(self, g: Gora):
        self.cur.execute("""
            UPDATE gore_podrobnosti SET
                name = %s, country = %s, mountain_range = %s, height_m = %s,
                coordinates = %s, type = %s, popularity = %s, num_paths = %s,
                num_gps_paths = %s, description = %s
            WHERE mountain_id = %s
        """, (
            g.name, g.country, g.mountain_range, g.height_m, g.coordinates, g.type,
            g.popularity, g.num_paths, g.num_gps_paths, g.description, g.mountain_id
        ))
        self.conn.commit()
